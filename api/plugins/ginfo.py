
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
    GINFO_USER_UID = 'DaLvSI2e2LPirXork6kMp4NsQ7O2'

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

    TRANSFORMATION_KX = 81.48592277749488
    TRANSFORMATION_KY = -81.9610812970396
    TRANSFORMATION_DX = 6275917.802625263
    TRANSFORMATION_DY = 11160459.85122114

    def linear_transform(self, x, y):
        """
            Applies a linear transform to the point x/y
        """
        return (
            x * self.TRANSFORMATION_KX + self.TRANSFORMATION_DX,
            y * self.TRANSFORMATION_KY + self.TRANSFORMATION_DY
        )

    def convert_position(self, x, y):
        """
          Converts the given position from x/y to lat/lng coordinates
          @param x, y: x/y Position of in the game
          @return: lat/lng for the same position on the ginfo map
        """
        (x, y) = self.linear_transform(x, y)
        return SphericalMercator.unproject(x, y)

    DEFAULT_MARKER_COLOR = "#1D8BF1"
    DEFAULT_MARKER_TYPE = 1
    DEFAULT_MARKER_SKIN = 0

    def update_position(self, character, group, access_token, marker_uid = None):
        """
          Posts the position of this character to Firebase
          @param character:
                    The character for which the position should be updated
          @param group:
                    The group in which the marker should be postet
          @param marker_uid:
                    Firebase-UID of an existing marker to update (if available).
                    If not available, a new marker will be created
        """
        (lat, lng) = self.convert_position(
            float(character.x), float(character.y))
        data = {
            "name": character.name,
            "updatedAt": {
                # This tells firebase to use its internal timestamp
                ".sv": "timestamp"
            },
            "createdAt": {
                # This tells firebase to use its internal timestamp
                ".sv": "timestamp"
            },
            "color": self.DEFAULT_MARKER_COLOR,
            "creatorId": self.GINFO_USER_UID,
            "position": {
                "lat": lat,
                "lng": lng
            },
            "type": self.DEFAULT_MARKER_TYPE,
            "skin": self.DEFAULT_MARKER_SKIN,
            "accessToken": access_token
        }

        if (marker_uid == None or marker_uid == ""):
            # No marker uid available -> create a new marker via POST
            r = requests.post(
                url = self.url_post(group),
                json=data
            )
            # Firebase responds with the UID of the created marker
            json_data = json.loads(r.text)
            if "error" in json_data:
                # TODO: Use proper logger
                print "Error from Ginfo Firebase: " + json_data["error"]
            else:
                marker_uid = json_data["name"]
        else:
            # UID of existing marker availabe -> update existing marker via PATCH
            r = requests.patch(
                url=self.url_patch(group, marker_uid),
                json=data
            )
            json_data = json.loads(r.text)
            if "error" in json_data:
                # TODO: Use proper logger
                print "Error from Ginfo Firebase: " + json_data["error"]
        return marker_uid


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
