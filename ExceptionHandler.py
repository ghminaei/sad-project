class Error(Exception):
    pass

class UsernamaNotFound(Error):
    pass
    # def __init__(self, expression, message):
    #     self.expression = expression
    #     self.message = message

class PasswordNotValid(Error):
    pass
    # def __init__(self, expression, message):
    #     self.expression = expression
    #     self.message = message

class NotAValidCmd(Error):
    pass
    # def __init__(self, expression, message):
    #     self.expression = expression
    #     self.message = message
class NoLabratoryFound(Error):
    pass