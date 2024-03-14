# utils.py
def user_directory_path(instance, filename):
    return 'profile_images/{0}/{1}'.format(instance.user.username, filename)
