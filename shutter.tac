from twisted.web.server import Site
from twisted.web.static import File
from twisted.application import service, internet

from twisted.python.log import ILogObserver, FileLogObserver
from twisted.python.logfile import DailyLogFile

from shutter.protocol import RemoteShutterFactory, ShutterJSONRPCProtocol

application = service.Application("shutter")

logfile = DailyLogFile("shutter.log", "./log")
application.setComponent(ILogObserver, FileLogObserver(logfile).emit)

s = service.MultiService()

static = internet.TCPServer(8000, Site(File("./static")))
static.setServiceParent(s)

shutter= internet.TCPServer(8001, RemoteShutterFactory(ShutterJSONRPCProtocol()))
shutter.setServiceParent(s)

s.setServiceParent(application)