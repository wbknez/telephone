"""

"""
import time
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule

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
            "Color": "blue" if person.data and person.is_waiting() else \
                _STATE_COLORS[person.state]}


_PARAMS = {
    "seed": int(time.time()),
    "num_people": UserSettableParameter("slider", "Number of People", 225, 2,
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
    "mu": UserSettableParameter("slider", "Average Number of People in a "
                                          "Social Network (μ)",
                                10, 0, 20, 1),
    "sigma": UserSettableParameter("slider", "Standard Deviation of Social "
                                             "Network (σ)",
                                   0, 0, 10, 0.1),
    "recip_prob": UserSettableParameter("slider", "Probability of "
                                                  "Reciprocation",
                                        1.0, 0.0, 1.0, 0.01),
    "require_mutual": UserSettableParameter("checkbox", "Mutal Contact "
                                                        "is Required",
                                            False),
    "width": 15,
    "height": 15
}

_KNOWING = {"Label": "knowing", "Color": "blue"}
_NOT_KNOWING = {"Label": "not-knowing", "Color": "red"}

_REPORTING = {"Label": "reporting", "Color": "green"}
_SEARCHING = {"Label": "searching", "Color": "red"}
_WAITING = {"Label": "waiting", "Color": "gray"}

knowledge_chart = ChartModule([_KNOWING, _NOT_KNOWING],
                       data_collector_name="collector")
state_chart = ChartModule([_REPORTING, _SEARCHING, _WAITING],
                          data_collector_name="collector")
grid = CanvasGrid(person_portrayal, 15, 15, 500, 500)
server = ModularServer(TelephoneModel, [grid, knowledge_chart, state_chart],
                       "Telephone Model", _PARAMS)
