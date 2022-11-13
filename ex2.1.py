from numpy.random import randint
import numpy as np

import SignalProbabilities as sgnp


def create_random_workload(N, top_inputs):
    """Creates a random workload of N size"""
    workload = []
    for _ in range(N):
        m = dict()
        for i in top_inputs:
            m[i] = randint(0, 2)
        workload.append(m)
    return workload


def modelsim_sp(**kwargs):
    """Simulates the signal probability for each net in a logic circuit given the signal probabilities of
    each input"""
    a, b, c = list(kwargs.values())
    e = sgnp.OPS["AND"]([a, b])
    f = sgnp.OPS["NOT"]([c])
    d = sgnp.OPS["AND"]([e, f])
    return {'e': e, 'f': f, 'd': d}


def modelsim_monte_carlo(N):
    """Simulates the switching activity for each net in a logic circuit for a random workload of N size"""
    workload = create_random_workload(N, ["a", "b", "c"])
    _e, _f, _d = 0, 0, 0
    _ec, _fc, _dc = 0, 0, 0
    for spnets in workload:
        net_values = modelsim_sp(**spnets)
        e, f, d = net_values["e"], net_values["f"], net_values["d"]
        _ec += 1 if e != _e else 0
        _fc += 1 if f != _f else 0
        _dc += 1 if d != _d else 0
        _e, _f, _d = e, f, d
    return {
        'e': _ec / N,
        'f': _fc / N,
        'd': _dc / N
    }


if __name__ == "__main__":
    np.random.seed(10)
    print("ex2.1")
    res = modelsim_sp(a=0.4400, b=0.4400, c=0.4400)
    print("Signal Probability", res)
    print("Switching Activity", [{k: 2*v*(1-v)} for k, v in res.items()])
    for n in [10, 100, 4400, 10_000, 20_000]:
        print(n, modelsim_monte_carlo(n))
