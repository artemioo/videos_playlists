from datetime import datetime
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config

settings = config.get_settings()


class Playlist(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    user_id = columns.UUID()
    updated = columns.DateTime(default=datetime.utcnow())
    hosts_id = columns.List(value_type=columns.Text)  # links to videos
    title = columns.Text()
