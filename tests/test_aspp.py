"""
Unit and integration tests for Anchor-Space Perturbation Profiling (ASPP)
and its integration into InvariantCoreConsensusV2.
"""

import numpy as np
import pandas as pd

from icc import AnchorSpacePerturbationProfiler as RootProfiler
from icc import ASPPConfig as RootASPPConfig
from icc.aspp import ASPP_FAMILIES, AnchorSpacePerturbationProfiler, ASPPConfig
from icc.consensus_v2 import InvariantCoreConsensusV2


def test_aspp_config_defaults_and_overrides():
    cfg = ASPPConfig()
    assert set(cfg.families) == set(ASPP_FAMILIES)
    assert cfg.repetitions == 2
    assert cfg.hi_threshold == 0.70
    assert cfg.lo_threshold == 0.45
    assert cfg.max_response_sd == 0.15

    custom_cfg = ASPPConfig(
        families=("sampling", "feature"),
        repetitions=1,
        hi_threshold=0.80,
    )
    assert len(custom_cfg.families) == 2
    assert custom_cfg.repetitions == 1
    assert custom_cfg.hi_threshold == 0.80


def test_aspp_standalone_profiler():
    rng = np.random.default_rng(42)
    # 3 well-separated clusters with informative + noise features
    X1 = rng.normal(loc=[-4, 0], scale=0.5, size=(25, 2))
    X2 = rng.normal(loc=[4, 0], scale=0.5, size=(25, 2))
    X3 = rng.normal(loc=[0, 4], scale=0.5, size=(25, 2))
    X_noise = rng.normal(size=(75, 10))
    X = np.hstack([np.vstack([X1, X2, X3]), X_noise])  # (75, 12)

    model = InvariantCoreConsensusV2(
        n_clusters=3,
        n_base_models=10,
        n_anchors=15,
        random_state=42,
    )
    model.fit(X)

    # Standalone profiler
    aspp_cfg = ASPPConfig(
        families=("sampling", "feature", "measurement"),
        repetitions=1,
        levels={"sampling": (0.2,), "feature": (0.3,), "measurement": (0.3,)},
        n_base_models=3,
        random_state=42,
    )
    profiler = AnchorSpacePerturbationProfiler(config=aspp_cfg)
    df = profiler.profile(model, X)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert set(df.columns).issuperset({
        "cluster", "size", "PSI", "reliability",
        "sampling", "feature", "measurement",
        "sampling_retention", "feature_retention", "measurement_retention",
        "sampling_anchor_coassoc", "feature_anchor_coassoc", "measurement_anchor_coassoc",
    })

    # Validate value constraints
    assert np.all(df["PSI"] >= 0.0) and np.all(df["PSI"] <= 1.0)
    for cat in df["reliability"]:
        assert cat in {"globally_invariant", "conditionally_invariant", "perturbation_fragile", "ambiguous"}

    # Assert profiler properties
    assert profiler.psi_ is not None and len(profiler.psi_) == 3
    assert profiler.reliability_categories_ is not None and len(profiler.reliability_categories_) == 3
    assert profiler.aspp_summary_ is not None


def test_aspp_integrated_enable_flag():
    rng = np.random.default_rng(101)
    X = rng.normal(size=(60, 8))

    aspp_cfg = ASPPConfig(
        families=("sampling", "algorithmic"),
        repetitions=1,
        levels={"sampling": (0.2,), "algorithmic": (0.5,)},
        n_base_models=3,
        random_state=101,
    )

    model = InvariantCoreConsensusV2(
        n_clusters=2,
        n_base_models=6,
        n_anchors=10,
        enable_aspp=True,
        aspp_config=aspp_cfg,
        random_state=101,
    )
    labels = model.fit_predict(X)

    assert labels.shape == (60,)
    assert model.fingerprints_ is not None
    assert isinstance(model.fingerprints_, pd.DataFrame)
    assert len(model.fingerprints_) == 2
    assert model.psi_ is not None and len(model.psi_) == 2
    assert model.reliability_categories_ is not None and len(model.reliability_categories_) == 2
    assert model.aspp_summary_ is not None
    assert "sampling_mean_ari" in model.aspp_summary_
    assert "algorithmic_mean_ari" in model.aspp_summary_


def test_predict_with_stability_inductive():
    rng = np.random.default_rng(202)
    X_train = np.vstack([
        rng.normal(loc=[-3, -3], scale=0.6, size=(30, 2)),
        rng.normal(loc=[3, 3], scale=0.6, size=(30, 2)),
    ])
    X_train = np.hstack([X_train, rng.normal(size=(60, 6))])  # (60, 8)

    X_test = np.vstack([
        rng.normal(loc=[-3, -3], scale=0.6, size=(10, 2)),
        rng.normal(loc=[3, 3], scale=0.6, size=(10, 2)),
    ])
    X_test = np.hstack([X_test, rng.normal(size=(20, 6))])    # (20, 8)

    aspp_cfg = ASPPConfig(
        families=("sampling", "feature"),
        repetitions=1,
        levels={"sampling": (0.2,), "feature": (0.3,)},
        n_base_models=3,
        random_state=202,
    )

    model = InvariantCoreConsensusV2(
        n_clusters=2,
        n_base_models=5,
        n_anchors=10,
        enable_aspp=True,
        aspp_config=aspp_cfg,
        random_state=202,
    )
    model.fit(X_train)

    # Inductive prediction with stability confidence
    res = model.predict_with_stability(X_test)
    assert isinstance(res, dict)
    assert set(res.keys()) == {"labels", "confidence", "margin", "psi", "reliability"}

    labels = res["labels"]
    confidence = res["confidence"]
    margin = res["margin"]
    psi = res["psi"]
    reliability = res["reliability"]

    assert labels.shape == (20,)
    assert confidence.shape == (20,)
    assert margin.shape == (20,)
    assert psi.shape == (20,)
    assert len(reliability) == 20

    # Confidence and margin must be bounded in [0, 1]
    assert np.all(confidence >= 0.0) and np.all(confidence <= 1.0)
    assert np.all(margin >= 0.0) and np.all(margin <= 1.0)

    # Confidence must not exceed raw margin since confidence = margin * (1 - psi)
    assert np.all(confidence <= margin + 1e-7)


def test_aspp_reproducibility():
    rng1 = np.random.default_rng(999)
    X = rng1.normal(size=(40, 6))

    aspp_cfg = ASPPConfig(
        families=("sampling", "measurement"),
        repetitions=1,
        levels={"sampling": (0.2,), "measurement": (0.3,)},
        n_base_models=3,
        random_state=42,
    )

    m1 = InvariantCoreConsensusV2(n_clusters=2, n_base_models=4, n_anchors=8, enable_aspp=True, aspp_config=aspp_cfg, random_state=42)
    m1.fit(X)

    m2 = InvariantCoreConsensusV2(n_clusters=2, n_base_models=4, n_anchors=8, enable_aspp=True, aspp_config=aspp_cfg, random_state=42)
    m2.fit(X)

    assert np.array_equal(m1.labels_, m2.labels_)
    assert np.allclose(m1.psi_, m2.psi_)
    assert m1.reliability_categories_ == m2.reliability_categories_


def test_aspp_with_batch_vector():
    rng = np.random.default_rng(555)
    X = rng.normal(size=(50, 6))
    batches = np.repeat([0, 1], 25)

    model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=10, random_state=555)
    model.fit(X, batch_vector=batches)

    aspp_cfg = ASPPConfig(
        families=("technical",),
        repetitions=1,
        levels={"technical": (0.3,)},
        n_base_models=3,
        random_state=555,
    )
    df = model.profile_perturbations(X, config=aspp_cfg, batch_vector=batches)
    assert len(df) == 2
    assert "technical" in df.columns
    assert "technical_anchor_coassoc" in df.columns


def test_root_import_parity():
    assert RootASPPConfig is ASPPConfig
    assert RootProfiler is AnchorSpacePerturbationProfiler
