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

Prepare a small spin chain Hamiltonian (as `SparsePauliOp`) and construct the PauliEvolutionGate for some time $t$:

```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp

H = SparsePauliOp.from_list([
    ("ZI", 1.0),
    ("IZ", 1.0),
    ("XX", 0.5),
])

t = 1.0
evolution = PauliEvolutionGate(H, time=t)
```

To construct the evolution circuit either a HighLevelSynthesis plugin can be used to transpile it:

```python
from qiskit import QuantumCircuit
from qiskit.transpiler import generate_preset_pass_manager
from qiskit.transpiler.passes.synthesis import HLSConfig

# Generate the circuit to be transpiled
qc = QuantumCircuit(2)
qc.append(evolution, [0, 1])

# Option 1: use a named scheme
options = {"name": "omelyan2",
           "reps": 50}

# Option 2: construct a custom OmelyanTrotter scheme
options = {"order": 2,
           "cycles": 2,
           "c_vec": [0.19318332, 0.30681667],
           "reps": 50}

hls_config = HLSConfig(PauliEvolution=[("omelyan_trotter", options)])
pass_manager = generate_preset_pass_manager(optimization_level=0, hls_config=hls_config)

circuit = pass_manager.run(qc)

print(circuit)
```

or it can be constructed natively by importing the necessary objects:

```python
from qiskit_omelyan import OmelyanTrotter, Omelyan2

# Option 1: use a named scheme
scheme = Omelyan2(reps=50)
circuit = scheme.synthesize(evolution)

# Option 2: construct a custom OmelyanTrotter
scheme = OmelyanTrotter(order=2, cycles=2, c_vec=[0.19318332, 0.30681667], reps=50)
circuit = scheme.synthesize(evolution)

print(circuit)
```

## Examples

Scripts for more examples can be found in [`examples/`](./examples) for both plugin usage and native support. See [`examples/README.md`](./examples/README.md) for more information.

Typical usage:
```bash
cd examples
python native/leapfrog2_circuit.py
python native/omelyan2.py
python plugin/named_scheme.py
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
