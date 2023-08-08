import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    host_id = columns.Text(primary_key=True)  # YouTube
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1) # UUID1
    host_servise = columns.Text(default='youtube')
    url = columns.Text()  # secure
    user_id = columns.UUID()       # owner
    title = columns.Text()
    # user_display_name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Video(email={self.email}, user_id={self.user_id})'

    @staticmethod
    def add_video(url, user_id=None):
        pass
