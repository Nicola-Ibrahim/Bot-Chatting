class UsernameUniquenessChecker:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def is_unique(self, username: str) -> bool:
        if self.user_repository.find_user_by_username(username):
            return False
        return True
