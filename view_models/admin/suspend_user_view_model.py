from view_models.base_view_model import BaseViewModel
from utils.re_patterns import PASS_PT, EMAIL_PT, LETTERS_NUMS
from utils import LANG
from models.Users import Users
import re


class SuspendUserViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.ban_time = self.req_dict.ban_time
        self.permanent = True if self.req_dict.permanent else False
        self.reason = str(self.req_dict.reason)

    def validation(self):
        super().validation()

        if not self.permanent and not self.ban_time:
            self.errors["ban"] = LANG.BAN_TIME_REQUIRED





