import pytest

from qiskit.circuit.library import HGate, PauliEvolutionGate
from qiskit.quantum_info import Operator, SparsePauliOp

import qiskit_omelyan
from qiskit_omelyan import Leapfrog2, OmelyanTrotter
from qiskit_omelyan.omelyan_plugin import PauliEvolutionSynthesisOmelyan

SCHEME_NAMES = [name for name in qiskit_omelyan.__all__ if name != "OmelyanTrotter"]

H = SparsePauliOp.from_list([("ZI", 1.0), ("IZ", 1.0), ("XX", 0.5)])
EVO = PauliEvolutionGate(H, time=0.1)

CUSTOM = {
    "order": 4,
    "cycles": 4,
    "c_vec": [0.29977221161128875, 0.45107524582283487, 0.26510491209675635, -0.51595236953088],
}


@pytest.mark.parametrize("name", SCHEME_NAMES)
def test_plugin_name_selects_matching_scheme(name):
    qc_plugin = PauliEvolutionSynthesisOmelyan().run(EVO, name=name.lower(), reps=2)
    # The plugin uses the same defaults as the scheme classes
    qc_direct = getattr(qiskit_omelyan, name)(reps=2).synthesize(EVO)

    assert qc_plugin == qc_direct
    assert Operator(qc_plugin).equiv(Operator(qc_direct))


def test_plugin_name_is_case_insensitive():
    qc_plugin = PauliEvolutionSynthesisOmelyan().run(EVO, name="Malezic_Ostmeyer8_q25")

    assert qc_plugin == qiskit_omelyan.Malezic_Ostmeyer8_q25().synthesize(EVO)


@pytest.mark.parametrize("merge_single", [False, True])
@pytest.mark.parametrize("merge_steps", [False, True])
def test_plugin_forwards_merge_options(merge_single, merge_steps):
    options = {"reps": 3, "merge_single": merge_single, "merge_steps": merge_steps}
    qc_plugin = PauliEvolutionSynthesisOmelyan().run(EVO, name="omelyan4", **options)

    assert qc_plugin == qiskit_omelyan.Omelyan4(**options).synthesize(EVO)


def test_plugin_custom_scheme():
    qc_plugin = PauliEvolutionSynthesisOmelyan().run(EVO, reps=2, **CUSTOM)
    qc_direct = OmelyanTrotter(**CUSTOM, reps=2, merge_single=True, merge_steps=True).synthesize(EVO)

    assert qc_plugin == qc_direct


def test_plugin_fallback_forwards_options():
    qc_plugin = PauliEvolutionSynthesisOmelyan().run(EVO, reps=5, insert_barriers=True)

    assert qc_plugin == Leapfrog2(reps=5, insert_barriers=True).synthesize(EVO)
    assert qc_plugin != Leapfrog2().synthesize(EVO)


def test_plugin_unknown_name_raises():
    with pytest.raises(ValueError, match="not recognized"):
        PauliEvolutionSynthesisOmelyan().run(EVO, name="malezic_ostmeyer8_q3O")


def test_plugin_unknown_name_raises_even_with_custom_scheme():
    with pytest.raises(ValueError, match="not recognized"):
        PauliEvolutionSynthesisOmelyan().run(EVO, name="custom_scheme", **CUSTOM)


@pytest.mark.parametrize("missing", ["order", "cycles", "c_vec"])
def test_plugin_incomplete_custom_scheme_raises(missing):
    options = {k: v for k, v in CUSTOM.items() if k != missing}

    with pytest.raises(ValueError, match=missing):
        PauliEvolutionSynthesisOmelyan().run(EVO, **options)


def test_plugin_ignores_other_gates():
    assert PauliEvolutionSynthesisOmelyan().run(HGate()) is None
