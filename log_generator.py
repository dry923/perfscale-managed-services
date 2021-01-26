#!/usr/bin/env python
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import sys
import argparse
import datetime
from time import sleep
import random
import string
import logging

def _message(size):
    msg = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(size))
    return msg

def main():
    parser = argparse.ArgumentParser(description="Generate lines of a fixed byte size at a frequency for a duration")
    parser.add_argument(
        '--size',
        type=int,
        help='Size in bytes of a message')
    parser.add_argument(
        '--messages-per-minute',
        type=int,
        help='How many messages to send in one minute')
    parser.add_argument(
        '--messages-per-second',
        type=int,
        help='How many messages to send in one second')
    parser.add_argument(
        '--duration',
        type=int,
        help='How long to run the test for in minutes')
    args = parser.parse_args()

    if args.messages_per_minute:
        total_messages = args.messages_per_minute * args.duration
        messages_per_second = args.messages_per_minute / 60
    elif args.messages_per_second:
        total_messages = args.messages_per_second * 60 * args.duration
        messages_per_second = args.messages_per_second
    else:
        print("NO RATE DEFINED EXITING")
        exit(1)
    delay = 1 / messages_per_second

    my_message = _message(args.size)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    count = 0
    while count < total_messages:
        if args.messages_per_minute:
            logger.info(my_message)
            sleep(delay)
            count += 1
        else:
            t = datetime.datetime.now()
            for x in range(0, messages_per_second):
                logger.info(my_message)
            tdiff = datetime.datetime.now() - t
            total_diff = tdiff.seconds + (tdiff.microseconds / 1000000)
            if total_diff < 1:
                sleep(1 - total_diff)
            count += messages_per_second


if __name__ == '__main__':
    sys.exit(main())
