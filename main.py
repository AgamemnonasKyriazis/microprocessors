import numpy as np
from itertools import product

from CircuitModeling import Circuit, Element
from CircuitSimulator import VirtualCircuitEmulator


def create_demo_circuit_in_mem() -> Circuit:
    # a, b, c, d, e, f
    signals_table = ['z']*6
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
    i_list = [elem.get_output_index() for elem in circuit.get_elements_table()]
    for N in [10, 100, 4400, 10_000, 20_000]:
        avg_switching_activity = vc_sim.simulate_circuit_with_workload(N)
        avg_switching_activity = [avg_switching_activity[i] for i in i_list]
        print(f"{N = } {avg_switching_activity = }")


def testbench_c(circuit: Circuit):
    sp_table = [0.4400]*len(circuit.get_top_inputs_indexes())
    vc_sim = VirtualCircuitEmulator(circuit=circuit)
    res = vc_sim.simulate_circuit(sp_table)
    print("Signal Probability", res)
    print("Switching Activity", list(map(lambda u: 2*u*(1-u), res)))


if __name__ == "__main__":
    np.random.seed(10)
    circuit = create_demo_circuit_in_mem()
    print(circuit)
    #testbench_a(circuit)
    #testbench_b(circuit)
    testbench_c(circuit)
    
    circuit = Circuit()
    circuit.load_from_file("circuit.txt")
    print(circuit)
    #testbench_a(circuit)
    #testbench_b(circuit)
    testbench_c(circuit)
