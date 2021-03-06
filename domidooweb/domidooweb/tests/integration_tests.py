import unittest
import transaction
import os
from pyramid import testing
import sure

from domidooweb.models import *
import domidooweb.views
from domidooweb.admin_views import *
from mock import Mock


dburl = 'sqlite://'
class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        
        DBSession.remove()

        engine = create_engine(dburl)
        
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        self.request = testing.DummyRequest()


    def tearDown(self):
        DBSession.remove()
        testing.tearDown()


    def test_that_about_page_can_be_reached(self):
        info = domidooweb.views.about(self.request)

        assert True

    def test_home_displays_the_list_of_all_places(self):
        place_repository = Mock(PlaceRepository)
        domidooweb.views.place_repository = place_repository
        place_repository.get_all.return_value = {'place1', 'place2', 'place3'}

        response = domidooweb.views.home(self.request)
        places = response['places']

        len(places).should.be.equal(3)

        





