import logging
import requests
import base64

_LOGGER = logging.getLogger(__name__)

class PowerView:
    """Class for interacting with the Powerview API."""

    REQUEST_TIMEOUT = 3.0

    def __init__(self, host):
        """Initialize the PowerView Hub."""
        if host is not None:
            self.host = 'http://' + host

    def make_request(self, method, request, data=None):
        try:
            if method is "get":
                r = requests.get(self.host + request)

                return r.json()

            elif method is "put":
                r = requests.put(self.host + request, json = data)

                return True

            else:
                return False

        except:
            return False

    def get_shades(self):
        """List all shades."""
        request = self.make_request("get","/api/shades")

        if request != False:

            request = request['shadeData']
            shades = []

            for x in request:

                shade = Shade(x['id'], base64.b64decode(x['name']).decode('UTF-8'), round((x['positions']['position1'] / 65535) * 100))
                shades.append(shade)

            return shades

        else:
            return False

    def get_status(self, shade):
        """Update status of shade."""
        shade.position = round((self.make_request("get","/api/shades/" + str(shade.id) + "?refresh=true")['shade']['positions']['position1'] / 65535) * 100)

        return shade.position

    def close_shade(self, shade):
        """Close a shade."""
        self.make_request("put","/api/shades/" + str(shade.id), {"shade": {"motion": "down"}})

        shade.position = 0

        return 0

    def open_shade(self, shade):
        """Open a shade."""
        self.make_request("put","/api/shades/" + str(shade.id), {"shade": {"motion": "up"}})

        shade.position = 100

        return 100

    def stop_shade(self, shade):
        """Stop a shade."""
        self.make_request("put","/api/shades/" + str(shade.id), {"shade": {"motion": "stop"}})

        return self.get_status(shade)

    def set_shade_position(self, shade, position: int):
        """Set a shade to a specific position."""
        if 0 <= position <= 100: 
            position = round(position * 65535 / 100)
            self.make_request("put","/api/shades/" + str(shade.id), { "shade": { "positions": { "posKind1": 1, "position1": position } } })

            shade.position = round(position / 65535 * 100)

            return shade.position
            
        else:

            return False

class Shade:
    """Class to represent a PowerView shade"""
    def __init__(self,
                 id: int,
                 name: str,
                 position: int):
        self.id = id
        self.name = name
        self.position = position