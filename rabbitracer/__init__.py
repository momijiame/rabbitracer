#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
import json
import uuid
import types
import inspect
from abc import ABCMeta, abstractmethod

from furl import furl
from kombu import Connection, Exchange, Queue


class MessageSerializer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def serialize(self, msg):
        pass


class JsonSerializer(MessageSerializer):

    def __init__(self, prettyprint=False):
        super(JsonSerializer, self).__init__()
        self.prettyprint = prettyprint

    def _is_acceptable(self, attr):
        acceptable_types = [
            types.NoneType,
            types.ListType,
            types.DictType,
            types.StringTypes,
            types.UnicodeType,
            types.BooleanType,
            types.IntType,
            types.LongType,
            types.FloatType,
        ]
        attr_type = type(attr)
        return attr_type in acceptable_types

    def _encode(self, msg, attr_name, attr):
        if attr_name != 'payload':
            return attr
        properties = msg.headers.get('properties')
        content_type = properties.get('content_type')
        if not content_type:
            return attr
        if content_type.startswith('application/json'):
            return json.loads(attr)
        return attr

    def serialize(self, msg):
        attrs = inspect.getmembers(
            msg,
            lambda attr: (
                not inspect.ismethod(attr) and
                not inspect.isfunction(attr)
            )
        )

        result = [
            (attr_name, self._encode(msg, attr_name, attr))
            for attr_name, attr in attrs if self._is_acceptable(attr)
        ]

        msg.ack()
        indent = 4 if self.prettyprint else None
        return json.dumps(result, indent=indent)


class FirehoseConsumer(object):
    __metaclass__ = ABCMeta

    EXCHANGE_NAME = 'amq.rabbitmq.trace'
    EXCHANGE_TYPE = 'topic'

    def __init__(self, uri):
        self.uri = uri

    @abstractmethod
    def on_message(self, msg):
        pass

    def start(self):
        trace_exchange = Exchange(self.EXCHANGE_NAME, self.EXCHANGE_TYPE)
        trace_queue = Queue(
            'firehose.' + str(uuid.uuid4()),
            exchange=trace_exchange,
            routing_key='#',
            auto_delete=True,
        )
        with Connection(self.uri) as connection:
            with connection.Consumer(
                trace_queue,
                callbacks=[
                    self.on_message,
                ],
            ):
                while True:
                    connection.drain_events()


class FirehoseJsonDumper(FirehoseConsumer):

    def __init__(self, uri, serializer=None):
        super(FirehoseJsonDumper, self).__init__(uri)
        self.serializer = serializer or JsonSerializer()

    def on_message(self, body, msg):
        serialized_msg = self.serializer.serialize(msg)
        print(serialized_msg)


def _parse_args():
    description = 'RabbitMQ firehose dump script'
    arg_parser = argparse.ArgumentParser(description=description)

    option_n_help = 'Set RabbitMQ Hostname'
    default_hostname = os.environ.get('RABBIT_HOSTNAME') or 'localhost'
    arg_parser.add_argument(
        '-n', '--hostname',
        type=str,
        required=False, default=default_hostname,
        help=option_n_help,
    )

    option_u_help = 'Set RabbitMQ Username'
    default_username = os.environ.get('RABBIT_USERNAME') or 'guest'
    arg_parser.add_argument(
        '-u', '--username',
        type=str,
        required=False, default=default_username,
        help=option_u_help,
    )

    option_p_help = 'Set RabbitMQ Password'
    default_password = os.environ.get('RABBIT_PASSWORD') or 'guest'
    arg_parser.add_argument(
        '-p', '--password',
        type=str,
        required=False, default=default_password,
        help=option_p_help,
    )

    option_v_help = 'Set RabbitMQ VirtualHost'
    default_virtualhost = os.environ.get('RABBIT_VIRTUALHOST') or '/'
    arg_parser.add_argument(
        '-v', '--virtualhost',
        type=str,
        required=False, default=default_virtualhost,
        help=option_v_help,
    )

    option_r_help = 'Pretty print'
    arg_parser.add_argument(
        '-i', '--pretty-print',
        action='store_true',
        required=False, default=False,
        help=option_r_help,
    )

    return arg_parser.parse_args()


def _build_uri(args):
    f = furl()
    f.scheme = 'amqp'
    f.username = args.username
    f.password = args.password
    f.hostname = args.hostname
    f.path = args.virtualhost
    return str(f)


def _main_loop(args):
    uri = _build_uri(args)
    serializer = JsonSerializer(args.pretty_print)
    consumer = FirehoseJsonDumper(uri, serializer)
    consumer.start()


def main():
    args = _parse_args()
    _main_loop(args)


if __name__ == '__main__':
    main()
