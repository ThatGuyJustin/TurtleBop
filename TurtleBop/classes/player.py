from disco.voice import VoiceConnection, YoutubeDLPlayable
from TurtleBop.models.guild import Guild

class MusicPlayer():

    def __init__(self, event, vs):
        self.guild = event.guild
        self.db_guild = Guild.using_id(event.guild.id)
        self.queue = [] #UserID, YTDL-Data
        self.player = VoiceConnection.from_channel(vs.channel, enable_events=True)
        self.volume = 50 # Guild.default_volume
    
    def current_playing(self):
        pass
    
    def get_queue(self):
        pass
    
    def set_volume(self, volume):
        # Testing to set volume
        dec = volume / 100
        self.player.set_volume(dec)

    def play(self, data, event):

        self.player.play(data)
        self.queue.append(Queue(event.author.id, data))

class Queue(object):

    def __init__(self, user, data):
        self.user = user
        self.data = data