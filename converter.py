import tkinter as tk
from tkinter import ttk, messagebox
import json
import xmltodict

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Format Converter")
        self.root.geometry("780x780")
        self.root.configure(bg="#f8f9fa")

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Header Label
        header_label = tk.Label(self.root, text="Data Format Converter", font=("Arial", 24, "bold"), bg="#f8f9fa", fg="#343a40")
        header_label.pack(pady=20)

        # Frame for input
        input_frame = ttk.LabelFrame(self.root, text="Input Data", padding=(10, 10))
        input_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Input text area
        self.input_text = tk.Text(input_frame, height=10, width=80, font=("Arial", 12), bg="#ffffff", fg="#343a40", wrap="word")
        self.input_text.pack(pady=10, padx=10)

        # Format instruction label
        self.format_label = tk.Label(input_frame, text="Enter valid JSON or XML data.", font=("Arial", 12), bg="#f8f9fa", fg="#6c757d")
        self.format_label.pack(pady=5)

        # Dropdown for selecting conversion type
        self.conversion_type = ttk.Combobox(self.root, values=[
            "JSON to XML", "XML to JSON", "XML to XSD", "XSD to XML", "JSON to OFS", "XML to OFS"
        ], font=("Arial", 12), state="readonly")
        self.conversion_type.bind("<<ComboboxSelected>>", self.update_format_instruction)
        self.conversion_type.pack(pady=10, padx=10)

        # Convert button
        self.convert_button = tk.Button(self.root, text="Convert", command=self.convert, width=20, bg="#007bff", fg="white", font=("Arial", 12, "bold"), borderwidth=0)
        self.convert_button.pack(pady=10)

        # Frame for output
        output_frame = ttk.LabelFrame(self.root, text="Output Data", padding=(10, 10))
        output_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Output text area
        self.output_text = tk.Text(output_frame, height=10, width=80, font=("Arial", 12), bg="#ffffff", fg="#343a40", wrap="word")
        self.output_text.pack(pady=10, padx=10)

        # Frame for copy and clear buttons
        button_frame = tk.Frame(self.root, bg="#f8f9fa")
        button_frame.pack(pady=10)

        # Copy button
        self.copy_button = tk.Button(button_frame, text="Copy Output", command=self.copy_output, width=20, bg="#28a745", fg="white", font=("Arial", 12, "bold"), borderwidth=0)
        self.copy_button.pack(side=tk.LEFT, padx=10)

        # Clear button
        self.clear_button = tk.Button(button_frame, text="Clear Output", command=self.clear_output, width=20, bg="#dc3545", fg="white", font=("Arial", 12, "bold"), borderwidth=0)
        self.clear_button.pack(side=tk.LEFT, padx=10)

    def update_format_instruction(self, event):
        conversion = self.conversion_type.get()
        if conversion:
            self.format_label.config(text=f"Enter valid {conversion.split()[0]} data.")

    def convert(self):
        conversion = self.conversion_type.get()
        input_data = self.input_text.get("1.0", tk.END).strip()

        try:
            if conversion == "JSON to XML":
                result = self.json_to_xml(input_data)
            elif conversion == "XML to JSON":
                result = self.xml_to_json(input_data)
            elif conversion == "XML to XSD":
                result = self.xml_to_xsd(input_data)
            elif conversion == "XSD to XML":
                result = self.xsd_to_xml(input_data)
            elif conversion == "JSON to OFS":
                result = self.json_to_ofs(input_data)
            elif conversion == "XML to OFS":
                result = self.xml_to_ofs(input_data)
            else:
                result = "Please select a conversion type."
            
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, result)
        except Exception as e:
            messagebox.showerror("Error", f"Conversion error: {str(e)}")

    def json_to_xml(self, json_data):
        dict_data = json.loads(json_data)
        xml_data = xmltodict.unparse({"root": dict_data}, pretty=True)
        return xml_data

    def xml_to_json(self, xml_data):
        dict_data = xmltodict.parse(xml_data)
        if 'root' in dict_data:
            dict_data = dict_data['root']  # Remove root if it exists
        json_data = json.dumps(dict_data, indent=4)
        return json_data

    def xml_to_xsd(self, xml_data):
        try:
            xml_dict = xmltodict.parse(xml_data)
            xsd = self.dict_to_xsd(xml_dict, root_element='root')
            return xsd
        except Exception as e:
            raise ValueError(f"Failed to convert XML to XSD: {str(e)}")

    def dict_to_xsd(self, xml_dict, root_element='root'):
        xsd = f"""<?xml version="1.0" encoding="utf-8"?>
<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified" xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="{root_element}">
        <xs:complexType>
            <xs:sequence>
"""
        for key, value in xml_dict[root_element].items():
            element_type, max_occurs = self.infer_type(value)
            xsd += f"                <xs:element name=\"{key}\" type=\"{element_type}\" maxOccurs=\"{max_occurs}\" />\n"
        
        xsd += """            </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:schema>"""
        return xsd

    def infer_type(self, value):
        if isinstance(value, dict):
            return "xs:string", "unbounded"  # Complex type, treat as unbounded
        elif isinstance(value, list):
            return "xs:string", "unbounded"  # List type, unbounded
        elif isinstance(value, str):
            return "xs:string", "1"  # Single string, occurs once
        elif isinstance(value, int):
            return "xs:integer", "1"  # Single integer, occurs once
        elif isinstance(value, float):
            return "xs:decimal", "1"  # Single decimal, occurs once
        else:
            return "xs:string", "1"  # Default to string

    def xsd_to_xml(self, xsd_data):
        try:
            # Convert the XSD string to bytes
            xsd_bytes = xsd_data.encode('utf-8')
            schema = etree.XML(xsd_bytes)
            root = schema.find("{http://www.w3.org/2001/XMLSchema}element")
            xml = self.generate_xml(root)
            return xml
        except Exception as e:
            raise ValueError(f"Failed to convert XSD to XML: {str(e)}")

    def generate_xml(self, xsd_element, indent_level=0):
        tag = xsd_element.attrib['name']
        indent = "  " * indent_level
        xml = f"{indent}<{tag}>\n"
        
        for child in xsd_element.findall("{http://www.w3.org/2001/XMLSchema}complexType"):
            for sequence in child.findall("{http://www.w3.org/2001/XMLSchema}sequence"):
                for element in sequence.findall("{http://www.w3.org/2001/XMLSchema}element"):
                    element_tag = element.attrib['name']
                    xml += f"{indent}  <{element_tag}></{element_tag}>\n"
                    if element.find("{http://www.w3.org/2001/XMLSchema}complexType") is not None:
                        xml += self.generate_xml(element, indent_level + 2)

        xml += f"{indent}</{tag}>"
        return xml

    def json_to_ofs(self, json_data):
        try:
            # Parse JSON data
            data = json.loads(json_data)
            txnRef = data.get('txnRef', '')
            accNumber = data.get('accNumber', '')
            date = data.get('date', '')

            # Construct the OFS Request message in the exact format requested
            request_message = f"TXNREF:1:1={txnRef},ACCNUM:1:1={accNumber},DATE:1:1={date}"

            return request_message
        except Exception as e:
            raise ValueError(f"Failed to convert JSON to OFS: {str(e)}")

    def xml_to_ofs(self, xml_data):
        try:
            # Parse XML data
            xml_dict = xmltodict.parse(xml_data)
            txnRef = xml_dict['root']['txnRef']
            accNumber = xml_dict['root']['accNumber']
            date = xml_dict['root']['date']

            # Construct the OFS Request message in the exact format requested
            request_message = f"TXNREF:1:1={txnRef},ACCNUM:1:1={accNumber},DATE:1:1={date}"

            return request_message
        except Exception as e:
            raise ValueError(f"Failed to convert XML to OFS: {str(e)}")

    def copy_output(self):
        output = self.output_text.get("1.0", tk.END).strip()
        self.root.clipboard_clear()
        self.root.clipboard_append(output)
        messagebox.showinfo("Copied", "Output copied to clipboard!")

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()
