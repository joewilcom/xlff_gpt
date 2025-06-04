import xml.etree.ElementTree as ET
from docx import Document

def extract_xlff_from_docx(docx_bytes):
    doc = Document(docx_bytes)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                text = cell.text.strip()
                if text.startswith('<?xml') or '<xliff' in text:
                    return text
    return None

def parse_xlff(xlff_content):
    try:
        root = ET.fromstring(xlff_content)
        translations = []
        for trans_unit in root.findall('.//trans-unit'):
            source = trans_unit.find('source').text if trans_unit.find('source') is not None else ''
            target = trans_unit.find('target').text if trans_unit.find('target') is not None else ''
            translations.append({'source': source, 'target': target})
        return translations
    except Exception as e:
        return [{'source': 'Error', 'target': str(e)}]