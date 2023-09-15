from src.db.models import Video
from src.repositories.base import BaseRepository


class VideoRepository(BaseRepository):
    model = Video
