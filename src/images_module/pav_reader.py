import cv2
import numpy as np

from ..utils.result import Result

class ImageReader():
    def __init__(self, image_data, image_id):
        self.image_data = image_data
        self.image_id = image_id

    @staticmethod
    def read_from_blob_data(blob_data, image_id) -> Result:
        try:
            nparr = np.frombuffer(blob_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            return ImageReader(img, image_id)
        except Exception as e:
            return Result.failure(f"Erro ao ler a imagem: {str(e)}!")