from apps.common.service import BaseModelService


class BarCodeService(BaseModelService):
    model = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
