import os

from flask import Flask, render_template, request, redirect, url_for
import zipfile
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import datetime

app = Flask(__name__)

# Defining a function to read PDF file
def read_pdf_file(file_path):
    resource_manager = PDFResourceManager()
    buffer = io.StringIO()
    laparams = LAParams()
    device = TextConverter(resource_manager, buffer, laparams=laparams)
    with open(file_path, 'rb') as fp:
        interpreter = PDFPageInterpreter(resource_manager, device)

        # Extract only the first page of the PDF
        for page in PDFPage.get_pages(fp, check_extractable=True, maxpages=1):
            interpreter.process_page(page)
        text = buffer.getvalue()

        # Extract only the first paragraph of the first page
        first_para = text.split('\\\\\\\\n\\\\\\\\n')[0]
    device.close()
    buffer.close()
    return first_para

def extract_information(file_path, search_term=None):
    # Create an empty list to store information extracted from files
    information = []
    # Loop through all files in the directory
    for filename in os.listdir(file_path):
        # Check if the file is a PDF file
        if filename.endswith('.pdf'):
            # Read the first paragraph of the PDF file
            first_para = read_pdf_file(os.path.join(file_path, filename))
            # Get the creation date of the file
            creation_date = datetime.datetime.fromtimestamp(os.path.getctime(os.path.join(file_path, filename)))
            # Add the information to the list
            information.append((filename, creation_date, first_para))
    # Filter the information based on the search term
    if search_term:
        information = [item for item in information if search_term.lower() in item[2].lower()]
    return information





@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the search term from the query parameter
    search_term = request.args.get('search')
    # Check if a file has been uploaded
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']
        # Extract the contents of the zip file
        with zipfile.ZipFile(io.BytesIO(uploaded_file.read()), 'r') as zip_ref:
            # Get the directory containing the files
            file_path = zip_ref.namelist()[0]
            # Extract the files to a temporary directory
            zip_ref.extractall('/tmp')
            # Extract information from the files
            information = extract_information('/tmp/' + file_path, search_term)
            # Render the HTML template with the information and search term
            return render_template('index.html', information=information, search_term=search_term)
    # Render the HTML template for uploading a file
    return render_template('upload.html')
if __name__ == '__main__':
    app.run(debug=True)



