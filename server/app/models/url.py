import datetime


class UrlModel:
    """
    Representation of a URL object.
    """

    def __init__(self,
                 full_url, shortcode, created_by_ip,
                 created_at=datetime.datetime.now(),
                 expires_at=datetime.datetime.now() + datetime.timedelta(weeks=24)
                 ):
        self.shortcode = shortcode
        self.full_url = full_url
        self.created_at = created_at
        self.expires_at = expires_at
        self.created_by_ip = created_by_ip

    def json(self):
        return {
            "shortcode": self.shortcode,
            "full_url": self.full_url,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "created_by_ip": self.created_by_ip
        }
