
class Utils(object):
    """This class allow one to create utility methods"""

    def __init__(self):
        pass

    def create_following_list(self, data):
        """This method creates a list from serialized following data"""
        username_list = []
        for a in data:
            username_list.append(a['username'])
        return username_list
