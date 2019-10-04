# -*- coding: utf-8 -*-
"""
Goodreads Activity
==================

A Pelican plugin to lists books from your Goodreads shelves.

Copyright (c) Talha Mansoor
"""

from __future__ import unicode_literals

import logging

logger = logging.getLogger(__name__)

from pelican import signals


class GoodreadsActivity:
    def __init__(self, generator, shelf=None):
        import feedparser

        if generator.settings["GOODREADS_ACTIVITY_FEED"]:
            activity_shelf = feedparser.parse(
                generator.settings["GOODREADS_ACTIVITY_FEED"]
            )
        elif generator.settings["GOODREADS_ACTIVITY_BASE"] and shelf:
            activity_shelf = (
                generator.settings["GOODREADS_ACTIVITY_BASE"] + shelf
            )
        self.activities = feedparser.parse(activity_shelf)

    def fetch(self):
        goodreads_activity = {
            "shelf_title": self.activities.feed.title,
            "books": [],
        }
        for entry in self.activities["entries"]:
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
            goodreads_activity["books"].append(book)

        return goodreads_activity


def fetch_goodreads_activity(gen, metadata):
    if (
        "GOODREADS_ACTIVITY_BASE" in gen.settings
        and "GOODREADS_SHELVES" in gen.settings
    ):
        base = gen.settings["GOODREADS_ACTIVITY_BASE"]
        shelves = gen.settings["GOODREADS_SHELVES"]
        for shelf in shelves:
            gen.settings["GOODREADS_ACTIVITY_FEED"] = base + shelf
            gen.context["goodreads_activity"] = []
            gen.context["goodreads_activity"].append(gen.goodreads.fetch())
    elif "GOODREADS_ACTIVITY_FEED" in gen.settings:
        gen.context["goodreads_activity"] = gen.goodreads.fetch()


def initialize_feedparser(generator):
    generator.goodreads = GoodreadsActivity(generator)


def register(shelf=None):
    try:
        signals.article_generator_init.connect(initialize_feedparser)
        signals.article_generator_context.connect(fetch_goodreads_activity)
    except ImportError:
        logger.warning(
            "`goodreads_activity` failed to load dependency `feedparser`."
            "`goodreads_activity` plugin not loaded."
        )
