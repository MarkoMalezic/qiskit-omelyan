import numpy as np
from qiskit.quantum_info import SparsePauliOp

def heisenbergXXZ(n, Jx=1.0, Jy=1.0, Jz=1.0, hz=0.1):
    """Return Heisenberg-chain Hamiltonian as SparsePauliOp on n qubits (open boundary)."""
    paulis = []
    coeffs = []

    def two_body_term(p, i, j, c):
        # p is "XX", "YY", or "ZZ"
        s = ["I"] * n
        s[i] = p[0]
        s[j] = p[1]
        paulis.append("".join(s))
        coeffs.append(c)

    def one_body_term(p, i, c):
        # p is "X" or "Z"
        s = ["I"] * n
        s[i] = p
        paulis.append("".join(s))
        coeffs.append(c)

    # nearest-neighbor couplings
    for i in range(n - 1):
        if Jx != 0: two_body_term("XX", i, i + 1, Jx)
        if Jy != 0: two_body_term("YY", i, i + 1, Jy)
        if Jz != 0: two_body_term("ZZ", i, i + 1, Jz)

    # local field
    for i in range(n):
        if hz != 0: one_body_term("Z", i, hz)

    return SparsePauliOp(paulis, coeffs=np.asarray(coeffs, dtype=float))
