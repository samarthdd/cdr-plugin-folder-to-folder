from osbot_utils.utils.Misc import datetime_now


class Status:

    def __init__(self):
        pass

    def now(self):
        data = {
            "date": datetime_now()
        }

        return data