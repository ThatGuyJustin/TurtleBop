# -*- coding: utf-8 -*-
import yaml
import re
import requests
import functools
import gevent
import psutil
import os
import json

from datetime import datetime, timedelta

from disco.types.message import MessageTable, MessageEmbed, MessageEmbedField, MessageEmbedThumbnail
from disco.api.http import APIException
from disco.bot import Bot, Plugin, CommandLevels
from disco.bot.command import CommandEvent
from disco.types.message import MessageEmbed
from disco.types.user import GameType, Status, Game
from disco.types.channel import ChannelType
from disco.util.sanitize import S

from TurtleBop import bot_config, Emitter
from TurtleBop.models.guild import Guild


class DevPlugin(Plugin):
    global_plugin = True

    def load(self, ctx):
        super(DevPlugin, self).load(ctx)

    @Plugin.command('botstats', aliases=['bs', 'sys'], group='dev', level=-1)
    def cmd_systen_stats(self, event):
        embed = MessageEmbed()
        embed.title = "Bot Stats"
        description = [
            "**Total Servers**: {}".format(str(len(self.client.state.guilds))),
            "**Total Users**: {}".format(str(len(self.client.state.users))),
            # "**Total Global Songs Played**: {}".format(Games.select(Games).count()),
            "\n",
            "__**System Stats**__",
            "**CPU Usage**: {}%".format(str(psutil.cpu_percent(interval=1))),
            "**Ram Usage**: {}%".format(str(psutil.virtual_memory().percent))
        ]
        embed.description = '\n'.join(description)
        event.msg.reply('', embed=embed)