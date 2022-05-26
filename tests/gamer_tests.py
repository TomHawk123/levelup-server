from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from levelupapi.models.gamer import Gamer
from levelupapi.views.gamers import GamerSerializer


class GamerTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']

    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_get_gamer(self):
        """Get Gamer Test"""
        # Grab a gamer object from the database
        gamer = Gamer.objects.first()

        url = f'/gamers/{gamer.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the gamer through the serializer that's being used in view
        expected = GamerSerializer(gamer)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)

    def test_list_gamers(self):
        """Test list gamers"""
        url = '/gamers'

        response = self.client.get(url)

        # Get all the gamers in the database
        # #and serialize them to get the expected output
        all_gamers = Gamer.objects.all()
        expected = GamerSerializer(all_gamers, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # response.data is the actual response from the url HTTP request
        self.assertEqual(expected.data, response.data)

    def test_delete_gamer(self):
        """Test delete gamer"""
        gamer = Gamer.objects.first()

        url = f'/gamers/{gamer.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the gamer
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
