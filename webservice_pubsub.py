from twisted.web import server, resource
from twisted.internet import defer, reactor
import websocket
import json

class Home(resource.Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return '<html><body>Hello This is Home</body></html>'

    def render_POST(self, request):
        topik = request.args["topik"]
        pesan = request.args["pesan"]
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:8002")
        dict_pesan = {
            "tipe" : "PUB",
            "topik" : topik,
            "pesan" : pesan
        }
        text_json = json.dumps(dict_pesan)
        ws.send(text_json)
        ret = ws.recv()
        print ret
        return "OK"


root = resource.Resource()
root.putChild("", Home())


factory = server.Site(root)
reactor.listenTCP(8001, factory)
reactor.run()
