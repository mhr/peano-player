# Peano Player

1. Install Lean (and elan)
2. Install JAX, Equinox, Optax
3. Install W&B

## Python deps (CPU, all platforms)
`$ pip install -r requirements.txt`

## GPU (Linux + CUDA 12; the paper's runs used this)
`$ pip install "jax[cuda12]==0.5.0"`