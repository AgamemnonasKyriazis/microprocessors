class Element:

    def __init__(self, name, operation_index, inputs_indexes, output_index) -> None:
        self.name = name
        self.operation_index = operation_index
        self.inputs_indexes = inputs_indexes
        self.output_index = output_index

    def __str__(self):
        return f"Name, {self.name}\t" \
               f"Operation index, {self.operation_index}\t" \
               f"Inputs indexes, {self.inputs_indexes}\t" \
               f"Output index, {self.output_index}\n"

    def get_name(self):
        return self.name

    def get_operation_index(self):
        return self.operation_index
    
    def get_inputs_indexes(self):
        return self.inputs_indexes
    
    def get_output_index(self):
        return self.output_index


class Circuit:

    def __init__(self, top_inputs_indexes=[], elements_type_table=[], elements_table=[], signals_table=[]) -> None:
        self.top_inputs_indexes = top_inputs_indexes
        self.elements_type_table = elements_type_table
        self.elements_table = elements_table
        self.signals_table = signals_table

    def load_from_file(self, file_name):
        _intermediate_signals = []
        _all_signals = []
        _top_inputs = []
        with open(file_name, "r") as fp:
            # read all lines
            lines = fp.readlines()
            line = lines[0]
            # if file starts with top inputs declaration
            if str(line).startswith("top_inputs"):
                print("Found top level inputs declaration")
                _top_inputs = list(map(str.strip, line.split(" ")))[1:]
                lines = lines[1:]
                # remove the first line
            # read all lines (remaining)
            for line in lines:
                # comments, ignore it
                if str(line).startswith("#"):
                    print("Found Comment")
                    continue
                # split each line
                elem_str_list = list(map(str.strip, line.split(" ")))
                # element type "AND", "OR", etc
                elem_type = elem_str_list[0]
                # element signal output
                elem_output = elem_str_list[1]
                # element signal inputs
                elem_inputs = elem_str_list[2:]
                # add element type to list (if not exists)
                if elem_type not in self.elements_type_table:
                    self.elements_type_table.append(elem_type)
                # element type index (we will use this on Element init)
                obj_elem_type_index = self.elements_type_table.index(elem_type)
                # element inputs indexes (we will use these on Element init)
                obj_elem_inputs_indexes = []
                for elem_input in elem_inputs:
                    # add element inputs in all signals
                    if elem_input not in _all_signals:
                        _all_signals.append(elem_input)
                    # element input index list (we will use this on Element init)
                    obj_elem_inputs_indexes.append(
                        _all_signals.index(elem_input)
                    )
                # add element output in all signals (if not exists)
                if elem_output not in _all_signals:
                    _all_signals.append(elem_output)
                    _intermediate_signals.append(elem_output)
                # element output index (we will use this on Element init)
                obj_elem_output_index = _all_signals.index(elem_output)
                # create new element object and add it to Elements table
                self.elements_table.append(
                    Element(
                        self._get_new_elem(),
                        obj_elem_type_index,
                        obj_elem_inputs_indexes,
                        obj_elem_output_index
                    )
                )
        if _top_inputs:
            print("Declaring top level inputs from file...")
            [self.top_inputs_indexes.append(_all_signals.index(i)) for i in _top_inputs]
        else:
            print("Searching for top level inputs...")
            for i in range(len(_all_signals)):
                if _all_signals[i] not in _intermediate_signals:
                    self.top_inputs_indexes.append(i)
        self.signals_table = ['z']*len(_all_signals)
        self.sort_circuit_elements()
        self.top_output_index = self.elements_table[-1].get_output_index()

    def sort_circuit_elements(self):
        # initialize variables for sorting the vc elements
        _sorted_elements_table = []
        _marked_elements = [0]*len(self.elements_table)
        _marked_signals = [0]*len(self.signals_table)
        for i in self.top_inputs_indexes:
            _marked_signals[i] = 1
        # sort virtual circuit elements (vc)
        while not all(_marked_elements):
            for ielem in range(len(self.elements_table)):
                elem = self.elements_table[ielem]
                can_eval = all([_marked_signals[isgn] for isgn in elem.get_inputs_indexes()])
                should_eval = _marked_elements[ielem] == 0
                if can_eval and should_eval:
                    # mark element
                    _marked_elements[ielem] = 1
                    # mark output signal
                    _marked_signals[elem.get_output_index()] = 1
                    # add element to sorted list
                    _sorted_elements_table.append(elem)
        self.elements_table = [elem for elem in _sorted_elements_table]

    def _get_new_elem(self):
        return f"E{len(self.elements_table) + 1}"

    def __str__(self):
        return f"Top inputs indexes, {self.top_inputs_indexes}\n" \
               f"Elements type table, {self.elements_type_table}\n" \
               f"Elements table,\n{''.join([elem.__str__() for elem in self.elements_table])}" \
               f"Signals table, {self.signals_table}"

    def get_top_inputs_indexes(self):
        return self.top_inputs_indexes

    def get_elements_type_table(self):
        return self.elements_type_table
    
    def get_elements_table(self):
        return self.elements_table
    
    def get_signals_table(self):
        return self.signals_table

    def update_signal(self, signal_index, signal_value):
        self.signals_table[signal_index] = signal_value
