from flask import Flask, render_template, request, send_file
import qrcode
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json
    text = data["text"]
    mode = data["mode"]

    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )

    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(
        fill_color=data["dark"],
        back_color=data["light"]
    ).convert("RGB")

    if mode == "brand":
        logo_data = data["logo"].split(",")[1]
        logo = Image.open(
            BytesIO(base64.b64decode(logo_data))
        ).convert("RGBA")

        logo.thumbnail((img.width // 3, img.height // 3))

        x = (img.width - logo.width) // 2
        y = (img.height - logo.height) // 2

        img.paste(logo, (x, y), logo)

    img = img.resize((int(data["size"]), int(data["size"])))

    output = BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    return send_file(
        output,
        mimetype="image/png",
        as_attachment=True,
        download_name="VS_QR.png"
    )

if __name__ == "__main__":
    app.run(debug=True)