import numpy as np


_xor = (lambda nets: (nets[0] * (1 - nets[1])) + ((1 - nets[0]) * nets[1]))
OPS = {
    "AND": (lambda nets: np.prod(nets)),
    "OR": (lambda nets: 1 - (np.prod([1 - sp for sp in nets]))),
    "XOR": (lambda nets: _xor(nets) if len(nets) == 2 else OPS["XOR"]([_xor(nets), *nets[2:]])),
    "NAND": (lambda nets: 1 - OPS["AND"](nets)),
    "NOR": (lambda nets: 1 - OPS["OR"](nets)),
    "XNOR": (lambda nets: 1 - OPS["XOR"](nets)),
    "NOT": (lambda nets: 1 - nets[0])
}


if __name__ == "__main__":
    spns = [0.5, 0.5, 0.3]
    for op in ["AND", "OR", "XOR", "NAND", "NOR", "XNOR"]:
        print(op)
        sp_out = OPS[op](spns)
        sa_out = 2*sp_out*(1 - sp_out)
        print(f"Signal Probability: {sp_out}, Switching Activity {sa_out}")

