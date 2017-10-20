"""

"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from .model import TelephoneModel
from .person import Person


_STATE_COLORS = {Person.State.Reporting: "green",
                 Person.State.Searching: "red",
                 Person.State.Waiting: "gray"}


def person_portrayal(person):
    """
    Returns the visualization attributes that describe the specified person's
    current state and data knowledge.

    :param person: The person to visualize.
    :return: A new portrayal.
    """
    return {"Shape": "circle", "Filled": "true", "r": "0.5",
            "Color": "blue" if person.data else _STATE_COLORS[person.state]}


grid = CanvasGrid(person_portrayal, 10, 10, 400, 400)
server = ModularServer(TelephoneModel, [grid],
                       "Telephone Model", {"seed": 0,
                                           "num_people": 100,
                                           "malicious_prob": 0,
                                           "data_prob": 0.05,
                                           "search_prob": 0.05,
                                           "width": 10,
                                           "height": 10})
