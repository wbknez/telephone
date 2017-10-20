"""

"""
from random import random

import numpy as np
from mesa import Model
from mesa.space import SingleGrid
from mesa.time import RandomActivation

from .network_gen import NetworkGenerator
from .person import Person


def is_malicious(model):
    """
    Returns whether or not a newly generated person should be considered
    malicious or not by choosing a random number and comparing it to the
    specified model's maliciousness probability.

    :param model: The model to use.
    :return: Whether or not a generated person is malicious.
    """
    return random() < model.malicious_prob


def is_knowledgeable(model, malicious):
    """
    Returns whether or not a newly generated person already knows an arbitrary
    bit of data by choosing a random number and comparing it to the specified
    model's knowledge probability.

    People that are malicious cannot also start the simulation with knowledge
    about a bit of data, otherwise the simulation risks being stuck in an
    infinite loop.

    :param model: The model to use.
    :param malicious: If the person is malicious.
    :return: Whether or not a generated person already knows about a bit of
    data.
    """
    return False if malicious else random() < model.data_prob


def initial_state(model, data):
    """
    Returns the initial state a newly generated person should be in by
    choosing a random number and comparing it to the specified model's search
    probability.

    People that already have knowledge of the data cannot be in a search state.

    :param model: The model to use.
    :param data: If the person already has data knowledge.
    :return: The type of state a person should be in.
    """
    if data or model.search_prob <= random():
        return Person.State.Waiting
    return Person.State.Searching


class TelephoneModel(Model):
    """

    """

    def __init__(self, seed, **kwargs):
        super().__init__(seed)
        self.collector = None
        self.data = {"waiting": 0, "reporting": 0, "searching": 0, "knowing": 0}
        self.grid = SingleGrid(kwargs["width"], kwargs["height"], False)
        self.params = kwargs
        self.people = []
        self.schedule = RandomActivation(self)

        self.create_people()
        self.create_networks()
        self.create_data_collector()

    def __getattr__(self, item):
        if item == "steps":
            return self.schedule.steps
        elif item in self.params:
            return self.params[item]

    def create_data_collector(self):
        """

        """
        pass

    def create_networks(self):
        """
        Creates a social network for each person generated for this simulation.
        """
        generator = NetworkGenerator(self.num_people)

        for person in self.people:
            generator.generate_for(person, self)

    def create_people(self):
        """
        Creates the population of people for this simulation.
        """
        current_id = 0

        for h in reversed(range(self.height)):
            for w in range(self.width):
                if current_id >= self.num_people:
                    return
                person = self.create_person(current_id)

                self.grid.place_agent(person, (w, h))
                self.people.append(person)
                current_id += 1

    def create_person(self, unique_id):
        """
        Creates a new person for this simulation, using user-specified
        parameters to determine whether the person will be malicious,
        have initial knowledge of a bit of data, or be searching for the data
        instead.

        :param unique_id: The unique identifier to use.
        :return: A new person.
        """
        person = Person(unique_id, self)

        person.max_contacts = np.random.normal(self.mu, self.sigma, 1)
        person.malicious = is_malicious(self)
        person.data = is_knowledgeable(self, person.malicious)
        person.state = initial_state(self, person.data)

        return person

    def step(self):
        """
        Updates the simulation for a single time step.
        """
        self.schedule.step()
