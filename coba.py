from PIL import Image, ImageDraw, ImageFont


def edit_invoice_nft(input_path, output_path, donor_name, amount):
    # 1. Buka gambar original
    img = Image.open(input_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # 2. Setup Font (Pastikan kamu punya file .ttf di folder yang sama)
    # Jika di Linux Mint, biasanya ada di /usr/share/fonts/
    try:
        font_main = ImageFont.truetype("arial.ttf", 40)
        font_sub = ImageFont.truetype("arial.ttf", 25)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # 3. Buat Overlay untuk menutupi teks "[DONOR NAME]"
    # Koordinat ini perkiraan, kamu harus sesuaikan dengan posisi di gambar
    # [x0, y0, x1, y1]
    overlay_shape = [330, 360, 500, 400]
    draw.rectangle(overlay_shape, fill=(20, 50, 50, 255))  # Warna gelap sesuai bg

    # 4. Tulis Data Baru
    draw.text((340, 365), donor_name, fill="white", font=font_sub)
    draw.text((340, 435), f"$ {amount}", fill="#00ffcc", font=font_main)

    # 5. Simpan Hasil
    img = img.convert("RGB")  # Balikkan ke RGB untuk simpan sebagai JPG/PNG
    img.save(output_path)
    print(f"NFT Invoice berhasil dibuat: {output_path}")


# Jalankan fungsi
edit_invoice_nft("./unnamed.jpg", "nft_final.png", "Adit", "250.00")
