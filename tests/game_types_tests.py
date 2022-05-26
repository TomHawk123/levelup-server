from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from levelupapi.models import Gamer
from levelupapi.models.gameType import GameType
from levelupapi.views.game_types import GameTypeSerializer


class GameTypeTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers',
                'game_types', 'games', 'game_types']

    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_list_game_types(self):
        """Test list game_types"""
        url = '/gametypes'

        response = self.client.get(url)

        # Get all the game_types in the database
        # #and serialize them to get the expected output
        all_game_types = GameType.objects.all()
        expected = GameTypeSerializer(all_game_types, many=True)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # response.data is the actual response from the url HTTP request
        self.assertEqual(expected.data, response.data)

    def test_get_game_type(self):
        """Get GameType Test"""
        # Grab a game_type object from the database
        game_type = GameType.objects.first()

        url = f'/gametypes/{game_type.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the game_type through the serializer that's being used in view
        expected = GameTypeSerializer(game_type)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)

    def test_delete_game_type(self):
        """Test delete game_type"""
        game_type = GameType.objects.first()

        url = f'/gametypes/{game_type.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the game_type
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
