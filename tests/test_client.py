# -*-coding: utf-8 -*-
import base64
import json
from async_scrapy_api.client import Client
from tornado.testing import AsyncHTTPTestCase, get_async_test_timeout
from tornado.web import RequestHandler
from tornado.web import Application

SCRAPYD_RESPONSE_OK = {
    'status': 'ok',
    'example': 'Test',
    'another-example': 'Another Test',
}

SCRAPYD_RESPONSE_ERROR = {
    'status': 'error',
    'message': 'Test Error'
}


class BaseHandler(RequestHandler):
    def auth(self, user="user", password="123"):
        authorization = self.request.headers.get("Authorization", '').replace('Basic ', '')
        if not authorization:
            return False
        _user, _password = base64.b64decode(authorization).decode().split(":")
        if user == _user and password == _password:
            return True
        return False


class TestScrapydServer(BaseHandler):
    def get(self, *args, **kwargs):
        if self.get_argument('ok', None):
            self.write(SCRAPYD_RESPONSE_OK)
        else:
            self.write(SCRAPYD_RESPONSE_ERROR)
            self.set_status(status_code=404)


class TestScrapydUserServer(BaseHandler):
    def post(self, *args, **kwargs):
        if not self.auth():
            self.write(SCRAPYD_RESPONSE_ERROR)
            self.set_status(status_code=404)
            return
        if self.get_argument('ok', None) and self.auth():
            self.write(SCRAPYD_RESPONSE_OK)
        else:
            self.write(SCRAPYD_RESPONSE_ERROR)
            self.set_status(status_code=404)


class TestClient(AsyncHTTPTestCase):
    def get_http_client(self, **kwargs):
        return Client(**kwargs)

    def tearDown(self):
        self.http_server.stop()
        self.io_loop.run_sync(self.http_server.close_all_connections,
                              timeout=get_async_test_timeout())
        super(AsyncHTTPTestCase, self).tearDown()

    def get_app(self):
        return Application([
            ('/', TestScrapydServer),
            ('/auth', TestScrapydUserServer),
        ])

    def test_get_no_user_response(self):
        self.http_client.get(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertAlmostEqual(json.loads(response.body.decode()), SCRAPYD_RESPONSE_ERROR)
        self.assertAlmostEqual(response.code, 404)

        self.http_client.get(self.get_url('/'), self.stop, params={"ok": 1})
        response = self.wait()
        self.assertAlmostEqual(json.loads(response.body.decode()), SCRAPYD_RESPONSE_OK)
        self.assertAlmostEqual(response.code, 200)

    def test_get_user_response(self):
        self.get_auth_client().post(url=self.get_url('/auth'), callback=self.stop, data={"ok": 1})
        response = self.wait()
        self.assertAlmostEqual(json.loads(response.body.decode()), SCRAPYD_RESPONSE_OK)
        self.assertAlmostEqual(response.code, 200)

        self.get_auth_client().post(url=self.get_url('/auth'), callback=self.stop)
        response = self.wait()
        self.assertAlmostEqual(json.loads(response.body.decode()), SCRAPYD_RESPONSE_ERROR)
        self.assertAlmostEqual(response.code, 404)

    def get_auth_client(self):
        return self.get_http_client(**{"username": "user", "password": "123"})
