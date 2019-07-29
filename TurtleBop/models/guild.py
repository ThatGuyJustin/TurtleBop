from TurtleBop.db import BaseModel
from peewee import (BigIntegerField, IntegerField, TextField, BooleanField,
                    DoesNotExist)
from playhouse.postgres_ext import BinaryJSONField, ArrayField
from datetime import datetime  # , timedelta
from TurtleBop import Emitter


@BaseModel.register
class Guild(BaseModel):
    guild_id = BigIntegerField(primary_key=True)
    owner_id = BigIntegerField(null=False)
    prefix = TextField(default="+", null=False)
    dj_roles = ArrayField(BigIntegerField, null=True, index=False)
    mod_role = BigIntegerField(null=True)
    commands_disabled_channels = ArrayField(
        BigIntegerField, null=True, index=False
    )
    logs_enabled = BooleanField(default=True)
    log_channel = BigIntegerField(null=True)

    class Meta:
        db_table = 'guilds'

    @classmethod
    def get_settings(cls, guild_id):
        try:
            return Guild.get(guild_id=guild_id)
        except Guild.DoesNotExist:
            return

    @classmethod
    def using_id(cls, guild_id):
        return Guild.get(guild_id=guild_id)