# 📝 SummarAIze – Flask Text Summarization App

A web-based text summarization system built using Flask that allows users to generate concise summaries from large text inputs or uploaded `.txt` files. The application optionally integrates with AWS S3 for file storage, making it scalable and cloud-ready.

---

## 🌐 Live Demo

https://summaraize-flask-app.onrender.com

---

## 🚀 Features

* ✍️ Input text manually or upload `.txt` files
* 📄 Generate concise summaries using NLP techniques
* ⬇️ Download summarized output as a file
* ☁️ Optional AWS S3 integration
* 🔒 Secure file handling and validation
* ⚡ Lightweight and fast Flask backend

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS (Jinja Templates)
* **Cloud (Optional):** AWS S3 (boto3)

**Libraries Used:**

* Flask
* nltk
* boto3
* gunicorn
* werkzeug

---

## 📁 Project Structure

```
SUMMARAIZE/
│
├── static/              # CSS, JS, assets
├── templates/           # HTML templates
│   ├── index.html
│   └── result.html
│
├── uploads/             # Uploaded and generated files
├── utils/
│   └── summarizer.py    # Core summarization logic
│
├── app.py               # Main Flask application
├── requirements.txt     # Dependencies
├── runtime.txt          # Python version for deployment
├── README.md
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```
git clone https://github.com/your-username/summaraize-flask-app.git
cd summaraize-flask-app
```

---

### 2. Create Virtual Environment

```
python -m venv venv
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows
```

---

### 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 4. Run the Application

```
python app.py
```

---

### 5. Open in Browser

```
http://127.0.0.1:5000
```

---

## 📌 Usage

1. Enter text or upload a `.txt` file
2. Click **Summarize**
3. View the generated summary
4. Download the result

---

## ⚠️ Constraints

* Only `.txt` files are supported
* Maximum file size: **2 MB**
* Maximum input length: **20,000 characters**

---

## ☁️ AWS S3 Integration (Optional)

Set environment variables:

```
S3_BUCKET=your-bucket-name
S3_REGION=your-region
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

---

## 🌍 Deployment

This project is deployed using Render.

**Build Command**

```
pip install -r requirements.txt
```

**Start Command**

```
gunicorn app:app
```

---

## 🔐 Security

* Secure file uploads using `werkzeug`
* Environment variables for sensitive data
* Input validation and size restrictions

---

## 📸 Future Improvements

* Support PDF/DOCX files
* Improve NLP summarization model
* Add user authentication
* Enhance UI/UX
* Real-time preview

---

## 👨‍💻 Author

**Sri Ahilesh**

---

## 📄 License

This project is licensed under the MIT License.

---

## 💡 Final Note

This project demonstrates backend development, NLP integration, file handling, and cloud deployment—making it a strong portfolio-ready application.
