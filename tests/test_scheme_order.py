import numpy as np
import pytest
from scipy.linalg import expm

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Operator, SparsePauliOp

import qiskit_omelyan

SCHEME_NAMES = [name for name in qiskit_omelyan.__all__ if name != "OmelyanTrotter"]


@pytest.mark.parametrize("name", SCHEME_NAMES)
def test_scheme_parameters_are_consistent(name):
    scheme = getattr(qiskit_omelyan, name)()

    assert len(scheme.c_vec) == scheme.cycles
    assert sum(scheme.c_vec) == pytest.approx(0.5, abs=1e-12)


@pytest.mark.parametrize("name", SCHEME_NAMES)
def test_scheme_converges_with_stated_order(name):
    # Non-commuting Hamiltonian with three terms, so multi-operator ramps are exercised
    H = SparsePauliOp.from_list([("XX", 1.0), ("ZI", 0.7), ("IZ", -0.4), ("YZ", 0.3)])
    scheme = getattr(qiskit_omelyan, name)(reps=1)

    def error(t):
        qc = scheme.synthesize(PauliEvolutionGate(H, time=t))
        return np.linalg.norm(Operator(qc).data - expm(-1j * t * H.to_matrix()), 2)

    # The local error of an order n scheme scales as t^(n+1), so halving t
    # divides it by 2^(n+1). t = 0.5 keeps all errors well above machine precision.
    measured_order = np.log2(error(0.5) / error(0.25)) - 1

    assert measured_order == pytest.approx(scheme.order, abs=0.5)
