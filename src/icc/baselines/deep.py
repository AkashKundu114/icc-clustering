"""
Deep clustering baselines for the ICC benchmark suite.

Methods:
- DEC: Deep Embedded Clustering (Xie et al., ICML 2016)
- IDEC: Improved Deep Embedded Clustering (Guo et al., IJCAI 2017) [STUB]
- CC: Contrastive Clustering (Li et al., AAAI 2021) [STUB]
- SCAN: Semantic Clustering via Nearest Neighbors (Van Gansbeke et al., ECCV 2020) [STUB]

References:
    Xie, Girshick, Farhadi. "Unsupervised deep embedding for clustering analysis." ICML, 2016.
    GitHub reference: https://github.com/XifengGuo/DEC-keras
"""

import os
import time
from typing import Any, List, Tuple

import numpy as np

from .classical import ModelMetadata

_SKLEARN_AVAILABLE = False
try:
    from sklearn.cluster import KMeans as _SkKMeans
    _test = _SkKMeans(n_clusters=2, n_init=1).fit_predict(np.zeros((4, 2)))
    _SKLEARN_AVAILABLE = True
except (ImportError, Exception):
    _SKLEARN_AVAILABLE = False


def _check_tensorflow():
    """
    Ensure TensorFlow or Keras is installed; raise informative ImportError otherwise.
    """
    # 1. Attempt TensorFlow import
    try:
        import tensorflow as tf
        _ = tf.__version__
        return "tensorflow"
    except (ImportError, Exception):
        pass

    # 2. Attempt Keras import with PyTorch fallback
    try:
        if "KERAS_BACKEND" not in os.environ:
            os.environ["KERAS_BACKEND"] = "torch"
        import keras
        _ = keras.__version__
        return "keras"
    except (ImportError, Exception) as err:
        raise ImportError(
            "TensorFlow and Keras are required for the DEC baseline. "
            "Install via: pip install 'icc[deep]' or pip install tensorflow keras"
        ) from err


def _import_deep_backend():
    """
    Import and initialize deep learning framework (TensorFlow/Keras or Keras-Torch).
    Raises informative ImportError if neither TensorFlow nor Keras is available.
    """
    _check_tensorflow()

    # Attempt TensorFlow first if functional
    try:
        import tensorflow as tf
        from tensorflow import keras
        from tensorflow.keras import layers, losses, models, optimizers
        # Quick validation
        _ = tf.constant(1.0)
        return "tensorflow", tf, keras, layers, models, optimizers, losses
    except (ImportError, Exception):
        pass

    # Fallback to Keras 3 with PyTorch backend
    if "KERAS_BACKEND" not in os.environ:
        os.environ["KERAS_BACKEND"] = "torch"
    import keras
    from keras import layers, losses, models, optimizers
    return "keras", None, keras, layers, models, optimizers, losses


def target_distribution(q: np.ndarray) -> np.ndarray:
    """
    Compute auxiliary target distribution P from soft assignment probabilities Q.

    Mathematical formulation (Xie et al., ICML 2016):
        p_{ij} = (q_{ij}^2 / f_j) / sum_{j'} (q_{ij'}^2 / f_{j'})
        where f_j = sum_i q_{ij} is the soft cluster frequency.

    Parameters
    ----------
    q : np.ndarray of shape (N, K)
        Soft cluster probabilities from Student's t-distribution kernel.

    Returns
    -------
    p : np.ndarray of shape (N, K)
        Refined target distribution normalized per row.
    """
    q_arr = np.asarray(q, dtype=np.float64)
    col_sums = q_arr.sum(axis=0) + 1e-10
    weight = q_arr ** 2 / col_sums
    row_sums = weight.sum(axis=1, keepdims=True) + 1e-10
    p = weight / row_sums
    return p.astype(np.float32)


def _build_clustering_layer_cls(layers_module):
    """Dynamically instantiate ClusteringLayer based on the active Keras layers module."""

    class ClusteringLayer(layers_module.Layer):
        """
        Clustering layer converts latent representations into soft cluster assignments
        using Student's t-distribution kernel (Xie et al., 2016).
        """
        def __init__(self, n_clusters: int, alpha: float = 1.0, initial_weights=None, **kwargs):
            super().__init__(**kwargs)
            self.n_clusters = n_clusters
            self.alpha = alpha
            self.initial_weights = initial_weights
            self.clusters = None

        def build(self, input_shape):
            feature_dim = input_shape[-1]
            self.clusters = self.add_weight(
                shape=(self.n_clusters, feature_dim),
                initializer="glorot_uniform",
                name="clusters",
                trainable=True,
            )
            if self.initial_weights is not None:
                self.set_weights(self.initial_weights)
                del self.initial_weights
            super().build(input_shape)

        def call(self, inputs):
            # Try keras.ops if available (Keras 3 multi-backend)
            try:
                from keras import ops
                inputs_exp = ops.expand_dims(inputs, axis=1)
                clusters_exp = ops.expand_dims(self.clusters, axis=0)
                dist_sq = ops.sum(ops.square(inputs_exp - clusters_exp), axis=-1)
                q = 1.0 / (1.0 + (dist_sq / self.alpha))
                q = ops.power(q, (self.alpha + 1.0) / 2.0)
                return q / ops.sum(q, axis=1, keepdims=True)
            except (ImportError, Exception):
                # Fallback to TensorFlow Keras backend
                import tensorflow as tf
                inputs_exp = tf.expand_dims(inputs, axis=1)
                clusters_exp = tf.expand_dims(self.clusters, axis=0)
                dist_sq = tf.reduce_sum(tf.square(inputs_exp - clusters_exp), axis=-1)
                q = 1.0 / (1.0 + (dist_sq / self.alpha))
                q = tf.pow(q, (self.alpha + 1.0) / 2.0)
                return q / tf.reduce_sum(q, axis=1, keepdims=True)

        def compute_output_shape(self, input_shape):
            return (input_shape[0], self.n_clusters)

        def get_config(self):
            config = super().get_config()
            config.update({
                "n_clusters": self.n_clusters,
                "alpha": self.alpha,
            })
            return config

    return ClusteringLayer


def build_autoencoder(
    dims: List[int],
    layers_module,
    models_module,
    act: str = "relu",
    init: str = "glorot_uniform",
) -> Tuple[Any, Any]:
    """
    Construct symmetric fully-connected autoencoder.

    Parameters
    ----------
    dims : list of int
        Layer dimensions: [D, 500, 500, 2000, 10]
    layers_module : module
        Keras layers module.
    models_module : module
        Keras models module.

    Returns
    -------
    autoencoder : Model
        Full reconstruction autoencoder (inputs -> reconstruction).
    encoder : Model
        Bottleneck encoder (inputs -> latent representations).
    """
    n_stacks = len(dims) - 1
    x_in = layers_module.Input(shape=(dims[0],), name="input")
    h = x_in

    # Encoder hidden layers
    for i in range(n_stacks - 1):
        h = layers_module.Dense(
            dims[i + 1],
            activation=act,
            kernel_initializer=init,
            name=f"encoder_{i}",
        )(h)

    # Latent bottleneck layer
    latent = layers_module.Dense(
        dims[-1],
        kernel_initializer=init,
        name="latent",
    )(h)

    # Decoder hidden layers
    h = latent
    for i in range(n_stacks - 1, 0, -1):
        h = layers_module.Dense(
            dims[i],
            activation=act,
            kernel_initializer=init,
            name=f"decoder_{i}",
        )(h)

    # Reconstruction output layer
    x_out = layers_module.Dense(
        dims[0],
        kernel_initializer=init,
        name="decoder_out",
    )(h)

    autoencoder = models_module.Model(inputs=x_in, outputs=x_out, name="autoencoder")
    encoder = models_module.Model(inputs=x_in, outputs=latent, name="encoder")
    return autoencoder, encoder


def run_dec(
    X: np.ndarray,
    k: int,
    seed: int = 42,
    pretrain_epochs: int = 200,
    finetune_epochs: int = 100,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Deep Embedded Clustering (DEC, Xie et al., ICML 2016).

    Pipeline:
    1. Symmetric Autoencoder: D -> 500 -> 500 -> 2000 -> 10 -> 2000 -> 500 -> 500 -> D
    2. Pretrain autoencoder with MSE reconstruction loss.
    3. Initialize cluster centers via KMeans on latent representations Z.
    4. Fine-tune end-to-end with KL-divergence clustering loss using Student-t kernel.

    Parameters
    ----------
    X : np.ndarray of shape (N, D)
        Input feature matrix.
    k : int
        Number of target clusters (K >= 2).
    seed : int, default=42
        Random seed for reproducibility.
    pretrain_epochs : int, default=200
        Number of epochs for autoencoder pretraining.
    finetune_epochs : int, default=100
        Maximum number of epochs for clustering fine-tuning.
    **kwargs : dict
        Optional hyperparameters:
        - dims: List[int], custom layer dimensions (default: [D, 500, 500, 2000, 10])
        - batch_size: int, mini-batch size (default: min(256, N))
        - lr_pretrain: float, learning rate for pretraining (default: 0.001)
        - lr_finetune: float, learning rate for fine-tuning (default: 0.001)
        - tol: float, convergence threshold for cluster label change (default: 0.001)

    Returns
    -------
    labels : np.ndarray of shape (N,)
        Discrete cluster assignments (int64, values in 0 to k-1).
    runtime_seconds : float
        Total elapsed execution time in seconds.
    metadata : ModelMetadata
        Diagnostic properties container (subclasses int with n_core = N).

    References
    ----------
    Xie, Girshick, Farhadi. "Unsupervised deep embedding for clustering analysis." ICML, 2016.
    """
    t0 = time.perf_counter()

    # 1. Validate inputs
    X_arr = np.asarray(X, dtype=np.float32)
    if X_arr.ndim != 2:
        raise ValueError(f"Input X must be a 2D matrix, got shape {X_arr.shape}")
    N, D = X_arr.shape
    if N < k:
        raise ValueError(f"Number of samples N={N} cannot be smaller than number of clusters k={k}")
    if k < 2:
        raise ValueError(f"Number of clusters k must be >= 2, got {k}")

    # 2. Check & load deep learning backend
    backend_type, tf_module, keras_module, layers_mod, models_mod, optimizers_mod, losses_mod = (
        _import_deep_backend()
    )

    # 3. Configure compute device and random seeds gracefully
    device_name = "cpu"
    if backend_type == "tensorflow" and tf_module is not None:
        try:
            gpus = tf_module.config.list_physical_devices("GPU")
            if gpus:
                for gpu in gpus:
                    try:
                        tf_module.config.experimental.set_memory_growth(gpu, True)
                    except Exception:
                        pass
                device_name = "gpu"
        except Exception:
            pass
        tf_module.random.set_seed(seed)
    else:
        try:
            import torch
            if torch.cuda.is_available():
                device_name = "gpu"
                torch.cuda.manual_seed_all(seed)
            torch.manual_seed(seed)
        except Exception:
            pass

    np.random.seed(seed)
    try:
        keras_module.utils.set_random_seed(seed)
    except Exception:
        pass

    # 4. Determine architecture dimensions
    default_dims = [D, 500, 500, 2000, 10]
    dims = kwargs.get("dims", default_dims)
    if len(dims) < 2 or dims[0] != D:
        dims = [D, 500, 500, 2000, 10]

    batch_size = kwargs.get("batch_size", min(512 if N > 5000 else 256, N))
    lr_pretrain = kwargs.get("lr_pretrain", 0.001)
    lr_finetune = kwargs.get("lr_finetune", 0.001)
    tol = kwargs.get("tol", 0.001)

    # 5. Build and pretrain autoencoder
    autoencoder, encoder = build_autoencoder(dims, layers_mod, models_mod)
    autoencoder.compile(
        optimizer=optimizers_mod.Adam(learning_rate=lr_pretrain),
        loss="mse",
    )

    callbacks_list = []
    try:
        if hasattr(keras_module, "callbacks"):
            callbacks_list.append(
                keras_module.callbacks.EarlyStopping(
                    monitor="loss",
                    patience=8,
                    min_delta=1e-4,
                    restore_best_weights=True,
                )
            )
    except Exception:
        pass

    if pretrain_epochs > 0:
        autoencoder.fit(
            X_arr,
            X_arr,
            batch_size=batch_size,
            epochs=pretrain_epochs,
            callbacks=callbacks_list if callbacks_list else None,
            shuffle=True,
            verbose=0,
        )

    # 6. Initialize cluster centers via KMeans on latent representations
    z = np.asarray(encoder.predict(X_arr, batch_size=batch_size, verbose=0))
    if _SKLEARN_AVAILABLE:
        try:
            kmeans = _SkKMeans(n_clusters=k, n_init=20, random_state=seed)
            y_pred = kmeans.fit_predict(z)
            centers = kmeans.cluster_centers_
        except Exception:
            from src.icc.core import run_clusterer
            y_pred = run_clusterer("kmeans", z, k, seed=seed)
            centers = np.array([z[y_pred == c].mean(axis=0) if np.any(y_pred == c) else z[c] for c in range(k)])
    else:
        from src.icc.core import run_clusterer
        y_pred = run_clusterer("kmeans", z, k, seed=seed)
        centers = np.array([z[y_pred == c].mean(axis=0) if np.any(y_pred == c) else z[c] for c in range(k)])

    # 7. Build DEC Model
    ClusteringLayer = _build_clustering_layer_cls(layers_mod)
    clustering_layer = ClusteringLayer(
        n_clusters=k,
        initial_weights=[centers],
        name="clustering",
    )
    dec_outputs = clustering_layer(encoder.output)
    dec_model = models_mod.Model(inputs=encoder.input, outputs=dec_outputs, name="DEC")

    dec_model.compile(
        optimizer=optimizers_mod.Adam(learning_rate=lr_finetune),
        loss=losses_mod.KLDivergence(),
    )

    # 8. Fine-tuning loop with Student-t clustering loss and target distribution P
    y_pred_last = np.copy(y_pred)
    for epoch in range(finetune_epochs):
        # Periodically compute soft assignments Q and target distribution P
        q = np.asarray(dec_model.predict(X_arr, batch_size=batch_size, verbose=0))
        p = target_distribution(q)
        y_pred = q.argmax(axis=1)

        # Check stopping criterion: delta label assignments
        delta_label = np.sum(y_pred != y_pred_last).astype(float) / N
        y_pred_last = np.copy(y_pred)

        if epoch > 0 and delta_label < tol:
            break

        # Train 1 epoch on (X, P)
        dec_model.fit(
            X_arr,
            p,
            batch_size=batch_size,
            epochs=1,
            shuffle=True,
            verbose=0,
        )

    # 9. Extract final predictions
    q_final = np.asarray(dec_model.predict(X_arr, batch_size=batch_size, verbose=0))
    final_labels = q_final.argmax(axis=1).astype(np.int64)

    runtime_seconds = time.perf_counter() - t0
    metadata = ModelMetadata(
        N,
        method="DEC",
        n_samples=N,
        n_features=D,
        n_clusters=k,
        latent_dim=dims[-1],
        pretrain_epochs=pretrain_epochs,
        finetune_epochs=finetune_epochs,
        device=device_name,
    )
    return final_labels, runtime_seconds, metadata


def run_idec(
    X: np.ndarray,
    k: int,
    seed: int = 42,
    pretrain_epochs: int = 200,
    finetune_epochs: int = 100,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Improved Deep Embedded Clustering (IDEC, Guo et al., IJCAI 2017).

    References
    ----------
    Guo et al. "Improved deep embedded clustering with local structure preservation."
    IJCAI, 2017.
    """
    raise NotImplementedError(
        "IDEC deep clustering baseline not yet implemented. Enable in Phase 4."
    )


def run_contrastive_clustering(
    X: np.ndarray,
    k: int,
    seed: int = 42,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Contrastive Clustering (CC, Li et al., AAAI 2021).

    References
    ----------
    Li, Hu, Liu, Peng, Zhou, Peng. "Contrastive clustering." AAAI, 2021.
    """
    raise NotImplementedError(
        "Contrastive Clustering baseline not yet implemented. Enable in Phase 4."
    )


def run_scan(
    X: np.ndarray,
    k: int,
    seed: int = 42,
    **kwargs,
) -> Tuple[np.ndarray, float, ModelMetadata]:
    """
    Execute Semantic Clustering via Nearest Neighbors (SCAN, Van Gansbeke et al., ECCV 2020).

    References
    ----------
    Van Gansbeke et al. "SCAN: Learning to classify images without labels." ECCV, 2020.
    """
    raise NotImplementedError(
        "SCAN baseline not yet implemented. Enable in Phase 4."
    )

