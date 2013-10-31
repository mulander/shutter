from twisted.web.server import Site
from twisted.web.static import File
from twisted.application import service, internet

application = service.Application("shutter")

static = internet.TCPServer(8000, Site(File("./static")))
static.setServiceParent(application)