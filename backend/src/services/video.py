from src.repositories.video import VideoRepository
from src.schemas import Video
from src.services.base import BaseService


class VideoService(BaseService):
    model = Video

    def __init__(self):
        super().__init__()
        self.repo = VideoRepository()
