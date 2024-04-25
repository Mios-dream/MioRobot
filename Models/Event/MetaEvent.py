class MetaEvent:

    def __init__(self, data: dict):

        self.Post_Type = data.get("post_type", None)
