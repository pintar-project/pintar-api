import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os

# Konfigurasi
cloudinary.config(
    cloud_name="ducs7evff",
    api_key="425416258425381",
    api_secret="QuASIRLKoNTzg-5PZ4_PKtHE7BI",
)


def upload_pdf_and_thumbnail(file_path, base_public_id):
    results = {}

    try:
        # 1. Upload sebagai PDF Asli (Resource Type: RAW)
        # Ini digunakan agar user bisa mendownload file aslinya
        print(f"Mengunggah file asli (PDF): {file_path}...")
        raw_upload = cloudinary.uploader.upload(
            file_path,
            public_id=f"{base_public_id}_file",
            resource_type="raw",
            overwrite=True,
        )
        results["pdf_url"] = raw_upload["secure_url"]

        # 2. Upload sebagai Image (Resource Type: IMAGE)
        # Ini digunakan khusus untuk generate thumbnail/preview halaman [cite: 418]
        print(f"Mengunggah versi thumbnail: {file_path}...")
        image_upload = cloudinary.uploader.upload(
            file_path,
            public_id=f"{base_public_id}_thumb",
            resource_type="image",
            overwrite=True,
        )

        # Generate URL Thumbnail dari halaman 1 (Contoh: Identitas Modul SMAN 34) [cite: 5, 26, 418]
        thumb_url, _ = cloudinary_url(
            f"{base_public_id}_thumb",
            resource_type="image",
            format="jpg",
            width=300,
            height=450,
            crop="fill",
            page=1,  # Mengambil halaman utama [cite: 5]
        )
        results["thumbnail_url"] = thumb_url

        return results

    except Exception as e:
        return f"Gagal: {e}"


file_target = "./XII_Sosiologi_KD-3.3_FINAL.pdf"
res = upload_pdf_and_thumbnail(file_target, "modul_sosiologi_12")

if isinstance(res, dict):
    print(f"\n--- Berhasil Diunggah ---")
    print(f"Link Download PDF: {res['pdf_url']}")
    print(f"Link Thumbnail Preview: {res['thumbnail_url']}")
