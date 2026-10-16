"""
Adversarial Input, Boundary Condition, and Security Hardening Tests for ICC-v2.

Covers:
1. Malformed and out-of-bounds initialization parameters.
2. Degenerate inputs (1D, 3D, empty arrays, N < K).
3. Hostile numerical values (NaN, +Inf, -Inf, unhandled types).
4. Un-fitted model invocation defenses.
5. Out-of-sample dimension mismatch and adversarial query defense.
6. Empty out-of-sample queries (zero-length batch safety).
7. Transform distance API consistency and extreme magnitude stability.
"""

import numpy as np
import pytest

from src.icc.consensus_v2 import InvariantCoreConsensusV2


class TestHyperparameterValidation:
    """Verifies that out-of-bound or malicious parameters are rejected at initialization."""

    @pytest.mark.parametrize("n_clusters", [0, 1, -2])
    def test_invalid_n_clusters(self, n_clusters):
        with pytest.raises(ValueError, match="n_clusters must be >= 2"):
            InvariantCoreConsensusV2(n_clusters=n_clusters)

    @pytest.mark.parametrize("n_base_models", [0, -1, -10])
    def test_invalid_n_base_models(self, n_base_models):
        with pytest.raises(ValueError, match="n_base_models must be >= 1"):
            InvariantCoreConsensusV2(n_clusters=3, n_base_models=n_base_models)

    @pytest.mark.parametrize("n_anchors", [0, -5])
    def test_invalid_n_anchors(self, n_anchors):
        with pytest.raises(ValueError, match="n_anchors must be >= 1"):
            InvariantCoreConsensusV2(n_clusters=3, n_anchors=n_anchors)

    @pytest.mark.parametrize("core_quantile", [-0.1, 0.0, 1.05, 2.0])
    def test_invalid_core_quantile(self, core_quantile):
        with pytest.raises(ValueError, match="core_quantile must be in \\(0, 1\\]"):
            InvariantCoreConsensusV2(n_clusters=3, core_quantile=core_quantile)

    @pytest.mark.parametrize("subspace_rate", [-0.5, 0.0, 1.1, 5.0])
    def test_invalid_subspace_rate(self, subspace_rate):
        with pytest.raises(ValueError, match="subspace_rate must be in \\(0, 1\\]"):
            InvariantCoreConsensusV2(n_clusters=3, subspace_rate=subspace_rate)

    @pytest.mark.parametrize("bad_mode", ["malicious_code", "exec", "__proto__", "eval"])
    def test_invalid_pool_mode(self, bad_mode):
        with pytest.raises(ValueError, match="Invalid pool_mode"):
            InvariantCoreConsensusV2(n_clusters=3, pool_mode=bad_mode)


class TestDegenerateFitInputs:
    """Verifies robustness against degenerate, malformed, or malicious training data."""

    def test_rejects_1d_input(self):
        model = InvariantCoreConsensusV2(n_clusters=2)
        X_1d = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        with pytest.raises(ValueError, match="Expected 2D feature matrix"):
            model.fit_predict(X_1d)

    def test_rejects_3d_input(self):
        model = InvariantCoreConsensusV2(n_clusters=2)
        X_3d = np.ones((10, 5, 2))
        with pytest.raises(ValueError, match="Expected 2D feature matrix"):
            model.fit_predict(X_3d)

    def test_rejects_empty_input(self):
        model = InvariantCoreConsensusV2(n_clusters=2)
        with pytest.raises(ValueError, match="Input feature matrix cannot be empty"):
            model.fit_predict(np.empty((0, 5)))
        with pytest.raises(ValueError, match="Input feature matrix cannot be empty"):
            model.fit_predict(np.empty((10, 0)))

    def test_rejects_fewer_samples_than_clusters(self):
        model = InvariantCoreConsensusV2(n_clusters=5)
        X = np.ones((4, 10))
        with pytest.raises(ValueError, match="n_samples=4 must be >= n_clusters=5"):
            model.fit_predict(X)

    def test_rejects_nan_values(self):
        model = InvariantCoreConsensusV2(n_clusters=2)
        rng = np.random.default_rng(42)
        X = rng.normal(size=(20, 5))
        X[3, 2] = np.nan
        with pytest.raises(ValueError, match="contains NaN or Inf"):
            model.fit_predict(X)

    def test_rejects_inf_values(self):
        model = InvariantCoreConsensusV2(n_clusters=2)
        rng = np.random.default_rng(42)
        X = rng.normal(size=(20, 5))
        X[10, 1] = np.inf
        with pytest.raises(ValueError, match="contains NaN or Inf"):
            model.fit_predict(X)

        X[10, 1] = -np.inf
        with pytest.raises(ValueError, match="contains NaN or Inf"):
            model.fit_predict(X)


class TestUnfittedModelGuards:
    """Ensures methods cannot be executed on unfitted estimators."""

    def test_unfitted_calls_raise_runtime_error(self):
        model = InvariantCoreConsensusV2(n_clusters=3)
        X_test = np.ones((5, 4))

        with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
            model.predict(X_test)

        with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
            model.predict_proba(X_test)

        with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
            model.predict_with_stability(X_test)

        with pytest.raises(RuntimeError, match="Model has not been fitted yet"):
            model.transform(X_test)


class TestOutOfSampleAdversarialInputs:
    """Verifies safe rejection and handling of malformed inductive query samples."""

    @pytest.fixture
    def fitted_model_and_data(self):
        rng = np.random.default_rng(42)
        X_train = rng.normal(size=(30, 8))
        model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=5, n_anchors=6, random_state=42)
        model.fit_predict(X_train)
        return model, rng

    def test_dimension_mismatch_rejection(self, fitted_model_and_data):
        model, rng = fitted_model_and_data
        # Fitted on D=8; test on D=5 and D=10
        X_wrong_1 = rng.normal(size=(10, 5))
        X_wrong_2 = rng.normal(size=(10, 10))

        with pytest.raises(ValueError, match="Feature dimension mismatch"):
            model.predict(X_wrong_1)

        with pytest.raises(ValueError, match="Feature dimension mismatch"):
            model.predict_proba(X_wrong_2)

        with pytest.raises(ValueError, match="Feature dimension mismatch"):
            model.transform(X_wrong_1)

    def test_out_of_sample_nan_inf_rejection(self, fitted_model_and_data):
        model, rng = fitted_model_and_data
        X_nan = rng.normal(size=(5, 8))
        X_nan[1, 2] = np.nan

        X_inf = rng.normal(size=(5, 8))
        X_inf[4, 0] = np.inf

        with pytest.raises(ValueError, match="X_new contains NaN or Inf"):
            model.predict(X_nan)

        with pytest.raises(ValueError, match="X_new contains NaN or Inf"):
            model.predict_proba(X_inf)

        with pytest.raises(ValueError, match="X_new contains NaN or Inf"):
            model.transform(X_nan)

    def test_out_of_sample_shape_rejection(self, fitted_model_and_data):
        model, _ = fitted_model_and_data
        with pytest.raises(ValueError, match="Expected 2D feature matrix"):
            model.predict(np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]))

    def test_empty_test_set_graceful_handling(self, fitted_model_and_data):
        model, _ = fitted_model_and_data
        X_empty = np.empty((0, 8))

        preds = model.predict(X_empty)
        assert preds.shape == (0,)
        assert preds.dtype == int

        proba = model.predict_proba(X_empty)
        assert proba.shape == (0, 3)
        assert proba.dtype == np.float64

        dist = model.transform(X_empty)
        assert dist.shape == (0, 3)
        assert dist.dtype == np.float64

        stab = model.predict_with_stability(X_empty)
        assert stab["labels"].shape == (0,)
        assert stab["confidence"].shape == (0,)
        assert stab["margin"].shape == (0,)


class TestTransformAndNumericalStability:
    """Tests the transform API and extreme magnitude stability."""

    def test_transform_predict_consistency(self):
        rng = np.random.default_rng(123)
        X_train = rng.normal(size=(40, 6))
        model = InvariantCoreConsensusV2(n_clusters=3, n_base_models=5, n_anchors=6, random_state=123)
        model.fit_predict(X_train)

        X_test = rng.normal(size=(10, 6))
        dists = model.transform(X_test, subspace=True)
        preds = model.predict(X_test, subspace=True)

        assert dists.shape == (10, 3)
        assert np.array_equal(np.argmin(dists, axis=1), preds)

    def test_scaled_data_stability(self):
        rng = np.random.default_rng(999)
        # Moderate extreme scaling (1e6) to test arithmetic stability without under/overflow
        X_scaled = rng.normal(scale=1e6, size=(30, 10))
        model = InvariantCoreConsensusV2(n_clusters=2, n_base_models=5, n_anchors=5, random_state=999)
        labels = model.fit_predict(X_scaled)
        assert labels.shape == (30,)
        assert not np.isnan(labels).any()
