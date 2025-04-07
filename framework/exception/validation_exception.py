class ValidationException(Exception):
    def __init__(self, param: str, val: str, message: str):
        self.param = param
        self.val = val
        self.message = message
        super().__init__(f"Validation failed [param:{param} : {message} (val: {val})]")

