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
    Malezic_Ostmeyer4_minimal,
    Yoshida6,
    Blanes_Moan6,
    Malezic_Ostmeyer6,
    Malezic_Ostmeyer6_minimal,
    Morales8,
    Malezic_Ostmeyer8_q21,
    Malezic_Ostmeyer8_q21_minimal,
    Malezic_Ostmeyer8_q25,
    Malezic_Ostmeyer8_q30,
    Morales10,
)

class PauliEvolutionSynthesisOmelyan(HighLevelSynthesisPlugin):
    """Synthesize a :class:`.PauliEvolutionGate` using OmelyanTrotter.

    This plugin name is ``PauliEvolution.omelyan_trotter`` which can be used as the key on
    an :class:`~.HLSConfig` object to use this method with :class:`~.HighLevelSynthesis`.

    Users can either:
      - Specify a built-in scheme with `name` (str), or
      - Provide all of `order`, `cycles`, and `c_vec` (a list of coefficients) for a custom scheme.
    If neither is given, the Leapfrog2 scheme is used.

    Note:
    If both `name` and (`order`, `cycles`, `c_vec`) are given, `name` is used and the others ignored.

    Raises:
        ValueError: If `name` is not a built-in scheme, or if only some of
            `order`, `cycles`, and `c_vec` are given.

    Options:
        - name (str): Name of a built-in scheme ("leapfrog2", "omelyan2", "forest_ruth4", etc.).
        - order (int): Order of the product formula (for custom schemes).
        - cycles (int): Number of cycles in the product formula (for custom schemes).
        - c_vec (list of float): Coefficients for the product formula (for custom schemes).
        - reps (int, default=1): Number of repetitions (time steps).
        - merge_single (bool, default=True): Merge identical single-qubit rotations within a step where possible.
        - merge_steps (bool, default=True): Merge the gates at points where two consecutive steps meet.
        - insert_barriers (bool, default=False): Insert barriers between steps.
        - cx_structure (str, default="chain"): Structure for CX gates ("chain" or "fountain").
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
        if not isinstance(high_level_object, PauliEvolutionGate):
            # Don't do anything if a gate is called "evolution" but is not an
            # actual PauliEvolutionGate
            return None

        # Options shared by all schemes, with the same defaults as the scheme classes
        scheme_options = {
            "reps": options.get("reps", 1),
            "merge_single": options.get("merge_single", True),
            "merge_steps": options.get("merge_steps", True),
            "insert_barriers": options.get("insert_barriers", False),
            "cx_structure": options.get("cx_structure", "chain"),
            "atomic_evolution": options.get("atomic_evolution"),
            "wrap": options.get("wrap", False),
            "preserve_order": options.get("preserve_order", True),
            "atomic_evolution_sparse_observable": options.get("atomic_evolution_sparse_observable", False),
        }

        # Named/known schemes
        scheme_name = options.get("name")
        if scheme_name:
            schemes = {
                "leapfrog2": Leapfrog2,
                "omelyan2": Omelyan2,
                "forest_ruth4": Forest_Ruth4,
                "omelyan4": Omelyan4,
                "malezic_ostmeyer4": Malezic_Ostmeyer4,
                "malezic_ostmeyer4_minimal": Malezic_Ostmeyer4_minimal,
                "yoshida6": Yoshida6,
                "blanes_moan6": Blanes_Moan6,
                "malezic_ostmeyer6": Malezic_Ostmeyer6,
                "malezic_ostmeyer6_minimal": Malezic_Ostmeyer6_minimal,
                "morales8": Morales8,
                "malezic_ostmeyer8_q21": Malezic_Ostmeyer8_q21,
                "malezic_ostmeyer8_q21_minimal": Malezic_Ostmeyer8_q21_minimal,
                "malezic_ostmeyer8_q25": Malezic_Ostmeyer8_q25,
                "malezic_ostmeyer8_q30": Malezic_Ostmeyer8_q30,
                "morales10": Morales10,
            }
            scheme_cls = schemes.get(scheme_name.lower())
            if scheme_cls is None:
                raise ValueError(
                    f"Scheme name '{scheme_name}' not recognized. Valid options: {list(schemes.keys())}."
                )
            return scheme_cls(**scheme_options).synthesize(high_level_object)

        # User-supplied scheme
        custom_keys = ("order", "cycles", "c_vec")
        given_keys = [k for k in custom_keys if k in options]
        if given_keys:
            missing_keys = [k for k in custom_keys if k not in options]
            if missing_keys:
                raise ValueError(
                    f"A custom scheme requires all of {list(custom_keys)}, but {missing_keys} are missing."
                )
            scheme = OmelyanTrotter(
                order=options["order"],
                cycles=options["cycles"],
                c_vec=options["c_vec"],
                **scheme_options,
            )
            return scheme.synthesize(high_level_object)

        # Fallback
        return Leapfrog2(**scheme_options).synthesize(high_level_object)
