import pytest

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp

from qiskit_omelyan import (
    Leapfrog2,
    Omelyan2,
    Forest_Ruth4,
    Omelyan4,
    Malezic_Ostmeyer4,
    Yoshida6,
    Blanes_Moan6,
    Malezic_Ostmeyer6,
    Morales8,
    Morales10,
)


@pytest.mark.parametrize(
    "scheme_cls,reps",
    [
        (Leapfrog2, 2),
        (Omelyan2, 2),
        (Forest_Ruth4, 2),
        (Omelyan4, 2),
        (Malezic_Ostmeyer4, 2),
        (Yoshida6, 2),
        (Blanes_Moan6, 2),
        (Malezic_Ostmeyer6, 2),
        (Morales8, 1),
        (Morales10, 1),
    ],
)
def test_all_schemes_synthesize_without_error(scheme_cls, reps):
    # Tiny Hamiltonian on 2 qubits: ZI + IZ + XX
    H = SparsePauliOp.from_list([("ZI", 1.0), ("IZ", 1.0), ("XX", 0.5)])
    evo = PauliEvolutionGate(H, time=0.1)

    scheme = scheme_cls(reps=reps, merge_single=True, merge_steps=True)
    qc = scheme.synthesize(evo)

    assert qc.num_qubits == 2
    assert qc.num_clbits == 0
    # Just make sure we produced *some* circuit
    assert qc.size() > 0