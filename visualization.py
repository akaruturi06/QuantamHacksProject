import networkx as nx

bs1 = "001"
bs2 = "010"
bs3 = "011"


def hamming(a, b): # return number of positions where they differ
    distance = 0
    if len(a) != len(b):
        raise ValueError("a and b are different lengths")
    for i in range(len(a)):
        if a[i] != b[i]:
            distance += 1
    return distance

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

def get_layout(graph): # runs nx.spring_layout(graph, seed=42) and returns the position dict. Use seed=42 so positions are stable across reruns
    return nx.spring_layout(graph, seed=42)

#print(hamming(bs1, bs3))

counts = {"000": 50, "001": 30, "010": 20}

print(get_layout(build_graph(counts)))
