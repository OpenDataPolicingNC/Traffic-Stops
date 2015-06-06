from django.test import TestCase
from django.contrib.auth.models import User

from nc.models import Stop
from nc.routers import StateDatasetRouter


class StateDatasetRouterTest(TestCase):
    def test_read_state_model(self):
        """Models within State apps should map to State DBs"""
        router = StateDatasetRouter()
        self.assertEqual('traffic_stops_nc', router.db_for_read(Stop))

    def test_read_other_model(self):
        """Models outside State apps should map to the default DB"""
        router = StateDatasetRouter()
        self.assertEqual('default', router.db_for_read(User))

    def test_write_state_model(self):
        """Models within State apps should map to State DBs"""
        router = StateDatasetRouter()
        self.assertEqual('traffic_stops_nc', router.db_for_write(Stop))

    def test_write_other_model(self):
        """Models outside State apps should map to the default DB"""
        router = StateDatasetRouter()
        self.assertEqual('default', router.db_for_write(User))

    def test_syncdb_state_model_defaultdb(self):
        """State models should not sync to the default DB"""
        router = StateDatasetRouter()
        self.assertFalse(router.allow_syncdb('default', Stop))

    def test_syncdb_other_model_defaultdb(self):
        """Other models should sync to the default DB"""
        router = StateDatasetRouter()
        self.assertTrue(router.allow_syncdb('default', User))

    def test_syncdb_state_model_statedb(self):
        """State models should sync to State DBs"""
        router = StateDatasetRouter()
        self.assertTrue(router.allow_syncdb('traffic_stops_nc', Stop))

    def test_syncdb_other_model_statedb(self):
        """Other models should not sync to State DBs"""
        router = StateDatasetRouter()
        self.assertFalse(router.allow_syncdb('traffic_stops_nc', User))
