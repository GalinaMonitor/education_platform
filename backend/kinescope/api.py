from typing import List, Optional

from pydantic import BaseModel, parse_obj_as
from requests import Session

from settings import settings


class VideoAsset(BaseModel):
    video_id: str
    quality: str
    download_link: str


class FileAsset(BaseModel):
    title: str
    filename: str
    url: str


class Video(BaseModel):
    id: str
    title: str
    play_link: str
    assets: List[VideoAsset]
    additional_materials: List[FileAsset]


# TODO Обработать запрос с пагинацией. Сейчас стоит per_page=3000
class KinescopeClient:
    def __init__(self) -> None:
        self.session = Session()
        self.session.headers.update({f"Authorization": f"Bearer {settings.kinescope_api_key}"})

    def get_project_video_list(self, project_id: str, video_ids: Optional[List[str]] = None) -> List[Video]:
        if video_ids:
            video_ids_param = ",".join(video_ids)
            response = self.session.get(
                f"https://api.kinescope.io/v1/videos/"
                f"?order=title.asc"
                f"&per_page=3000"
                f"&project_id={project_id}"
                f"&video_ids[]={video_ids_param}"
            )
        else:
            response = self.session.get(
                f"https://api.kinescope.io/v1/videos/" f"?order=title.asc" f"&per_page=3000" f"&project_id={project_id}"
            )
        video_list = parse_obj_as(List[Video], response.json()["data"])
        return video_list
