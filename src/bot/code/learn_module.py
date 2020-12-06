#!/usr/bin/env python3
import os
import json

import mysql_helper

end_of_message = "~~~~END~~~~~!"


def learn(dictionary, first_words, message):
    tokens = message.split(" ")

    if len(tokens) > 1:
        first_words.append(tokens[0])

    for i in range(0, len(tokens) - 1):

        current = tokens[i]
        next_w = tokens[i + 1]

        if current in dictionary:

            if next_w in dictionary[current]:
                dictionary[current][next_w] = dictionary[current][next_w] + 1
            else:
                dictionary[current][next_w] = 1

        else:
            dictionary[current] = {next_w: 1}

        if i == len(tokens) - 2:
            if next_w in dictionary and end_of_message in dictionary[next_w]:
                dictionary[next_w][end_of_message] = dictionary[next_w][end_of_message] + 1
            else:
                dictionary[next_w] = {end_of_message: 1}


def main(author, server):
    dictionary = dict()
    first_words = []
    messages = mysql_helper.load_messages(author, server)

    for message in messages:
        for m in message:
            learn(dictionary, first_words, m)

    key = author + "_" + server
    result = {"key": key,
              "content": {"dictionary": dictionary, "first_words": first_words}}

    print(result)

    mysql_helper.write_dictionary(key, json.dumps(result))
