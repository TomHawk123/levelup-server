from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event
from levelupapi.models import Game
from levelupapi.models import Gamer


class EventView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """The retrieve method will get a single object 
        from the database based on the pk (primary key) in 
        the url. We will use the ORM to get the data, then the 
        serializer to convert the data to json. Add the 
        following code to the retrievemethod, making sure 
        the code is tabbed correctly:

        Returns:
            Response -- JSON serialized game type
        """
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def list(self, request):
        """The list method is responsible for getting 
        the whole collection of objects from the database. 
        The ORM method for this one is all. Here is the code 
        to add to the method:

        Returns:
            Response -- JSON serialized list of game types
        """
        events = Event.objects.all()
        game = request.query_params.get('maker', None)
        if game is not None:
            events = events.filter(game_id=game)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        OLD CODE WITHOUT VALIDATION:
        organizer = Gamer.objects.get(pk=request.data["organizer"])

        game = Game.objects.get(pk=request.data["game"])

        event = Event.objects.create(
            game=game,
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            organizer=organizer
        )
        serializer = EventSerializer(event)
        return Response(serializer.data)
        Returns
            Response -- JSON serialized game instance
        """
        # Next, we retrieve the GameType object from the database.
        # We do this to make sure the game type the user is trying
        # to add the new game actually exists in the database.
        # The data passed in from the client is held in the
        # request.data dictionary. Whichever keys are used on the
        # request.data must match what the client is passing to
        # the server.
        # To add the game to the database, we call the create
        # ORM method and pass the fields as parameters to the
        # function. Here’s the sql that will run:
        # The key on the request.data["key"] is for what is
        # being passed in the body of the create request.

        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data['game'])
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=organizer, game=game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for an game
        # event = Event.objects.get(pk=pk)
        # game = Game.objects.get(pk=request.data['game'])
        # event.game = game
        # event.description = request.data["description"]
        # event.date = request.data["date"]
        # event.time = request.data["time"]
        # organizer = Gamer.objects.get(pk=request.data['organizer'])
        # event.organizer = organizer
        # event.save()

        # return Response(None, status=status.HTTP_204_NO_CONTENT)

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        game = Game.objects.get(pk=request.data['game'])
        serializer = CreateEventSerializer(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(game=game)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # uses a list, but what comes out is a dictionary
        fields = [
            'id',
            'game',
            'description',
            'date',
            'time',
            'organizer'
        ]


# The serializer class determines how the Python data should
# be serialized to be sent back to the client. Put the
# following code at the bottom of the same module as above.
# Make sure it is outside of the view class.


class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Event
        fields = (
            'id',
            'game',
            'description',
            'date',
            'time',
            'organizer'
        )
        depth = 3
