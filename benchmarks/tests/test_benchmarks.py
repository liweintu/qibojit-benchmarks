import pytest
from benchmarks.scripts import circuit_benchmark


def assert_logs(logs, nqubits, backend, nreps=1):
    assert logs[-1]["nqubits"] == nqubits
    assert logs[-1]["backend"] == backend
    assert logs[-1]["simulation_times_mean"] >= 0
    assert logs[-1]["transfer_times_mean"] >= 0
    assert len(logs[-1]["simulation_times"]) == nreps
    assert len(logs[-1]["transfer_times"]) == nreps


@pytest.mark.parametrize("nqubits", [3, 4])
@pytest.mark.parametrize("backend", ["qibojit", "qibotf", "tensorflow", "numpy"])
@pytest.mark.parametrize("transfer", [False, True])
@pytest.mark.parametrize("nreps", [1, 5])
@pytest.mark.parametrize("swaps", [False, True])
def test_qft_benchmark(nqubits, backend, nreps, transfer, swaps):
    logs = circuit_benchmark(nqubits, backend, circuit_name="qft",
                             nreps=nreps, transfer=transfer,
                             options=f"swaps={swaps}")
    assert_logs(logs, nqubits, backend, nreps)
    target_options = f"nqubits={nqubits}, swaps={swaps}"
    assert logs[-1]["circuit"] == "qft"
    assert logs[-1]["options"] == target_options


@pytest.mark.parametrize("nqubits", [3, 4])
@pytest.mark.parametrize("backend", ["qibojit", "qibotf"])
@pytest.mark.parametrize("varlayer", [False, True])
def test_variational_benchmark(nqubits, backend, varlayer):
    logs = circuit_benchmark(nqubits, backend, circuit_name="variational",
                             options=f"varlayer={varlayer}")
    assert_logs(logs, nqubits, backend)
    target_options = f"nqubits={nqubits}, nlayers=1, varlayer={varlayer}"
    assert logs[-1]["circuit"] == "variational"
    assert logs[-1]["options"] == target_options


# TODO: Complete tests