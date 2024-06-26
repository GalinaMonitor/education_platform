from fastapi import Depends

from src.repositories.theme import ThemeRepository
from src.schemas import Theme
from src.services.base import BaseService


class ThemeService(BaseService):
    model = Theme

    def __init__(self, repo: ThemeRepository = Depends()):
        super().__init__()
        self.repo = repo
