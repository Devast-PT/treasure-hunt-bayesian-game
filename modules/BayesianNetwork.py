import random

from modules.GameData import GameData
import pprint

class BayesianNetwork:
    """
    Represents a Bayesian Network for calculating the probability of treasure locations
    based on signal strengths and evidence updates.

    The Bayesian Network is used for a probabilistic inference system. It maintains
    a network of nodes representing signal locations and the treasure, as well as
    edges representing dependencies. The network computes conditional probabilities
    based on detected signals and updates beliefs based on evidence.

    :ivar network: The Bayesian network representation containing nodes, edges,
        probabilities, and evidences. Nodes include "Treasure" and signal locations;
        edges define dependencies; probabilities store initial and conditional
        probabilities; evidences record observed data.
    :type network: dict
    """
    def __init__(self):
        rows, columns = GameData.columns, GameData.rows
        total = GameData.totalLocations

        # Create initial setup
        self.network = {
            "nodes": ["Treasure"],
            "edges": [],
            "probabilities": {},
            "evidences": [] #Takes edge + Signal Read
        }

        # Fill nodes / edges
        for row in range(1, rows + 1):
            for column in range(1, columns + 1):
                signalnode = f"S({row},{column})"
                self.network["nodes"].append(signalnode)
                self.network["edges"].append(("Treasure", signalnode))

        # Fill initial Treasure prob
        self.network["probabilities"]["Treasure"] = {
            f"({row},{col})": 1/total for row in range(1, rows + 1) for col in range(1, columns + 1)
        }

        # Fill Conditional Prob
        self.fill_conditional_probabilities()



    def fill_conditional_probabilities(self):
        """
        Fills the conditional probabilities for signal nodes in the Bayesian network based
        on the positions of potential treasure locations. The distances between signal nodes
        and treasure positions are calculated using the Chebyshev distance formula, and the
        probabilities are determined by a detector probability function.
        """
        treasure_positions = list(self.network["probabilities"]["Treasure"].keys())

        for edge in self.network["edges"]:
            _, signal_node = edge
            self.network["probabilities"][signal_node] = {}
            for treasure_position in treasure_positions:
                t_row, t_col = map(int, treasure_position.strip("()").split(","))
                s_row, s_col = map(int, signal_node.strip("S()").split(","))

                # fórmula da distância de Chebyshev
                distance = max(abs(t_row - s_row),abs(t_col - s_col))
                self.network["probabilities"][signal_node][treasure_position] = detectorFactoryProb(distance)

    def get_initial_belief(self):
        return self.network["probabilities"]["Treasure"]

    def update_belief(self, prior):
        """
        Updates the belief of the Bayesian network based on given prior and
        the latest evidence in the network. The method pops the most recent
        evidence from the network, adjusts the belief using the given conditional
        probabilities for the evidence, and normalizes the belief distribution.
        """
        evidence = self.network["evidences"].pop()
        signal_node, signal_value = evidence[0], evidence[1]

        belief = {key: value * self.network["probabilities"][signal_node][key][signal_value]
                  for key, value in prior.items()} # Calculate the new belief

        normal_factor = sum(belief.values())
        new_belief = {key: (prob / normal_factor) for key, prob in belief.items()}

        return new_belief

    def evidenceGenerator(self, row, column):
        """
        Determines and generates evidence signal for a given location on a grid based on the
        Conditional Probability Table (CPT) associated with the location and the treasure's position.
        It evaluates the probabilities for different signal levels by comparing random values against
        cumulative probabilities defined in the CPT. The generated signal evidence is then stored
        in the network's evidence list.
        """
        position_treasure = GameData.treasureLocation

        # Grab CPT for the location to detect (CPT stands for Conditional Probability Table)
        cpt = self.network["probabilities"][f"S({row},{column})"][position_treasure]
        random_probability = random.random()
        probability_signal_1 = cpt["+"]
        probability_signal_2 = cpt["++"] + probability_signal_1
        probability_signal_3 = cpt["+++"] + probability_signal_2
        probability_signal_4 = cpt["++++"] + probability_signal_3

        signal_return = ""

        if probability_signal_1 >= random_probability:
            signal_return = '+'
        elif probability_signal_2 >= random_probability:
            signal_return = "++"
        elif probability_signal_3 >= random_probability:
            signal_return = "+++"
        elif probability_signal_4 >= random_probability:
            signal_return = "++++"
        else:
            print(f"Error Detection on S({row},{column}) with treasure on {position_treasure}")

        self.network["evidences"].append((f"S({row},{column})", signal_return))

        return signal_return

def detectorFactoryProb(distance):
    """
    Determines and returns a dictionary representing probabilities based on the
    given `distance`. This function uses pattern matching to associate specific
    distances with a predefined probability distribution across four categories.
    """
    match distance:
        case 0:
            return {
                "++++": 0.8,
                "+++": 0.1,
                "++": 0.07,
                "+": 0.03
            }
        case 1:
            return {
                "++++": 0.08,
                "+++": 0.8,
                "++": 0.08,
                "+": 0.04
            }
        case 2:
            return {
                "++++": 0.04,
                "+++": 0.08,
                "++": 0.8,
                "+": 0.08
            }
        case _:
            return {
                "++++": 0.03,
                "+++": 0.07,
                "++": 0.1,
                "+": 0.8
            }