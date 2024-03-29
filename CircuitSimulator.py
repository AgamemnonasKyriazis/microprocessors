from copy import deepcopy

from numpy.random import randint

from CircuitModeling import Circuit, Element
from SignalProbabilities import OPS


def create_random_workload(N, size):
    """Creates a random workload of N size"""
    workload = []
    for _ in range(N):
        m = [randint(0, 2) for _ in range(size)]
        workload.append(m)
    return workload


class VirtualCircuitEmulator:

    def __init__(self, circuit: Circuit) -> None:
        self.circuit = circuit

    def process(self, element: Element):
        op = OPS[
            self.circuit.get_elements_type_table()[
                element.get_operation_index()
            ]
        ]
        element_inputs = [self.circuit.get_signals_table()[i] for i in element.get_inputs_indexes()]
        element_output = op(element_inputs)
        self.circuit.update_signal(element.get_output_index(), element_output)


    def simulate_circuit(self, inputs):
        """
            Simulates the circuit for the given inputs.

                Parameters:
                    inputs (list): The inputs to be assigned
                
                Returns:
                    signals_table (list): The current state of the circuit's signal table
        """
        for i in range(len(self.circuit.get_top_inputs_indexes())):
            signal_index = self.circuit.get_top_inputs_indexes()[i]
            self.circuit.update_signal(signal_index, inputs[i])
        for elem in self.circuit.get_elements_table():
            self.process(elem)
        return self.circuit.get_signals_table()


    def simulate_circuit_with_workload(self, N=None, workload=None):
        """
            Simulates the circuit for a given (or random) workload.

                Parameters:
                    N (int): Workload size
                    workload (list): Workload to use in simulation
                
                Returns:
                    switches_table (list): Number of switches done for each signal
        """
        size = len(self.circuit.get_top_inputs_indexes())
        workload = create_random_workload(N, size) if workload is None else workload
        switches_table = [0]*len(self.circuit.get_signals_table())
        old_signals_values = deepcopy(self.simulate_circuit(workload[0]))
        for inputs in workload[1:]:
            new_signals_values = deepcopy(self.simulate_circuit(inputs))           
            for elem in self.circuit.get_elements_table():
                i = elem.get_output_index()
                switches_table[i] += 1 if old_signals_values[i] != new_signals_values[i] else 0
            old_signals_values = deepcopy(new_signals_values)
        return switches_table
