from apps.common.service import BaseModelService


class BarCodeService(BaseModelService):
    model = None
    search_keywords = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
