import flask
from flask import request
from werkzeug.datastructures import MultiDict


class BaseViewModel:

    def __init__(self):
        self.req = request
        self.req_dict = create_dict("")
        self.errors = {}
        self.htmx_req = 'HX-Request' in flask.request.headers

    @classmethod
    def validate(cls):
        obj = cls()
        obj.validation()
        return obj

    def validation(self):
        pass

    def to_dict(self):
        return self.__dict__


class Req2Dict(dict):
    """
    Req2Dict

    This class extends the built-in `dict` class and provides a convenient way to convert a Flask request object into a dictionary-like object.

    Methods:
        - __init__(self, *args, def_val=None, **kwargs): Initializes a new instance of Req2Dict.
        - __getattr__(self, key): Retrieves the value of the specified key from the dictionary.

    Attributes:
        - def_val: The default value to be returned if a key is not found in the dictionary.

    Usage:
        req = request
        req_dict = Req2Dict(req.args, def_val='N/A')
        value = req_dict.some_key

    Example:
        req = request
        req_dict = Req2Dict(req.args, def_val='N/A')
        some_value = req_dict.some_key

        If the 'some_key' is present in req.args, its value will be assigned to 'some_value'. Otherwise, 'N/A' will be assigned to 'some_value'.
    """
    def __init__(self, *args, def_val=None, **kwargs):
        self.def_val = def_val
        super().__init__(*args, **kwargs)

    def __getattr__(self, key):
        return self.get(key, self.def_val)


def create_dict(def_val=None, **kwargs):
    """
    :param def_val: The default value to assign to any missing key in the final dictionary (default is None).
    :param kwargs: Keyword arguments that will be merged into the final dictionary.
    :return: A dictionary created from combining the request arguments, headers, form data, and additional keyword arguments.
    """
    req = request
    args = req.args

    if isinstance(req.args, MultiDict):
        args = req.args.to_dict()

    form = req.form
    if isinstance(req.args, MultiDict):
        form = req.form.to_dict()

    files = req.files
    if isinstance(req.files, MultiDict):
        files = req.files.to_dict()


    data = {
        **args,
        **req.headers,
        **form,
        **files,
        **kwargs
    }

    return Req2Dict(data, def_val=def_val)
