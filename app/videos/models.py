import uuid
from app.config import get_settings
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from app.users.exceptions import InvalidUserIDException
from app.users.models import User

from .extractors import extract_video_id
from .exceptions import InvalidYouTubeVideoURLException, VideoAlreadyAddedException

settings = get_settings()


class Video(Model):
    __keyspace__ = settings.ASTRADB_KEYSPACE
    host_id = columns.Text(primary_key=True)  # a part of YouTube link
    db_id = columns.UUID(primary_key=True, default=uuid.uuid1)  #  UUID1
    host_service = columns.Text(default='youtube')
    url = columns.Text()  # secure
    user_id = columns.UUID()       # owner
    title = columns.Text()
    # user_display_name

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Video(host_id={self.host_id}, host_service={self.host_service})'

    def render(self):
        """
        метод для получения шаблона сервиса. Для работы с сервисами помимо YouTube
        """
        from app.main import templates  # because of a circular import error
        basename = self.host_service
        template_name = f'videos/renderers/{basename}.html'
        context = {'host_id': self.host_id}
        t = templates.get_template(template_name)
        return t.render(context)

    def as_data(self):
        return {f'{self.host_service}_id': self.host_id, 'path': self.path}

    @property
    def path(self):
        return f"/videos/{self.host_id}"  # get a link like '/videos/vnSVYUJrAZU'

    @staticmethod
    def add_video(url, user_id=None, **kwargs):
        host_id = extract_video_id(url)  #vnSVYUJrAZU
        if host_id is None:
            raise InvalidYouTubeVideoURLException('Invalid YouTube Video URL')
        user_exists = User.check_exists(user_id)
        if user_exists is None:
            raise InvalidUserIDException('Invalid user_id')
        q = Video.objects.allow_filtering().filter(host_id=host_id, user_id=user_id)
        if q.count() != 0:
            raise VideoAlreadyAddedException('Video already added')
        return Video.create(host_id=host_id, user_id=user_id, url=url, **kwargs)
