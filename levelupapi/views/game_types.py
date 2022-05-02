"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from levelupapi.models import GameType


class GameTypeView(ViewSet):
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
        try:
            game_type = GameType.objects.get(pk=pk)
            serializer = GameTypeSerializer(game_type)
            return Response(serializer.data)
        except GameType.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """The list method is responsible for getting 
        the whole collection of objects from the database. 
        The ORM method for this one is all. Here is the code 
        to add to the method:

        Returns:
            Response -- JSON serialized list of game types
        """
        game_types = GameType.objects.all()
        serializer = GameTypeSerializer(game_types, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests to get all game types

        Returns:
            Response -- 204
        """
        game_type = GameType.objects.get(pk=pk)
        game_type.label = request.data['label']
        game.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests to get all game types

        Returns:
            Response -- 204
        """
        game_type = GameType.objects.get(pk=pk)
        game_type.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

# The serializer class determines how the Python data should
# be serialized to be sent back to the client. Put the
# following code at the bottom of the same module as above.
# Make sure it is outside of the view class.


class GameTypeSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = GameType
        fields = ('id', 'label')
        depth = 2
