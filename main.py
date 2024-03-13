import pyttsx3
from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm,CSRFProtect
from wtforms import SubmitField,FileField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
import PyPDF2
import os
app = Flask(__name__)
Bootstrap5(app)

app.config["SECRET_KEY"] = "jhskdjfhidsfhdk"
csrf = CSRFProtect(app)

# # Initialize the TTS engine
engine = pyttsx3.init()

engine.setProperty('rate', 150)    # Speed of speech (words per minute)
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

voices = engine.getProperty('voices')

# Select the voice you want to use
# Example: voice with index 1 (usually a female voice)
engine.setProperty('voice', voices[1].id)

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class UploadForm(FlaskForm):
    file=FileField("Upload Your File",validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/',methods=["POST","GET"])
def home():
    upload = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join('uploads',filename)
        file.save(file_path)

        with open(file_path, 'rb') as data:
            reader = PyPDF2.PdfReader(data)
            text = ''
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
            print(text)
        engine.say(text)
        engine.runAndWait()
        return "File Uploaded Successfully"

    return render_template('user.html',form=upload)


if __name__ == "__main__":
    app.run(debug=True)
