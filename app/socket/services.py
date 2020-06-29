"""Additional methods to be used by controller layer and socket layer"""
import json
from json import JSONDecodeError
from typing import List, AnyStr, Union

import feedparser
from flask_jwt_extended import decode_token
from jwt import ExpiredSignatureError

from app.socket.constants import NEWS_CONFIG, CHAT_ROOM
from app import redis
from app.auth.models import User

redis_client = redis.client


def get_my_rooms(user_id: AnyStr) -> List:
    """
    This method will return the rooms user is in
    :param user_id: The email of the user
    :return: List of the rooms user is in
    """
    # TODO: Get the rooms user is in based on the email provided
    return [
        CHAT_ROOM
    ]


def get_my_friends(user_id: AnyStr) -> List:
    """
    This method will return all the friends the user has
    :param user_id:
    :return:
    """
    friends = []
    # TODO: To replace this with retrieving records from custom table Friends
    users = list(User.query.with_entities(User.email))
    for user in users[3:]:
        friends.append(user[0])
    return friends


def get_user_from_token(token: AnyStr) -> Union[ValueError, AnyStr]:
    """
    This method takes the token and tries to fetch user email out of it
    :param token: String containing the token
    :return: User email in string format
    """
    try:
        user = json.loads(decode_token(token)['identity'])['email']
        return user
    except ExpiredSignatureError:
        raise ValueError("Token Expired")
    except JSONDecodeError:
        return ValueError("Invalid Token")


def get_news(channel_name: AnyStr) -> List:
    """
    This method fetches news from different sources and returns them in list
    :param channel_name: Name of channel to fetch news
    :return: List containing top 10 news headlines
    """
    news_items = []
    current_channel = NEWS_CONFIG[channel_name]
    news_feed = feedparser.parse(current_channel['rss_url'])

    top_articles = news_feed.entries[:10]
    for article in top_articles:
        news_items.append({'title': article['title'], 'link': article['link']})

    return news_items


def get_user(sid: AnyStr) -> Union[AnyStr, None]:
    """
    This method takes the socket_id as input and tries to find related token
    from cache
    :param sid:
    :return: Auth token related to this socket_id
    """
    token = redis_client.get(sid)
    return token.decode() if token else None


def save_user(sid: AnyStr, token: AnyStr) -> None:
    """
    This method saves a mapping of socket_id and token in the cache
    To fetch later
    :param sid: socket id
    :param token: Auth token
    :return: None
    """
    redis_client.set(sid, token)


def remove_user(sid: AnyStr) -> None:
    """
    This method removes a value from cache by finding the equivalent socket id
    :param sid: socket it
    :return: None
    """
    redis_client.delete(sid)
