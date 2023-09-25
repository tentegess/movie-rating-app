from view_models.base_view_model import BaseViewModel
from utils import LANG


class ForgotPsdViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.name = str(self.req_dict.name)

    def validation(self):
        super().validation()

        if not self.name:
            self.errors["name"] = LANG.EMPTY_LOGIN
        elif len(self.name) < 3 or len(self.name) > 64:
            self.errors["name"] = LANG.WRONG_LOGIN_LEN
