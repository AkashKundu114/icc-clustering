import numpy as np
import pytest

from src.icc.consensus_v2 import InvariantCoreConsensusV2 as ICC
from src.icc.core import build_dataset


def _data():
    return build_dataset(20, "gaussian", noise_seed=0, sizes=[40, 40, 40], k=3, signal_dim=2)

def test_beta_is_deprecated_and_has_no_effect():
    X, _ = _data()
    with pytest.warns(DeprecationWarning):
        m1 = ICC(n_clusters=3, beta=5.0, random_state=0)
    m2 = ICC(n_clusters=3, random_state=0)
    assert np.array_equal(m1.fit_predict(X), m2.fit_predict(X))

def test_default_behaviour_unchanged_options_are_opt_in():
    X, _ = _data()
    base = ICC(n_clusters=3, random_state=0).fit_predict(X)
    same = ICC(n_clusters=3, random_state=0, pool_mode="legacy", embedding="legacy").fit_predict(X)
    assert np.array_equal(base, same)

@pytest.mark.parametrize("emb", ["legacy", "transfer_cut"])
def test_embedding_finite_and_valid_labels(emb):
    X, _ = _data()
    m = ICC(n_clusters=3, random_state=0, embedding=emb)
    lab = m.fit_predict(X)
    assert np.isfinite(m.U_emb_).all() and set(lab) <= {0, 1, 2}

def test_invalid_options_raise():
    X, _ = _data()
    with pytest.raises(ValueError):
        ICC(n_clusters=3, embedding="nope").fit_predict(X)
    with pytest.raises(ValueError):
        ICC(n_clusters=3, pool_mode="nope").fit_predict(X)

@pytest.mark.parametrize("mode", ["bc_frac", "random_frac"])
def test_pool_mode_frac_options(mode):
    X, _ = _data()
    m = ICC(n_clusters=3, pool_mode=mode, pool_frac=0.10, random_state=0)
    lab = m.fit_predict(X)
    assert len(lab) == len(X)
    assert set(lab) <= {0, 1, 2}
    assert m.selected_features_ is not None
    assert len(m.selected_features_) >= 2
