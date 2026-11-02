r"""Record Loop 5.9 baseline hashes/inventories from existing bytes.

Expected inputs: target Git checkout, local D:\Final Year Project and audit
directories 5.6-5.8. Outputs only under audit/loop5_9.
"""
from pathlib import Path
import csv, hashlib, subprocess

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'audit'/'loop5_9'
FYP=Path(r'D:\Final Year Project')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_csv(path,rows,fields):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

def main():
    rows=[]
    for base in [ROOT/'audit'/'loop5_6',ROOT/'audit'/'loop5_7',ROOT/'audit'/'loop5_8']:
        for p in sorted(base.rglob('*')):
            if p.is_file(): rows.append(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}  {p.stat().st_size}")
    manuscripts=[]
    candidate_roots=[FYP/'paper',FYP/'springer_manuscript',FYP/'submission',FYP/'manuscript']
    suffixes={'.tex','.bib','.bbl','.docx','.pdf','.md','.png','.jpg','.jpeg','.svg','.csv'}
    for base in candidate_roots:
        if not base.exists(): continue
        for p in sorted(base.rglob('*')):
            if not p.is_file() or p.suffix.lower() not in suffixes: continue
            if p.suffix.lower() in {'.png','.jpg','.jpeg','.svg'} and 'figure' not in str(p).lower(): continue
            manuscripts.append({'version_source':'separate local FYP worktree; not authenticated submission version','path':str(p),'relative_path':p.relative_to(FYP).as_posix(),'bytes':p.stat().st_size,'modified_local':__import__('datetime').datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(timespec='seconds'),'sha256':sha(p),'tracked_in_fyp':subprocess.run(['git','-C',str(FYP),'ls-files','--error-unmatch',p.relative_to(FYP).as_posix()],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0})
    # Target repository's paper directory is ignored; inventory actual files if any.
    for p in sorted((ROOT/'paper').rglob('*')) if (ROOT/'paper').exists() else []:
        if p.is_file() and p.suffix.lower() in suffixes:
            manuscripts.append({'version_source':'target local ignored/untracked paper tree','path':str(p),'relative_path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'modified_local':__import__('datetime').datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat(timespec='seconds'),'sha256':sha(p),'tracked_in_fyp':False})
    write_csv(OUT/'manuscript_version_inventory.csv',manuscripts,['version_source','path','relative_path','bytes','modified_local','sha256','tracked_in_fyp'])
    for r in manuscripts:
        rows.append(f"{r['sha256']}  {r['path']}  {r['bytes']}")
    (OUT/'baseline_sha256sums.txt').write_text('\n'.join(rows)+'\n',encoding='utf-8')
    print('baseline audit files hashed',len(rows),'manuscript/candidate files',len(manuscripts))

if __name__=='__main__':main()
