"""

"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid

from .model import TelephoneModel
from .person import Person


def person_portrayal(person):
    """


    :param person: The person to visualize.
    :return: A new portrayal.
    """
    return {"Shape": "circle", "Filled": "true", "r": "0.5",
            "Color": "blue" if person.data else "red" \
                if person.state == Person.State.Searching else "gray"}


grid = CanvasGrid(person_portrayal, 10, 10, 400, 400)
server = ModularServer(TelephoneModel, [grid],
                       "Telephone Model", {"seed": 0,
                                           "num_people": 100,
                                           "malicious_prob": 0,
                                           "data_prob": 0.05,
                                           "search_prob": 0.05,
                                           "width": 10,
                                           "height": 10})
