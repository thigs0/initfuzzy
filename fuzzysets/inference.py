import numpy as np
from fuzzysets import CauchyFuzzySet
from typing import Callable, List, Dict, Tuple

class TakagiSugenoInference:
    """
    The TakagiSugeno use implementation of FuzzySet and Tnorm to calculate inference

    paramns
    rules: function that return np.array with values of activation  
    """
    def __init__(self):
        self.rules: List[Tuple[Callable[[float], float], CauchyFuzzySet]] = []

    def add_rule(self, antecedent: Callable[[float], float], consequent):
        """
        Adiciona uma regra fuzzy.

        :param antecedent: função de pertinência (mu(x)) para a entrada
        :param consequent: conjunto fuzzy do tipo CauchyFuzzySet como saída
        """
        self.rules.append((antecedent, consequent))

    def infer(self, input_value: list, universe:np.ndarray) -> float:
        """
        Realiza a inferência Mamdani e retorna o valor defuzzificado.

        :param input_value: va:wqlor numérico de entrada
        :param resolution: número de pontos para amostragem na saída
        :return: valor defuzzificado (saída)
        """

        output_membership = np.zeros_like(universe)

        consequent_values = np.array([consequent(*input_value)])
        W = np.zeros(len(consequent_values))
        k=0
        for antecedent, consequent in self.rules:
            W[k] = antecedent(input_value)  # grau de ativação
            k+=1
        # Defuzzificação: centroide
        numerator = np.dot(consequent_values, W)
        W2 = np.dot(W, W)
        return numerator/W2

class MamdaniInference:
    """
    """

    def __init__(self):
        self.rules: List[Tuple[Callable[[float], float], CauchyFuzzySet]] = []

    def add_rule(self, antecedent: Callable[[float], float], consequent):
        """
        Adiciona uma regra fuzzy.

        :param antecedent: função de pertinência (mu(x)) para a entrada
        :param consequent: conjunto fuzzy do tipo CauchyFuzzySet como saída
        """
        self.rules.append((antecedent, consequent))

    def infer(self, input_value: list, universe:np.ndarray) -> float:
        """
        Realiza a inferência Mamdani e retorna o valor defuzzificado.

        :param input_value: va:wqlor numérico de entrada
        :param resolution: número de pontos para amostragem na saída
        :return: valor defuzzificado (saída)
        """

        output_membership = np.zeros_like(universe)

        for antecedent, consequent in self.rules:
            degree = antecedent(input_value)  # grau de ativação
            consequent_values = np.array([consequent.mu(x) for x in universe])
            output_membership = np.fmax(output_membership, np.fmin(degree, consequent_values))

        # Defuzzificação: centroide
        numerator = np.sum(universe * output_membership)
        denominator = np.sum(output_membership)

        if denominator == 0:
            return 0.0  # sem ativação

        return numerator / denominator

