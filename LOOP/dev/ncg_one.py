import sys, time
import numpy as np
from scipy import stats

def bc(x):
    n = len(x)
    g = stats.skew(x, bias=False)
    k = stats.kurtosis(x, fisher=True, bias=False)
    return (g**2 + 1.0) / (k + 3.0 * (n - 1) ** 2 / ((n - 2) * (n - 3)))

def nmodes(x, h, grid):
    d = np.exp(-(grid[:, None] - x[None, :]) ** 2 / (2 * h * h)).sum(1)
    return int(np.sum((d[1:-1] > d[:-2]) & (d[1:-1] > d[2:])))

def crit_h(x, grid):
    lo, hi = 0.01, 2.5
    if nmodes(x, lo, grid) <= 1:
        return lo
    for _ in range(12):
        mid = 0.5 * (lo + hi)
        if nmodes(x, mid, grid) <= 1:
            hi = mid
        else:
            lo = mid
    return hi

def scb_decoy(x, rng, grid):
    h = crit_h(x, grid)
    xs = rng.choice(x, len(x))
    m = x.mean()
    return m + (xs - m + h * rng.standard_normal(len(x))) / np.sqrt(1 + h * h / x.var())

def sn_decoy(x, rng):
    try:
        a, loc, sc = stats.skewnorm.fit(x)
        return stats.skewnorm.rvs(a, loc, sc, size=len(x), random_state=rng)
    except Exception:
        return rng.normal(x.mean(), x.std(), len(x))

def knock(W, q):
    for t in np.sort(np.abs(W[W != 0])):
        if (1 + np.sum(W <= -t)) / max(1, np.sum(W >= t)) <= q:
            return np.where(W >= t)[0]
    return np.array([], dtype=int)

def make(N, D, dstar, delta, fam, rng):
    y = rng.choice([-1, 1], N)
    X = np.empty((N, D))
    for j in range(D):
        if j < dstar:
            X[:, j] = y * delta + rng.standard_normal(N)
        elif fam == "Gaussian":
            X[:, j] = rng.standard_normal(N)
        elif fam == "Uniform":
            X[:, j] = rng.uniform(0, 1, N)
        elif fam == "Beta31":
            X[:, j] = rng.beta(3, 1, N)
    X = (X - X.mean(0)) / X.std(0)
    return X

def score(S, dstar, D):
    S = np.asarray(S)
    if len(S) == 0:
        return 0.0, 0.0
    fdp = np.sum(S >= dstar) / len(S)
    pw = np.sum(S < dstar) / dstar
    return fdp, pw

def run(fam, delta, reps, use_sn, N=250, D=300, dstar=20, q=0.10):
    grid = np.linspace(-3.5, 3.5, 200)
    res = {"SCB": [], "SN": [], "G2": []}
    for r in range(reps):
        rng = np.random.default_rng(10000 + r)
        X = make(N, D, dstar, delta, fam, rng)
        s = np.array([bc(X[:, j]) for j in range(D)])
        st = np.array([bc(scb_decoy(X[:, j], rng, grid)) for j in range(D)])
        res["SCB"].append(score(knock(s - st, q), dstar, D))
        if use_sn:
            sn = np.array([bc(sn_decoy(X[:, j], rng)) for j in range(D)])
            res["SN"].append(score(knock(s - sn, q), dstar, D))
        cap = max(100, int(np.ceil(0.15 * D)))
        cand = np.where(s >= 5 / 9)[0]
        cand = cand[np.argsort(-s[cand])][:cap]
        res["G2"].append(score(cand, dstar, D))
    out = {}
    for k, v in res.items():
        if v:
            a = np.array(v)
            out[k] = (a[:, 0].mean(), a[:, 1].mean())
    return out

if __name__ == "__main__":
    fam, delta, reps, sn = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), sys.argv[4] == "1"
    t0 = time.time()
    o = run(fam, delta, reps, sn)
    s = " | ".join(f"{k}: FDP={v[0]:.2f} power={v[1]:.2f}" for k, v in o.items())
    print(f"N=250 D=300 d*=20 nuisance={fam:8s} half-sep={delta} reps={reps}: {s} [{time.time()-t0:.0f}s]", flush=True)
