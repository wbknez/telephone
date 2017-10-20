"""
Contains all of the classes and functions necessary to generate simple,
directed social networks.
"""
import random


def can_link_to(person, contact, model):
    """
    Determines whether or not the specified person can form a social network
    link to the specified contact.

    :param person: The person wanting to link.
    :param contact: The contact to determine link eligibility.
    :param model: The model to use.
    """
    if model.require_mutual and \
                    len(contact.contacts) >= contact.max_contacts and \
            not person.unique_id in contact.contacts:
        return False
    return True


def can_reciprocate(person, contact, model):
    """
    Determines whether or not the specified person can form a reciprocal link
    with the specified contact.

    Please note that this function is different than can_link_to() because
    this project's user-selectable requirements have already been met in
    order for the initial link to be created.

    :param person: The person forming a reciprocal link from.
    :param contact: The person to form a link to.
    :param model: The model to use.
    :return: Whether or not a reciprocal link may form.
    """
    return len(person.contacts) < person.max_contacts and \
           not contact.unique_id in person.contacts and \
           random.random() < model.recip_prob


def link_to(person, contact, model):
    """
    Creates both a link in specified person's social network to the specified
    contact as well as attempting to form a reciprocal link if necessary.

    :param person: The person to link from.
    :param contact: The person to link to.
    :param model: The model to use.
    """
    person.add_contact(contact)

    if model.require_mutual or can_reciprocate(contact, person, model):
        contact.add_contact(person)


class NetworkGenerator:
    """
    Represents a mechanism for generating simple, potentially mutual social
    networks.

    By default (as specified by the user-selectable model parameters) this
    generator prefers mutual social network links but not require,
    or enforce, them.  This means that without such a requirement a network
    link may be one way, causing the network to potentially be much wider
    than it otherwise would be.  Conceptually, these networks are not
    intended to be classified as intimate or anything that indicates extreme
    selection, so not requiring mutuality is acceptable in this context.  In
    addition, the use of the reciprocation probability also achieves this
    effect in a more fine-grained manner, allowing the user to control the
    spread of contacts through mutual addition.

    The one requirement this generator always respects is each person's
    maximum number of contacts.  Despite the checks in this project being
    greater than or equals, this generator guarantees that the number of
    contacts of each agent's social network will be strictly less than the
    allowed maximum (per standard array rules).

    This generator uses a simple brute-force algorithm that takes advantage
    of each person in this simulation being given a unique identifier
    starting from zero.  Potential contact candidates are created from the
    disjunctive union of the total possible identifiers and the ones that
    have already been added to a person's contact list.  These candidates are
    shuffled and then evaluated for connection.  This process continues until
    either there are no more candidates or the total number of contacts for
    that person is reached.
    """

    def __init__(self, max_size):
        self.network = list(range(max_size))

    def generate_for(self, person, model):
        """
        Generates a new social network for the specified person using
        user-selected parameters from the specified model.

        :param person: The person to generate a social network for.
        :param model: The model to use.
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
