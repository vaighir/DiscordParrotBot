#!/usr/bin/env python3
import os
import json

import mysql_helper


def learn(dictionary, first_words, message):
    tokens = message.split(" ")

    if len(tokens) > 1:
        first_words.append(tokens[0])

    for i in range(0, len(tokens)-1):
        current = tokens[i]

        next = tokens[i+1]

        if current in dictionary:
            nextWords = dictionary[current]

            if next in nextWords:
                dictionary[current][next] = dictionary[current][next] + 1
            else:
                dictionary[current][next] = 1

        else:
            dictionary[current] = {next: 1}


def main(author, server):
    # TODO delete old dictionary from the database
    dictionary = dict()
    first_words = []
    messages = mysql_helper.load_messages(author, server)

    for message in messages:
        for m in message:
            learn(dictionary, first_words, m)

    for x in dictionary:
        print(x)
        for y in dictionary[x]:
            print(y, ":", dictionary[x][y])

    key = author + "_" + server
    result = {key: {"dictionary": dictionary, "first_words": first_words}}

    # TODO save new dictionary into the database
