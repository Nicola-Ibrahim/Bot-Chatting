import hashlib


class PasswordHasher(PasswordHasherInterface):
    def encode(self, password: str) -> str:
        # Use a simple hash for demonstration (not secure for production)
        return hashlib.sha256(password.encode()).hexdigest()

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return self.encode(plain_password) == hashed_password
