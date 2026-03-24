import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from core import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)


def upload_file(file_folder: str, file):
    return cloudinary.uploader.upload(file, folder=file_folder)


def upload_pdf_with_thumbnail(file_folder: str, file):
    raw_upload = cloudinary.uploader.upload(
        file, folder=file_folder, resource_type="raw"
    )

    file.seek(0)

    image_upload = cloudinary.uploader.upload(
        file, folder=f"{file_folder}/thumbnails", resource_type="image"
    )

    thumb_url, _ = cloudinary_url(
        image_upload["public_id"],
        resource_type="image",
        format="jpg",
        width=300,
        height=450,
        crop="limit",
        page=1,
    )

    return {
        "pdf_url": raw_upload["secure_url"],
        "view_url": image_upload["secure_url"],
        "thumbnail_url": thumb_url,
    }
