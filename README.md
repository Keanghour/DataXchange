# DataXchange
A simple GUI tool for converting between JSON, XML, XSD, and OFS formats using Python's tkinter. The app supports conversions like JSON to XML, XML to JSON, and more. Users can input data, select a conversion type, and view or copy the output. It also includes options for clearing the output.

---

# Data Format Converter App

This app allows you to convert between various data formats like JSON, XML, XSD, and OFS using a simple GUI built with Python’s tkinter library.

## Features
- Convert between:
  - JSON to XML
  - XML to JSON
  - XML to XSD
  - XSD to XML
  - JSON to OFS
  - XML to OFS
- Copy or clear output easily.

## How to Use
1. **Input Data**: Paste your JSON, XML, or XSD data into the input text area.
2. **Select Conversion Type**: Choose the conversion (e.g., JSON to XML) from the dropdown.
3. **Convert**: Click "Convert" to get the result in the output text area.
4. **Copy or Clear**: Use "Copy Output" to copy the result or "Clear Output" to delete it.

## Requirements
- Python 3.x
- Required libraries:
  - `tkinter` (comes with Python)
  - `json`
  - `xmltodict`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Run the script:
   ```bash
   python converter_app.py
   ```

## License

This project is open-source under the MIT License.
