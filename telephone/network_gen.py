"""

"""
import random


def can_link_to(person, contact, model):
    """

    :param person: The person wanting to link.
    :param contact: The contact to determine link eligibility.
    :param model: The model to use.
    """
    if model.require_mutual and \
            len(contact.contacts) >= contact.max_contacts and \
            not person.unique_id in contact.contacts:
        return False
    return True


def link_to(person, contact, model):
    """

    :param person:
    :param contact:
    :param model:
    """
    person.contacts.append(contact.unique_id)

    if model.require_mutual:
        contact.contacts.append(person.unique_id)


class NetworkGenerator:
    """

    """

    def __init__(self, max_size):
        self.network = list(range(max_size))

    def generate_for(self, person, model):
        """

        :param person:
        :param model:
        """
        contacts = [x for x in self.network \
                    if not x == person.unique_id and not x in person.contacts]

        random.shuffle(contacts)
        for contact_id in contacts:
            if len(person.contacts) >= person.max_contacts:
                return

            contact = model.people[contact_id]
            if can_link_to(person, contact, model):
                link_to(person, contact, model)
