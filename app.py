from flask import Flask, request, send_file, render_template
from PIL import Image
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_images():

    if 'images' not in request.files:
        return "No images uploaded"

    files = request.files.getlist("images")

    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)

    for file in files:

        image = Image.open(file.stream)

        if image.mode != "RGB":
            image = image.convert("RGB")

        temp_name = "temp_image.jpg"
        image.save(temp_name)

        c.drawImage(temp_name, 0, 0, width=letter[0], height=letter[1])
        c.showPage()

        os.remove(temp_name)

    c.save()
    pdf_buffer.seek(0)

    return send_file(pdf_buffer,
                     as_attachment=True,
                     download_name="converted.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
