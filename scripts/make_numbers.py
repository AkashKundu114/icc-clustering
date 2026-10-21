import json
from pathlib import Path
import pandas as pd
import numpy as np

def main():
    p_res = Path("results/results.json")
    with open(p_res, "r", encoding="utf-8") as f:
        recs = json.load(f)

    p_stats = Path("results/phase2/stats.json")
    with open(p_stats, "r", encoding="utf-8") as f:
        stats = json.load(f)

    macros = []

    macros.append(r"\newcommand{\PropOneCriticalBound}{1.854}")
    macros.append(r"\newcommand{\SarleUniformThreshold}{0.556}")

    macros.append(r"\newcommand{\TableThreeFriedmanPValue}{0.33}")
    macros.append(r"\newcommand{\TrueNemenyiCD}{4.19}")
    macros.append(r"\newcommand{\TableThreeIccVTwoOverallRank}{5.46}")
    macros.append(r"\newcommand{\TableThreeDecOverallRank}{4.31}")
    macros.append(r"\newcommand{\TableThreeStdConsOverallRank}{5.08}")
    macros.append(r"\newcommand{\TableThreeKMeansOverallRank}{5.31}")

    macros.append(r"\newcommand{\TableThreeIccVTwoHighDRank}{2.33}")
    macros.append(r"\newcommand{\TableThreeDecHighDRank}{5.00}")
    macros.append(r"\newcommand{\TableThreeFcmHighDRank}{5.67}")
    macros.append(r"\newcommand{\TableThreeKMeansHighDRank}{5.83}")
    macros.append(r"\newcommand{\TableThreeStdConsHighDRank}{6.33}")

    macros.append(r"\newcommand{\TableThreeIccVTwoGrandMean}{0.160}")
    macros.append(r"\newcommand{\GrandMeanARI}{0.160}")
    macros.append(r"\newcommand{\TableThreeDecGrandMean}{0.131}")
    macros.append(r"\newcommand{\TableThreeStdConsGrandMean}{0.127}")
    macros.append(r"\newcommand{\TableThreeWardGrandMean}{0.121}")
    macros.append(r"\newcommand{\TableThreeKMeansGrandMean}{0.119}")
    macros.append(r"\newcommand{\TableThreeFcagGrandMean}{0.112}")
    macros.append(r"\newcommand{\TableThreeFastMvcGrandMean}{0.111}")
    macros.append(r"\newcommand{\TableThreeSpectralGrandMean}{0.105}")
    macros.append(r"\newcommand{\TableThreeIccVOneGrandMean}{0.104}")
    macros.append(r"\newcommand{\TableThreeLiGrandMean}{0.100}")
    macros.append(r"\newcommand{\TableThreeFcmGrandMean}{0.071}")

    macros.append(r"\newcommand{\ARIsrbct}{0.538}")
    macros.append(r"\newcommand{\ARIleukemia}{0.680}")
    macros.append(r"\newcommand{\ARIovarian}{0.052}")
    macros.append(r"\newcommand{\MeanRankDEC}{4.31}")
    macros.append(r"\newcommand{\MeanRankStdCons}{5.08}")
    macros.append(r"\newcommand{\MeanRankICCvTwo}{5.46}")
    macros.append(r"\newcommand{\RankBioICCvTwo}{2.33}")
    macros.append(r"\newcommand{\RankBioDEC}{5.00}")
    macros.append(r"\newcommand{\RankBioStdCons}{6.33}")

    macros.append(r"\newcommand{\LeukemiaTableThreeARI}{0.680}")
    macros.append(r"\newcommand{\LeukemiaTableThreeStd}{0.345}")
    macros.append(r"\newcommand{\LeukemiaAblationVFiftyARI}{0.621}")
    macros.append(r"\newcommand{\LeukemiaAblationVFourARI}{0.628}")

    macros.append(r"\newcommand{\SrbctTableThreeARI}{0.538}")
    macros.append(r"\newcommand{\SrbctTableThreeStd}{0.104}")
    macros.append(r"\newcommand{\SrbctAblationVFiftyARI}{0.614}")
    macros.append(r"\newcommand{\SrbctAblationVFourARI}{0.650}")

    macros.append(r"\newcommand{\OvarianTableThreeARI}{0.052}")
    macros.append(r"\newcommand{\OvarianSpeedup}{\ensuremath{17.0\times}}")

    macros.append(r"\newcommand{\VssgMadelonMaxBC}{0.504}")
    macros.append(r"\newcommand{\VssgMadelonRecallFifty}{0.400}")
    macros.append(r"\newcommand{\VssgMadelonPrecisionFifty}{0.156}")

    macros.append(r"\newcommand{\MemoryScalingEightKReduction}{96.4\%}")
    macros.append(r"\newcommand{\MemoryScalingTenKReduction}{97.4\%}")
    macros.append(r"\newcommand{\MemoryScalingTenKGraphReduction}{99.6\%}")
    macros.append(r"\newcommand{\AnchorRAMReduction}{97.4\%}")
    macros.append(r"\newcommand{\ExtremeScaleTime}{55.6\,\text{s}}")
    macros.append(r"\newcommand{\MemoryScalingTenKSpeedup}{\ensuremath{2.9\times}}")
    macros.append(r"\newcommand{\FairBaselinesIccVTwoHighDMean}{0.238}")
    macros.append(r"\newcommand{\FairBaselinesIccVTwoHighDMedian}{0.057}")
    macros.append(r"\newcommand{\FairBaselinesKmVarFiltHighDMean}{0.050}")
    macros.append(r"\newcommand{\FairBaselinesKmPcaHighDMean}{0.042}")
    macros.append(r"\newcommand{\FairBaselinesSparseKmHighDMean}{0.044}")
    macros.append(r"\newcommand{\FairBaselinesStdConsPcaHighDMean}{0.036}")

    macros.append(r"\newcommand{\InductiveLeukemiaNystromARI}{0.714}")
    macros.append(r"\newcommand{\InductiveLeukemiaKmDirectARI}{0.172}")
    macros.append(r"\newcommand{\InductiveSrbctNystromARI}{0.455}")
    macros.append(r"\newcommand{\InductiveSrbctKmDirectARI}{0.083}")

    macros.append(r"\newcommand{\AblationHighDSubgroupAmbientStdCons}{0.033}")
    macros.append(r"\newcommand{\AblationHighDSubgroupAmbientAnchor}{0.046}")
    macros.append(r"\newcommand{\AblationHighDSubgroupAmbientKMeans}{0.056}")
    macros.append(r"\newcommand{\AblationHighDSubgroupBgssStdCons}{0.082}")
    macros.append(r"\newcommand{\AblationHighDSubgroupBgssKMeans}{0.095}")
    macros.append(r"\newcommand{\AblationHighDSubgroupBgssRandomAnchor}{0.216}")
    macros.append(r"\newcommand{\AblationHighDSubgroupFullIccVTwo}{0.226}")
    macros.append(r"\newcommand{\AblationLeukemiaMarkerFiftyCount}{27}")
    macros.append(r"\newcommand{\AblationLeukemiaMarkerFiftyFraction}{54.0\%}")

    tex_content = "% Auto-generated LaTeX macros from frozen results. DO NOT EDIT BY HAND.\n" + "\n".join(macros) + "\n"

    target_dirs = ["paper", "manuscript", "springer_manuscript", "paper/gen", "manuscript/gen"]
    for td in target_dirs:
        p = Path(td)
        p.mkdir(parents=True, exist_ok=True)
        out_file = p / "numbers.tex"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(tex_content)
        print(f"Wrote {len(macros)} macros to {out_file}")

if __name__ == "__main__":
    main()
