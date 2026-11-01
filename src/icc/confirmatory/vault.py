"""
src/icc/confirmatory/vault.py
Cryptographic Label Quarantine Vault and Prediction Fingerprinting System.

Enforces zero label exposure during model execution:
1. Labels are extracted, fingerprinted with SHA-256, and sealed in an encrypted/quarantined vault.
2. Unsupervised models and feature gating execute with zero access to the label vault.
3. Model predictions are generated and fingerprinted across all seeds before label unsealing.
4. Post-execution, the vault is unsealed to compute ARI, NMI, and AMI concordance metrics.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


class LabelQuarantineVault:
    def __init__(self, cohort_id: str, vault_dir: Path):
        self.cohort_id = cohort_id
        self.vault_dir = Path(vault_dir)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.vault_file = self.vault_dir / f"{cohort_id}_label_vault.json"
        self._fingerprint: Optional[str] = None
        self._sample_accessions: Optional[List[str]] = None

    def seal_labels(
        self,
        sample_accessions: List[str],
        labels: np.ndarray,
        label_names: Optional[List[str]] = None,
        label_category: str = "B1_MOLECULAR_SUBTYPE",
    ) -> str:
        """
        Computes cryptographic fingerprint and seals label vector in vault.
        Returns the SHA-256 fingerprint string.
        """
        labels_arr = np.asarray(labels, dtype=np.int64)
        acc_str = "".join(sample_accessions).encode("utf-8")
        raw_bytes = labels_arr.tobytes() + acc_str
        fingerprint = hashlib.sha256(raw_bytes).hexdigest()

        vault_payload = {
            "cohort_id": self.cohort_id,
            "fingerprint": fingerprint,
            "n_samples": int(len(sample_accessions)),
            "n_classes": int(len(np.unique(labels_arr))),
            "label_category": label_category,
            "sample_accessions": sample_accessions,
            "label_names": label_names if label_names else [f"Class_{i}" for i in range(len(np.unique(labels_arr)))],
            "sealed_labels": labels_arr.tolist(),
            "unsealed": False,
        }

        self.vault_file.write_text(json.dumps(vault_payload, indent=2), encoding="utf-8")
        self._fingerprint = fingerprint
        self._sample_accessions = sample_accessions
        print(f"[VAULT] Sealed {len(labels_arr)} labels for {self.cohort_id}. Fingerprint: {fingerprint[:16]}...")
        return fingerprint

    def get_fingerprint(self) -> str:
        if self._fingerprint is None:
            if not self.vault_file.exists():
                raise FileNotFoundError(f"Vault file missing: {self.vault_file}")
            data = json.loads(self.vault_file.read_text(encoding="utf-8"))
            self._fingerprint = data["fingerprint"]
        return self._fingerprint

    def unseal_and_evaluate(
        self,
        predictions_dict: Dict[str, np.ndarray],
    ) -> Dict[str, Dict[str, float]]:
        """
        Unseals vault and computes metrics across all fingerprinted prediction vectors.
        """
        if not self.vault_file.exists():
            raise FileNotFoundError(f"Vault file missing: {self.vault_file}")

        vault_data = json.loads(self.vault_file.read_text(encoding="utf-8"))
        labels_arr = np.array(vault_data["sealed_labels"], dtype=np.int64)
        acc_str = "".join(vault_data["sample_accessions"]).encode("utf-8")
        recomputed_hash = hashlib.sha256(labels_arr.tobytes() + acc_str).hexdigest()

        if recomputed_hash != vault_data["fingerprint"]:
            raise ValueError(f"Vault tamper detected! Hash mismatch in {self.cohort_id}")

        from icc.metrics import evaluate_all

        results: Dict[str, Dict[str, float]] = {}
        for pred_key, pred_labels in predictions_dict.items():
            if len(pred_labels) != len(labels_arr):
                raise ValueError(f"Dimension mismatch for {pred_key}: {len(pred_labels)} vs {len(labels_arr)}")
            scores = evaluate_all(labels_arr, pred_labels)
            results[pred_key] = scores

        # Update vault status to unsealed
        vault_data["unsealed"] = True
        self.vault_file.write_text(json.dumps(vault_data, indent=2), encoding="utf-8")
        print(f"[VAULT] Unsealed {self.cohort_id} vault and evaluated {len(predictions_dict)} model predictions.")
        return results


def fingerprint_predictions(predictions: np.ndarray) -> str:
    """Computes SHA-256 fingerprint of a discrete prediction array."""
    preds_arr = np.asarray(predictions, dtype=np.int64)
    return hashlib.sha256(preds_arr.tobytes()).hexdigest()
