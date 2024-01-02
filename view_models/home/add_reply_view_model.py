from utils import LANG
from view_models.base_view_model import BaseViewModel


class AddReplyViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.reply = self.req_dict.reply

    def validation(self):
        super().validation()

        if not self.reply:
            self.errors["reply"] = LANG.REPLY_REQUIRED
