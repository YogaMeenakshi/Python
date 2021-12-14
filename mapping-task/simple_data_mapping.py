"""
Module name : simple_data_mapping.py
Created on : 12/14/2021
created by : Sasikumar Ramakrishnan
"""

# Adding logging module
import logging

# Create and configure logger
logging.basicConfig(filename="data_mapping.log",
                    format='%(asctime)s %(message)s',
                    filemode='a')
log = logging.getLogger()
log.setLevel(logging.DEBUG)

try:
    # Importing necessary modules
    import models
    import requests
    from datetime import datetime, timedelta
    from re import sub, compile
    import schedule
    from time import sleep
    from sys import argv
    log.info("All modules imported!")
except ImportError:
    log.error("Unable to import necessary modules. Please install and retry!")
except Exception as e:
    raise Exception(e)


# variable declaration
INTERVAL = int(argv[1]) if argv[1] else 5
NEW_ARTICLE = False if argv[2].lower() == "false" else True
REGEX = compile('<.*?>')

url_list = {
    "list": "https://mapping-test.fra1.digitaloceanspaces.com/data/list.json",
    "detail": "https://mapping-test.fra1.digitaloceanspaces.com/data/articles/{0}.json",
    "media": "https://mapping-test.fra1.digitaloceanspaces.com/data/media/{0}.json",
}


def connect(url):
    """
    :param url: URL in string format to connect API and pull data.
    :return: data in json format.
    """

    try:
        with requests.get(url) as data:
            if data:
                return data.json()
            else:
                log.info('Connection Success to the API.')
    except requests.HTTPError as http_err:
        log.error(f'HTTP error occurred: {http_err}')
    except Exception as err:
        log.error(f'Other error occurred: {err}')


def remove_html_tags(text_with_html):
    """
    :param text_with_html: text with html elements or not.
    :return: text without html element.
    """
    text = sub(REGEX, '', text_with_html)
    return text


def process_article(new=False):
    """
    :param new: Flags to identify and process old articles (Boolean)
    :return: None
    """

    # getting articles list
    log.info("Getting articles list.")
    article_list = connect(url_list["list"])

    for article in article_list:
        article_id = article["id"]

        # getting articles details
        log.info("Getting articles details")
        details = connect(url_list["detail"].format(article_id))

        # getting media details if it is there
        log.info("Getting media details if it is there")
        media = connect(url_list["media"].format(article_id))

        if details:
            mod_flag = False
            five_minute_less = timedelta(minutes=INTERVAL)
            parsing_datetime = datetime.now() - five_minute_less

            # converting to date objects
            details["publication_date"] = datetime.strptime(details["pub_date"].replace(";", ":"), '%Y-%m-%d-%H:%M:%S')
            if details.get("mod_date"):
                details["modification_date"] = datetime.strptime(details["mod_date"].replace(";", ":"),
                                                                 '%Y-%m-%d-%H:%M:%S')
                if details["modification_date"] >= parsing_datetime:
                    mod_flag = True

            if (details["publication_date"] >= parsing_datetime and new) or (mod_flag and new) or not new:
                sections = details["sections"]
                for _sections in sections:
                    if _sections.get("text"):
                        # Removing html elements from texts
                        log.info("Removing html elements from texts")
                        _sections["text"] = remove_html_tags(_sections["text"])
                    _type = _sections["type"]

                    if _type == "media":
                        _id = _sections["id"]
                        if media:
                            for m in media:
                                if m["id"] == _id:
                                    sections.remove(_sections)

                                    # converting to date objects
                                    if m.get("pub_date"):
                                        m["publication_date"] = datetime.strptime(m["pub_date"].replace(";", ":"),
                                                                                  '%Y-%m-%d-%H:%M:%S')
                                    if m.get("mod_date"):
                                        m["modification_date"] = datetime.strptime(m["mod_date"].replace(";", ":"),
                                                                                   '%Y-%m-%d-%H:%M:%S')
                                    sections.append(m)

                try:
                    test = models.Article(**details)
                    print(test.dict())
                except Exception as er:
                    log.error(f"Not able to process this article : {article_id}")
                    log.info(e)
                    raise Exception(er)


log.info("Functions and variables declared and initiated!")

if __name__ == '__main__':
    log.info("Started processing the articles for every 5 or given minutes!")
    schedule.every(INTERVAL).minutes.do(process_article, NEW_ARTICLE)

    while True:
        try:
            schedule.run_pending()
            sleep(1)
        except Exception as e:
            log.error("Not able to process the articles! Please take a look.")
            log.error(e)
            raise Exception(e)
