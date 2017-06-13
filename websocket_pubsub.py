from twisted.internet import protocol, reactor
from txws import WebSocketFactory
import json

clients = []
subs = {}

class EchoServer(protocol.Protocol) :

    def connectionMade(self) :
        print "Koneksi dibuat"
        clients.append(self)

    def connectionLost(self) :
        print "Koneksi putus"
        clients.remove(self)

    def dataReceived(self, data) :
        dict_pesan = json.loads(data)
        tipe = dict_pesan["tipe"]
        if tipe == "SUB" :
            topik = dict_pesan["topik"]
            if topik in subs :
                subs[topik].append(self)
            else :
                subs[topik] = []
                subs[topik].append(self)
            for cl in clients :
                cl.transport.write("OK")
        if tipe == "PUB" :
            pesan = dict_pesan["pesan"][0]
            topik = dict_pesan["topik"][0]
            if topik in subs :
                list_subs = subs[topik]
                for cl in list_subs :
                    cl.transport.write(pesan)
            else :
                for cl in clients :
                    cl.transport.write("ERROR")
            for cl in clients :
                cl.transport.write("OK")
class EchoFactory(protocol.Factory):

    def buildProtocol(self, address) :
        return EchoServer()

factory = EchoFactory()
reactor.listenTCP(8002, WebSocketFactory(factory))
reactor.run()
