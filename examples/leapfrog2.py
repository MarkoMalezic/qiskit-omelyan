import numpy as np
from scipy.linalg import expm

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import Statevector
from qiskit_omelyan import Leapfrog2

from model import heisenbergXXZ

# This example demonstrates how to use the Leapfrog2 scheme to build
# a quantum circuit for time evolution under a Heisenberg XXZ Hamiltonian.
# The script computes the fidelity and error of the evolved state compared
# to the exact evolution using matrix exponentiation.
if __name__ == "__main__":

    # ---------------------- Model parameters ----------------------

    n = 5   # number of spins/qubits

    Jx, Jy, Jz = 1.0, 1.0, 1.0    # coupling constants
    hz = 0.1      # local field strength

    # 1) Build Hamiltonian
    H = heisenbergXXZ(n, Jx=Jx, Jy=Jy, Jz=Jz, hz=hz)

    # ----------------- Time evolution parameters ------------------

    t = 1.0      # total evolution time
    reps = 100    # number of steps
    merge_single = True   # Merge consecutive single-qubit gates into one
    merge_steps = True    # Merge consecutive steps

    # 2) Build the product formula using OmelyanTrotter
    leapfrog2 = Leapfrog2(reps=reps, merge_single=merge_single, merge_steps=merge_steps)

    # ------------------ Time evolution circuit --------------------

    # 3) Build the circuit for the time evolution operator U(t) = exp(-i t H)
    evo = PauliEvolutionGate(H, time=t)
    evo_circuit = leapfrog2.synthesize(evo)

    # ---------------------- State evolution -----------------------

    psi0 = Statevector.from_label("01011")   # Initial state
    psi = psi0.evolve(evo_circuit)            # Evolved state

    # Exact time evolution using matrix exponentiation
    H_mat = H.to_matrix()
    U_exact = expm(-1j * t * H_mat)
    psi_exact = Statevector(U_exact @ psi0.data)

    # Compute fidelity and error
    fidelity = abs(psi_exact.data.conj() @ psi.data)**2
    print("Fidelity:", fidelity)

    error = np.linalg.norm(psi_exact.data - psi.data)
    print("Error:", error)
