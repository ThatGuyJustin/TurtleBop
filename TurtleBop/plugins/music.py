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

from TurtleBop import bot_config, Emitter, CommandFail, CommandSuccess
from disco.voice import VoiceConnection, YoutubeDLPlayable
from TurtleBop.models.guild import Guild
from TurtleBop.classes.player import MusicPlayer

class MusicPlugin(Plugin):
    global_plugin = True

    def load(self, ctx):
        super(MusicPlugin, self).load(ctx)
        self.players = {}
    
    @Plugin.command('join', aliases=['connect', 'LOVEME', '404smells', 'bigduck'], level=-1)
    def connect_to_voice(self, event):
        """
        Use this command to join me into a vc!
        """

        vs = event.guild.get_member(event.author).get_voice_state()
        
        if not vs:
            raise CommandFail('You\'re not in a voice channel.')
        if event.guild.id in self.players:
            if self.players[event.guild.id].channel_id == vs.channel_id:
                raise CommandFail('I\'m already in that channel.')
            else:
                self.players[event.guild.id].set_channel(vs.channel)
                return

        player = MusicPlayer(event, vs)

        self.players[event.guild.id] = player


    @Plugin.command('play', '<song:str>', level=-1)
    def on_play(self, event, song):
        """
        Use this command to play music!
        """

        if event.guild.id not in self.players:
            raise CommandFail('Not in a voice channel here.')

        playables = list(YoutubeDLPlayable.from_url(song))
        for playable in playables:
            self.players[event.guild.id].play(playable, event)
