import qrcode
import os

QR_FOLDER = "assets/qr"


def generate_qr(teacher_id):

    if not os.path.exists(QR_FOLDER):
        os.makedirs(QR_FOLDER)

    filename = f"{teacher_id}.png"

    filepath = os.path.join(QR_FOLDER, filename)

    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(f"teachtwin://{teacher_id}")
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save(filepath)

    return filepath
