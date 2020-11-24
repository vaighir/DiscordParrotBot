#!/usr/bin/env python3
import os
import json

import mongo_helper
import learn_module

def main(author, server):

    # TODO get the learn result from mongodb
    # key = author + "_" + server

    learn_result = learn_module.main(author, server)

    dictionary = learn_result['content']['dictionary']
    first_words = learn_result['content']['first_words']

    print(first_words)
