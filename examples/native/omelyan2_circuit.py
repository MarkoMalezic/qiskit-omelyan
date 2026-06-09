from qiskit.circuit.library import PauliEvolutionGate
from qiskit_omelyan import Omelyan2

from model import heisenbergXXZ

# This example demonstrates how to use the Omelyan2 scheme to build
# a quantum circuit for time evolution under a Heisenberg XXZ Hamiltonian
# A single step is used to show the structure of the circuit with q=1 cycle
if __name__ == "__main__":

    # ---------------------- Model parameters ----------------------

    nq = 3   # number of spins/qubits

    Jx, Jy, Jz = 1.0, 1.0, 1.0    # coupling constants
    hz = 0.1      # local field strength

    # 1) Build Hamiltonian
    H = heisenbergXXZ(nq, Jx=Jx, Jy=Jy, Jz=Jz, hz=hz)
    print(H)

    # ----------------- Time evolution parameters ------------------

    t = 1.0      # total evolution time
    reps = 1      # number of steps
    merge_single = True   # Merge consecutive single-qubit gates into one
    merge_steps = True    # Merge consecutive steps

    # 2) Build the product formula using OmelyanTrotter
    omelyan2 = Omelyan2(reps=reps, merge_single=merge_single, merge_steps=merge_steps)

    # ------------------ Time evolution circuit --------------------

    # 3) Build the circuit for the time evolution operator U(t) = exp(-i t H)
    evo = PauliEvolutionGate(H, time=t)
    evo_circuit = omelyan2.synthesize(evo)
    print(evo_circuit)
