import re

with open('manuscript/main_fixed.tex', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Frontmatter extraction
abs_m = re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}', text, re.DOTALL)
abstract_text = abs_m.group(1).strip() if abs_m else ''

kw_m = re.search(r'\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}', text, re.DOTALL)
keywords_text = kw_m.group(1).strip() if kw_m else ''

body_start = text.find(r'\section{Introduction}')
if body_start == -1:
    body_start = text.find(r'\IEEEraisesectionheading{\section{Introduction}')

body_end = text.find(r'\section*{Data and Code Availability}')
if body_end == -1:
    body_end = text.find(r'\bibliographystyle')

body = text[body_start:body_end]

# Clean body
body = body.replace(r'\IEEEraisesectionheading{\section{Introduction}\label{sec:intro}}', r'\section{Introduction}\label{sec:intro}')
body = body.replace(r'\section{Introduction}\label{sec:intro}}', r'\section{Introduction}\label{sec:intro}')
body = re.sub(r'\\IEEEPARstart\{([A-Z])\}\{([a-zA-Z]+)\}', r'\1\2', body)

# Replace input{gen/numbers.tex} with input{numbers.tex}
body = body.replace('input{gen/numbers.tex}', 'input{numbers.tex}')

# Remove resizebox around tables as sn-jnl provides native table styling
body = re.sub(r'\\resizebox\{\\columnwidth\}\{!\}\{%?\s*', '', body)
body = re.sub(r'\\end\{tabular\}%?\s*\}', r'\\end{tabular}', body)

# Frontmatter preamble
preamble = r'''\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}

\usepackage{graphicx}
\usepackage{multirow}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{amsthm}
\usepackage{mathrsfs}
\usepackage[title]{appendix}
\usepackage{xcolor}
\usepackage{textcomp}
\usepackage{manyfoot}
\usepackage{booktabs}
\usepackage{algorithm}
\usepackage{algorithmicx}
\usepackage{algpseudocode}
\usepackage{listings}
\usepackage{subfig}

\theoremstyle{thmstyleone}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}

\theoremstyle{thmstyletwo}
\newtheorem{example}{Example}
\newtheorem{remark}{Remark}

\theoremstyle{thmstylethree}
\newtheorem{definition}{Definition}
\newtheorem{assumption}{Assumption}

\input{numbers.tex}

\raggedbottom

\begin{document}

\title[Inductive Consensus Clustering]{Inductive Consensus Clustering: Geometry-Calibrated Ensemble Distillation for High-Dimensional Noise Regimes}

\author*[1]{\fnm{Akash} \sur{Kundu}}\email{akash231001001449@technoindiaeducation.com}

\author[1]{\fnm{Trinankur} \sur{Guha}}\email{trinankur231001001450@technoindiaeducation.com}

\author[1]{\fnm{Rupankar} \sur{Ghatak}}\email{rupankar231001001438@technoindiaeducation.com}

\author[1]{\fnm{Anubhab} \sur{Naskar}}\email{anubhab231001001443@technoindiaeducation.com}

\author[1]{\fnm{Kalyan Kumar} \sur{Das}}\email{kalyan.biltu@gmail.com}

\affil*[1]{\orgdiv{Department of Computer Science and Engineering}, \orgname{Techno India University}, \orgaddress{\street{EM-4, Sector V, Bidhannagar}, \city{Kolkata}, \postcode{700091}, \state{West Bengal}, \country{India}}}

\abstract{''' + abstract_text + r'''}

\keywords{''' + keywords_text + r'''}

\maketitle

'''

declarations = r'''
\backmatter

\bmhead{Supplementary information}
Supplementary data, extended sensitivity heatmaps, and ablation logs are provided in the reproducibility repository.

\bmhead{Acknowledgements}
The authors thank the Department of Computer Science and Engineering, Techno India University, for computational infrastructure support.

\section*{Declarations}

\begin{itemize}
\item \textbf{Funding:} No specific external grant funding was received for this study.
\item \textbf{Conflict of interest/Competing interests:} The authors declare that they have no competing financial or non-financial interests directly or indirectly related to the work submitted for publication.
\item \textbf{Ethics approval and consent to participate:} Not applicable. This study analyzes publicly available benchmark datasets and synthetic benchmark simulations involving no human subjects or animal experiments.
\item \textbf{Consent for publication:} All authors reviewed and approved the final manuscript for submission.
\item \textbf{Data availability:} All real-world benchmark datasets utilized in this study (CNS, Colon, Indian Pines, Isolet, Leukemia, Madelon, 20 Newsgroups, Ovarian, Prostate, Sonar, SRBCT, Extended Yale B, Zheng68k) are publicly accessible. Preprocessed benchmark arrays are mirrored at: \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.0.0}).
\item \textbf{Materials availability:} Not applicable.
\item \textbf{Code availability:} The complete, fully reproducible Python implementation of ICC-v2, benchmark harnesses, validation scripts, and figure generation routines are released under the MIT License at: \url{https://github.com/AkashKundu114/icc-clustering} (release tag \texttt{v2.0.0}).
\item \textbf{Author contribution:} A. Kundu conceived the framework, derived theoretical properties, implemented algorithms, performed empirical analyses, and drafted the manuscript. T. Guha, R. Ghatak, and A. Naskar designed baseline pipelines, contributed to computational scaling experiments, and validated code integrity. K. K. Das supervised the research, reviewed statistical methodologies, and edited the manuscript.
\item \textbf{Use of Artificial Intelligence Disclosure:} In accordance with Springer Nature Editorial Policies regarding generative AI and large language models, the authors disclose that an AI coding assistant was used during the preparation of this work solely to assist with code optimization and automated grammar and syntax checks. No AI tools were used for the conception of research hypotheses, mathematical derivations, experimental designs, empirical analyses, scientific conclusions, or manuscript drafting. All intellectual work and manuscript content were produced and verified exclusively by the authors.
\end{itemize}

\bibliography{references}

\end{document}
'''

full_text = preamble + body + declarations

with open('springer_manuscript/main.tex', 'w', encoding='utf-8') as out:
    out.write(full_text)

print('Generated springer_manuscript/main.tex successfully! Length:', len(full_text))
