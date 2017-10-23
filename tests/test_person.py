"""

"""
from unittest import TestCase

from telephone.person import Person


class PersonTest(TestCase):
    """
    Test suite for Person.
    """

    class TestModel:
        """
        A simple test model.
        """

        def __init__(self):
            self.people = []
            self.steps = 0

    def setUp(self):
        self.model = PersonTest.TestModel()
        self.person = Person(0, self.model, None)
        self.contact = Person(1, self.model)

        self.model.people = [self.person, self.contact]

    def tearDown(self):
        pass

    def test_available(self):
        self.assertTrue(self.person.is_available())

    def test_available_correctly_handles_next_step(self):
        self.person.set_busy()
        self.assertFalse(self.person.is_available())

        self.model.steps += 1
        self.assertTrue(self.person.is_available())

    def test_not_available_when_busy(self):
        self.person.set_busy()
        self.assertFalse(self.person.is_available())

    def test_call_makes_both_busy(self):
        self.person.call(self.contact)

        self.assertTrue(self.contact.busy)
        self.assertTrue(self.person.busy)

    def test_call_correctly_updates_last_called(self):
        self.person.last_dialed = -1
        self.person.call(self.contact)

        self.assertEqual(1, self.person.last_dialed)

    def test_report_back_bails_early_when_no_requester_exists(self):
        self.person.requester = -1
        self.person.state = Person.State.Reporting

        self.person.report_back(None)
        self.assertEqual(Person.State.Waiting, self.person.state)

    def test_report_back_raises_exception_when_caller_does_not_know_data(self):
        self.person.data = False
        self.assertRaises(ValueError, self.person.report_back, self.contact)

    def test_report_back_succeeds_when_requester_does_not_know_data(self):
        self.contact.state = Person.State.Searching
        self.person.data = True
        self.person.malicious = False
        self.person.requester = 1
        self.person.state = Person.State.Reporting

        self.assertFalse(self.contact.data)
        self.assertEqual(Person.State.Searching, self.contact.state)

        self.person.report_back(self.contact)

        self.assertTrue(self.contact.busy)
        self.assertTrue(self.contact.data)
        self.assertEqual(Person.State.Waiting, self.contact.state)
        self.assertTrue(self.person.busy)
        self.assertEqual(-1, self.person.requester)
        self.assertEqual(Person.State.Waiting, self.person.state)

    def test_report_back_propagates_up_search_network_correctly(self):
        self.contact.requester = 2
        self.contact.state = Person.State.Searching
        self.person.data = True
        self.person.malicious = False
        self.person.requester = 1
        self.person.state = Person.State.Reporting

        self.assertFalse(self.contact.data)
        self.assertEqual(Person.State.Searching, self.contact.state)

        self.person.report_back(self.contact)

        self.assertTrue(self.contact.busy)
        self.assertTrue(self.contact.data)
        self.assertEqual(Person.State.Reporting, self.contact.state)
        self.assertTrue(self.person.busy)
        self.assertEqual(-1, self.person.requester)
        self.assertEqual(Person.State.Waiting, self.person.state)

    def test_respond_to_returns_false_when_data_is_unknown(self):
        self.person.data = False
        self.assertFalse(self.person.respond_to(self.contact))
        self.assertEqual(Person.State.Searching, self.person.state)

    def test_respond_to_returns_true_when_data_is_known(self):
        self.person.data = True
        self.assertTrue(self.person.respond_to(self.contact))

    def test_respond_to_always_false_when_malicious(self):
        self.person.data = False
        self.person.malicious = True

        self.assertFalse(self.person.respond_to(self.contact))
        self.person.data = True
        self.assertFalse(self.person.respond_to(self.contact))

    def test_respond_to_preserves_existing_search_state(self):
        self.person.data = False
        self.person.requester = 2
        self.person.state = Person.State.Searching

        self.assertFalse(self.person.respond_to(self.contact))
        self.assertEqual(2, self.person.requester)
        self.assertEqual(Person.State.Searching, self.person.state)
