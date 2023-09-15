from src.db.models import Theme
from src.repositories.base import BaseRepository


class ThemeRepository(BaseRepository):
    model = Theme
