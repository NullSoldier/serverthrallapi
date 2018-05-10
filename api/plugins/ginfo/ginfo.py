import math

import requests

from firebase_pushid import PushID
from ginfocharacter import GinfoCharacter


class GinfoPlugin(object):
    """
      GinfoPlugin provides methods to post a position to the ginfo firebase database
    """
    API_URL = 'https://ginfo-34baa.firebaseio.com'
    GAME = 'conanexiles'
    MAP = 'conanexiles_desert'
    SERVERTHRALL_USER_UID = 'y67Efa3kddSuhb26UoUapIJakMh1'

    def __init__(self):
        self.uid_generator = PushID()

    def marker_path(self, group, marker):
        """
            Returns the path to which a marker has to be posted in the firebase database

            @param group: UID of the ginfo group for which the marker should be posted
            @param marker: UID of the marker that should be posted
        """
        return 'games/%s/groups/%s/maps/%s/markers/%s' % (self.GAME, group, self.MAP, marker)

    def access_token_path(self, group, marker):
        """
            Returns the path to which the groups access token has to be posted in the firebase database

            @param group: UID of the ginfo group for which the marker should be posted
            @param marker: UID of the marker that should be posted
        """
        return 'groupAccessTokenVerifier/%s/%s' % (group, marker)

    TRANSFORMATION_KX = 50.60049940473328
    TRANSFORMATION_KY = -50.83608443474857
    TRANSFORMATION_DX = -2644742.2783469525
    TRANSFORMATION_DY = -2647361.614800021

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

    def update_position(self, character, group, access_token):
        """
          Posts the position of this character to Firebase
          @param character:
                    The character for which the position should be updated
          @param group:
                    The group in which the marker should be postet
          @param access_token:
                    Access token for the ginfo group
        """
        (lat, lng) = self.convert_position(
            float(character.x), float(character.y))

        ginfo_character, created = GinfoCharacter.objects.get_or_create(
            character_id=character.id)
        if created:
            ginfo_character.ginfo_marker_uid = self.uid_generator.next_id()
            ginfo_character.save()

        data = {
            self.marker_path(group, ginfo_character.ginfo_marker_uid): {
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
                "creatorId": self.SERVERTHRALL_USER_UID,
                "position": {
                    "lat": lat,
                    "lng": lng
                },
                "type": self.DEFAULT_MARKER_TYPE,
                "skin": self.DEFAULT_MARKER_SKIN,
            },
            self.access_token_path(group, ginfo_character.ginfo_marker_uid): access_token
        }

        response = requests.patch(
            url=self.API_URL + '/.json',
            json=data
        )
        try:
            json_data = response.json()
            if "error" in json_data:
                # TODO: Use proper logger
                print "Error from Ginfo Firebase: " + json_data["error"]
        except:
            pass


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
