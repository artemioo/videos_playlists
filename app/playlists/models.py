from datetime import datetime
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app import config
from app.videos.models import Video

settings = config.get_settings()


class Playlist(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)
    user_id = columns.UUID()
    updated = columns.DateTime(default=datetime.utcnow())
    hosts_id = columns.List(value_type=columns.Text)  # links to videos
    title = columns.Text()

    @property
    def path(self):
        return f'/playlists/{self.db_id}'

    def add_host_ids(self, host_ids=[], replace_all=False):
        if not isinstance(host_ids, list):
            return False
        if replace_all:
            self.hosts_id = host_ids
        else:
            self.hosts_id += host_ids
        self.updated = datetime.utcnow()
        self.save()
        return True

    def get_videos(self):
        videos = []
        for host_id in self.hosts_id:
            try:
                video_obj = Video.objects.get(host_id=host_id)
            except:
                video_obj = None
            if video_obj is not None:
                videos.append(video_obj)
        return videos