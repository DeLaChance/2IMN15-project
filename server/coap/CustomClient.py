from coapthon.client.helperclient import HelperClient
from coapthon.messages.request import Request
from coapthon import defines
import threading

class CustomClient(HelperClient):
    def __init__(self, server):
        super(CustomClient, self).__init__(server)

    def get(self, path, payload, callback=None):  # pragma: no cover
        request = Request()
        request.destination = self.server
        request.code = defines.Codes.GET.number
        request.uri_path = path
        request.payload = payload
        if callback is not None:
            thread = threading.Thread(target=self._thread_body, args=(request, callback))
            thread.start()
        else:
            self.protocol.send_message(request)
            response = self.queue.get(block=True)
            return response