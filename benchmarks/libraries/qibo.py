from benchmarks.libraries import abstract


class Qibo(abstract.AbstractBackend):

    def __init__(self):
        import qibo
        from qibo import models
        self.name = "qibo"
        self.qibo = qibo
        self.models = models
        self.__version__ = qibo.__version__

    def from_qasm(self, qasm):
        return self.models.Circuit.from_qasm(qasm)

    def __call__(self, circuit):
        return circuit()

    def transpose_state(self, x):
        return x

    def get_precision(self):
        return self.qibo.get_precision()

    def set_precision(self, precision):
        self.qibo.set_precision(precision)

    def get_device(self):
        return self.qibo.get_device()


class QiboJit(Qibo):

    def __init__(self):
        super().__init__()
        self.qibo.set_backend("qibojit")
        self.name = "qibojit"


class QiboTF(Qibo):

    def __init__(self):
        super().__init__()
        self.qibo.set_backend("qibotf")
        self.name = "qibotf"


class QiboFusion(Qibo):

    def __init__(self, max_qubits=2):
        super().__init__()
        self.name = "qibo-fusion"
        self.max_qubits = max_qubits

    def from_qasm(self, qasm):
        circuit = super().from_qasm(qasm)
        return circuit.fuse(max_qubits=self.max_qubits)
