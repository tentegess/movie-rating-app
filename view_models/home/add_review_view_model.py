from view_models.base_view_model import BaseViewModel


class AddReviewViewModel(BaseViewModel):

    def __init__(self):
        super().__init__()
        self.rating = self.req_dict.rating
        self.header = self.req_dict.header
        self.review = self.req_dict.review
