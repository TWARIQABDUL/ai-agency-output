import os
import secrets
import stat

SECRET_KEY_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.flasksecret')

def _ensure_secure_permissions(filepath):
    expected_mode = 0o600
    try:
        os.chmod(filepath, expected_mode)
        st = os.stat(filepath)
        if (st.st_mode & 0o777) != expected_mode:
            raise RuntimeError(
                f"Permissions for '{filepath}' could not be set or verified to {oct(expected_mode)}. "
                "It might exist with insecure permissions. Consider deleting it and using the SECRET_KEY environment variable."
            )
    except OSError as e:
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except OSError:
                pass
        raise RuntimeError(
            f"Failed to set secure permissions ({oct(expected_mode)}) for SECRET_KEY file '{filepath}': {e}. "
            "Consider setting the SECRET_KEY environment variable instead."
        ) from e

def _load_or_generate_secret_key():
    env_secret_key = os.environ.get('SECRET_KEY')
    if env_secret_key:
        return env_secret_key

    if os.path.exists(SECRET_KEY_FILE_PATH):
        _ensure_secure_permissions(SECRET_KEY_FILE_PATH)
        try:
            with open(SECRET_KEY_FILE_PATH, 'r') as f:
                file_secret_key = f.read().strip()
            if file_secret_key:
                return file_secret_key
        except IOError as e:
            raise RuntimeError(f"Failed to read existing SECRET_KEY file '{SECRET_KEY_FILE_PATH}': {e}.") from e

    new_secret_key = secrets.token_hex(32)
    try:
        with open(SECRET_KEY_FILE_PATH, 'w') as f:
            f.write(new_secret_key)
    except IOError as e:
        raise RuntimeError(f"Failed to write SECRET_KEY file '{SECRET_KEY_FILE_PATH}': {e}.") from e
    
    _ensure_secure_permissions(SECRET_KEY_FILE_PATH)
    
    return new_secret_key

class Config:
    SECRET_KEY = _load_or_generate_secret_key()
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False