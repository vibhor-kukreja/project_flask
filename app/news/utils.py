import json
import feedparser

from flask_jwt_extended import decode_token
from json import JSONDecodeError

from app import redis

redis_client = redis.client

news_configs = {
    'bbc':
        {
            "time_stamp_format": "%a, %d %b %Y %H:%M:%S %Z",
            "rss_url": "http://feeds.bbci.co.uk/news/world/rss.xml"
        },
    'times':
        {
            "time_stamp_format": "%a, %d %b %Y %H:%M:%S %Z",
            "rss_url": "https://timesofindia.indiatimes.com/"
                       "rssfeeds/-2128936835.cms"
        },
    'ndtv':
        {
            "time_stamp_format": "%B %d, %Y %H:%M %p",
            "rss_url": "http://feeds.feedburner.com/"
                       "ndtvnews-top-stories?format=xml"
        }
}


def get_user(sid):
    token = redis_client.get(sid)
    return token


def get_user_from_token(token):
    try:
        user = json.loads(decode_token(token)['identity'])['email']
        return user
    except JSONDecodeError as j_err:
        # emit("throw_error", "Invalid User Token, Please Login Again")
        return None


def save_user(sid, token):
    # user = get_user_from_token(token)
    redis_client.set(sid, token)


def remove_user(sid):
    redis_client.delete(sid)


# def save_time_string(channel_name, time_string):
#     time_stamp_format = news_configs[channel_name]['time_stamp_format']
#     news_latest_timestamp = datetime.timestamp(
#         datetime.strptime(time_string, time_stamp_format))
#     time_stamps[channel_name] = news_latest_timestamp


def get_news(channel_name):
    news_items = []
    current_channel = news_configs[channel_name]
    news_feed = feedparser.parse(current_channel['rss_url'])
    # latest_news_time = news_feed.entries[0]['published']
    top_articles = news_feed.entries[:10]
    for article in top_articles:
        news_items.append({'title': article['title'], 'link': article['link']})
    # save_time_string(channel_name, latest_news_time)
    return news_items
