class BaseException(Exception):
    def __init__(self, message=''): Exception.__init__(self, message)


class not_found_city(BaseException):
    def __init__(self):
        self.message = "not_found_city"


class not_found_poi(BaseException):
    def __init__(self, available_tags=None):
        self.message = "not_found_poi"
        self.available_tags = available_tags