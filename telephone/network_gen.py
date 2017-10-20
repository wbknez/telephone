"""

"""
import random


class NetworkGenerator:
    """

    """

    def __init__(self, max_size):
        self.network = list(range(max_size))

    def can_link_to(self, person, contact, model):
        if model.require_mutual and \
                        len(contact.contacts) >= contact.max_contacts and \
                not person.unique_id in contact.contacts:
            return False
        return True

    def generate_for(self, person, model):
        """

        :param person:
        :param model:
        """
        contacts = [x for x in self.network \
                if not x == person.unique_id and not x in person.contacts]
        in_theory = person.max_contacts - len(person.contacts)
        num_contacts = min(in_theory, len(contacts))

        random.shuffle(contacts)
        for contact_id in contacts:
            if len(person.contacts) >= num_contacts:
                return

            contact = model.people[contact_id]
            if self.can_link_to(person, contact, model):
                self.link_to(person, contact, model)

    def link_to(self, person, contact, model):
        person.contacts.append(contact.unique_id)

        if model.require_mutual:
            contact.contacts.append(person.unique_id)
