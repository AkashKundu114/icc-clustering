from pathlib import Path
import csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"loop6_0_artifact_manifest.csv"
SUMS=ROOT/"SHA256SUMS"
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""):h.update(b)
 return h.hexdigest()
def main():
 files=sorted(p for p in ROOT.rglob("*") if p.is_file() and p.resolve() not in {MANIFEST.resolve(),SUMS.resolve()})
 rows=[]
 for p in files:
  rel=p.relative_to(ROOT).as_posix(); kind="script" if p.suffix==".py" else ("machine-readable" if p.suffix in {".csv",".json"} else "report/artifact")
  rows.append({"relative_path":rel,"bytes":p.stat().st_size,"sha256":sha(p),"class":kind})
 with MANIFEST.open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=["relative_path","bytes","sha256","class"]);w.writeheader();w.writerows(rows)
 files2=sorted(p for p in ROOT.rglob("*") if p.is_file() and p.resolve()!=SUMS.resolve())
 SUMS.write_text("".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in files2),encoding="utf-8")
 print(f"manifest_rows={len(rows)} checksum_entries={len(files2)}")
if __name__=="__main__":main()
