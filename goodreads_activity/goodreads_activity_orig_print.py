# -*- coding: utf-8 -*-
"""
Goodreads Activity
==================
A Pelican plugin to lists books from your Goodreads shelves.
Copyright (c) Talha Mansoor
"""

from __future__ import unicode_literals

import logging
import pdb

from pprint import pprint

from pelican import signals

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# logger.propogate = False
# log_formatter = logging.Formatter(
# "%(asctime)s :: %(name)s :: %(levelname)s :: %(message)s"
# "%(name)s :: %(levelname)s :: %(message)s"
# )
# chatter = logging.StreamHandler()
# chatter.setLevel(logging.DEBUG)
# chatter.setFormatter(log_formatter)
# logger.addHandler(chatter)


class GoodreadsActivity:
    def __init__(self, generator):
        import feedparser

        pdb.set_trace()
        logger.info("Populating self.activities")
        print("Settings:")
        pprint(generator.settings)
        pdb.set_trace()
        # logger.debug("Settings: %s", generator.settings)
        logger.debug("Feed: %s", generator.settings["GOODREADS_ACTIVITY_FEED"])
        pdb.set_trace()
        self.activities = feedparser.parse(
            generator.settings["GOODREADS_ACTIVITY_FEED"]
        )
        pdb.set_trace()
        print("self.activities:")
        pprint(self.activities)
        pdb.set_trace()
        # logger.debug("self.activities: %s", self.activities)

    def fetch(self):
        pdb.set_trace()
        logger.info("Starting fetch method")
        # print("Starting fetch method")
        pdb.set_trace()
        goodreads_activity = {
            "shelf_title": self.activities.feed.title,
            "books": [],
        }
        pdb.set_trace()
        # print("goodreads_activity:")
        # pprint(goodreads_activity)
        # logger.debug(goodreads_activity)
        for entry in self.activities["entries"]:
            pdb.set_trace()
            book = {
                "title": entry.title,
                "author": entry.author_name,
                "link": entry.link,
                "l_cover": entry.book_large_image_url,
                "m_cover": entry.book_medium_image_url,
                "s_cover": entry.book_small_image_url,
                "description": entry.book_description,
                "rating": entry.user_rating,
                "review": entry.user_review,
                "tags": entry.user_shelves,
            }
            pdb.set_trace()
            logger.debug("New book: %s", book)
            pdb.set_trace()
            goodreads_activity["books"].append(book)
            # print(goodreads_activity)
            pdb.set_trace()

        logger.info("fetch method run complete")
        return goodreads_activity


def fetch_goodreads_activity(gen, metadata):
    logger.info("Fetching goodreads_activity")
    print("Generator settings:")
    logger.debug("Generator settings: {}".format(gen.settings))
    if "GOODREADS_ACTIVITY_FEED" in gen.settings:
        pdb.set_trace()
        gen.context["goodreads_activity"] = gen.goodreads.fetch()
        pdb.set_trace()
        logger.debug("Context: %s", gen.context)
        pprint(gen.settings)
        pdb.set_trace()


def initialize_feedparser(generator):
    logger.info("Initializing feedparser")
    pdb.set_trace()
    generator.goodreads = GoodreadsActivity(generator)
    pdb.set_trace()
    logger.info("Feedparser initialized")
    pdb.set_trace()


def register():
    try:
        logger.info("Firing init signal")
        pdb.set_trace()
        signals.article_generator_init.connect(initialize_feedparser)
        pdb.set_trace()
        logger.info("Init signal success")
        pdb.set_trace()
        logger.info("Firing fetch signal")
        pdb.set_trace()
        signals.article_generator_context.connect(fetch_goodreads_activity)
        pdb.set_trace()
        logger.info("Fetch signal success")
        pdb.set_trace()
    except ImportError:
        logger.warning(
            "`goodreads_activity` failed to load dependency `feedparser`."
            "`goodreads_activity` plugin not loaded."
        )
