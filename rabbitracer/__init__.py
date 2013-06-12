#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import uuid
import types

from furl import furl
from kombu import Connection, Exchange, Queue


def process_message(body, message):

    def _is_hidden(attribute_name):
        return attribute_name.startswith('_')

    def _is_acceptable(attribute_refs):
        attribute_type = type(attribute_refs)
        acceptable_types = [
            types.NoneType, types.ListType, types.DictType,
            types.StringTypes, types.UnicodeType, types.BooleanType,
            types.IntType, types.LongType, types.FloatType,
        ]
        for acceptable_type in acceptable_types:
            if attribute_type == acceptable_type:
                return True
        return False

    def _encode(attribute_name, attribute_refs):
        if attribute_name != 'payload':
            return attribute_refs
        properties = message.headers.get('properties')
        content_type = properties.get('content_type')
        if not content_type:
            return attribute_refs
        if content_type.startswith('application/json'):
            return json.loads(attribute_refs)
        return attribute_refs

    dump_dict = {}
    for attr_name in dir(message):
        if _is_hidden(attr_name):
            continue
        attribute = getattr(message, attr_name)
        if not _is_acceptable(attribute):
            continue
        dump_dict[attr_name] = _encode(attr_name, attribute)
    message.ack()
    print(json.dumps(dump_dict))


def parse_arguments():
    description = 'RabbitMQ firehose dump script'

    option_n_help = 'hostname'
    option_u_help = 'username'
    option_w_help = 'password'
    option_v_help = 'virtualhost'

    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('-n', '--hostname', help=option_n_help,
                            required=False, default='localhost')
    arg_parser.add_argument('-u', '--username', help=option_u_help,
                            required=False, default='guest')
    arg_parser.add_argument('-w', '--password', help=option_w_help,
                            required=False, default='guest')
    arg_parser.add_argument('-v', '--virtualhost', help=option_v_help,
                            required=False, default='/')
    global ARGS
    ARGS = arg_parser.parse_args()


def main_loop():

    def _build_url():
        f = furl()
        f.scheme = 'amqp'
        f.username = ARGS.username
        f.password = ARGS.password
        f.hostname = ARGS.hostname
        f.path = ARGS.virtualhost
        return str(f)

    trace_exchange = Exchange('amq.rabbitmq.trace', 'topic')
    trace_queue = Queue('firehose.' + str(uuid.uuid4()),
                        exchange=trace_exchange,
                        routing_key='#',
                        auto_delete=True)
    with Connection(_build_url()) as connection:
        with connection.Consumer(trace_queue, callbacks=[process_message]):
            while True:
                connection.drain_events()


def main():
    parse_arguments()
    main_loop()


if __name__ == '__main__':
    main()
