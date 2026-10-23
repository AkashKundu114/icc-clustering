import numpy as np
from scipy import stats

def bc(x):
    n = len(x)
    g = stats.skew(x, bias=False)
    k = stats.kurtosis(x, fisher=True, bias=False)
    return (g**2 + 1.0) / (k + 3.0 * (n - 1) ** 2 / ((n - 2) * (n - 3)))

def draw(fam, n, rng):
    if fam == "F1 Gaussian":
        return rng.standard_normal(n)
    if fam == "F2 t5":
        return rng.standard_t(5, n)
    if fam == "F3 Uniform":
        return rng.uniform(0, 1, n)
    if fam == "F4 Beta(3,1)":
        return rng.beta(3, 1, n)
    if fam == "F5 log1p Poisson-lognormal":
        lam = np.exp(rng.normal(1, 1, n))
        return np.log1p(rng.poisson(lam))
    if fam == "Informative D=2":
        s = rng.choice([-1, 1], n)
        return s * 2.0 + rng.standard_normal(n)
    if fam == "Informative D=3":
        s = rng.choice([-1, 1], n)
        return s * 3.0 + rng.standard_normal(n)

if __name__ == "__main__":
    fams = ["F1 Gaussian", "F2 t5", "F3 Uniform", "F4 Beta(3,1)", "F5 log1p Poisson-lognormal", "Informative D=2", "Informative D=3"]
    rng = np.random.default_rng(10000)
    print("Finite-sample corrected BC: mean (sd) and P(BC>=5/9)")
    for fam in fams:
        row = []
        for n in [60, 100, 250, 1000]:
            v = np.array([bc(draw(fam, n, rng)) for _ in range(2000)])
            row.append(f"N={n}: {v.mean():.3f} ({v.std():.3f}) P={np.mean(v >= 5/9):.2f}")
        print(f"{fam:28s} " + " | ".join(row))

    print()
    print("Population BC checks via large sample (N=200000)")
    for fam in fams:
        x = draw(fam, 200000, rng)
        g = stats.skew(x); k = stats.kurtosis(x)
        print(f"{fam:28s} BC={(g**2+1)/(k+3):.4f} skew={g:.3f} exkurt={k:.3f}")

    print()
    a = np.linspace(-40, 40, 4001)
    best = 0
    for al in a:
        d = al / np.sqrt(1 + al**2)
        m = stats.skewnorm.stats(al, moments="sk")
        g, k = float(m[0]), float(m[1])
        b = (g**2 + 1) / (k + 3)
        best = max(best, b)
    print(f"Max population BC over skew-normal family: {best:.4f}")
