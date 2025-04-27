import hashlib
import os


def get_password_hash(password: str) -> str:
    """Hashes a password using SHA-256 with a salt."""
    # Generate a random salt
    salt = os.urandom(16)  # 16 bytes salt
    # Create a sha256 hash of the password and salt
    password_hash = hashlib.sha256(salt + password.encode("utf-8")).hexdigest()
    # Return the salt and hashed password concatenated together (so we can later verify)
    return f"{salt.hex()}${password_hash}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verifies if the provided password matches the stored hash."""
    # Split the stored hash into salt and hash components
    salt_hex, stored_password_hash = stored_hash.split("$")
    salt = bytes.fromhex(salt_hex)

    # Hash the provided password with the stored salt
    provided_hash = hashlib.sha256(salt + plain_password.encode("utf-8")).hexdigest()

    # Compare the provided hash with the stored hash
    return provided_hash == stored_password_hash
