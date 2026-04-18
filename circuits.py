import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

sim = AerSimulator()
rng = np.random.default_rng(7)

def circuit_superposition(n_qubits=4):
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.h(q)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def circuit_layered_phase(n_qubits=4):
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.h(q)
        qc.rz((q + 1) * np.pi / 5, q)
    for q in range(n_qubits - 1):
        qc.cx(q, q + 1)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def circuit_ring_entangler(n_qubits=4):
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.ry(np.pi / (q + 2), q)
    for q in range(n_qubits - 1):
        qc.cz(q, q + 1)
    qc.cz(n_qubits - 1, 0)
    for q in range(n_qubits):
        qc.h(q)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

def fourth_circuit(n_qubits=6):
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.ry(np.pi / (q+2), q)
    for q in range(n_qubits -1):
        qc.cz(q, q + 1)
    qc.cz(n_qubits -2, 0)
    qc.measure(range(n_qubits), range(n_qubits))
    return qc

circuit_library = {
    "superposition": circuit_superposition,
    "layered": circuit_layered_phase,
    "ring": circuit_ring_entangler,
    "fourth": fourth_circuit
}

def run_circuits(name, shots=3000):
    if name not in circuit_library:
        raise ValueError(f"Unknown circuit: {name}")

    qc = circuit_library[name]()   # build circuit
    tqc = transpile(qc, sim)       # optimize for simulator

    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()

    return counts

def get_all_counts():
    results = {}

    for name in circuit_library:
        results[name] = run_circuits(name, shots=3000)

    return results

all_counts = get_all_counts()
print(all_counts["layered"])
print(all_counts["fourth"])