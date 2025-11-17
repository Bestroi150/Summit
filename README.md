# Summit

A Flask web application for creating, editing, viewing, and managing XML files with user data.

## Overview

Summit provides a user-friendly interface for working with XML data. Users can create XML documents with structured information, edit existing XML files, view their contents, and manage multiple versions of their data.

## Features

- **Create XML**: Submit user information (name, surname, age, gender) and custom fields to generate formatted XML files
- **Edit XML**: Upload and modify existing XML files with version control
- **View XML**: Display XML file contents with structured data visualization
- **Download**: Save generated XML files locally
- **File Management**: Browse and manage XML files through the web interface
- **Pretty Print**: Automatic XML formatting with proper indentation

## Project Structure

```
Summit/
├── app.py                 # Flask application and routing
├── templates/             # HTML templates
│   ├── index.html        # Main form for creating XML
│   ├── edit.html         # XML editing interface
│   ├── view.html         # XML viewing interface
│   ├── open.html         # File browser and viewer
│   ├── indexes.html      # Index/view page
│   ├── cess.html         # Additional page
│   └── 404.html          # Error page
├── schema/                # XSD schema files
├── TEI/                   # TEI XML samples
├── geodata.csv            # Data file
└── README.md              # This file
```

## Installation

1. Clone or download this repository
2. Set up a Python virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install required dependencies:
   ```bash
   pip install flask
   ```

## Usage

1. Run the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and navigate to `http://localhost:5000`
3. Use the interface to:
   - **Create**: Fill out the form with user data and custom fields to generate XML
   - **Edit**: Upload an XML file to modify and create versioned updates
   - **View**: Upload XML files to display their structured content
   - **Open**: Browse and view existing XML files

## API Routes

- `GET /` - Main page with XML creation form
- `POST /submit` - Submit form data and create XML file
- `GET /download/<filename>` - Download XML file
- `GET/POST /open` - View and open XML files
- `GET/POST /edit` - Edit XML files
- `POST /save` - Save edited XML with version control
- `GET /view` - View XML data
- `POST /upload` - Upload and display XML file contents

## Requirements

- Python 3.x
- Flask

## Known Limitations

- File handling is basic; production deployments should use proper file storage
- Error handling could be enhanced
- No user authentication currently implemented

## Future Enhancements

- TEI XML format support
- Schema validation
- Advanced error handling
- User authentication
- Database integration
- Batch file processing

## License

See LICENSE file for details

## Support

For issues or suggestions, please open an issue on the GitHub repository.
