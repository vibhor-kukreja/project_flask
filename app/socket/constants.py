"""Manage constants for the socket integration"""
NEWS_CONFIG = {
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

CHAT_ROOM = "chat_room"
