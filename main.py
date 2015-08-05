#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import ndb
from google.appengine.api import users
import random
import json
import webapp2
import jinja2
import os

jinja_environment= jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class User(ndb.Model):
    name= ndb.StringProperty()
    level= ndb.IntegerProperty()
    points = ndb.IntegerProperty()
    email_address = ndb.StringProperty()
    useridentification=ndb.StringProperty()


class Question(ndb.Model):
    act_question= ndb.StringProperty(required=True)
    q_id= ndb.IntegerProperty()
    category= ndb.StringProperty(required= True)
    level = ndb.IntegerProperty(required = True)
    type_question= ndb.StringProperty()
    point_level = ndb.IntegerProperty()
    answer= ndb.StringProperty()

question1=Question(act_question= "How many moons does earth have?", category="Science", level= 1, answer="1")
question1.put()

question2=Question(act_question= "If the number of protons in an element is seven, how many electrons does it have", category="Science", level= 3, answer="seven")
question2.put()

question3=Question(act_question= "How many planets are there?", category="Science", level= 2, answer="Eight")
question3.put()

question4=Question(act_question= "How many moons does Saturn have?", category="Science", level= 4, answer="Sixty Two")
question4.put()

question5=Question(act_question= "What is the main element in Earth's atmosphere", category="Science", level= 2, answer="1")
question5.put()





class SettingsHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('templates/frontpage.html')
        self.response.out.write(template.render())

    def post(self):
        x=self.request.get('name')
        user1=User(name=x, level=1, points=0)
        user1.put()
        # level_html=User.query(user_id).fetch()


        getname={'user_name' : x}
        template = jinja_environment.get_template('templates/frontpage.html')
        self.response.out.write(template.render(getname))


class FrontPage(webapp2.RequestHandler):
    def get(self):

        user_api_user=users.get_current_user()
        if user_api_user:
            query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()

            if query_results:
                template = jinja_environment.get_template('templates/frontpage.html')
                self.response.out.write(template.render())

            else:
                user_from_model=User(useridentification=user_api_user.user_id())
                user_from_model.put()
                template = jinja_environment.get_template('templates/settings.html')
                self.response.out.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.url))


    def post(self):
        game_template = jinja_environment.game_template('templates/startGame.html')




class GameHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.out.write(template.render())



class AddQHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World')
        template = jinja_environment.get_template('templates/addq.html')
        self.response.out.write(template.render())
class  InstructionsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello World')
        template = jinja_environment.get_template('templates/instructions.html')
        self.response.out.write(template.render())

class ScienceHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/science.html')
        self.response.out.write(template.render())


class SocialStudiesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/ss.html')
        self.response.out.write(template.render())


class MathHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/math.html')
        self.response.out.write(template.render())













app = webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/frontpage', SettingsHandler),
    ('/startGame', GameHandler),
    ('/addQ', AddQHandler),
    ('/instructions', InstructionsHandler),
    ('/science', ScienceHandler),
    ('/ss', SocialStudiesHandler),
    ('/math', MathHandler),
    ('/settings', SettingsHandler)
], debug=True)
