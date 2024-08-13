import qrcode
import time
from pathlib import Path
from apps.common.service import BaseModelService
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


class QRCodeService(BaseModelService):
    model = None
    search_keywords = []

    def __init__(self, data=None, file_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
        self.file_path = file_path
        self.version = kwargs.get("version", 1)
        self.box_size = kwargs.get("box_size", 10)
        self.border = kwargs.get("border", 4)
        self.fill_color = kwargs.get("fill_color", "black")
        self.back_color = kwargs.get("back_color", "white")
        self.error_correction = qrcode.constants.ERROR_CORRECT_L

    def generate(self):
        qr = qrcode.QRCode(
            version=self.version,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(self.data)
        qr.make(fit=True)

        image = qr.make_image(fill_color=self.fill_color, back_color=self.back_color)
        return image

    def generate_and_save_in_storage(self):
        image_data = None
        image = self.generate()

        # temporary save file in container for creating storage object
        temp_image_path = f"temp_data_{time.time()}.png"
        image.save(temp_image_path)
        with open(temp_image_path, "rb") as file:
            image_data = file.read()

        # save file into Default Storage
        final_path = default_storage.save(self.file_path, ContentFile(image_data))

        # remove temporary file
        Path(temp_image_path).unlink()
        return final_path
