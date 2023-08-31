from view_models.base_view_model import BaseViewModel
from utils import LANG


class LoginViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.name = str(self.req_dict.name)
        self.password = str(self.req_dict.password)

    def validation(self):
        super().validation()


        if not self.name:
            self.errors["name"] = LANG.EMPTY_LOGIN

        if not self.password:
            self.errors["password"] = LANG.EMPTY_PASSWORD


