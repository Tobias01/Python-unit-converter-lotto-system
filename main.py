#!/usr/bin/env python
import os
import jinja2
import webapp2

from random import randint


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class LottoHandler(BaseHandler):
    def get(self):
        numbers = []
        for i in range(6):
            n = randint(1, 45)
            numbers.append(n)
        return self.render_template("lotto.html", {'numbers': numbers})

class ShoutHandler(BaseHandler):
    def get(self):
        return self.render_template('shout-form.html')

class ShoutResultHandler(BaseHandler):
    def post(self):
        text = self.request.get('text')
        text = text.upper()
        return self.render_template('shout-result.html', {'text': text})



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/lotto', LottoHandler),
    webapp2.Route('/shout', ShoutHandler),
    webapp2.Route('/shout-result', ShoutResultHandler),
], debug=True)
