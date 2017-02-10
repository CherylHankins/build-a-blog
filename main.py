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
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    #to retain valid user input 1 of 3
    #def render_newpost(self, title = "", blog = "", error = "")
        #self.render("newpost.html", title = title, blog = blog, error = error)

    def get(self):
        self.render("newpost.html")
        #to retain valid user input 2 of 3
        #self.render_newpost()

    def post(self):
        subject = self.request.get("title")
        blog = self.request.get("blog")

        if subject and blog:
            c = Blog(title = title, blog = blog)
            c.put()

            self.redirect("/")

        else:
            error = "Both Title and Blog are required."
            self.render("newpost.html", error = error)
            #to retain valid user input 3 of 3
            #self.render_newpost(title, blog, error)


class Blog(db.Model):
    title = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
