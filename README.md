# qiskit-omelyan

Omelyan-based (and related) product-formula schemes for Hamiltonian time evolution in Qiskit.

This package provides multiple splitting / symplectic integrator-inspired schemes (e.g. Leapfrog, Omelyan, Yoshida, Forest–Ruth, Blanes–Moan, Morales, etc.) and exposes them as synthesizers for Qiskit’s `PauliEvolutionGate`.

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

```python
from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit_omelyan import Leapfrog2

# Example Hamiltonian
H = SparsePauliOp.from_list([
    ("ZI", 1.0),
    ("IZ", 1.0),
    ("XX", 0.5),
])

t = 1.0
evo = PauliEvolutionGate(H, time=t)

scheme = Leapfrog2(reps=10, merge_single=True, merge_steps=True)
qc = scheme.synthesize(evo)

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

> Some examples compute an “exact” reference evolution using `scipy.linalg.expm`, so keep the number of qubits small.

## License

Apache License 2.0 — see [`LICENSE`](./LICENSE).
