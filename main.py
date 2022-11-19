import numpy as np
import matplotlib.pyplot as plt
from numpy.random import randint

from itertools import product

from CircuitModeling import Circuit, Element
from CircuitSimulator import VirtualCircuitEmulator
from GeneticAlgorithm import GeneticAlgorithm
from Utilities import disp_progress_bar


def create_demo_circuit_in_mem() -> Circuit:
    # a, b, c, d, e, f
    signals_table = [0]*6
    # a, b, c
    top_inputs_indexes = [0, 1, 2]
    # AND, NOT
    elements_type_table = ["AND", "NOT"]
    # AND E1
    and_1 = Element(
        name="E1",
        operation_index=0,
        inputs_indexes=[0, 1],
        output_index=3
    )
    not_1 = Element(
        name="E2",
        operation_index=1,
        inputs_indexes=[2],
        output_index=4
    )
    and_2 = Element(
        name="E3",
        operation_index=0,
        inputs_indexes=[3, 4],
        output_index=5
    )
    elements_table = [and_1, not_1, and_2]
    c = Circuit(
        top_inputs_indexes=top_inputs_indexes,
        elements_type_table=elements_type_table,
        elements_table=elements_table,
        signals_table=signals_table
    )
    return c


def testbench_a(circuit: Circuit):
    size = len(circuit.get_top_inputs_indexes())
    inputs_table = list(product([0, 1], repeat=size))
    vc_sim = VirtualCircuitEmulator(circuit=circuit)
    i = circuit.get_elements_table()[-1].get_output_index()
    print(f"(a, b, c) : d")
    for inputs in inputs_table:
        print(f"{inputs} : {vc_sim.simulate_circuit(inputs)[i]}")


def testbench_b(circuit: Circuit):
    vc_sim = VirtualCircuitEmulator(circuit=circuit)
    for N in [10, 100, 4400, 10_000, 20_000]:
        switches_table = vc_sim.simulate_circuit_with_workload(N)
        i_list = [elem.get_output_index() for elem in circuit.get_elements_table()]
        switches_table = [switches_table[i] for i in i_list]
        avg_switching_activity = list(map((lambda u: u/N), switches_table))
        print(f"{N = } {avg_switching_activity = }")


def testbench_c(circuit: Circuit):
    sp_table = [0.5]*len(circuit.get_top_inputs_indexes())
    vc_sim = VirtualCircuitEmulator(circuit=circuit)
    i_list = [elem.get_output_index() for elem in circuit.get_elements_table()]
    res = vc_sim.simulate_circuit(sp_table)
    res = [circuit.get_signals_table()[i] for i in i_list]
    print("Signal Probability", res)
    print("Switching Activity", list(map(lambda u: 2*u*(1-u), res)))


def homework4_1(circuit: Circuit):
    print("Executing random search")
    n = 10
    l = 2
    vc_sim = VirtualCircuitEmulator(circuit=circuit)
    
    def objective(inputs):
        switches_table = vc_sim.simulate_circuit_with_workload(workload=inputs)
        switches_table = [switches_table[i] for i in circuit.get_output_signals_indexes()]
        score = sum(switches_table)
        #circuit.reset()
        return score
    
    genetic_algorithm = GeneticAlgorithm(N=n, L=l, M=0.01, objective=objective)
    genetic_algorithm.init_individuals(gene_size=len(circuit.get_top_inputs_indexes()))
    genetic_algorithm.evaluate()
    x = list(range(n))
    y = [s for s in genetic_algorithm.get_score_per_individual()]
    return (x, y)


def homework4_3(circuit: Circuit):
    print("Executing genetic algorithm")
    n = 30
    l = 2
    Gen = 100
    m = 0.05
    
    vc_sim = VirtualCircuitEmulator(circuit=circuit)
    
    def objective(inputs):
        switches_table = vc_sim.simulate_circuit_with_workload(workload=inputs)
        switches_table = [switches_table[i] for i in circuit.get_output_signals_indexes()]
        score = sum(switches_table)
        circuit.reset()
        return score

    genetic_algorithm = GeneticAlgorithm(N=n, L=l, M=m, objective=objective)
    genetic_algorithm.init_individuals(gene_size=len(circuit.get_top_inputs_indexes()))

    x = list(range(Gen))
    y = []
    for g in range(Gen):
        genetic_algorithm.run()
        m_i = genetic_algorithm.get_max_score_index()
        max_score = genetic_algorithm.get_score_per_individual()[m_i]
        disp_progress_bar(low=g, high=Gen)
        y.append(max_score)
    return (x, y)


if __name__ == "__main__":
    # Lab 3
    np.random.seed(10)
    #circuit = create_demo_circuit_in_mem()
    #print(circuit)
    #testbench_a(circuit)
    #testbench_b(circuit)
    #testbench_c(circuit)
    
    circuit = Circuit()
    circuit.load_from_file("circuit2.txt")
    print(circuit)
    #testbench_a(circuit)
    #testbench_b(circuit)
    #testbench_c(circuit)
    
    # Lab 4
    x, y = homework4_1(circuit)
    plt.plot(x, y)
    plt.title("Random Search")
    plt.xlabel("individual")
    plt.ylabel("switches")
    plt.show()
'''
    for i in range(4):
        x, y = homework4_3(circuit)
        print(f"Done executing worker {i}")
        plt.plot(x, y)
    plt.title("Genetic Algorithm")
    plt.xlabel("gen")
    plt.ylabel("score")
    plt.show()
'''