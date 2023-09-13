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



@app.route('/edit/<filename>', methods=['GET', 'POST'])

def edit(filename):
    try:
        filepath = os.path.join('.', f"{filename}.xml")
        tree = ET.parse(filepath)
        root = tree.getroot()

        if request.method == 'POST':
            # Update form data
            name = request.form['name']
            surname = request.form['surname']
            age = request.form['age']
            gender = request.form['gender']

            # Update XML element
            user_elem = root.find('user')
            name_elem = user_elem.find('name')
            name_elem.text = name
            surname_elem = user_elem.find('surname')
            surname_elem.text = surname
            age_elem = user_elem.find('age')
            age_elem.text = age
            gender_elem = user_elem.find('gender')
            gender_elem.text = gender

            # Update extra fields in XML element
            extra_fields_elems = user_elem.findall('field')
            for field_elem in extra_fields_elems:
                field_name_elem = field_elem.find('name')
                field_name = field_name_elem.text
                field_value_elem = field_elem.find('value')
                field_value = request.form.get(field_name)
                if field_value:
                    field_value_elem.text = field_value

            tree.write(filepath)

            return 'Data updated successfully'

        else:
            # Get form data from XML element
            name = root.find('user/name').text
            surname = root.find('user/surname').text
            age = root.find('user/age').text
            gender = root.find('user/gender').text

            # Get extra fields from XML element
            extra_fields = []
            extra_fields_elems = root.findall('user/field')
            for field_elem in extra_fields_elems:
                field_name = field_elem.find('name').text
                field_value = field_elem.find('value').text
                extra_fields.append((field_name, field_value))

            return render_template('edit.html', filename=filename, name=name, surname=surname, age=age, gender=gender, extra_fields=extra_fields)

    except Exception as e:
        print(e)
        return 'Error: Could not edit data'



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
