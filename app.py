import os
from flask import Flask, render_template, request, jsonify
from downloader import download_video

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/browse")
def browse():
    path = request.args.get("path", os.path.expanduser("~"))
    path = os.path.abspath(path)

    if not os.path.isdir(path):
        return jsonify({"error": "Not a valid directory"}), 400

    entries = []
    try:
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            if os.path.isdir(full) and not name.startswith("."):
                entries.append(name)
    except PermissionError:
        return jsonify({"error": "Permission denied"}), 403

    parent = os.path.dirname(path)
    return jsonify({"current": path, "parent": parent, "folders": entries})


@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url", "").strip()
    folder = data.get("folder", "").strip()

    if not url:
        return jsonify({"success": False, "error": "URL is required"}), 400
    if not folder or not os.path.isdir(folder):
        return jsonify({"success": False, "error": "Invalid output folder"}), 400

    result = download_video(url, folder)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
