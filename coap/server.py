from coapthon.server.coap import CoAP
from exampleresources import BasicResource

class CoAPServer(CoAP):
    def __init__(self, host, port):
        CoAP.__init__(self, (host, port))
        self.add_resource("testing/", BasicResource())

def main():
    server = CoAPServer("0.0.0.0", 5683)
    try:
        print("Waiting for requests...")
        server.listen()
    except KeyboardInterrupt:
        print("Server shutdown")
        server.close()
        print("Exiting...")

if __name__ == "__main__":
    main()
