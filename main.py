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
import webapp2
import jinja2
import os

jinja_environment= jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)

class User(ndb.Model):
    email = ndb.StringProperty(required= True)
    name= ndb.StringProperty(required= True)
    level= ndb.IntegerProperty(required = True)
    password= ndb.StringProperty(required =True)
    points = ndb.IntegerProperty()

user1= User(email="dt4@gmail.com", name="DT4", level=7, password="dt4cssi", points=342)
user1.put()
class Question(ndb.Model):
    act_question= ndb.StringProperty(required=True)
    category= ndb.StringProperty(required= True)
    level = ndb.IntegerProperty(required = True)
    type_question= ndb.StringProperty()
    point_level = ndb.IntegerProperty()
    answer= ndb.StringProperty()

question1=Question(act_question= "How many moons does earth have?", category="Science", level= 1, answer="1")
question2=Question(act_question= "If the number of protons in an element is seven, how many electrons does it have", category="Science", level= 4, answer="seven")
question3=Question(act_question= "How many planets are there?", category="Science", level= 2, answer="Eight")
question4=Question(act_question= "How many moons does Saturn have?", category="Science", level= 3, answer="Sixty Two")
question5=Question(act_question= "What is the main element in Earth's atmosphere", category="Science", level= 1, answer="1")
question5=


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/mainpage.html')
        self.response.out.write(template.render())
    def post(self):
        frontpage_template = jinja_environment.frontpage_template('templates/frontpage.html')

class FrontPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/frontpage.html')
        self.response.out.write(template.render())
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
        self.response.write(user1.name + " level" + str(user1.level))

class SocialStudiesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/ss.html')
        self.response.out.write(template.render())
        self.response.write(user1.name + " level" + str(user1.level))

class MathHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/math.html')
        self.response.out.write(template.render())
        self.response.write(user1.name + " level" + str(user1.level))









app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/frontPage', FrontPage),
    ('/startGame', GameHandler),
    ('/addQ', AddQHandler),
    ('/instructions', InstructionsHandler),
    ('/science', ScienceHandler),
    ('/ss', SocialStudiesHandler),
    ('/math', MathHandler)
], debug=True)
