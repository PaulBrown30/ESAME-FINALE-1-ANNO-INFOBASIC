

class AppException(Exception):
    def __init__(self, message,status):
        super().__init__(message)
        self.message = message
        self.status = status

    def to_dict(self):
        return {
            "message": self.message,
            "status": self.status
            }