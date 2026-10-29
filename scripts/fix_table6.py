import os

with open("paper/main.tex", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "Prostate" in line and "5{,}966" in line:
        line = line.replace("5{,}966", "12{,}600").replace("58.5", "123.5")
    elif "Madelon" in line and "2{,}600" in line:
        line = line.replace("2{,}600", "500").replace("0.19", "1.00")
    elif "PBMC68k-red" in line and "68{,}579" in line:
        line = line.replace("68{,}579", "700").replace("1{,}000", "765").replace("$11$", "$10$").replace("0.01", "1.09")
    elif "20 Newsgroups" in line and "20{,}000" in line:
        line = line.replace("20{,}000", "10{,}000").replace("1.06", "0.53")
    new_lines.append(line)

with open("paper/main.tex", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Updated Table 6 successfully.")
