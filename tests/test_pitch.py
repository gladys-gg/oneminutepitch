import unittest
from app.models import Pitch,User
from flask_login import current_user
from app import db

class TestPitch(unittest.TestCase):

        def setUp(self):
            self.user_gladys = User(username = 'gladys',
                                    password = '123',
                                    email = 'hh@dd.c')
            self.new_pitch = Pitch(id=1,
                                        title='Pick up line',
                                        content="my first pick up line",
                                        category_id='pick up line',
                                        comments="hello",
                                        user_id = self.user_gladys)

    def tearDown(self):
        Pitch.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch,Pitch))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_pitch.id,1)
        self.assertEquals(self.new_pitch.title,'Pitch itself')
        self.assertEquals(self.new_pitch.content,"this is my first pick up line")
        self.assertEquals(self.new_pitch.category_id,'pick up line')
        self.assertEquals(self.new_pitch.comments, 'hello')
        self.assertEquals(self.new_pitch.user,self.user_gladys)


    def test_save_pitch(self):
        self.new_pitch.save_pitch()
        self.assertTrue(len(Pitch.query.all())>0)


    def test_get_pitch_by_id(self):

        self.new_pitch.save_pitch()
        got_pitches = Pitch.get_pitch(1)
        self.assertTrue(len(got_pitches) == 1)