from twisted.web import server
from txjsonrpc.web import jsonrpc

class ShutterJSONRPCProtocol(jsonrpc.JSONRPC):
    def __init__(self):
        pass
    def jsonrpc_snapshots(self, url):
        return []

class RemoteShutterFactory(server.Site):
    def startFactory(self):
        pass