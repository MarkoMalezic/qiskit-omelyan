from qiskit import QuantumCircuit
from qiskit.circuit.library.pauli_evolution import PauliEvolutionGate
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler import generate_preset_pass_manager

# Qiskit 2.4.1: HighLevelSynthesis + HLSConfig are here
from qiskit.transpiler.passes.synthesis.high_level_synthesis import HLSConfig
from qiskit.transpiler.passes.synthesis.plugin import HighLevelSynthesisPluginManager


def main():
    op = SparsePauliOp(["XXI", "ZZI", "IXX", "IZZ"], coeffs=[1.0, 1.0, 1.0, 1.0])
    evol = PauliEvolutionGate(op, time=1.0)

    print("PauliEvolutionGate.name:", evol.name)

    qc = QuantumCircuit(3)
    qc.append(evol, [0, 1, 2])

    print("Input circuit:")
    print(qc)
    print()

    pmgr = HighLevelSynthesisPluginManager()
    print("Methods for PauliEvolution:", pmgr.method_names("PauliEvolution"))
    print()

    named_schemes = ["leapfrog2", "omelyan2", "forest_ruth4", "omelyan4", "malezic_ostmeyer4",
                     "yoshida6", "blanes_moan6", "malezic_ostmeyer6", "morales8", "morales10"]

    options = {"name": named_schemes[0], # Change this to test different named schemes
               "reps": 1}
    
    hls_config = HLSConfig(PauliEvolution=[("omelyan_trotter", options)])

    pass_manager = generate_preset_pass_manager(optimization_level=3, hls_config=hls_config)

    out = pass_manager.run(qc)

    print("Output circuit:")
    print(out)


if __name__ == "__main__":
    main()