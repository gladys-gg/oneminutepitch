import unittest
from app.models import Comment,User
from flask_login import current_user
from app import db

class CommentTest(unittest.TestCase):

        def setUp(self):
            self.user_gladys = User(username = 'gladys',
                                    password = '123',
                                    email = 'hh@dd.c')
            self.new_comment = Comment(id=12345,
                                        post_comment="hello",
                                        category_id='pick up line',
                                        pitches="this is my first pitch",
                                        user_id = self.user_gladys)

    def tearDown(self):
        Comment.query.delete()
        User.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment,Comment))


    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.id,1)
        self.assertEquals(self.new_comment.post_comment,"hello")
        self.assertEquals(self.new_comment.category_id,'pick up line')
        self.assertEquals(self.new_comment.pitch, 'this is my first pitch')
        self.assertEquals(self.new_comment.user,self.user_gladys)


    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)


    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_comments(1)
        self.assertTrue(len(got_comments) == 1)