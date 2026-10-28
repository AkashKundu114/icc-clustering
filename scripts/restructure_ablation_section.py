def restructure():
    tex_path = "paper/main.tex"
    with open(tex_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 1. Update Section 1 roadmap paragraph
    old_roadmap = r"Section~\ref{sec:evaluation} reports experimental evaluation covering computational scalability, 13-cohort benchmarks, statistical testing, ablation studies, and convergence analyses. Section~\ref{sec:applications} discusses real-world application case studies and their limits."
    new_roadmap = r"Section~\ref{sec:evaluation} reports experimental evaluation covering computational scalability, 13-cohort benchmarks, statistical testing, and convergence analyses. Section~\ref{sec:ablation} presents the ablation study, factorial interaction, and feature saliency audits. Section~\ref{sec:applications} discusses real-world application case studies and their limits."
    
    if old_roadmap in text:
        text = text.replace(old_roadmap, new_roadmap)
        print("Updated Section 1 roadmap paragraph.")
    else:
        print("Warning: old roadmap string not found!")

    # 2. Extract Convergence Analysis block
    conv_start = text.find(r"\subsection{Convergence Analysis}\label{sec:convergence}")
    conv_end = text.find(r"\section{Real-World Applications}\label{sec:applications}")
    if conv_start == -1 or conv_end == -1:
        print("Error: Could not locate Convergence Analysis or Real-World Applications!")
        return

    conv_block = text[conv_start:conv_end].strip()

    # 3. Extract Ablation Study block
    ablation_start = text.find(r"\subsection{Ablation Study}\label{sec:ablation}")
    if ablation_start == -1:
        print("Error: Could not locate \\subsection{Ablation Study}!")
        return

    ablation_content = text[ablation_start:conv_start].strip()

    # Turn Ablation Study into a top-level section with structured subsections
    ablation_content = ablation_content.replace(
        r"\subsection{Ablation Study}\label{sec:ablation}",
        r"\section{Ablation Study and Modular Decomposition}\label{sec:ablation}"
    )
    ablation_content = ablation_content.replace(
        r"\textbf{Architectural Variant Specification:}",
        r"\subsection{Architectural Knockout Variants (V0--V5)}\label{sec:ablation_variants}"
    )
    ablation_content = ablation_content.replace(
        r"\textbf{Per-Dataset Ablation Performance Across High-$D$ Benchmarks:}",
        r"\subsection{Per-Dataset Performance Across High-$D$ Benchmarks}\label{sec:ablation_per_dataset}"
    )
    ablation_content = ablation_content.replace(
        r"\textbf{Factorial Decomposition and Component Contributions:}\label{sec:exp2_knockout}",
        r"\subsection{Factorial Decomposition and Synergistic Interaction}\label{sec:exp2_knockout}"
    )
    ablation_content = ablation_content.replace(
        r"\textbf{Anchor Certification Null Result:}",
        r"\subsection{Anchor Certification Null Result}\label{sec:ablation_null}"
    )
    ablation_content = ablation_content.replace(
        r"\textbf{BGSS Feature Saliency and Interpretability Audit:}",
        r"\subsection{Unsupervised Feature Saliency and Interpretability Audit}\label{sec:ablation_saliency}"
    )

    # Reconstruct text:
    # Before ablation: text[:ablation_start]
    # Then conv_block (inside Section 6 as 6.4)
    # Then blank line
    # Then ablation_content (as Section 7)
    # Then text[conv_end:] (Section 8: Real-World Applications...)
    
    before_ablation = text[:ablation_start].rstrip()
    after_conv = text[conv_end:]

    new_text = (
        before_ablation + "\n\n" +
        conv_block + "\n\n\n" +
        ablation_content + "\n\n\n" +
        after_conv
    )

    with open(tex_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("Successfully restructured Ablation Study into Section 7 in paper/main.tex!")

if __name__ == "__main__":
    restructure()
