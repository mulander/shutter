from twisted.trial import unittest
from twisted.internet import reactor

from txjsonrpc.web.jsonrpc import Proxy
from txjsonrpc import jsonrpclib

from shutter.protocol import RemoteShutterFactory, ShutterJSONRPCProtocol
from shutter import config

import psycopg2

class ShutterJSONRPCTestCase(unittest.TestCase):
    def setUp(self):
        self.port = reactor.listenTCP(8001, RemoteShutterFactory(ShutterJSONRPCProtocol()))
        self.client = Proxy('http://127.0.0.1:8001', version=jsonrpclib.VERSION_2)

        self.conn = psycopg2.connect(config.DB_CONN)
        self.cur  = self.conn.cursor()
    def tearDown(self):
        self.port.stopListening()
        self.conn.close()
    def test_snapshots_empty(self):
        def _result(value):
            self.assertTrue(value['error'] is None)
            self.assertFalse(value['result'] is None)
            self.assertEqual(value['result'], [])
        return self.client.callRemote("snapshots", "http://programistamag.pl").addCallback(_result)
    def test_snapshots_fake_entries(self):
        def _result(value):
            # Cleanup the added entries
            self.cur.execute("DELETE FROM shutter.urls")
            self.conn.commit()
            # Check the return values
            self.assertEqual(value['result'], ["fake3.png", "fake2.png", "fake1.png"])
        # Add fake entries into the database
        url = "http://fake.test.com"
        self.cur.execute("""INSERT INTO shutter.urls(url)
                                 VALUES (%s) 
                              RETURNING id
        """, [url])
        url_id = self.cur.fetchone()[0]
        def _make_file(fakeFile):
            self.cur.execute("""INSERT INTO shutter.snapshots(url_id, file_path)
                                     VALUES (%s, %s)""", [url_id, fakeFile])
            self.conn.commit()
        _make_file("fake1.png")
        _make_file("fake2.png")
        _make_file("fake3.png")

        return self.client.callRemote("snapshots", "http://fake.test.com").addCallback(_result)