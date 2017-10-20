"""

"""
import random
from enum import Enum, unique

import numpy as np
from mesa import Agent


def contacts_filter(contact):
    """

    :param contact:
    :return:
    """
    pass


class Person(Agent):
    """


    Attributes:
        contacts (numpy.array): This person's social network.
        data (bool): Whether or not this person knows the answer.
        malicious (bool): Whether or not this person is a bad actor.
    """

    @unique
    class State(Enum):
        """

        """

        Reporting = 0
        """
        Represents a person who has successfully found out the answer to an 
        arbitrary question and is attempting to report her findings to the person
        who originally asked, if any.
        """

        Searching = 1
        """
        Represents a person who is currently searching for an arbitrary bit of 
        data in order to either inform themselves or someone else.
        """

        Waiting = 2
        """
        Represents a person who is neither reporting to someone nor searching
        for an answer.
        """

    def __init__(self, unique_id, model, contacts=None, data=False,
                 malicious=False, state=State.Waiting):
        super().__init__(unique_id, model)

        if contacts is None:
            contacts = []

        self.contacts = contacts
        self.busy = False
        self.data = data
        self.last_dialed = -1
        self.malicious = malicious
        self.requester = -1
        self.state = state
        self.timestamp = 0

    def __eq__(self, other):
        if isinstance(other, Person):
            return np.array_equal(self.contacts, other.contacts) and \
                     self.busy == other.busy and self.data == other.data and \
                     self.last_dialed == other.last_dialed and \
                     self.malicious == other.malicious
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    def call(self, other):
        """
        Conceptually "calls" the specified person and asks them whether or
        not they have an arbitrary bit of data.

        :param other: The (other) person to call.
        """
        self.set_busy()
        other.set_busy()
        self.data = other.respond_to(self)
        self.last_dialed = other.unique_id

    def check_availability(self):
        """
        Checks whether or not this person's busy state is accurate for the
        current time step.
        """
        if self.timestamp != self.model.steps:
            self.busy = False
            self.timestamp = self.model.steps

    def finish_search(self):
        """

        """
        self.requester = -1
        self.state = Person.State.Waiting

    def is_available(self):
        """
        Returns whether or not this person is available for a phone
        conversation.

        :return: The availability of this person.
        """
        self.check_availability()
        return not self.busy

    def receive_update_from(self, caller):
        """

        :param caller:
        """
        if not caller.data:
            raise ValueError("Contact does not know the bit of data.")

        self.data = True
        self.state = Person.State.Reporting

    def report_back(self, callee):
        """
        Attempts to call and inform the original person who asked about the
        data what it actually is.

        :param callee: The person to report back to.
        """
        if callee is None:
            self.state = Person.State.Waiting
            return

        if callee.is_available():
            callee.set_busy()
            callee.receive_update_from(self)
            self.set_busy()
            self.finish_search()

    def respond_to(self, caller):
        """
        Conceptually "responds" to the specified caller by returning whether
        or not this person knows an arbitrary bit of data.  If this person
        does not, then she begins calling others on her contact list in
        search of it.  Otherwise, this person will return a positive result
        unless she is malicious, in which case she will always return
        negatively.

        :return: Whether or not this person knows an arbitrary bit of data.
        """
        if not self.data and self.requester == -1:
            self.state = Person.State.Searching
            self.requester = caller.unique_id

        return self.data if not self.malicious else False

    def search_contacts(self):
        """
        Searches this person's contacts for someone to call and ask about an
        arbitrary bit of data; if someone is found, a call is initiated.

        There are two rules that govern which contact is selected:
            1. The contact cannot be the person who initially made the
            request, if any, causing this person to search.
            2. The contact cannot be the last person this person called.
        """
        choices = filter(contacts_filter, self.contacts)
        if choices:
            self.call(random.choice(choices))

    def set_busy(self):
        """
        Sets this person's busy state to True if it is not already for the
        current time step.
        """
        self.check_availability()
        self.busy = True

    def step(self):
        """
        Updates this person's state during a single step of a simulation.
        """
        if self.is_available():
            if self.state == Person.State.Reporting:
                callee = self.model.people[self.requester] \
                    if not self.requester == -1 else None
                self.report_back(callee)
            elif self.state == Person.State.Searching:
                self.search_contacts()
