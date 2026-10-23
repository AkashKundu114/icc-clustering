from pathlib import Path

path = Path("scripts/run_passE_all.py")
text = path.read_text(encoding="utf-8")

old_block = """                rec = {
                    "dataset": dname, "N": N, "D": D, "K": K,
                    "model": mname, "seed": seed,
                    "ari": score_ari, "nmi": score_nmi,
                    "elapsed_sec": elap
                }
                records.append(rec)
                done_keys.add((dname, mname, seed))

        # Checkpoint after each dataset
        pd.DataFrame(records).to_csv(out_file, index=False)"""

new_block = """                rec = {
                    "dataset": dname, "N": N, "D": D, "K": K,
                    "model": mname, "seed": seed,
                    "ari": score_ari, "nmi": score_nmi,
                    "elapsed_sec": elap
                }
                records.append(rec)
                done_keys.add((dname, mname, seed))

            # Checkpoint after each model completes
            pd.DataFrame(records).to_csv(out_file, index=False)
            print(f"    [OK] {mname} on {dname} complete ({len(records)}/{13*11*10} total records saved).", flush=True)

        # Checkpoint after each dataset
        pd.DataFrame(records).to_csv(out_file, index=False)"""

assert old_block in text, "old_block not found in run_passE_all.py"
path.write_text(text.replace(old_block, new_block), encoding="utf-8")
print("[OK] Successfully added per-model checkpointing and flushing to run_passE_all.py")
