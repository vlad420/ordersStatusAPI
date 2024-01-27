import os


def get_chrome_profile_path():
    # Calea standard pe Windows
    return os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data')
