import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import networkx as nx

sim = AerSimulator() #starts simulation for computer
rng = np.random.default_rng(7)

# aliyah
def circuit_superposition(n_qubits=4): #creates circuit and applies the H gates to the circuit
    qc = QuantumCircuit(n_qubits, n_qubits) #Starter Code
    for q in range(n_qubits):
        qc.h(q)
    qc.measure(range(n_qubits), range(n_qubits)) #turns qubits into classical bits
    return qc

# aliyah
def circuit_layered_phase(n_qubits=4):  #creates circuit and applies the H, RZ, and CX gates to it relative to the number of qubits
    qc = QuantumCircuit(n_qubits, n_qubits) #Starter Code
    for q in range(n_qubits):
        qc.h(q)
        qc.rz((q + 1) * np.pi / 5, q)
    for q in range(n_qubits - 1):
        qc.cx(q, q + 1)
    qc.measure(range(n_qubits), range(n_qubits)) #turns qubits into classical bits
    return qc

# aliyah
def circuit_ring_entangler(n_qubits=4): #creates circuit and applies the H, RY, and CZ gates to it relative to the number of qubits
    qc = QuantumCircuit(n_qubits, n_qubits) #Starter Code
    for q in range(n_qubits):
        qc.ry(np.pi / (q + 2), q)
    for q in range(n_qubits - 1):
        qc.cz(q, q + 1)
    qc.cz(n_qubits - 1, 0)
    for q in range(n_qubits):
        qc.h(q)
    qc.measure(range(n_qubits), range(n_qubits)) #turns qubits into classical bits
    return qc

# aliyah
def fourth_circuit(n_qubits=6): #creates circuit and applies the RY and CZ gates to it relative to the number of qubits (Starter Code)
    qc = QuantumCircuit(n_qubits, n_qubits)
    for q in range(n_qubits):
        qc.ry(np.pi / (q+2), q)
    for q in range(n_qubits -1):
        qc.cz(q, q + 1)
    qc.cz(n_qubits -2, 0)
    qc.measure(range(n_qubits), range(n_qubits)) #turns qubits into classical bits
    return qc

circuit_library = { #creates key for the run circuits function (ChatGPT)
    "superposition": circuit_superposition,
    "layered": circuit_layered_phase,
    "ring": circuit_ring_entangler,
    "fourth": fourth_circuit
}

# aliyah
def run_circuits(name, shots=3000): #checks to see if name is one of the circuits (ChatGPT)
    if name not in circuit_library:
        raise ValueError(f"Unknown circuit: {name}")

    qc = circuit_library[name]()   # build circuit
    tqc = transpile(qc, sim)       # optimize for simulator

    result = sim.run(tqc, shots=shots).result()
    counts = result.get_counts()

    return counts

# aliyah
def get_all_counts(): #ChatGPT   Counts each bit string for each specific circuit
    results = {}

    for name in circuit_library:
        results[name] = run_circuits(name, shots=3000)

    return results

# ankita-- i understand this
def hamming(a, b): # return number of positions where they differ
    distance = 0
    if len(a) != len(b):
        raise ValueError("a and b are different lengths")
    for i in range(len(a)):
        if a[i] != b[i]:
            distance += 1
    return distance

# ankita -- kind of understand
def build_graph(counts): # creates a network graph where each bitstring is a node (weight = counts) and edges connect pairs with Hamming distance exactly 1
    graph = nx.Graph()
    for bitstring,count in counts.items():
        graph.add_node(bitstring,count=count)

    bitstrings = list(counts.keys())
    for i in range (len(bitstrings)):
        for j in range (i+1, len(bitstrings)):
            if(hamming(bitstrings[i], bitstrings[j]) == 1):
                graph.add_edge(bitstrings[i],bitstrings[j])

    return graph

#ankita -- dont really understand
def get_layout(graph): # runs nx.spring_layout(graph, seed=42) and returns the position dict. Use seed=42 so positions are stable across reruns
    return nx.spring_layout(graph, seed=42)

#ankita -- kind of understand
def calculate_entropy(counts):
    total = sum(counts.values())
    entropy_dict = {}

    for bitstring, count in counts.items():
        p = count / total
        entropy = -p * np.log2(p) if p > 0 else 0
        entropy_dict[bitstring] = entropy

    return entropy_dict

#ankita -- no idea what this does
def get_graph_data(counts):
    graph = build_graph(counts)
    entropies = calculate_entropy(counts)

    nodes = []
    for node in graph.nodes():
        nodes.append({
            'id': node,
            'count': counts[node],
            'entropy': entropies[node]
        })

    edges = list(graph.edges())

    layout = get_layout(graph)

    return nodes, edges, layout

all_counts = get_all_counts()
print(all_counts["layered"])
print(all_counts["fourth"]) #Tests if functions work

