#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import uuid
import types
import inspect
from abc import ABCMeta, abstractmethod

from furl import furl
from kombu import Connection, Exchange, Queue


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

    def __init__(self, uri):
        super(FirehoseJsonDumper, self).__init__(uri)
        self.serializer = JsonSerializer()

    def on_message(self, msg):
        serialized_msg = self.serializer.serialize(msg)
        print(serialized_msg)


class MessageSerializer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def serialize(self, msg):
        pass


class JsonSerializer(MessageSerializer):

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
            lambda key, value: (
                not inspect.ismethod(key) and
                not inspect.isfunction(key)
            )
        )

        result = [
            (attr_name, self._encode(msg, attr_name, attr))
            for attr_name, attr in attrs if self._is_acceptable(attr)
        ]

        msg.ack()
        return json.dumps(result)


def _parse_args():
    description = 'RabbitMQ firehose dump script'

    option_n_help = 'Set RabbitMQ Hostname'
    option_u_help = 'Set RabbitMQ Username'
    option_w_help = 'Set RabbitMQ Password'
    option_v_help = 'Set RabbitMQ VirtualHost'

    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument(
        '-n', '--hostname',
        default='localhost',
        help=option_n_help,
    )
    arg_parser.add_argument(
        '-u', '--username',
        default='guest',
        help=option_u_help,
    )
    arg_parser.add_argument(
        '-w', '--password',
        default='guest',
        help=option_w_help,
    )
    arg_parser.add_argument(
        '-v', '--virtualhost',
        default='/',
        help=option_v_help,
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


def _main_loop(uri):
    consumer = FirehoseJsonDumper(uri)
    consumer.start()


def main():
    args = _parse_args()
    uri = _build_uri(args)
    _main_loop(uri)


if __name__ == '__main__':
    main()
