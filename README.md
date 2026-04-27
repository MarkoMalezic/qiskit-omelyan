# qiskit-omelyan

Omelyan-type (and related) **symmetric product formulas** for Hamiltonian time evolution in Qiskit.

This project provides a general ramp-based construction, **`OmelyanTrotter`**, along with a collection of well-known optimized schemes from the literature. The goal is to give you more control over time-evolution circuit synthesis—especially when you want **lower Trotter error at fixed (or comparable) gate depth** than standard Suzuki–Trotter constructions.

The implementation integrates with Qiskit’s existing operator and synthesis stack:
- `SparsePauliOp` for representing Hamiltonians
- `PauliEvolutionGate` for defining time evolution
- `ProductFormula`-style synthesis to generate circuits

## Features

### `OmelyanTrotter` (general framework)

`OmelyanTrotter` is a symmetric product-formula constructor (subclassing Qiskit’s `ProductFormula`) based on **ramp notation**. It supports:

- **even orders** (`order`)
- **cycles** (`cycles`)
- **symmetric parameter vectors** (`c_vec`)
- **multiple steps** (`reps`)
- optional circuit optimizations:
  - merging consecutive identical single-qubit rotations (`merge_single`)
  - merging boundaries between consecutive steps (`merge_steps`)

This makes it possible to implement a broad family of symmetric product formulas in a uniform way and to reproduce known optimized schemes from the literature.

### Built-in schemes

This repository includes ready-to-use schemes implemented as subclasses/instances of `OmelyanTrotter`, including:

- **2nd order**: `Leapfrog2`, `Omelyan2`
- **4th order**: `Forest_Ruth4`, `Omelyan4`, `Malezic_Ostmeyer4`
- **6th order**: `Yoshida6`, `Blanes_Moan6`, `Malezic_Ostmeyer6`
- **8th / 10th order**: `Morales8`, `Morales10`

### Collection of schemes

All top most efficient schemes at orders $n = 2, 4, 6$ are collected in the repository: https://github.com/MarkoMalezic/efficient-trotterizations. These are based on the paper by Malezic & Ostmeyer ([arXiv: 2601.18756](https://arxiv.org/abs/2601.18756))

## Installation

### From PyPI
```bash
pip install "qiskit-omelyan"
```

### With example dependencies
```bash
pip install "qiskit-omelyan[examples]"
```

### From GitHub (latest `main`)
```bash
pip install "qiskit-omelyan @ git+https://github.com/MarkoMalezic/qiskit-omelyan.git"
```

With example dependencies:
```bash
pip install "qiskit-omelyan[examples] @ git+https://github.com/MarkoMalezic/qiskit-omelyan.git"
```

## Quick start

Minimal example (Hamiltonian as `SparsePauliOp`):

```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp

from qiskit_omelyan import OmelyanTrotter, Omelyan2  # or any other scheme

t = 1.0

H = SparsePauliOp.from_list([
    ("ZI", 1.0),
    ("IZ", 1.0),
    ("XX", 0.5),
])

evolution = PauliEvolutionGate(H, time=t)

# Option 1: use a ready-to-use scheme
synth = Omelyan2(reps=50, merge_single=True, merge_steps=True)
qc = synth.synthesize(evolution)

# Option 2: construct a custom OmelyanTrotter
# qc = OmelyanTrotter(order=2, cycles=1, c_vec=[...], reps=50).synthesize(evolution)

print(qc)
```

## Examples

See [`examples/`](./examples) and [`examples/README.md`](./examples/README.md).

Typical usage:
```bash
cd examples
python leapfrog2_circuit.py
python omelyan2.py
```

Some examples compare against exact statevector evolution for small systems using `scipy.linalg.expm`, so keep the number of qubits small.

## Validation / comparison

The schemes in this repository are designed to be comparable to existing Qiskit synthesis methods such as `SuzukiTrotter` (and, in a different regime, `QDrift`). For small systems, you can validate correctness by comparing against exact matrix exponentiation and evaluating fidelity/error.

## References

- I. Omelyan, I. Mryglod and R. Folk, *Optimized Forest–Ruth- and Suzuki-like Algorithms for Integration of Motion in Many-body Systems* (2002)
- N. Hatano and M. Suzuki, *Finding Exponential Product Formulas of Higher Orders* (2005)
- H. Yoshida, *Construction of higher order symplectic integrators* (1990)
- L. Verlet, *Computer "Experiments" on Classical Fluids* (1967)
- E. Forest and R. D. Ruth, *Fourth-order Symplectic Integration* (1990)
- S. Blanes and P. Moan, *Practical Symplectic Partitioned Runge–Kutta and Runge–Kutta–Nyström Methods* (2002)
- M. E. S. Morales, P. C. S. Costa, D. K. Burgarth, Y. R. Sanders, *Greatly improved higher-order product formulae for quantum simulation* (2022)
- J. Ostmeyer, *Optimised Trotter decompositions for Classical and Quantum Computing* (2023)
- M. Maležič and J. Ostmeyer, *Efficient Trotter–Suzuki Schemes for Long-Time Quantum Dynamics* (2026)

## License

Apache License 2.0 — see [`LICENSE`](./LICENSE).
