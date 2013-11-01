from twisted.enterprise import adbapi
from twisted.web import server
from txjsonrpc.web import jsonrpc

from shutter import config
from shutter.service import Shutter

class ShutterJSONRPCProtocol(jsonrpc.JSONRPC):
    def __init__(self):
        self.service = Shutter()
    def jsonrpc_snapshots(self, url):
        return self.service.snapshots(url)

class RemoteShutterFactory(server.Site):
    def startFactory(self):
        dbpool = adbapi.ConnectionPool("psycopg2", config.DB_CONN, cp_reconnect=True)
        self.resource.service.setup_database(dbpool)