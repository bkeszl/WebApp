import webapp2
import jinja2
import os
from models import Message


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
        params = {"user_name": "Hank",
                  "input_text": None,
        }
        self.render_template("landing.html", params)

    def post(self):
        input_text = self.request.get("some_text")
        msg = Message(message_text = input_text)
        msg.put()
        params = {  "user_name": "Hank",
                    "input_text": self.request.get("some_text")
        }
        self.render_template("landing.html", params)

class ListHandler(BaseHandler):
    def get(self):
        message_list = ["adfiua", "dgfheuzrhgi", "egugwbvi", "132413254"]
        params = {"message_list": message_list}
        self.render_template("message_list.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/list', ListHandler),
], debug=True)