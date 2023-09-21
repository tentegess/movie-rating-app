from view_models.base_view_model import BaseViewModel
from utils import LANG


class SearchUserViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.query = str(self.req_dict.query)
        print(self.req_dict)

