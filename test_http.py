"""Exercise the real HTTP boundary without needing Ollama or the compiler."""
import http.client
import json
import threading
import unittest
from unittest.mock import patch
import server

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        class QuietHandler(server.Handler):
            def log_message(self, *args): pass
        cls.http = server.ThreadingHTTPServer(('127.0.0.1', 0), QuietHandler)
        cls.worker = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.worker.start()

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.worker.join(5)

    def request(self, path, data=None, headers=None, method='POST'):
        connection = http.client.HTTPConnection('127.0.0.1', self.http.server_port, timeout=5)
        try:
            connection.request(method, path, json.dumps(data), headers or {})
            response = connection.getresponse()
            return response.status, json.loads(response.read())
        finally:
            connection.close()

    def test_invalid_requests_return_json_and_server_recovers(self):
        for data in (None, [], {'mode':'invented'}, {'plan':[]}):
            with self.subTest(data=data):
                status, body = self.request('/api/generate', data)
                self.assertEqual(status, 422)
                self.assertIn('error', body)
        status, body = self.request('/api/status', method='GET')
        self.assertEqual(status, 200)
        self.assertFalse(body['runtimeValidated'])

    def test_remote_origin_rejected_before_model_call(self):
        with patch('server.generate') as generate:
            status, _ = self.request('/api/generate', {}, {'Origin':'https://example.com'})
            self.assertEqual(status, 403)
            generate.assert_not_called()

    def test_second_generation_does_not_queue_another_model_request(self):
        server.AI_LOCK.acquire()
        try:
            with patch('server.generate') as generate:
                status, _ = self.request('/api/generate', {})
                self.assertEqual(status, 409)
                generate.assert_not_called()
        finally:
            server.AI_LOCK.release()

    def test_provider_failure_releases_generation_lock(self):
        with patch('server.generate', side_effect=OSError('provider unavailable')):
            self.assertEqual(self.request('/api/generate', {'prompt':'test','model':'test'})[0], 503)
        with patch('server.generate', return_value={'schema':1}):
            status, body = self.request('/api/generate', {'prompt':'test','model':'test'})
            self.assertEqual(status, 200)
            self.assertEqual(body['plan'], {'schema':1})

    def test_invalid_build_does_not_require_compiler_and_releases_lock(self):
        with patch.dict('os.environ', {'NEWSERV_PATH':''}):
            for value in (None, [], {}, {'plan':[]}):
                self.assertEqual(self.request('/api/compile', value)[0], 422)
            self.assertEqual(self.request('/api/compile', {'plan':{}})[0], 503)

    def test_source_files_are_not_served(self):
        self.assertEqual(self.request('/server.py', method='GET')[0], 404)

if __name__ == '__main__':
    unittest.main()
