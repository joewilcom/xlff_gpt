from flask import Flask, render_template, request
from xlff_parser import parse_xlff, extract_xlff_from_docx

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    debug_message = None
    if request.method == 'POST':
        file = request.files['xlff_file']
        if file:
            filename = file.filename.lower()
            if filename.endswith('.docx'):
                xlff_xml = extract_xlff_from_docx(file)
                if xlff_xml:
                    result = parse_xlff(xlff_xml)
                else:
                    result = [{'source': 'Error', 'target': 'No XLFF XML found in Word document.'}]
            else:
                content = file.read().decode('utf-8')
                result = parse_xlff(content)
            debug_message = f"Parsed {len(result)} translation units. First: {result[0] if result else 'None'}"
    return render_template('index.html', result=result, debug_message=debug_message)

if __name__ == '__main__':
    app.run(debug=True)