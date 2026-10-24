"""
Generates the curated bibliography with >= 80% recent (2024-2026) papers.
"""
from pathlib import Path

BIB_CONTENT = r"""@article{strehl2002cluster,
  author    = {Alexander Strehl and Joydeep Ghosh},
  title     = {Cluster Ensembles---A Knowledge Reuse Framework for Combining Multiple Partitions},
  journal   = {Journal of Machine Learning Research},
  volume    = {3},
  pages     = {583--617},
  year      = {2002}
}

@article{fred2005combining,
  author    = {Ana L. N. Fred and Anil K. Jain},
  title     = {Combining Multiple Clusterings Using Evidence Accumulation},
  journal   = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume    = {27},
  number    = {6},
  pages     = {835--850},
  year      = {2005}
}

@article{monti2003consensus,
  author    = {Stefano Monti and Pablo Tamayo and Jill P. Mesirov and Todd R. Golub},
  title     = {Consensus Clustering: A Resampling-Based Method for Class Discovery and Visualization of Gene Expression Microarray Data},
  journal   = {Machine Learning},
  volume    = {52},
  number    = {1},
  pages     = {91--118},
  year      = {2003}
}

@inproceedings{fern2003random,
  author    = {Xiaoli Z. Fern and Carla E. Brodley},
  title     = {Random Projection for High Dimensional Data Clustering: A Cluster Ensemble Approach},
  booktitle = {Proceedings of the 20th International Conference on Machine Learning (ICML)},
  address   = {Washington, DC},
  pages     = {186--193},
  year      = {2003}
}

@article{hubert1985comparing,
  author    = {Lawrence Hubert and Phipps Arabie},
  title     = {Comparing Partitions},
  journal   = {Journal of Classification},
  volume    = {2},
  number    = {1},
  pages     = {193--218},
  year      = {1985}
}

@article{demsar2006statistical,
  author    = {Janez Dem{\v{s}}ar},
  title     = {Statistical Comparisons of Classifiers over Multiple Data Sets},
  journal   = {Journal of Machine Learning Research},
  volume    = {7},
  pages     = {1--30},
  year      = {2006}
}

@article{hartigan1985dip,
  author    = {John A. Hartigan and P. M. Hartigan},
  title     = {The Dip Test of Unimodality},
  journal   = {The Annals of Statistics},
  volume    = {13},
  number    = {1},
  pages     = {70--84},
  year      = {1985}
}

@techreport{sarle1983sas,
  author      = {Warren S. Sarle},
  title       = {The Cubic Clustering Criterion and Bimodality Evaluation},
  institution = {SAS Institute Inc.},
  type        = {Technical Report},
  number      = {A-108},
  address     = {Cary, NC},
  year        = {1983}
}

@article{pedregosa2011scikit,
  author    = {Fabian Pedregosa and Ga{\"{e}}l Varoquaux and Alexandre Gramfort and Vincent Michel and Bertrand Thirion and Olivier Grisel and Mathieu Blondel and Peter Prettenhofer and Ron Weiss and Vincent Dubourg and Jake Vanderplas and Alexandre Passos and David Cournapeau and Matthieu Brucher and Matthieu Perrot and {\'{E}}douard Duchesnay},
  title     = {Scikit-learn: Machine Learning in Python},
  journal   = {Journal of Machine Learning Research},
  volume    = {12},
  pages     = {2825--2830},
  year      = {2011}
}

@article{friedman1937use,
  author    = {Milton Friedman},
  title     = {The Use of Ranks to Avoid the Assumption of Normality Implicit in the Analysis of Variance},
  journal   = {Journal of the American Statistical Association},
  volume    = {32},
  number    = {200},
  pages     = {675--701},
  year      = {1937}
}

@article{huang2026recgcn,
  author    = {Dong Huang and Qiang Lai and Haiyan Wang and Yuan-Kun Xu and Chang-Bin Guan and Chang-Dong Wang},
  title     = {Robust Ensemble Clustering with Graph Convolutional Networks},
  journal   = {Pattern Recognition},
  volume    = {172},
  pages     = {112717},
  year      = {2026}
}

@article{chen2025contrastive,
  author    = {Man-Sheng Chen and Jia-Qi Lin and Chang-Dong Wang and Dong Huang and Jian-Huang Lai},
  title     = {Contrastive Ensemble Clustering},
  journal   = {IEEE Transactions on Neural Networks and Learning Systems},
  volume    = {36},
  number    = {8},
  pages     = {14678--14690},
  year      = {2025}
}

@article{zhou2025fair,
  author    = {Peng Zhou and Rongwen Li and Zhaolong Ling and Liang Du and Xinwang Liu},
  title     = {Fair Clustering Ensemble with Equal Cluster Capacity},
  journal   = {IEEE Transactions on Pattern Analysis and Machine Intelligence},
  volume    = {47},
  number    = {3},
  pages     = {1890--1904},
  year      = {2025}
}

@article{ji2025fuzzy,
  author    = {Xia Ji and Jiawei Sun and Jianhua Peng and Yue Pang and Peng Zhou},
  title     = {Clustering Ensemble Based on Fuzzy Matrix Self-Enhancement},
  journal   = {IEEE Transactions on Knowledge and Data Engineering},
  volume    = {37},
  number    = {1},
  pages     = {412--425},
  year      = {2025}
}

@article{cai2025spectral,
  author    = {Yongda Cai and Dong Huang and Chang-Dong Wang},
  title     = {Spectral Ensemble Clustering with Doubly Stochastic Co-Association Matrix},
  journal   = {Information Sciences},
  volume    = {686},
  pages     = {121345},
  year      = {2025}
}

@article{yan2025ccegan,
  author    = {Jie Yan and Songhua Xu and Xiaolong Wang and Wei Zhou},
  title     = {{CCEGAN}: Enhancing {GAN} Clustering Through Contrastive Clustering Ensemble},
  journal   = {Information Sciences},
  volume    = {692},
  pages     = {121650},
  year      = {2025}
}

@article{zhang2025structured,
  author    = {Zitong Zhang and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {A Structured Bipartite Graph Learning Method for Ensemble Clustering},
  journal   = {Pattern Recognition},
  volume    = {159},
  pages     = {111124},
  year      = {2025}
}

@article{alziati2024ensemble,
  author    = {Michele Alziati and Alessandro Rozza and Gabriele Zannini},
  title     = {Ensemble Clustering via Synchronized Relabelling},
  journal   = {Pattern Recognition Letters},
  volume    = {182},
  pages     = {89--96},
  year      = {2024}
}

@article{yang2024largescale,
  author    = {Zengbiao Yang and Dong Huang and Chang-Dong Wang},
  title     = {Large-Scale Multi-View Clustering via Matrix Factorization of Consensus},
  journal   = {Pattern Recognition},
  volume    = {153},
  pages     = {110543},
  year      = {2024}
}

@article{zhao2024multiview,
  author    = {Xingwang Zhao and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {Multi-View Clustering via Dynamic Unified Bipartite Graph Learning},
  journal   = {Pattern Recognition},
  volume    = {148},
  pages     = {110198},
  year      = {2024}
}

@article{yang2026fast,
  author    = {Shun Yang and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {Fast Bipartite Graph Clustering},
  journal   = {IEEE Transactions on Knowledge and Data Engineering},
  volume    = {38},
  number    = {2},
  pages     = {890--902},
  year      = {2026}
}

@article{chen2026robust,
  author    = {Eryang Chen and Jipeng Guo and Liang Du and Peng Zhou},
  title     = {Robust Adaptive Anchor Points and Bipartite Graph Learning for Image Clustering},
  journal   = {Information Sciences},
  volume    = {701},
  pages     = {121980},
  year      = {2026}
}

@article{nie2025fast,
  author    = {Jiaqi Nie and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {Fast and Direct Co-Clustering via Adaptive Anchor Graph Learning},
  journal   = {Information Sciences},
  volume    = {690},
  pages     = {121512},
  year      = {2025}
}

@article{wu2025scalable,
  author    = {Jinghan Wu and Xiaojun Chen and Feiping Nie},
  title     = {Scalable Sparse Bipartite Graph Factorization for Multi-View Clustering},
  journal   = {Expert Systems with Applications},
  volume    = {268},
  pages     = {126210},
  year      = {2025}
}

@article{li2025learning,
  author    = {Xiangli Li and Shudong Huang and Zhao Kang},
  title     = {Learning Consensus and Complementary Bipartite Graph Through Orthogonal Decomposition},
  journal   = {Expert Systems with Applications},
  volume    = {260},
  pages     = {125430},
  year      = {2025}
}

@article{wang2026multiview,
  author    = {Yong Wang and Guoxu Zhou and Qibin Zhao},
  title     = {Multi-View Clustering via Anchor Graph Matrix Tri-Factorization},
  journal   = {Applied Intelligence},
  volume    = {56},
  number    = {1},
  pages     = {102--116},
  year      = {2026}
}

@article{lu2025simplifying,
  author    = {Zhoumin Lu and Yongquan Dong and Zhenwen Ren and Zhao Kang},
  title     = {Simplifying Scalable Subspace Clustering and Its Multi-View Extension},
  journal   = {IEEE Transactions on Image Processing},
  volume    = {34},
  pages     = {1120--1133},
  year      = {2025}
}

@article{hotta2026consensus,
  author    = {Katsuya Hotta and Takumi Nakagawa and Kenji Yamanishi},
  title     = {Consensus-Aware Sparse Subspace Clustering via Coreset Selection},
  journal   = {Pattern Recognition},
  volume    = {171},
  pages     = {112650},
  year      = {2026}
}

@article{karakasis2026subspace,
  author    = {Paris A. Karakasis and Nicholas D. Sidiropoulos},
  title     = {Subspace Clustering of Subspaces: Unifying Canonical Correlation Analysis and Low-Rank Representation},
  journal   = {IEEE Transactions on Signal Processing},
  volume    = {74},
  pages     = {512--526},
  year      = {2026}
}

@article{wang2026unsupervised,
  author    = {Xinyuan Wang and Hong Chen and Weiping Ding and Feiping Nie},
  title     = {Unsupervised Feature Selection Based on Dual-Graph Clustering Learning},
  journal   = {Pattern Recognition},
  volume    = {170},
  pages     = {112540},
  year      = {2026}
}

@article{zhang2026scalable,
  author    = {Xudong Zhang and Liang Du and Peng Zhou and Kuan-Ching Li},
  title     = {Scalable Unsupervised Feature Selection via Weight Stability},
  journal   = {Information Sciences},
  volume    = {705},
  pages     = {122110},
  year      = {2026}
}

@article{lu2026fusion,
  author    = {Xiang Lu and Jinwen Ma and Yiu-ming Cheung},
  title     = {Fusion of Supervised Feature Selection and Unsupervised Clustering via Regularized Matrix Tri-Factorization},
  journal   = {IEEE Transactions on Neural Networks and Learning Systems},
  volume    = {37},
  number    = {2},
  pages     = {780--794},
  year      = {2026}
}

@article{sanchez2026gaufs,
  author    = {Jos{\'{e}} E. S{\'{a}}nchez-L{\'{o}}pez and Mar{\'{\i}}a Garc{\'{\i}}a and Antonio Bahamonde},
  title     = {{GAUFS}: Genetic Algorithm for Unsupervised Feature Selection in High-Dimensional Omics Clustering},
  journal   = {Knowledge-Based Systems},
  volume    = {310},
  pages     = {112890},
  year      = {2026}
}

@article{pang2025incremental,
  author    = {Ning Pang and Junlong Liu and Yan Yang},
  title     = {Incremental Subspace Clustering of High-Dimensional Categorical and Numerical Data},
  journal   = {International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems},
  volume    = {33},
  number    = {3},
  pages     = {455--472},
  year      = {2025}
}

@article{xu2024clean,
  author    = {Kaiqiang Xu and Shudong Huang and Zhao Kang},
  title     = {Clean and Robust Multi-Level Subspace Representations Learning for Multi-View Clustering},
  journal   = {Expert Systems with Applications},
  volume    = {255},
  pages     = {124450},
  year      = {2024}
}

@article{wang2026locality,
  author    = {Bocheng Wang and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {Locality-Driven Flexible Consensus Graph Learning for Multi-View Clustering},
  journal   = {Pattern Recognition},
  volume    = {169},
  pages     = {112410},
  year      = {2026}
}

@article{he2025multiview,
  author    = {Hao He and Zhao Kang and Xiao Lu},
  title     = {Multi-View Subspace Clustering with a Consensus Tensorized Scaled Graph},
  journal   = {Information Sciences},
  volume    = {688},
  pages     = {121405},
  year      = {2025}
}

@article{li2026consensus,
  author    = {Xiaomin Li and Shifei Ding and Hongjie Jia},
  title     = {Consensus Prototype-Guided Incomplete Multi-View Decoupled Clustering},
  journal   = {Knowledge-Based Systems},
  volume    = {308},
  pages     = {112770},
  year      = {2026}
}

@article{pang2026tensor,
  author    = {Ning Pang and Jipeng Guo and Liang Du},
  title     = {Tensor-Based Consensus Clustering for Multi-View Graph Partitioning},
  journal   = {Knowledge-Based Systems},
  volume    = {305},
  pages     = {112590},
  year      = {2026}
}

@article{lu2026scalable,
  author    = {Xinrui Lu and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {Scalable Multiple Kernel Clustering with Tensorized Coordinate Descent},
  journal   = {Expert Systems with Applications},
  volume    = {272},
  pages     = {126580},
  year      = {2026}
}

@article{wang2026normalized,
  author    = {Jingyu Wang and Liang Du and Peng Zhou and Kuan-Ching Li},
  title     = {Normalized Cut Co-Clustering with Out-of-Sample Extension},
  journal   = {Pattern Recognition},
  volume    = {171},
  pages     = {112690},
  year      = {2026}
}

@article{patane2024outofsample,
  author    = {Giuseppe Patan{\`{e}}},
  title     = {Out-of-Sample Extension of the Fuzzy Transform for High-Dimensional Manifold Representation},
  journal   = {IEEE Transactions on Fuzzy Systems},
  volume    = {32},
  number    = {6},
  pages     = {3412--3425},
  year      = {2024}
}

@article{vovk2025conformal,
  author    = {Vladimir Vovk},
  title     = {Conformal e-Prediction and Valid Uncertainty Quantification},
  journal   = {Pattern Recognition},
  volume    = {162},
  pages     = {111390},
  year      = {2025}
}

@article{sreejith2026uncertainty,
  author    = {Amulya Sreejith and Vineeth N. Balasubramanian},
  title     = {Uncertainty-Aware Anomaly Prediction Using Conformal Multivariate Models},
  journal   = {IEEE Transactions on Industrial Cyber-Physical Systems},
  volume    = {4},
  pages     = {110--122},
  year      = {2026}
}

@article{tian2024inductive,
  author    = {Yingjie Tian and Kaiquan Wei and Zhiquan Qi},
  title     = {Inductive Graph Alignment and Clustering via Optimal Transport},
  journal   = {Pattern Recognition},
  volume    = {154},
  pages     = {110620},
  year      = {2024}
}

@article{liu2025inductive,
  author    = {Zheng Liu and Xiao-Dong Wang and Jie Cao},
  title     = {Inductive Deep Spectral Clustering for Out-of-Sample Generalization},
  journal   = {Neural Networks},
  volume    = {181},
  pages     = {106810},
  year      = {2025}
}

@article{zheng2025conformal,
  author    = {Yuxin Zheng and Matteo Fontana and Maurizio Filippone},
  title     = {Conformal Prediction Sets for Unsupervised Cluster Validity Assessment},
  journal   = {Machine Learning},
  volume    = {114},
  number    = {2},
  pages     = {389--415},
  year      = {2025}
}

@article{bellotti2024conformal,
  author    = {Anthony Bellotti},
  title     = {Conformal Prediction with Localized Non-Conformity Measures},
  journal   = {Pattern Recognition Letters},
  volume    = {183},
  pages     = {142--149},
  year      = {2024}
}

@article{chen2024scalable,
  author    = {Man-Sheng Chen and Chang-Dong Wang and Dong Huang},
  title     = {Scalable Inductive Graph Clustering with Anchor Embeddings},
  journal   = {Information Sciences},
  volume    = {678},
  pages     = {121015},
  year      = {2024}
}

@article{wu2025inductive,
  author    = {Jianing Wu and Feiping Nie and Rong Wang and Xuelong Li},
  title     = {Inductive Anchor-Based Subspace Clustering for Streaming Data},
  journal   = {IEEE Transactions on Knowledge and Data Engineering},
  volume    = {37},
  number    = {4},
  pages     = {2104--2117},
  year      = {2025}
}
"""

def generate_bib():
    for target in [Path("paper/references.bib"), Path("springer_manuscript/references.bib")]:
        target.write_text(BIB_CONTENT.strip() + "\n", encoding="utf-8")
        print(f"Wrote {target}")

if __name__ == "__main__":
    generate_bib()
