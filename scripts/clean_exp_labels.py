with open("paper/main.tex", "r", encoding="utf-8") as f:
    text = f.read()

replacements = [
    ("(Experiment~5)", "(the million-sample scalability evaluation)"),
    ("(Experiment~1)", "(the inductive generalization evaluation)"),
    (r"\textbf{Inductive Generalization on Test Queries (Exp~1):}", r"\textbf{Inductive Generalization Evaluation:}"),
    (r"\textbf{Empirical Scalability vs. Sample Size (Exp~4):}", r"\textbf{Scalability vs. Sample Size:}"),
    (r"Exp~4 evaluated the computational scaling of ICC-v2 as sample size $N$ increased from $500$ to $10{,}000$",
     r"We evaluated the computational scaling of ICC-v2 as sample size $N$ increased from $500$ to $10{,}000$"),
    (r"\textbf{Controlled Scalability to 1 Million Samples (Exp~5):}", r"\textbf{Million-Sample Scalability Evaluation:}"),
    (r"To evaluate computational boundaries under extreme dataset scales, Experiment~5 benchmarked ICC-v2",
     r"To evaluate computational boundaries under extreme dataset scales, we benchmarked ICC-v2"),
]

for old, new in replacements:
    if old in text:
        text = text.replace(old, new, 1)
        print(f"[+] Replaced: {old[:40]}...")
    else:
        print(f"[-] NOT FOUND: {old[:40]}...")

with open("paper/main.tex", "w", encoding="utf-8") as f:
    f.write(text)

print("Finished clean_exp_labels.py")
