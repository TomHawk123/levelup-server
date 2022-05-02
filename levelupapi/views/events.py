"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import Event


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
            'description',
            'date',
            'time',
            'game',
            'organizer'
        )
        depth = 2