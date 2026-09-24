from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

recommendations = {
    "Plastic": {
        "reuse": "Reuse clean plastic containers for storage.",
        "repair": "Repair reusable plastic items when practical.",
        "donate": "Donate clean, usable containers to someone who needs them.",
        "recycle": "Check local recycling rules for the plastic type."
    },

    "Paper": {
        "reuse": "Reuse one-sided paper for notes or rough work.",
        "repair": "Repair torn books with suitable binding materials.",
        "donate": "Donate readable books and notebooks.",
        "recycle": "Recycle clean, dry paper."
    },

    "Metal": {
        "reuse": "Reuse clean metal containers for storage.",
        "repair": "Repair damaged metal items when practical.",
        "donate": "Donate usable utensils or metal household items.",
        "recycle": "Send scrap metal to an appropriate recycling facility."
    },

    "Glass": {
        "reuse": "Reuse intact glass jars for storage.",
        "repair": "Ask a professional about repairing valuable glass items.",
        "donate": "Donate intact, usable glass containers.",
        "recycle": "Recycle glass according to local collection rules."
    },

    "Organic": {
        "reuse": "Use suitable food scraps for composting.",
        "repair": "Not usually applicable to organic waste.",
        "donate": "Share safe, edible surplus food through suitable food donation services.",
        "recycle": "Compost suitable organic waste."
    },

    "Electronic": {
        "reuse": "Reuse working electronics or accessories.",
        "repair": "Consult a qualified technician for repair.",
        "donate": "Donate working devices through a suitable organization.",
        "recycle": "Use an authorized e-waste collection or recycling center."
    },

    "Textile": {
        "reuse": "Turn old fabric into cleaning cloths or useful crafts.",
        "repair": "Sew small tears or replace missing buttons.",
        "donate": "Donate clean, wearable clothes.",
        "recycle": "Find a textile recycling collection point."
    }
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "waste_image" not in request.files:
        return "Please select an image."

    file = request.files["waste_image"]
    category = request.form.get("category", "")

    if file.filename == "":
        return "Please select an image."

    if category not in recommendations:
        return "Please select a valid waste category."

    filename = os.path.basename(file.filename)

    if not filename:
        return "Invalid file name."

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    result = recommendations[category]

    return f"""
    <html>
    <head>
        <title>ReLife AI Recommendations</title>
    </head>

    <body style="font-family:Arial; padding:40px; background:#f4f8f3;">

        <h1 style="color:#27834b;">♻️ ReLife AI Results</h1>

        <h2>Waste Category: {category}</h2>

        <h3>♻️ Reuse</h3>
        <p>{result['reuse']}</p>

        <h3>🔧 Repair</h3>
        <p>{result['repair']}</p>

        <h3>💚 Donate</h3>
        <p>{result['donate']}</p>

        <h3>🌱 Recycle</h3>
        <p>{result['recycle']}</p>

        <br>
        <a href="/">Back to Home</a>

    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True)