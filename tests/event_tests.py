from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from levelupapi.models import Gamer
from levelupapi.models.event import Event
from levelupapi.views.events import CreateEventSerializer, EventSerializer


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']

    def setUp(self):
        # Grab the first Gamer object from the database and add their token to the headers
        self.gamer = Gamer.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """Create event test"""
        url = "/events"

        # Define the Game properties
        # The keys should match what the create method is expecting
        # Make sure this matches the code you have
        event = {
            "game": 1,
            "description": "game-test",
            "date": "1999-01-01",
            "time": "20:00",
            "organizer": 1
        }

        response = self.client.post(url, event, format='json')

        # The _expected_ output should come first when using an assertion with 2 arguments
        # The _actual_ output will be the second argument
        # We _expect_ the status to be status.HTTP_201_CREATED and it _actually_ was response.status_code
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        # Get the last game added to the database, it should be the one just created
        new_event = Event.objects.last()

        # Since the create method should return the serialized version of the newly created game,
        # Use the serializer you're using in the create method to serialize the "new_game"
        # Depending on your code this might be different
        expected = CreateEventSerializer(new_event)

        # Now we can test that the expected output matches what was actually returned
        self.assertEqual(expected.data, response.data)

    def test_get_event(self):
        """Get Event Test"""
        # Grab a event object from the database
        event = Event.objects.first()

        url = f'/events/{event.id}'

        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Like before, run the event through the serializer that's being used in view
        expected = EventSerializer(event)

        # Assert that the response matches the expected return data
        self.assertEqual(expected.data, response.data)

    def test_list_events(self):
        """Test list events"""
        url = '/events'

        response = self.client.get(url)

        # Get all the events in the database
        # #and serialize them to get the expected output
        all_events = Event.objects.all()
        for event in all_events:
            event.joined = self.gamer in event.attendees.all()
        expected = EventSerializer(all_events, many=True)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # response.data is the actual response from the url HTTP request
        self.assertEqual(expected.data, response.data)

    def test_delete_event(self):
        """Test delete event"""
        event = Event.objects.first()

        url = f'/events/{event.id}'
        response = self.client.delete(url)

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        # Test that it was deleted by trying to _get_ the event
        # The response should return a 404
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
