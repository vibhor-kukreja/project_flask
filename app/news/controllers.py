from flask import Blueprint, request
from app import success, socketIo, redis

import json
from flask_socketio import join_room, leave_room, emit, send, rooms, close_room

from app.news.utils import save_user, get_news, \
    get_user_from_token, get_user, remove_user

redis_client = redis.client
chat_room = "chat_room"
mod_socket_news = Blueprint("news", __name__, url_prefix="/news")


@mod_socket_news.route("/", methods=["POST"])
def initial_response() -> None:
    """
       :return: JSON response
    """
    channel_name = request.get_json()['channelName']
    news = get_news(channel_name)
    return success(data=json.dumps(news))


@socketIo.on("login")
def user_logged_in(token):
    """
    This method when triggered, logs in the user and save it's entry in cache
    by mapping the request_session_id with the token
    :param token:
    :return:
    """
    user = get_user_from_token(token)

    join_room(user)
    save_user(request.sid, token) # store in cache
    print("{} has logged in".format(user))
    # TODO: In progress, multiple device login
    # emit("multi_login", room=user)


@socketIo.on("disconnect")
def user_left():
    """
    Find the user from the sid, and based on it, remove it from its room
    Runs in case of refresh or window close
    :return:
    """
    auth_token = get_user(request.sid)
    user = get_user_from_token(auth_token)
    leave_room(user)

    remove_user(request.sid)  # remove from cache

    # TODO: Currently there's no mechanism to track which socket connection
    # is part of which room, which is to be implemented
    leave_room(chat_room)
    emit("user_left", room=chat_room, include_self=False)


@socketIo.on("join_room")
def user_joined_room(token, room_name=chat_room):
    """
    This method lets the user join a specific room_name,
    when not provided automatically joins in the chat_room
    :param token:
    :param room_name:
    :return:
    """
    user = get_user_from_token(token)
    join_room(room_name)

    print("{} has joined room: {}".format(user, room_name))

    # this informs all the existing users about a new admission in the room
    emit("user_joined", user, room=room_name)


@socketIo.on("leave_room")
def user_logged_out(token, room_name=chat_room):
    """
    When user logs out, the system automatically
    removes it from respective rooms
    :param token:
    :param room_name:
    :return:
    """
    user = get_user_from_token(token)
    leave_room(user)  # remove from the user's room

    leave_room(room_name)  # remove from the chat room
    remove_user(request.sid)  # remove from cache

    # inform others to remove him from chat
    print("{} has left chat".format(user))
    emit("user_left", user, room=room_name, include_self=False)
    # emit("multi_login", room=user)


@socketIo.on("message")
def send_messages(token, recipient, message_text):

    user = get_user_from_token(token)
    new_message = "{}:{}".format(user, message_text)
    emit("message", new_message, room=recipient)
    # if recipient == "All":
    #     emit("message", new_message, room=chat_room)
    # else:


"""
{id: token, id: token, id: token}
token -> usr_name -> room.append


# refresh 
id left, id join -> 

# disconnect
id left, join with new

#logout
id left
"""
