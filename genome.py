from dataclasses import dataclass
from enum import Enum
from random import choice, randint, random

TARGET = 832
NUMBERS = [50, 75, 4, 7, 3, 6]

# probability of using a number in an expression when not required
# (as opposed to another expression)
NUMBER_PROBABILITY = 1 / 3


class Operator(Enum):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3


@dataclass
class Expression:
    left: int | Expression = -1
    operator: Operator = Operator.ADD
    right: int | Expression = -1


Node = Expression | int


class Genome:
    def __init__(self) -> None:
        self.fitness: float = 0

        self.target: int = TARGET
        self.unused_numbers: list[int] = [x for x in NUMBERS]

        self.expression: Expression = Expression()
        self.populate_expression(self.expression, len(self.unused_numbers))

    def populate_expression(self, expression: Expression, num_available: int) -> None:
        expression.operator = Operator(randint(0, 3))

        if num_available == 2 or num_available == 3:
            x = choice(self.unused_numbers)
            expression.left = x
            self.unused_numbers.remove(x)

            if num_available == 2 or random() < NUMBER_PROBABILITY:
                x = choice(self.unused_numbers)
                expression.right = x
                self.unused_numbers.remove(x)
            else:
                expression.right = Expression()
                self.populate_expression(expression.right, num_available - 1)

        else:
            if random() < (1 - NUMBER_PROBABILITY) ** 2:
                available_left = randint(2, num_available - 2)

                expression.left = Expression()
                self.populate_expression(expression.left, available_left)

                expression.right = Expression()
                self.populate_expression(expression.right, num_available - available_left)  # fmt: off
            else:
                x = choice(self.unused_numbers)
                expression.left = x
                self.unused_numbers.remove(x)

                if random() < NUMBER_PROBABILITY / (2 - NUMBER_PROBABILITY):
                    x = choice(self.unused_numbers)
                    expression.right = x
                    self.unused_numbers.remove(x)
                else:
                    expression.right = Expression()
                    self.populate_expression(expression.right, num_available - 1)

    def evaluate_node(self, node: Node) -> float:
        if isinstance(node, int):
            return node

        if node.operator == Operator.ADD:
            return self.evaluate_node(node.left) + self.evaluate_node(node.right)
        if node.operator == Operator.SUB:
            return self.evaluate_node(node.left) - self.evaluate_node(node.right)
        if node.operator == Operator.MUL:
            return self.evaluate_node(node.left) * self.evaluate_node(node.right)
        else:
            return self.evaluate_node(node.left) / self.evaluate_node(node.right)

    def calculate_fitness(self) -> None:
        self.fitness = 1000 - abs(self.target - self.evaluate_node(self.expression))

    def remove_node(self, node: Node) -> None:
        pass

    def mutate(self) -> None:
        pass
