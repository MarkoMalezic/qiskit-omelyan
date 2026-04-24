````markdown name=examples/README.md
# Examples

This directory contains **standalone example scripts** that demonstrate how to use the
`qiskit-omelyan` product-formula (Omelyan-type) schemes to build time-evolution circuits
for a simple Heisenberg XXZ spin chain.

These examples are meant for **learning and experimentation**, not as automated unit tests.

## Prerequisites

1. Install `qiskit-omelyan` (pick one):

### Install from PyPI (once published)
```bash
pip install qiskit-omelyan
```

### Install from GitHub (development / latest `main`)
```bash
pip install "git+https://github.com/MarkoMalezic/qiskit-omelyan.git"
```

2. Install extra dependencies used by the examples:
```bash
pip install numpy scipy
```

> Notes:
> - `scipy` is only used here to compute the "exact" evolution via matrix exponentiation (`scipy.linalg.expm`)
>   so we can estimate fidelity/error for small systems.

## How to run

These scripts are intended to be run **from inside the `examples/` directory**:

```bash
cd examples
python leapfrog2_circuit.py
python leapfrog2.py
```

If you use a virtual environment, make sure it is activated before running the scripts.

## Shared model helper

Most examples import the Heisenberg XXZ Hamiltonian builder from:

- `model.py` → `heisenbergXXZ(...)`

This returns a `qiskit.quantum_info.SparsePauliOp` that is used to build a
`qiskit.circuit.library.PauliEvolutionGate`.

## What each example does

There are two common types of examples:

### 1) Circuit structure examples (`*_circuit.py`)
These scripts build and print the time-evolution circuit (typically with `reps = 1`)
so you can see the structure of the scheme.

Example:
```bash
cd examples
python leapfrog2_circuit.py
```

### 2) Accuracy examples (fidelity/error vs exact evolution)
These scripts:
1. Build `U(t) ≈ exp(-i t H)` using a chosen scheme
2. Evolve an initial `Statevector`
3. Compute the **exact** evolution using `expm(-i t H)` for small `n`
4. Print fidelity and state-vector error

Example:
```bash
cd examples
python omelyan2.py
```

## Tips

- Keep `n` small (e.g., `n=3..5`) when using the "exact evolution" scripts, because
  exact matrix exponentiation scales as `2^n`.
- Increase `reps` to improve approximation accuracy (at the cost of deeper circuits).
- If you want to compare schemes fairly, use the same `n`, couplings, `t`, and `reps`.

## Troubleshooting

### `ModuleNotFoundError: No module named 'model'`
Make sure you are running from the `examples/` directory:
```bash
cd examples
python leapfrog2.py
```

### `ModuleNotFoundError: No module named 'qiskit_omelyan'`
You likely haven’t installed the package into your current environment. Reinstall with:
```bash
pip install "git+https://github.com/MarkoMalezic/qiskit-omelyan.git"
```

### `ModuleNotFoundError: No module named 'scipy'`
Install the example dependencies:
```bash
pip install scipy numpy
```

## License / attribution

These examples are provided as part of the `qiskit-omelyan` repository for educational use.
````
