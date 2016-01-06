from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from CustomRequestLayer import CustomRequestLayer

class CustomCoAP(CoAP):
    def __init__(self, server_address, multicast=False, starting_mid=None):
        super(CustomCoAP, self).__init__(server_address, multicast, starting_mid)
        self._requestLayer = CustomRequestLayer(self)

    def add_resource(self, path, resource):
        """
        Helper function to add resources to the resource directory during server initialization.

        :param path: the path for the new created resource
        :type resource: Resource
        :param resource: the resource to be added
        """

        assert isinstance(resource, Resource)
        path = path.strip("/")
        paths = path.split("/")
        actual_path = ""
        i = 0
        for p in paths:
            i += 1

            if p == "*":
                continue

            actual_path += "/" + p
            try:
                res = self.root[actual_path]
            except KeyError:
                res = None
            if res is None:
                if len(paths) != i:
                    return False
                resource.path = actual_path
                self.root[actual_path] = resource
        return True