import zeep


from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport

session = Session()
session.auth = HTTPBasicAuth('admin','admin')
client = Client('http://192.168.1.51/services.wsdl',
    transport=Transport(session=session))

for service in client.wsdl.services.values():
    print ("service:", service.name)
    for port in service.ports.values():
        operations = sorted(
            port.binding._operations.values(),
            key=operator.attrgetter('name'))

        for operation in operations:
            print ("method :", operation.name)
            print ("  input :", operation.input.signature())
            print ("  output:", operation.output.signature())
            print()
    print()




#print (client.wsdl.services.values())
#print(client.service.GetSceneProfiles())