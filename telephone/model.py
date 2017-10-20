"""

"""
from random import random

from mesa import Model
from mesa.time import RandomActivation

from .person import Person


class TelephoneModel(Model):
    """

    """

    def __init__(self, seed, **kwargs):
        super().__init__(seed)
        self.data = {}
        self.params = kwargs
        self.people = []
        self.schedule = RandomActivation(self)

        self.create_people()
        self.create_networks()
        self.create_data_collectors()

    def __getattr__(self, item):
        if item == "steps":
            return self.schedule.steps

    def create_data_collectors(self):
        """

        """
        pass

    def create_networks(self):
        """

        """
        pass

    def create_people(self):
        """

        """
        for i in range(self.params["num_people"]):
            is_malicious = random() < self.params["malicious_prob"]
            knows_data = random() < self.params["data_prob"]
            start_state = Person.State.Searching \
                if random() < self.params["search_prob"] and not knows_data \
                else Person.State.Waiting
            self.people.append(Person(i, self, data=knows_data,
                                      malicious=is_malicious,
                                      state=start_state))

    def step(self):
        """
        Updates the simulation for a single time step.
        """
        self.schedule.step()
