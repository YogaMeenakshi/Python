"""

"""

import models
import requests
from datetime import datetime
import re
import schedule
import time

url_list = {
    "list": "https://mapping-test.fra1.digitaloceanspaces.com/data/list.json",
    "detail": "https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{0}.json",
    "media": "https://mapping-test.fra1.digitaloceanspaces.com/data/media/{0}.json",
}

REGEX = re.compile('<.*?>')


def connect(url):
    """
    :param url:
    :return:
    """
    with requests.get(url) as data:
        if data:
            return data.json()
        else:
            return ""


def remove_html_tags(text_with_html):
    text = re.sub(REGEX, '', text_with_html)
    return text


def process_article(article_list):
    for article in article_list:
        article_id = article["id"]
        details = connect(url_list["detail"].format(article_id))
        media = connect(url_list["media"].format(article_id))

        if details:
            sections = details["sections"]
            for _sections in sections:
                if _sections.get("text"):
                    _sections["text"] = remove_html_tags(_sections["text"])
                _type = _sections["type"]

                if _type == "media":
                    _id = _sections["id"]
                    for m in media:
                        if m["id"] == _id:
                            sections.remove(_sections)

                            if m.get("pub_date"):
                                m["publication_date"] = datetime.strptime(m["pub_date"].replace(";", ":"),
                                                                          '%Y-%m-%d-%H:%M:%S')
                            if m.get("mod_date"):
                                m["modification_date"] = datetime.strptime(m["mod_date"].replace(";", ":"),
                                                                           '%Y-%m-%d-%H:%M:%S')
                            sections.append(m)

            details["publication_date"] = datetime.strptime(details["pub_date"].replace(";", ":"), '%Y-%m-%d-%H:%M:%S')
            if details.get("mod_date"):
                details["modification_date"] = datetime.strptime(details["mod_date"].replace(";", ":"),
                                                                 '%Y-%m-%d-%H:%M:%S')

            try:
                test = models.Article(**details)
                print(test.dict())
            except Exception as e:
                print(details)
                print(e)


if __name__ == '__main__':
    articles_list = connect(url_list["list"])
    schedule.every(1).minutes.do(process_article, articles_list)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print("Not able to process the articles!")
            raise Exception(e)