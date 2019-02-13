#!/usr/bin/env python
import re
import os
import sys

import pocket
import requests
import bitly_api

POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
if not POCKET_CONSUMER_KEY:
  raise ValueError("Environment variable POCKET_CONSUMER_KEY required")

RE_LWN_ARTICLE_LINK = re.compile("https://lwn.net/Articles/(\d+)/")

RE_SUBSCRIBER_LINK_FORM = re.compile(
    "<input type=\"hidden\" name=\"articleid\" value=\"(\d+)\">")

RE_SUBSCRIBER_LINK = re.compile("https://lwn.net/SubscriberLink/(\d+)/.+/")

BITLY_ACCESS_TOKEN = "BITLY_ACCESS_TOKEN"

def get_bitly_connection():
    """Create a Connection base on username and access token credentials"""
    if BITLY_ACCESS_TOKEN not in os.environ:
        raise ValueError("Environment variable '{}' required".format(BITLY_ACCESS_TOKEN))
    access_token = os.getenv(BITLY_ACCESS_TOKEN)
    bitly = bitly_api.Connection(access_token=access_token)
    return bitly


def main():
  access_token = os.getenv("POCKET_ACCESS_TOKEN")
  p = pocket.Pocket(POCKET_CONSUMER_KEY, access_token)

  non_articles = p.get(domain="lwn.net", detailType="simple",
                            state="unread")

  parsed_articles = []
  for entry_id, entry in non_articles[0].get('list', {}).items():
    if int(entry.get("is_article", "0")) == 0:
      item_id = entry.get("item_id", "")
      title = entry.get("given_title", "")
      url = entry.get("given_url", "")
      result = RE_LWN_ARTICLE_LINK.search(url)
      if not result:
        print("Skipping %s..." % title)
        continue
      parsed_articles.append((result.group(1), title, url, item_id))

  print("Found the following articles:")
  for article in parsed_articles:
    print("[%s] %s (%s) {%s}" % article)
  print("")
  result = input("Try to convert into articles? [y/N] ") if os.isatty(sys.stdin.fileno()) else 'y'
  if result != "y":
    print("Aborting")
    sys.exit(1)

  session = requests.Session()
  session.post(
    "https://lwn.net/Login/",
    data={"Username": os.getenv("LWNNET_USERNAME"),
          "Password": os.getenv("LWNNET_PASSWORD")}).cookies

  bitly = get_bitly_connection()

  couldnt_add = []

  for article in parsed_articles:
    link = session.post("https://lwn.net/SubscriberLink/MakeLink",
                        data={"articleid": article[0]})

    RE_SUBLINK = re.compile(
        "<a href=\"(https://lwn.net/SubscriberLink/%s/.+)\">"
        % article[0])
    m = RE_SUBLINK.search(link.text)
    if not m:
      # If it's not subscriber-only content, create shorten URL to trick Pocket
      # into re-evaluating the article
      if "This item is not subscriber-only content" in link.text:
        data = bitly.shorten(article[2])
        link = data.get("url")
      else:
        print("Could not find subscriber link in response for article '%s'" % article[1])
        couldnt_add.append(article)
        continue
    else:
      link = m.group(1)

    if not link:
      print("Couldn't generate new link for article '%s'" % article[1])
      continue

    print("Adding subscriber link: %s" % link)
    result = p.add(link)
    item = result[0].get('item', None)
    if not item:
      print("Error adding subscriber link for article '%s'" % article[1])
      continue
    print("Deleting '%s'" % article[1])
    p.delete(article[3], wait=False)

  if couldnt_add:
    print("Couldn't add the following articles:")
    for article in couldnt_add:
      print("[%s] %s (%s) {%s}" % article)

if __name__ == '__main__':
  main()
