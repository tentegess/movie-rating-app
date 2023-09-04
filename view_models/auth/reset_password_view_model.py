from view_models.base_view_model import BaseViewModel
from utils.re_patterns import PASS_PT, EMAIL_PT, LETTERS_NUMS
from utils import LANG
from models.Users import Users
import re


class ResetPasswordViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.password = str(self.req_dict.password)
        self.confirm_password = str(self.req_dict.confirm_password)

    def validation(self):
        super().validation()

        if not self.password:
            self.errors["password"] = LANG.EMPTY_PASSWORD
        elif len(self.password) < 8 or len(self.password) > 32:
            self.errors["password"] = LANG.WRONG_PASSWORD_LEN
        elif not re.match(PASS_PT, self.password):
            self.errors["password"] = LANG.WRONG_PASSWORD_FORMAT

        if self.password != self.confirm_password:
            self.errors["password"] = LANG.NOT_EQUAL_PASSWORD
        if (not self.confirm_password and self.password) or (self.confirm_password and not self.password):
            self.errors["password"] = LANG.NOT_REPEAT_PASSWORD




