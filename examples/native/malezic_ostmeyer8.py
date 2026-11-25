import numpy as np
from scipy.linalg import expm

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Statevector
from qiskit_omelyan import (
    Malezic_Ostmeyer8_q21,
    Malezic_Ostmeyer8_q23,
    Malezic_Ostmeyer8_q25,
    Malezic_Ostmeyer8_q30,
)

from model import heisenbergXXZ

# This example demonstrates how to use the eighth-order Malezic_Ostmeyer8 schemes
# (at q = 21, 23, 25 and 30 cycles) to build quantum circuits for time evolution
# under a Heisenberg XXZ Hamiltonian.
# For each scheme the script computes the fidelity and error of the evolved state
# compared to the exact evolution using matrix exponentiation, together with the
# depth and size of the circuit.
if __name__ == "__main__":

    # ---------------------- Model parameters ----------------------

    nq = 5   # number of spins/qubits

    Jx, Jy, Jz = 1.0, 1.0, 1.0    # coupling constants
    hz = 0.1      # local field strength

    # 1) Build Hamiltonian
    H = heisenbergXXZ(nq, Jx=Jx, Jy=Jy, Jz=Jz, hz=hz)

    # ----------------- Time evolution parameters ------------------

    t = 1.0      # total evolution time
    # Number of steps per scheme, such that the cost (cycles * reps) is roughly 100 for all of them
    reps = {Malezic_Ostmeyer8_q21: 5, Malezic_Ostmeyer8_q23: 4,
            Malezic_Ostmeyer8_q25: 4, Malezic_Ostmeyer8_q30: 3}
    merge_single = True   # Merge consecutive single-qubit gates into one
    merge_steps = True    # Merge consecutive steps

    # Exact time evolution using matrix exponentiation
    psi0 = Statevector.from_label("01011")   # Initial state
    U_exact = expm(-1j * t * H.to_matrix())
    psi_exact = Statevector(U_exact @ psi0.data)

    # 2) Time evolution operator U(t) = exp(-i t H)
    evo = PauliEvolutionGate(H, time=t)

    for scheme_class in (Malezic_Ostmeyer8_q21, Malezic_Ostmeyer8_q23,
                         Malezic_Ostmeyer8_q25, Malezic_Ostmeyer8_q30):

        # 3) Build the product formula and the circuit
        scheme = scheme_class(reps=reps[scheme_class], merge_single=merge_single, merge_steps=merge_steps)
        evo_circuit = scheme.synthesize(evo)

        # 4) Evolve the initial state and compare to the exact evolution
        psi = psi0.evolve(evo_circuit)
        fidelity = abs(psi_exact.data.conj() @ psi.data)**2
        error = np.linalg.norm(psi_exact.data - psi.data)

        print(f"{scheme_class.__name__} (reps = {reps[scheme_class]}):")
        print("  Fidelity:", fidelity)
        print("  Error:", error)
        print("  Depth:", evo_circuit.depth(), " Size:", evo_circuit.size())
