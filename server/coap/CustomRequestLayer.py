from coapthon.layers.requestlayer import RequestLayer
from coapthon.messages.response import Response
from coapthon import defines

class CustomRequestLayer(RequestLayer):
    def _find_resource(self, path):
        path = path.strip("/")
        paths = path.split("/")
        actual_path = ""

        for p in paths:
            actual_path += "/" + p

            try:
                resource = self._server.root[actual_path]
                resource.index = None
            except KeyError:
                # Remove dynamic parameter in URI
                actual_path = "/".join(actual_path.split("/")[0:-1])

                # Save index such that it can be used within the resource
                resource.index = p

        resource.path = actual_path

        return resource

    def _handle_request(self, transaction, method):
        """
        :type transaction: Transaction
        :param transaction:
        :rtype : Transaction
        """
        path = str("/" + transaction.request.uri_path)
        transaction.response = Response()
        transaction.response.destination = transaction.request.source
        transaction.response.token = transaction.request.token
        if path == defines.DISCOVERY_URL:
            transaction = self._server.resourceLayer.discover(transaction)
        else:
            resource = self._find_resource(path) # CUSTOM

            if resource is None or path == '/':
                # Not Found
                transaction.response.code = defines.Codes.NOT_FOUND.number
            else:
                method = getattr(resource, method, None)
                transaction.resource = method(request=transaction.request)

                if resource.etag in transaction.request.etag:
                    transaction.response.code = defines.Codes.VALID.number
                else:
                    transaction.response.code = defines.Codes.CONTENT.number

                try:
                    transaction.response.payload = resource.payload
                except:
                    pass

        return transaction


    def _handle_get(self, transaction):
        """
        :type transaction: Transaction
        :param transaction:
        :rtype : Transaction
        """
        self._handle_request(transaction, "render_GET")

    def _handle_put(self, transaction):
        """

        :type transaction: Transaction
        :param transaction:
        :rtype : Transaction
        """
        self._handle_request(transaction, "render_PUT")

    def _handle_post(self, transaction):
        """
        :type transaction: Transaction
        :param transaction:
        :rtype : Transaction
        """
        self._handle_request(transaction, "render_POST")

    def _handle_delete(self, transaction):
        """

        :type transaction: Transaction
        :param transaction:
        :rtype : Transaction
        """
        self._handle_request(transaction, "render_DELETE")