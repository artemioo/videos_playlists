import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

from app.users.models import User
from app.videos.extractors import extract_video_id

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    host_id = columns.Text(primary_key=True)  # YouTube
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1) # UUID1
    host_service = columns.Text(default='youtube')
    url = columns.Text()  # secure
    user_id = columns.UUID()       # owner
    title = columns.Text()
    # user_display_name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Video(host_id={self.host_id}, host_service={self.host_service})'

    @staticmethod
    def add_video(url, user_id=None):
        host_id = extract_video_id(url)  #vnSVYUJrAZU
        if host_id is None:
            raise Exception('Invalid YouTube Video URL')
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise Exception('Invalid user_id')
        q = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise Exception('Video already added')
        return Video.create(host_id=host_id, user_id=user_id, url=url)
# https://www.youtube.com/watch?v=vnSVYUJrAZU