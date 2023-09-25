from view_models.base_view_model import BaseViewModel
from utils.re_patterns import PASS_PT, EMAIL_PT, LETTERS_NUMS
from utils import LANG
from models.Users import Users
import re


class AddUserViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.email = self.req_dict.email.lower()
        self.name = str(self.req_dict.name)
        self.password = str(self.req_dict.password)
        self.admin = True if self.req_dict.admin else False
        self.active = True if self.req_dict.active else False

    def validation(self):
        super().validation()

        if not self.email:
            self.errors["email"] = LANG.EMPTY_EMAIL
        elif not re.match(EMAIL_PT, self.email):
            self.errors["email"] = LANG.WRONG_EMAIL_FORMAT
        elif len(self.email) < 3 or len(self.email) > 64:
            self.errors["name"] = LANG.WRONG_EMAIL_LEN
        elif Users.query.filter_by(email=self.email).first():
            self.errors["email"] = LANG.EMAIL_EXIST

        if not self.name:
            self.errors["name"] = LANG.EMPTY_LOGIN
        elif not re.match(LETTERS_NUMS, self.name):
            self.errors["name"] = LANG.WRONG_LOGIN_FORMAT
        elif len(self.name) < 3 or len(self.name) > 24:
            self.errors["name"] = LANG.WRONG_LOGIN_LEN
        if Users.query.filter_by(name=self.name).first():
            self.errors["name"] = LANG.LOGIN_EXIST

        if not self.password:
            self.errors["password"] = LANG.EMPTY_PASSWORD
        elif len(self.password) < 8 or len(self.password) > 32:
            self.errors["password"] = LANG.WRONG_PASSWORD_LEN
        elif not re.match(PASS_PT, self.password):
            self.errors["password"] = LANG.WRONG_PASSWORD_FORMAT




