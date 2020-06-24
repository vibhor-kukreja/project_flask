"""All socket related methods"""
from typing import AnyStr

from flask import request
from flask_socketio import join_room, emit

from app import socketIo
from app.socket.services import get_user_from_token, get_user, save_user, \
    remove_user

chat_room = "chat_room"


@socketIo.on("login")
def user_logged_in(token: AnyStr) -> None:
    """
    This method when triggered, logs in the user and save it's entry in cache
    by mapping the request_session_id with the token
    :param token: String containing the token
    :return: None
    """
    user = get_user_from_token(token)
    join_room(user)

    save_user(request.sid, user)  # store in cache

    print("{} has logged in".format(user))


@socketIo.on("join_room")
def user_joined_room(token: AnyStr, room_name: AnyStr = chat_room) -> None:
    """
    This method lets the user join a specific room_name,
    when not provided automatically joins in the chat_room
    :param token: String containing the token
    :param room_name: The room name to join
    :return: None
    """
    user = get_user_from_token(token)
    join_room(room_name)
    emit("joined-room", room_name, room=user)

    print("{} has joined room: {}".format(user, room_name))


@socketIo.on("logout")
def logout_user(token: AnyStr) -> None:
    """
    This methods logs out the user from the system and breaks the socket
    :param token: String containing the socket
    :return: None
    """
    user = get_user_from_token(token)
    leave_room(user)
    remove_user(request.sid)

    print("{} has logged out".format(user))


@socketIo.on("disconnect")
def user_disconnected() -> None:
    """
    Find the user from the sid, and based on it, remove it from its room
    Runs in case of refresh or window close
    :return:
    """
    user = get_user(request.sid)
    if user:
        leave_room(user)
        leave_room(chat_room)
        remove_user(request.sid)


@socketIo.on("leave_room")
def leave_room(token: AnyStr, room_name: AnyStr = chat_room) -> None:
    """
    This method when triggered via socket,
    Causes the user to leave the chat room
    :param token: String containing the token
    :param room_name: Room To Leave
    :return: None
    """
    user = get_user_from_token(token)
    leave_room(chat_room)

    print("{} has left room: {}".format(user, room_name))


@socketIo.on("message")
def send_messages(token: AnyStr, recipient: AnyStr, message_text: AnyStr):
    """
    This method is used to send messages between one user to another
    And also from one user to a whole room containing different users
    :param token: String containing the token
    :param recipient: Person/Room to receive the message
    :param message_text: The Text To Send to that user/room
    :return: None
    """
    user = get_user_from_token(token)
    new_message = "{}:{}".format(user, message_text)

    emit("new-message", new_message, room=recipient)
