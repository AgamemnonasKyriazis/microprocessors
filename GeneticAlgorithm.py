from numpy.random import randint, rand
from copy import deepcopy, copy

class Individual:

    def __init__(self, name, gene, objective, score=0) -> None:
        self.name = name
        self.gene = gene
        self.score = score
        self.objective = objective

    def __str__(self) -> str:
        return f"{self.name}, {self.gene}, {self.score}"

    def evaluate(self):
        self.score = self.objective(self.gene)
        return self.score

    def get_name(self):
        return self.name
    
    def get_score(self):
        return self.score

    def get_gene(self):
        return self.gene


class GeneticAlgorithm:

    def __init__(self, N, L, M, objective) -> None:
        self.individuals = None
        self.score_per_individual = [0]*N
        self.max_score_index = 0
        self.L = L
        self.N = N
        self.gene_size = 0
        self.M = M
        self.objective = objective

    def __str__(self) -> str:
        return '\n'.join([ind.__str__() for ind in self.individuals])

    def init_individuals(self, gene_size):
        self.individuals = []
        self.gene_size = gene_size
        for _ in range(self.N):
            self.individuals.append(
                Individual(
                    name=f"I{_}",
                    gene=randint(low=0, high=2, size=(self.L, gene_size)).tolist(),
                    objective=self.objective
                )
            )

    def evaluate(self):
        self.score_per_individual = list(map(Individual.evaluate, self.individuals))
        self.max_score_index = self.score_per_individual.index(max(self.score_per_individual))

    def exploit_explore(self):

        def select_top_two_individuals() -> list:
            # max
            i1 = self.max_score_index
            _scores =  copy(self.score_per_individual)
            _scores[self.max_score_index] = 0
            # second max
            i2 = _scores.index(max(_scores))
            return i1, i2
        
        top_two_individuals = select_top_two_individuals()
        i1 = self.individuals[top_two_individuals[0]]
        i2 = self.individuals[top_two_individuals[1]]
        next_generation = [deepcopy(i1), deepcopy(i2)]
        while len(next_generation) != self.N:
            i1_gene = deepcopy(i1.get_gene())
            i2_gene = deepcopy(i2.get_gene())
            r = randint(low=0, high=self.L)
            # cross
            ch1 = i1_gene[:r] + i2_gene[r:]
            ch2 = i2_gene[:r] + i1_gene[r:]
            # mutate
            for i in range(self.L):
                for j in range(self.gene_size):
                    if rand() <= self.M:
                        ch1[i][j] = 1 - ch1[i][j]
                    if rand() <= self.M:
                        ch2[i][j] = 1 - ch2[i][j]
            # init offsprings
            next_generation.append(    
                Individual(
                    name=i1.get_name() + f"I{len(next_generation)}",
                    gene=ch1,
                    objective=self.objective,
                    score=0
                )
            )
            next_generation.append(
                Individual(
                    name=i2.get_name() + f"I{len(next_generation)}",
                    gene=ch2,
                    objective=self.objective,
                    score=0
                )
            )
        self.individuals = deepcopy(next_generation)

    def get_individuals(self):
        return self.individuals
    
    def get_max_score_index(self):
        return self.max_score_index
    
    def get_score_per_individual(self):
        return self.score_per_individual

    def run(self):
        self.evaluate()
        self.exploit_explore()
        self.evaluate()