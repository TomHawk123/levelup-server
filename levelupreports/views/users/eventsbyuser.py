"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View
from levelupapi.models import event
from levelupreports.views.helpers import dict_fetch_all


class UserEventList(View):
    def get(self, request):
        with connection.cursor() as db_cursor:

            # TODO: Write a query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT le.id,
              le.date,
              le.time,
              lg.title as game_name,
              au.first_name || " " || au.last_name as full_name,
              lgr.id as gamer_id
            FROM levelupapi_event le
              JOIN levelupapi_gamer lgr ON lgr.id = le.organizer_id
              JOIN auth_user au ON au.id = lgr.user_id
              JOIN levelupapi_game lg ON le.game_id           
            """)
            # Pass the db_cursor to the dict_fetch_all function to turn the fetch_all() response into a dictionary
            dataset = dict_fetch_all(db_cursor)

            events_by_user = []

            for row in dataset:
                # TODO: Create a dictionary called event that includes
                # the event id, date, time, game_name, and attending_gamer_name
                # from the row dictionary
                event = {
                    'id': row['id'],
                    'date': row['date'],
                    'time': row['time'],
                    'game_name': row['game_name']
                }

                # See if the gamer has been added to the events_by_user list already
                user_dict = None
                for user_event in events_by_user:
                    if user_event['gamer_id'] == row['gamer_id']:
                        user_dict = user_event

                if user_dict:
                    # If the user_dict is already in the events_by_user list, append the game to the games list
                    user_dict['events'].append(event)
                else:
                    # If the user is not on the events_by_user list, create and add the user to the list
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })

        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
