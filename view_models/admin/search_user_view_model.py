from view_models.base_view_model import BaseViewModel
from utils import LANG


class SearchUserViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.query = str(self.req_dict.query)
        self.admins = True if self.req_dict.only_admins else False
        self.suspended = True if self.req_dict.only_suspended else False
