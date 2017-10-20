"""

"""
import time
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
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
    return {"Shape": "circle" if not person.malicious else "rect",
            "Filled": "true", "r": "0.5", "Layer": "0", "w": "0.5", "h": "0.5",
            "Color": "blue" if person.data else _STATE_COLORS[person.state]}


_PARAMS = {
    "seed": int(time.time()),
    "num_people": UserSettableParameter("slider", "Number of Agents", 100, 2,
                                        225, 1),
    "data_prob": UserSettableParameter("slider", "Probability of Initial "
                                                 "Knowledge",
                                       0.05, 0.0, 1.0, 0.01),
    "malicious_prob": UserSettableParameter("slider", "Probability of "
                                                      "Maliciousness",
                                            0.05, 0.0, 1.0, 0.01),
    "search_prob": UserSettableParameter("slider", "Probability of Initial "
                                                   "Search Desire",
                                         0.05, 0.0, 1.0, 0.01),
    "width": 15,
    "height": 15
}


grid = CanvasGrid(person_portrayal, 15, 15, 500, 500)
server = ModularServer(TelephoneModel, [grid],
                       "Telephone Model", _PARAMS)
