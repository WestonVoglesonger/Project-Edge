class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.message = f"User with id {user_id} not found."
        super().__init__(self.message)

class EmailAlreadyRegisteredException(Exception):
    """Exception raised when an email is already registered."""
    def __init__(self, email: str):
        self.email = email
        self.message = f"Email {email} is already registered."
        super().__init__(self.message)

class TagNotFoundException(Exception):
    """Exception raised when a tag is not found."""
    def __init__(self, tag_id: int):
        self.tag_id = tag_id
        self.message = f"User with id {tag_id} not found."
        super().__init__(self.message)

class CredentialsException(Exception):
    """Exception raised when the credentials could not be validated"""
    def __init__(self):
        self.message="Could not validate credentials"
        super().__init__(self.message)

class ProjectNotFoundException(Exception):
    """Exception raised when a project is not found."""
    pass
