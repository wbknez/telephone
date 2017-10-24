"""
Contains the classes and functions necessary to define the agents for this
project's agent-based simulation.
"""
import random
from enum import Enum, unique

import numpy as np
from mesa import Agent


class Person(Agent):
    """
    Represents a single person, or agent, in a simulation about information
    flow through a population's composite social network.

    Attributes:
        contacts (numpy.array): This person's social network.
        busy (bool): Whether or not this person is available for a call.
        data (bool): Whether or not this person knows the answer.
        last_dialed (int): The identifier of the last person this person called.
        last_dialed_time (int): The time step that the last call took place.
        malicious (bool): Whether or not this person is a bad actor.
        max_contacts (int): The total number of contacts this person may have.
        requester (int): The person that caused this person to begin searching.
        state (Person.State): The current state of this person.
        timestamp (int): The time step that this person's busy state was set.
    """

    @unique
    class State(Enum):
        """
        Represents the different states a person may be in.
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
        self.last_dialed_time = -1
        self.malicious = malicious
        self.max_contacts = 0
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

    def add_contact(self, contact):
        """
        Adds the specified contact to this person's list of contacts (which
        represents their social network).

        :param contact: The person to add.
        """
        self.contacts.append(contact.unique_id)

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
        self.last_dialed_time = self.model.steps

        if self.data:
            self.state = Person.State.Reporting if not self.requester == -1 \
                else Person.State.Waiting

    def check_availability(self):
        """
        Checks whether or not this person's busy state is accurate for the
        current time step.
        """
        if self.timestamp != self.model.steps:
            self.busy = False
            self.timestamp = self.model.steps

    def check_last_dialed(self):
        """
        Checks whether or not a sufficient amount of time has passed before
        this person may call the last person they dialed again.
        """
        if not self.last_dialed == -1 and \
                not self.model.last_dialed_threshold == -1:
            if self.model.steps - self.last_dialed_time > \
                    self.model.last_dialed_threshold:
                self.last_dialed = -1

    def filter_predicate(self, contact_id):
        """
        Returns whether or not the specified contact is available for a call.

        The three rules that govern this process are:
            1. A contact cannot be called twice in a row.
            2. The original person who sparked this person's search cannot be
            contacted unless this person is reporting the answer.
            3. A contact must not already be engaged in a call with someone
            else.

        :param contact_id: The identifier of the person to check.
        :return: Whether or not a contact is available for a call.
        """
        contact = self.model.people[contact_id]
        return not contact.unique_id == self.last_dialed and \
               not contact.unique_id == self.requester and \
               contact.is_available()

    def finish_search(self):
        """
        Conceptually "finishes" a search by resetting this person's state to
        simply waiting and removing the original requester.
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

    def is_reporting(self):
        """
        Returns whether or not this person is trying to report their
        knowledge of an arbitrary bit of data to the person who originally
        asked them for it.

        :return: Whether or not this person's state is reporting.
        """
        return self.state == Person.State.Reporting

    def is_searching(self):
        """
        Returns whether or not this person is searching their contacts and
        calling them in order to find an arbitrary bit of data.

        :return: Whether or not this person's state is searching.
        """
        return self.state == Person.State.Searching

    def is_waiting(self):
        """
        Returns whether or not this person is simply waiting (i.e. doing
        nothing).

        :return: Whether or not this person's state is waiting.
        """
        return self.state == Person.State.Waiting

    def receive_update_from(self, caller):
        """
        Conceptually, "receives an update" from the specified caller that
        notifies this person of the true value of an arbitrary piece of data.

        :param caller: The person performing the notification.
        """
        if not caller.data:
            raise ValueError("Contact does not know the bit of data.")

        self.data = True
        self.state = Person.State.Reporting if not self.requester == -1 else \
            Person.State.Waiting

    def report_back(self, callee):
        """
        Attempts to call and inform the original person who asked about the
        data what it actually is.

        There are two situations where the specified callee is not informed:
            1. If this person is malicious.
            2. If the callee does not exist.

        :param callee: The person to report back to.
        """
        if callee is None or self.malicious:
            self.finish_search()
        else:
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
        if not self.data and self.requester == -1 and \
                not self.state == Person.State.Searching:
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
        self.check_last_dialed()
        choices = list(filter(self.filter_predicate, self.contacts))
        if choices:
            to_call = random.choice(choices)
            self.call(self.model.people[to_call])

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
