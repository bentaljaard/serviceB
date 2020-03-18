import tornado.ioloop
import tornado.web
import os
import requests
import json



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
        r = None
        error_message = None
        
        try:
            # r = requests.get("http://localhost:8080")
            r = requests.get(os.environ['TARGET_SERVICE'], headers=headers, verify=False , timeout=0.01)
            #r = requests.get("https://external-app2.app1.svc/customsearch/v1?key=INSERT_YOUR_API_KEY&cx=017576662512468239146:omuauf_lfve&q=lectures", headers=headers, verify=False)
        except (requests.exceptions.ConnectionError):
            print("Unable to connect")
            error_message = "Connection Error"

        response_message = dict()
        response_message["service"] = "b"
        
        target_service = dict()
        target_service["service"] = "c"
        if r is not None:
            print(r)
            target_service["payload"] = r.json()
            target_service["http_code"] = r.status_code
        else:
            target_service["payload"] = "null"
            target_service["http_code"] = "null"
            target_service["error_message"] = error_message

        

        response_message["target_service"] = target_service
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(response_message))

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
