import tornado.ioloop
import tornado.web
import os
import requests

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        # self.write(os.environ['response_message'])
        headers = self.request.headers
        keys = list(headers.keys())
        for key in keys:
            if not key.startswith('X'):
                headers.pop(key)
        print(headers)
        r = requests.get(os.environ['target_service'], headers=headers)

        self.write(r.text)

class HealthHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("healthy")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/health", HealthHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()