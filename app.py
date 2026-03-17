from flask import Flask, request, send_file, render_template
from PIL import Image
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    files = request.files.getlist("images")  # get all uploaded images
    pdf_buffer = io.BytesIO()

    # Create a blank PDF using Pillow
    image_list = []
    for file in files:
        img = Image.open(file).convert("RGB")  # ensure RGB mode
        image_list.append(img)

    # Save all images into one PDF
    if image_list:
        image_list[0].save(
            pdf_buffer,
            save_all=True,
            append_images=image_list[1:],  # add remaining images
            format="PDF"
        )

    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name="converted.pdf")

if __name__ == "__main__":
    app.run(debug=True)
