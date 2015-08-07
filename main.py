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
import logging
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
    status=ndb.StringProperty()



class Question(ndb.Model):
    act_question= ndb.StringProperty(required=True)
    q_id= ndb.IntegerProperty()
    category= ndb.StringProperty(required= True)
    level = ndb.IntegerProperty(required = True)
    point_level = ndb.IntegerProperty()
    answer= ndb.StringProperty()
    explain = ndb. StringProperty()


class FrontPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/frontpage.html')
        self.response.out.write(template.render())
        self.response.write(question_qry.answer)

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
            query_results = User.query(User.useridentification == users.get_current_user().user_id()).fetch()

            if query_results:
                template = jinja_environment.get_template('templates/frontpage.html')
                self.response.out.write(template.render())

            else:
                template = jinja_environment.get_template('templates/settings.html')
                self.response.out.write(template.render())
        else:
            self.redirect(users.create_login_url(self.request.url))


    def post(self):
        game_template = jinja_environment.game_template('templates/startGame.html')


class SettingsHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('templates/frontpage.html')
        self.response.out.write(template.render())

    def post(self):
        x=self.request.get('name')
        user_api_user=users.get_current_user()
        user_from_model=User(useridentification=user_api_user.user_id(), name=x, level=1, points=0)
        user_from_model.put()

        query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()

        if query_results:
            user_api_user=users.get_current_user()
            user_name = query_results[0].name

        else:
            user_name=x

        getname={'user_name':user_name}

        template = jinja_environment.get_template('templates/frontpage.html')
        self.response.out.write(template.render(getname))





class GameHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/game.html')
        self.response.out.write(template.render())



class AddQHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/addq.html')
        self.response.out.write(template.render())

    def post(self):
        x=self.request.get('Question')
        y=int(self.request.get('Level'))
        a=self.request.get('Answer')
        b=self.request.get('Category')
        c=self.request.get('Explanation')

        question=Question(act_question=x, level=y, answer=a.lower(), category=b, explain = c, q_id=random.randint(1,1000), point_level=100)
        question.put()

        getq={'user_question':x, 'user_level':y, 'user_answer':a, 'user_category':b}

        template = jinja_environment.get_template('templates/resultsq.html')
        self.response.out.write(template.render(getq))


class  StatsHandler(webapp2.RequestHandler):
    def get(self):

        user_api_user=users.get_current_user()
        query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()

        if  query_results[0].points <=500:
            query_results[0].level =1
            query_results[0].put()
            query_results[0].status = str("YOU SHOULD PROBABLY GIVE UP :)")


        elif 500 < query_results[0].points <=1000:
             query_results[0].level =2
             query_results[0].status = str("LAME")
             query_results[0].put()
        elif 1000 < query_results[0].points <=2000:
            query_results[0].level =3
            query_results[0].status = str("NOVICE")
            query_results[0].put()


        elif 2000 < query_results[0].points <=6000:
            query_results[0].level =4
            query_results[0].status = str("SOMEWHERE BETWEEN A NOVICE AND AN IMPROVING NOVICE")
            query_results[0].put()
        elif 6000 < query_results[0].points <=15000:
            query_results[0].level = 5
            query_results[0].status = str("IMPROVING NOVICE")
            query_results[0].put()

        elif 15000 < query_results[0].points <=25000:
            query_results[0].level = 6
            query_results[0].status = str("SILVER")
            query_results[0].put()

        elif 25000 < query_results[0].points <= 40000:
            query_results[0].level = 7
            query_results[0].status = str("GOLD")
            query_results[0].put()

        elif 40000 < query_results[0].points <= 50000:
            query_results[0].level = 8
            query_results[0].status = str("PLATINUM")
            query_results[0].put()
        else:
            query_results[0].level = 9
            query_results[0].status = str("RULER OF THE WORLD")
            query_results[0].put()




        template_vars = {'userlevel': query_results[0].level, 'username' : query_results[0].name, 'userpoints' : query_results[0].points,'userstatus':query_results[0].status
            }





        template = jinja_environment.get_template('templates/stats.html')
        self.response.out.write(template.render(template_vars))


questionindex=[]
class ScienceHandler(webapp2.RequestHandler):

    def get(self):

        questions=Question.query().filter(Question.category==str('Science')).fetch()
        randnum = random.randint(0,len(questions)-1)
        logging.info("YOU HAVE THIS MANY QUESTIONS" + str(len(questions)))

        if len(questionindex) == len(questions):
                template = jinja_environment.get_template('templates/done.html')
                self.response.out.write(template.render())




        while randnum in questionindex:
            randnum =random.randint(0,len(questions)-1)


        if randnum not in questionindex:
            questionindex.append(randnum)

            userq = questions[randnum].act_question
            questionid=questions[randnum].q_id

            user_api_user=users.get_current_user()
            query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()
            template_vars = {
            'user_question': userq,
            'question_id' : questionid, 'userlevel': query_results[0].level, 'username' : query_results[0].name, 'userpoints' : query_results[0].points, 'randnum' : randnum
                }

            template = jinja_environment.get_template('templates/science.html')
            self.response.out.write(template.render(template_vars))








    def post (self):

        user_answers = self.request.get('answerofuser')
        questionid = self.request.get('question_id')


        question=Question.query().filter(Question.q_id==int(questionid)).fetch()
        answer = question[0].answer
        explain = question[0].explain


        user_api_user=users.get_current_user()
        query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()
        points = query_results[0].points




        if user_answers.lower().strip() == answer:
            self.response.write('Correct')
            query_results[0].points += 100
            query_results[0].put()



        elif user_answers.lower().strip()!= answer:
            self.response.write('Wrong, it was ' + answer + '. ' + explain)
            if query_results[0].points == 0:
                query_results[0].put()
            else:
                query_results[0].points -= 50
                query_results[0].put()

        else:
            self.response.write('Error! You need to type something in')




questionindex=[]
class SocialStudiesHandler(webapp2.RequestHandler):
    def get(self):
        questions=Question.query().filter(Question.category==str('Social Studies')).fetch()
        randnum = random.randint(0,len(questions)-1)
        logging.info("YOU HAVE THIS MANY QUESTIONS" + str(len(questions)))
        if len(questionindex) == len(questions):
                template = jinja_environment.get_template('templates/done.html')
                self.response.out.write(template.render())




        while randnum in questionindex:
            randnum =random.randint(0,len(questions)-1)


        if randnum not in questionindex:
            questionindex.append(randnum)

            userq = questions[randnum].act_question
            questionid=questions[randnum].q_id

            user_api_user=users.get_current_user()
            query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()
            template_vars = {
            'user_question': userq,
            'question_id' : questionid, 'userlevel': query_results[0].level, 'username' : query_results[0].name, 'userpoints' : query_results[0].points, 'randnum' : randnum
                }

            template = jinja_environment.get_template('templates/science.html')
            self.response.out.write(template.render(template_vars))





    def post (self):

        user_answers = self.request.get('answerofuser')
        questionid = self.request.get('question_id')


        question=Question.query().filter(Question.q_id==int(questionid)).fetch()
        answer = question[0].answer
        explain = question[0].explain


        user_api_user=users.get_current_user()
        query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()
        points = query_results[0].points




        if user_answers.lower().strip() == answer:
            self.response.write('Correct')
            query_results[0].points += 100
            query_results[0].put()




        elif user_answers.lower().strip()!= answer:
            self.response.write('Wrong, it was ' + answer + '. ' + explain)
            if query_results[0].points == 0:
                query_results[0].put()
            else:
                query_results[0].points -= 50
                query_results[0].put()

        else:
            self.response.write('Error! You need to type something in')


questionindex=[]

class MathHandler(webapp2.RequestHandler):
    def get(self):
        questions=Question.query().filter(Question.category==str('Math')).fetch()
        randnum = random.randint(0,len(questions)-1)
        logging.info("YOU HAVE THIS MANY QUESTIONS" + str(len(questions)))
        if len(questionindex) == len(questions):
                template = jinja_environment.get_template('templates/done.html')
                self.response.out.write(template.render())




        while randnum in questionindex:
            randnum =random.randint(0,len(questions)-1)


        if randnum not in questionindex:
            questionindex.append(randnum)

            userq = questions[randnum].act_question
            questionid=questions[randnum].q_id

            user_api_user=users.get_current_user()
            query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()
            template_vars = {
            'user_question': userq,
            'question_id' : questionid, 'userlevel': query_results[0].level, 'username' : query_results[0].name, 'userpoints' : query_results[0].points, 'randnum' : randnum
                }

            template = jinja_environment.get_template('templates/science.html')
            self.response.out.write(template.render(template_vars))








    def post (self):

        user_answers = self.request.get('answerofuser')
        questionid = self.request.get('question_id')


        question=Question.query().filter(Question.q_id==int(questionid)).fetch()
        answer = question[0].answer
        explain = question[0].explain


        user_api_user=users.get_current_user()
        query_results = User.query(User.useridentification == user_api_user.user_id()).fetch()
        points = query_results[0].points




        if user_answers.lower().strip() == answer:
            self.response.write('Correct')
            query_results[0].points += 100
            query_results[0].put()




        elif user_answers.lower().strip()!= answer:
            self.response.write('Wrong, it was ' + answer + '. ' + explain)
            if query_results[0].points == 0:
                query_results[0].put()
            else:
                query_results[0].points -= 50
                query_results[0].put()

        else:
            self.response.write('Error! You need to type something in')

class AboutHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/about.html')
        self.response.out.write(template.render())









app = webapp2.WSGIApplication([
    ('/', FrontPage),
    ('/about',AboutHandler),
    ('/frontpage', SettingsHandler),
    ('/startGame', GameHandler),
    ('/addQ', AddQHandler),
    ('/stats', StatsHandler),
    ('/science', ScienceHandler),
    ('/ss', SocialStudiesHandler),
    ('/math', MathHandler),
    ('/settings', SettingsHandler)
], debug=True)
