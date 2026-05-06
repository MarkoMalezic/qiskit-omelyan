from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.passes.synthesis.plugin import HighLevelSynthesisPlugin
from qiskit.circuit.library.pauli_evolution import PauliEvolutionGate
from .omelyan_schemes import (
    OmelyanTrotter,
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

class OmelyanTrotterPlugin(HighLevelSynthesisPlugin):
    """High-level synthesis plugin for Omelyan product formulas for PauliEvolutionGate.

    Users can either:
      - Specify a built-in scheme with `name` (str), or
      - Provide all of `order`, `cycles`, and `c_vec` (a list of coefficients) for a custom scheme.
    
    Note:
    If both `name` and (`order`, `cycles`, `c_vec`) are given, `name` is used and the others ignored.

    Options:
        - name (str): Name of a built-in scheme ("leapfrog2", "omelyan2", "forest_ruth4", etc.).
        - order (int): Order of the product formula (for custom schemes).
        - cycles (int): Number of cycles in the product formula (for custom schemes).
        - c_vec (list of float): Coefficients for the product formula (for custom schemes).
        - reps (int, default=1): Number of repetitions (time steps).
        - merge_single (bool, default=False): Merge consecutive single-step evolutions.
        - merge_steps (bool, default=False): Merge consecutive steps of the same type.
        - insert_barriers (bool, default=False): Insert barriers between steps.
        - cx_structure (str, default="chain"): Structure for CX gates ("chain", "star", etc.).
        - atomic_evolution (callable or None, default=None): Custom function for atomic evolutions (advanced).
        - wrap (bool, default=False): Wrap the entire sequence in a single gate.
        - preserve_order (bool, default=True): Preserve order of terms in the input Hamiltonian.
        - atomic_evolution_sparse_observable (bool, default=False): Use sparse observable for atomic evolution synthesis.
    """

    @property
    def name(self):
        return "omelyan_trotter"

    @property
    def description(self):
        return "Omelyan product formulas for PauliEvolutionGate."

    @property
    def supported(self):
        return [PauliEvolutionGate]

    def run(
        self,
        high_level_object,
        coupling_map=None,
        target=None,
        qubits=None,
        **options,
    ) -> QuantumCircuit:
        options = options or {}

        # Named/known schemes
        scheme_name = options.get("name")
        if scheme_name:
            schemes = {
                "leapfrog2": Leapfrog2,
                "omelyan2": Omelyan2,
                "forest_ruth4": Forest_Ruth4,
                "omelyan4": Omelyan4,
                "malezic_ostmeyer4": Malezic_Ostmeyer4,
                "yoshida6": Yoshida6,
                "blanes_moan6": Blanes_Moan6,
                "malezic_ostmeyer6": Malezic_Ostmeyer6,
                "morales8": Morales8,
                "morales10": Morales10,
            }
            scheme_cls = schemes.get(scheme_name.lower())
            if scheme_cls is not None:
                scheme = scheme_cls(
                    reps=options.get("reps", 1),
                    merge_single=options.get("merge_single", False),
                    merge_steps=options.get("merge_steps", False),
                    insert_barriers=options.get("insert_barriers", False),
                    cx_structure=options.get("cx_structure", "chain"),
                    atomic_evolution=options.get("atomic_evolution"),
                    wrap=options.get("wrap", False),
                    preserve_order=options.get("preserve_order", True),
                    atomic_evolution_sparse_observable=options.get("atomic_evolution_sparse_observable", False),
                )
                return scheme.synthesize(high_level_object)
            else:
                raise ValueError(f"Scheme name '{scheme_name}' not recognized. Valid options: {list(schemes.keys())}")

        # User-supplied scheme
        if all(k in options for k in ("order", "cycles", "c_vec")):
            scheme = OmelyanTrotter(
                order=options["order"],
                cycles=options["cycles"],
                c_vec=options["c_vec"],
                reps=options.get("reps", 1),
                merge_single=options.get("merge_single", False),
                merge_steps=options.get("merge_steps", False),
                insert_barriers=options.get("insert_barriers", False),
                cx_structure=options.get("cx_structure", "chain"),
                atomic_evolution=options.get("atomic_evolution"),
                wrap=options.get("wrap", False),
                preserve_order=options.get("preserve_order", True),
                atomic_evolution_sparse_observable=options.get("atomic_evolution_sparse_observable", False),
            )
            return scheme.synthesize(high_level_object)

        # Fallback
        scheme = Leapfrog2()
        return scheme.synthesize(high_level_object)