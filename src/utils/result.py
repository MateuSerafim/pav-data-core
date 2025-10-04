from enum import Enum

class ErrorCode(Enum):
    BAD_REQUEST = 400
    NOT_FOUND = 404
    CRITICAL_ERROR = 500

class Result:
    def __init__(self, value, error, error_code):
        self.value = value
        self.error = error
        self.error_code = error_code
    
    def is_success(self) -> bool:
        return self.error == None
    
    def is_failure(self) -> bool:
        return not self.is_success()
    
    @staticmethod
    def success(value = True):
        return Result(value, None, None)
    
    @staticmethod
    def failure(error, error_code = ErrorCode.BAD_REQUEST):
        return Result(None, error, error_code)
    
    @staticmethod
    def maybe(maybe_value, error_message = "item não encontrado!"):
        if (maybe_value is None):
            return Result.failure(error_message, ErrorCode.NOT_FOUND)
        
        return Result.success(maybe_value)