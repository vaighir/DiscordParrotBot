#!/usr/bin/env python3
import os
import json
import random

import learn_module
import mysql_helper


def pick_random(words_list):
    rand = random.randint(0, len(words_list)-1)
    first_word = words_list[rand]
    return first_word


def get_next_word(last_word, first_word, dictionary):
    if last_word in dictionary:
        candidates = dictionary[last_word]
        candidates_as_list = []

        for c in candidates:
            f = candidates[c]
            for i in range(0, f):
                candidates_as_list.append(c)

        rand = random.randint(0, len(candidates_as_list)-1)
        return candidates_as_list[rand]

    else:
        new_word = first_word
        return new_word


def generate(dictionary, first_word):

    # TODO mark ending of messages in learning module and use it to terminate the message instead of random length
    length = random.randint(1, 10)

    if len(dictionary) < 1:
        return ""

    last_word = "!parrot"
    result = ""
    for i in range(0, length):

        new_word = get_next_word(last_word, first_word, dictionary)
        result = result + " " + new_word
        last_word = new_word

    return result


def main(author, server):

    message = ""

    key = author + "_" + server
    learn_result_as_tuple = mysql_helper.load_dictionary(key)[0]
    for lr in learn_result_as_tuple:
        learn_result = json.loads(lr)
        print(type(learn_result))
        print(learn_result)

        dictionary = learn_result['content']['dictionary']
        first_words = learn_result['content']['first_words']

        beginning = pick_random(first_words)
        message = generate(dictionary, beginning)

    print(message)

    return "%s said: %s" % (author, message)
