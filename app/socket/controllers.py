"""URLs related to socket integration"""
import json

from flask import Blueprint, request, Response

from app import success
from app.socket.services import get_my_friends, get_user_from_token, \
    get_news, get_my_rooms

mod_socket = Blueprint("socket", __name__, url_prefix="/socket")


@mod_socket.route("/news/", methods=["POST"])
def get_initial_news_response() -> Response:
    """
    This method fetches the top 10 news from various sources
    And returns to the API
    :return: JSON response
    """
    channel_name = request.get_json()['channelName']
    news = get_news(channel_name)
    return success(data=json.dumps(news))


@mod_socket.route("/users/", methods=["POST"])
def get_users() -> Response:
    """
    This method returns a list of all the friends and rooms the user is in
    Based on the provided token
    :return: Response containing list of friends and rooms
    """
    data = request.get_json()
    token = data['token']
    users = []
    user_id = get_user_from_token(token)

    # get all the friends and rooms the user is attached to
    friends = get_my_friends(user_id)
    rooms = get_my_rooms(user_id)

    users.extend(friends)
    users.extend(rooms)

    return success(data=json.dumps(users))
