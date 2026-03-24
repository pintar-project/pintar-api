import cloudinary
import cloudinary.uploader
from core import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_file(file_folder: str, file):
    return cloudinary.uploader.upload(file, folder=file_folder)
