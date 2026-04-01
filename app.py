import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
from utils.summarizer import summarize_text
import boto3

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"txt"}
MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = os.environ.get("FLASK_SECRET", "supersecretkey")

# Optional S3 config (set these env vars if you want S3 integration)
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_REGION = os.environ.get("S3_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file_to_s3(local_path, s3_key):
    if not S3_BUCKET:
        return None
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_ACCESS_KEY,
                      aws_secret_access_key=AWS_SECRET_KEY,
                      region_name=S3_REGION)
    s3.upload_file(local_path, S3_BUCKET, s3_key)
    s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"
    return s3_url

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # priority: file upload, else text area
        text_input = request.form.get("text_input", "").strip()
        file = request.files.get("file")
        if file and file.filename != "":
            if not allowed_file(file.filename):
                flash("Only .txt files are allowed.")
                return redirect(request.url)
            filename = secure_filename(file.filename)
            local_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(local_path)
            with open(local_path, "r", encoding="utf-8", errors="ignore") as f:
                text_input = f.read()
            # optional upload to S3
            if S3_BUCKET:
                upload_file_to_s3(local_path, f"uploads/{filename}")
        if not text_input:
            flash("Please provide text or upload a .txt file to summarize.")
            return redirect(request.url)
        # limit input length
        if len(text_input) > 20000:
            flash("Input text too large. Please submit under 20,000 characters.")
            return redirect(request.url)
        summary = summarize_text(text_input)
        # save summary to a file for download
        out_filename = "summary.txt"
        out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_filename)
        with open(out_path, "w", encoding="utf-8") as fo:
            fo.write(summary)
        return render_template("result.html", summary=summary)
    return render_template("index.html")

@app.route("/download")
def download():
    path = os.path.join(app.config['UPLOAD_FOLDER'], "summary.txt")
    if not os.path.exists(path):
        flash("No summary available. Generate a summary first.")
        return redirect(url_for("index"))
    return send_file(path, as_attachment=True, download_name="summary.txt")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
