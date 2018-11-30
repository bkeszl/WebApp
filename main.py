import webapp2
import jinja2
import os
from models import Message
import datetime
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        params = {"user_name": "Gaylilla69",
                  "input_text": None,
        }
        self.render_template("landing.html", params)

    def post(self):
        input_text = self.request.get("some_text")
        msg = Message(message_text = input_text)
        msg.put()
        params = {  "user_name": "Gaylilla69",
                    "input_text": self.request.get("some_text")
        }
        self.render_template("landing.html", params)

class ListHandler(BaseHandler):
    def get(self):
        messages = Message.query().order(Message.created).fetch()
        params = {"message_list": messages}
        self.render_template("message_list.html", params)

class MessageDetailsHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {"message": message}
        self.render_template("message_details.html", params)

class MessageEditHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {"message": message}
        self.render_template("message_edit.html", params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.message_text = self.request.get("message_text")
        message.modified = datetime.datetime.now()
        message.put()
        self.redirect("/message/%s" % message_id)

class MessageDeleteHandler(BaseHandler):
    def get(self, message_id):
        message = Message.get_by_id(int(message_id))
        params = {"message": message}
        self.render_template("message_delet.html", params)

    def post(self, message_id):
        message = Message.get_by_id(int(message_id))
        message.visible = False
        message.put()
        self.redirect("/list")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/list', ListHandler),
    webapp2.Route('/message/<message_id:\d+>', MessageDetailsHandler),
    webapp2.Route('/message/<message_id:\d+>/edit', MessageEditHandler),
    webapp2.Route('/message/<message_id:\d+>/delete', MessageDeleteHandler),
], debug=True)