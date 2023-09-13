from flask import Flask, render_template, request, send_file, abort
import xml.etree.ElementTree as ET
import os
import codecs
import xml.dom.minidom

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['GET', 'POST'])


def submit():
    try:
        # Get form data
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        gender = request.form['gender']

        # Create XML element
        user = ET.Element('user')
        name_elem = ET.SubElement(user, 'name')
        name_elem.text = name
        surname_elem = ET.SubElement(user, 'surname')
        surname_elem.text = surname
        age_elem = ET.SubElement(user, 'age')
        age_elem.text = age
        gender_elem = ET.SubElement(user, 'gender')
        gender_elem.text = gender

        # Add extra fields to XML element
        field_names = request.form.getlist('field_name[]')
        field_values = request.form.getlist('field_value[]')
        for i in range(len(field_names)):
            field_name = field_names[i]
            field_value = field_values[i]
            if field_name and field_value:
                field_elem = ET.SubElement(user, field_name.lower())
                field_elem.text = field_value

          # Pretty print XML
        xml_string = ET.tostring(user, encoding='utf-8')
        xml_parsed = xml.dom.minidom.parseString(xml_string)
        xml_pretty = xml_parsed.toprettyxml(indent='    ')

        # Write XML to file
        filename = request.form['filename']
        filepath = os.path.join('.', f"{filename}.xml")
        with codecs.open(filepath, "w", "utf-8") as f:
            f.write(xml_pretty)

        return 'Data saved successfully'
    except Exception as e:
        print(e)
        return 'Error: Could not save data'



@app.route('/download/<filename>')
def download(filename):
    try:
        filepath = os.path.join('.', f"{filename}.xml")
        return send_file(filepath, as_attachment=True)
    except FileNotFoundError:
        abort(404)


@app.route('/open', methods=['GET', 'POST'])
def open_file():
    files = [f for f in os.listdir('.') if f.endswith('.xml')]

    if request.method == 'POST':
        filename = request.form.get('filename')
        file = request.files.get('file')
        if file:
            content = file.read().decode('utf-8')
        elif filename:
            try:
                filepath = os.path.join('.', filename)
                with open(filepath, 'rb') as file:
                    content = file.read().decode('utf-8')
            except FileNotFoundError:
                return 'File not found.'
        else:
            return 'No file selected.'

        return render_template('open.html', files=files, content=content, filename=filename)

    else:
        return render_template('open.html', files=files)



@app.route('/edit', methods=['GET', 'POST'])
def edit():
    try:
        if request.method == 'POST':
            # Check if an XML file is provided for opening
            open_file = request.files.get('open_file')
            if open_file:
                # Read and decode the XML content
                xml_content = open_file.read().decode('utf-8')  # Change 'utf-8' to the actual encoding
                user = parse_xml(xml_content)
                return render_template('edit.html', user=user)

        # If no XML file is uploaded, display a blank form
        return render_template('edit.html', user={})

    except Exception as e:
        return str(e)


@app.route('/save', methods=['POST'])
def save():
    try:
        # Retrieve the edited user data from the form
        name = request.form.get('name')
        surname = request.form.get('surname')
        age = request.form.get('age')
        gender = request.form.get('gender')

        # Create an XML string with the updated user data
        xml_data = f'''
        <user>
            <name>{name}</name>
            <surname>{surname}</surname>
            <age>{age}</age>
            <gender>{gender}</gender>
        </user>
        '''

        # Construct the filename based on user input and add 'edited' to the filename
        filename = f"{name}_edited_v1.xml"  # Initial version number
        version = 1

        while os.path.isfile(filename):
            version += 1
            filename = f"{name}_edited_v{version}.xml"

        # Save edited file to the 'updates' folder
        update_filepath = os.path.join(UPDATE_FOLDER, filename)
        with open(update_filepath, 'w', encoding='utf-8') as file:
            file.write(xml_data)

        return render_template('success.html')

    except Exception as e:
        return str(e)
        
def parse_xml(xml_content):
    root = ET.fromstring(xml_content)

    user = {       
        'name': root.find('name').text,
        'surname': root.find('surname').text,
        'age': root.find('age').text,
        'gender': root.find('gender').text,
    }

    return user

@app.route('/view', methods=['GET', 'POST'])
def indexes():
    return render_template('indexes.html')

@app.route('/upload', methods=['POST'])
def upload():
    xml_file = request.files['xml_file']
    xml_data = xml_file.read()

    root = ET.fromstring(xml_data)

    user = {}
    user['name'] = root.find('name').text
    user['surname'] = root.find('surname').text
    user['age'] = root.find('age').text
    user['gender'] = root.find('gender').text
    user['occupation'] = root.find('occupation').text

    return render_template('view.html', user=user)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
