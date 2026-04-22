import numpy as np
from scipy.linalg import expm

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit.synthesis import SuzukiTrotter
from qiskit_omelyan import Leapfrog2, Omelyan2, Forest_Ruth4, Omelyan4, Malezic_Ostmeyer4, Yoshida6, Blanes_Moan6, Malezic_Ostmeyer6, Morales8, Morales10

def heisenberg_chain_hamiltonian(
  n,
  Jx=1.0, Jy=1.0, Jz=1.0, hz=0.0,
):
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

  # local fields
  for i in range(n):
      if hz != 0: one_body_term("Z", i, hz)

  return SparsePauliOp(paulis, coeffs=np.asarray(coeffs, dtype=float))


# --- user choices ---
n = 4
t = 10.0

Jx, Jy, Jz = 1.0, 1.0, 1.0   
hz = 0.1

reps = 100

# 1) Build H
H = heisenberg_chain_hamiltonian(n, Jx=Jx, Jy=Jy, Jz=Jz, hz=hz)

print(H)

# 2) Define the abstract evolution gate U(t)=exp(-i t H)
evo = PauliEvolutionGate(H, time=t)

# 3) Choose Suzuki–Trotter synthesis and turn it into an explicit circuit
SuzukiLie = SuzukiTrotter(order=1, reps=reps, cx_structure="chain", preserve_order=True)
SuzukiSymmetric = SuzukiTrotter(order=2, reps=reps, cx_structure="chain", preserve_order=True)
SuzukiFR = SuzukiTrotter(order=4, reps=reps, cx_structure="chain", preserve_order=True)
SuzukiSixth = SuzukiTrotter(order=6, reps=reps, cx_structure="chain", preserve_order=True)

scheme_dir = "/home/marko/Faks/PhD/Projects/Trotterization/Code/Coefficients/Data/Schemes/Trotter_Suzuki/long_double/"

#np.set_printoptions(precision=30)

merge_single = True
merge_steps = True

leapfrog2 = Leapfrog2(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
omelyan2 = Omelyan2(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
forest_ruth4 = Forest_Ruth4(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
omelyan4 = Omelyan4(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True) # Wrong
malezic_ostmeyer4 = Malezic_Ostmeyer4(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
yoshida6 = Yoshida6(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
blanes_moan6 = Blanes_Moan6(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
malezic_ostmeyer6 = Malezic_Ostmeyer6(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
morales8 = Morales8(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)
morales10 = Morales10(reps=reps, merge_single=merge_single, merge_steps=merge_steps, cx_structure="chain", preserve_order=True)


evo_circuit = malezic_ostmeyer4.synthesize(evo)

#print(evo_circuit)

psi0 = Statevector.from_label("0111")
psi = psi0.evolve(evo_circuit)

H_mat = H.to_matrix()
U_exact = expm(-1j * t * H_mat)

psi_exact = Statevector(U_exact @ psi0.data)

fidelity = abs(psi_exact.data.conj() @ psi.data)**2
print("Fidelity:", fidelity)

error = np.linalg.norm(psi_exact.data - psi.data)
print("Error:", error)
