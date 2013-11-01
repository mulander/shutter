from twisted.trial import unittest
from twisted.internet import reactor

from txjsonrpc.web.jsonrpc import Proxy
from txjsonrpc import jsonrpclib

from shutter.protocol import RemoteShutterFactory, ShutterJSONRPCProtocol

class ShutterJSONRPCTestCase(unittest.TestCase):
    def setUp(self):
        self.port = reactor.listenTCP(8001, RemoteShutterFactory(ShutterJSONRPCProtocol()))
        self.client = Proxy('http://127.0.0.1:8001', version=jsonrpclib.VERSION_2)
    def tearDown(self):
        self.port.stopListening()
    def test_snapshots_empty(self):
    	def _result(value):
    		self.assertTrue(value['error'] is None)
    		self.assertFalse(value['result'] is None)
    		self.assertEqual(value['result'], [])
        return self.client.callRemote("snapshots", "http://programistamag.pl").addCallback(_result)