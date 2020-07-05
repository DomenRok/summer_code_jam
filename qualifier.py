"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
from functools import total_ordering
from collections import Counter

import datetime
import typing
import re


class ArticleField:
    """The `ArticleField` class for the Advanced Requirements."""

    def __init__(self, field_type: typing.Type[typing.Any]):
        self.field_type = field_type

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.field_type):
            raise TypeError(f"Expected an instance of `{self.field_type}` for attribute `{self.name}`, got {type(value)} instead.")
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


@total_ordering
class Article:
    """The `Article` class you need to write for the qualifier."""
    id = 0
    attribute = ArticleField(field_type=int)

    def __init__(self, title: str, author: str, publication_date: datetime.datetime, content: str):
        self.id = Article.id
        type(self).id += 1

        self.title = title
        self.author = author
        self._content = content
        self.publication_date = publication_date
        self.last_edited = None

    def __repr__(self):
        return f"<Article title=\"{self.title}\" author='{self.author}' publication_date='{datetime.datetime.isoformat(self.publication_date)}'>"

    def __len__(self):
        return len(self.content)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self.last_edited = datetime.datetime.now()

    @content.deleter
    def content(self):
        self._content = None
        self.last_edited = datetime.datetime.now()

    def short_introduction(self, n_characters: int):
        length_of_last_word = len(re.split("[ \n]", self.content[:n_characters])[-1])
        return self.content[0: n_characters - length_of_last_word - 1]

    def most_common_words(self, n: int):
        counter = Counter()
        for word in list(filter(None, re.split(r"\W+", self.content))):
            counter[word.lower()] += 1
        return {k: v for k, v in sorted(counter.items(), key=lambda item: item[1], reverse=True)[:n]}

    def __eq__(self, other):
        return self.publication_date == other.publication_date

    def __gt__(self, other):
        return self.publication_date > other.publication_date
