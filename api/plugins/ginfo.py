
"""
  Integration into the Ginfo Map via Firebase REST API
"""
from django.http import HttpResponse, HttpRequest
import requests
import math
import json
from api.models import Character
from datetime import datetime


class GinfoPlugin(object):
    """
      GinfoPlugin provides methods to post a position to the ginfo firebase database
    """
    API_URL = 'https://ginfo-dev.firebaseio.com'
    GAME = 'conanexiles'
    MAP = 'conanexiles_desert'

    def __init__(self):
        pass

    def url_post(self, group):
        """
          Returns the url for posting a marker for the given group

          @param group: UID of the ginfo group for which the marker should be created
        """
        return self.API_URL + '/games/' + self.GAME + '/groups/' + \
            group + '/maps/' + self.MAP + '/markers.json'

    def url_patch(self, group, marker):
        """
          Returns the url for patching an existing marker for the given group

          @param group: UID of the ginfo group for which the marker was created
          @param marker: UID of the existing ginfo marker that should be updated
        """
        return self.API_URL + '/games/' + self.GAME + '/groups/' + group + \
            '/maps/' + self.MAP + '/markers/' + marker + '/.json'

    def convert_position(self, x, y):
        """
          Converts the given position from x/y to lat/lng coordinates
          @param x, y: x/y Position of in the game
          @return: lat/lng for the same position on the ginfo map
        """
        # TODO: Apply correct linear transformation
        return SphericalMercator.unproject(x, y)

    DEFAULT_MARKER_COLOR = "#1D8BF1"
    DEFAULT_MARKER_TYPE = 1
    DEFAULT_MARKER_SKIN = 0

    def update_position(self, character, group):
        """
          Posts the position of this character to Firebase
        """

        (lat, lng) = self.convert_position(
            float(character.x), float(character.y))
        data = {
            "name": character.name,
            "updatedAt": {
                ".sv": "timestamp"
            },
            "color": self.DEFAULT_MARKER_COLOR,
            "creatorId": "TODO",
            "createdAt": {
                ".sv": "timestamp"
            },
            "position": {
                "lat": lat,
                "lng": lng
            },
            "type": self.DEFAULT_MARKER_TYPE,
            "skin": self.DEFAULT_MARKER_SKIN
        }

        url = self.url_patch(group, '-KnjCenU4ja7Ms7LF1mA')
        print(url)
        requests.patch(
            url=url,
            json=data
        )


class SphericalMercator(object):
    R = 6378137
    MAX_LATITUDE = 85.0511287798

    @staticmethod
    def project(lat, lng):
        """
          Converts a lat/lng coordiante to a x/y point
        """
        d = math.pi / 180.0
        lat = max(
            min(SphericalMercator.MAX_LATITUDE, lat), -
            SphericalMercator.MAX_LATITUDE
        )
        sin = math.sin(lat * d)
        return (
            SphericalMercator.R * lng * d,
            SphericalMercator.R * math.log((1 + sin) / (1 - sin)) / 2.0
        )

    @staticmethod
    def unproject(x, y):
        """
          Converts a x/y point to a lat/lng coordinate
        """
        d = 180.0 / math.pi
        return (
            (2.0 * math.atan(math.exp(y / SphericalMercator.R)) - (math.pi / 2.0)) * d,
            x * d / SphericalMercator.R
        )
