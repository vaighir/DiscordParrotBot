#!/usr/bin/env python3
import os
import json

import mysql_helper


def main(author, server):
    messages = mysql_helper.load_messages(author, server)

    for m in messages:
        print(m)
