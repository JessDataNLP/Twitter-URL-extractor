import re
import requests
from bs4 import BeautifulSoup

def extract_website_name(url):
    """
    Extracts the domain name from a URL.

    :param url: The URL string.
    :return: The extracted domain name or an empty string if none is found.
    """
    pattern = r"https?://([^/]+)/?"
    match = re.search(pattern, url)
    return match.group(1) if match else ""

def classify_url(url):
    """
    Classifies a URL based on its domain.

    :param url: The URL string.
    :return: A string indicating the category of the URL.
    """
    if not isinstance(url, str):
        return "NaN"
    if "youtube.com" in url:
        return "youtube"
    elif "twitter.com" in url:
        return "twitter"
    elif "instagram.com" in url or "tiktok.com" in url:
        return "other_social_media"
    elif "telegram.org" in url:
        return "telegram"
    else:
        return "website"

def extract_telegram_account(url):
    """
    Extracts the Telegram account name from a URL.

    :param url: The Telegram URL string.
    :return: The extracted Telegram account name or an empty string if none is found.
    """
    pattern = r"https?://t.me/([^/?]+)"
    match = re.search(pattern, url)
    return match.group(1) if match else ""

def get_video_title(url):
    """
    Retrieves the title of a YouTube video from its URL.

    :param url: The YouTube video URL string.
    :return: The video title or an error message if the title cannot be retrieved.
    """
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title_tag = soup.find('title')
            return title_tag.text.replace(' - YouTube', '') if title_tag else 'Title not found'
    except Exception as e:
        return f'Failed to retrieve page: {e}'
    return 'Failed to retrieve page'
