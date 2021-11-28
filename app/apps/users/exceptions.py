class ErrorCodes:
    CODE_FAILED_GETTING_DATA_FROM_EXTERNAL_API = 400


class UserGeneratorException(Exception):
    def __init__(self, *args, error_code, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_code = error_code
