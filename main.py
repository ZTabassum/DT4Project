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

class Question(ndb.Model):
    act_question= ndb.StringProperty(required=True)
    category= ndb.StringProperty(required= True)
    level = ndb.IntegerProperty(required = True)
    type_question= ndb.StringProperty()
    point_level = ndb.IntegerProperty()
    answer= ndb.StringProperty()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        template = jinja_environment.get_template('templates/mainpage.html')
        self.response.out.write(template.render())
    def post(self):
        game_template = jinja_environment.game_template('templates/game.html')


class GameHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/startGame', GameHandler)
], debug=True)
