import numpy as np
import pytest
from scipy.linalg import expm

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector

from qiskit_omelyan import Omelyan2


@pytest.mark.parametrize("reps", [1, 2, 5, 10])
def test_omelyan2_approximates_exact_time_evolution(reps):
    # Keep this small so exact expm is cheap and stable
    H = SparsePauliOp.from_list([("ZI", 0.7), ("IZ", -0.4), ("XX", 0.2)])
    t = 0.2
    evo = PauliEvolutionGate(H, time=t)

    scheme = Omelyan2(reps=reps, merge_single=True, merge_steps=True)
    qc = scheme.synthesize(evo)

    psi0 = Statevector.from_label("00")
    psi_approx = psi0.evolve(qc)

    U_exact = expm(-1j * t * H.to_matrix())
    psi_exact = Statevector(U_exact @ psi0.data)

    fidelity = abs(np.vdot(psi_exact.data, psi_approx.data)) ** 2

    # Loose threshold: fidelity should improve with reps, but keep it robust.
    # For reps >= 5, this should typically be very high for this tiny example.
    if reps >= 5:
        assert fidelity > 0.99
    else:
        assert fidelity > 0.9