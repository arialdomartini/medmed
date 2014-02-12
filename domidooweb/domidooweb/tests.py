import unittest
import transaction
import os
from pyramid import testing

from .models import DBSession

dburl = 'sqlite://'
class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        
        DBSession.remove()

        engine = create_engine(dburl)
        from .models import (
            Base,
            Place,
            )
        
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = Place(name='one')
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_that_home_can_be_reached(self):
        from .views import home
        request = testing.DummyRequest()
        info = home(request)
        self.assertEqual(info['project'], 'domidooweb')

    def test_that_a_new_place_can_be_added(self):
        from .views import place_new
        from .models import Place
        request = testing.DummyRequest()
        import json
        json_data = {'name':'doh'}
        request.json_body = json_data
        result = place_new(request)

        actual = DBSession.query(Place).filter_by(name='doh').first()

        self.assertIsNotNone(actual)
