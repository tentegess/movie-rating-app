from view_models.base_view_model import BaseViewModel
from utils import LANG
import flask


class AddMovieViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.title = self.req_dict.title
        self.desc = self.req_dict.desc
        self.release = self.req_dict.release
        self.poster = self.req_dict.poster if self.req_dict.poster else None

    def validation(self):
        super().validation()

        if not self.title:
            self.errors["title"] = LANG.TITLE_REQUIRED

        if self.poster:
            if self.poster.content_type not in ["image/jpeg", "image/png"]:
                self.errors["poster"] = LANG.WRONG_PHOTO_FORMAT


