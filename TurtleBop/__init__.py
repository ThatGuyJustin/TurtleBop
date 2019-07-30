# -*- coding: utf-8 -*-
from collections import namedtuple
from eventemitter import EventEmitter

import yaml
with open("config.yaml", 'r') as config_yml:
    base_config = yaml.safe_load(config_yml)

bot_config = namedtuple("config", base_config.keys())(*base_config.values())


def update_config():
    with open("config.yaml", 'r') as config_yml_new:
        new_base_config = yaml.safe_load(config_yml_new)
        bot_config = namedtuple(
            "config", new_base_config.keys()
        )(*new_base_config.values())


# YES_EMOJI = ':yes:594231233228177408'
# NO_EMOJI = ':no:594231233022525468'
# YES_EMOJI_ID = 594231233228177408
# NO_EMOJI_ID = 594231233022525468


def get_client():
    from disco.client import ClientConfig, Client

    config = ClientConfig()
    config.token = bot_config.token
    return Client(config)


class CustomEmitter(EventEmitter):
    pass


Emitter = CustomEmitter()

class CommandResponse(Exception):
    EMOJI = None

    def __init__(self, response):
        if self.EMOJI:
            response = '{} {}'.format(self.EMOJI, response)
        self.response = response

class CommandFail(CommandResponse):
    EMOJI = ':no_entry_sign: `Error`:'


class CommandSuccess(CommandResponse):
    EMOJI = ':ballot_box_with_check:'
