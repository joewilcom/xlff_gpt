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
    """Parse an XLFF/XLIFF string and return a list of translation units."""
    try:
        root = ET.fromstring(xlff_content)

        # Handle namespaces transparently. When the document uses a default
        # namespace, ``ElementTree`` requires the namespace to be provided when
        # searching for tags.  Extract the namespace if present and build the
        # search paths accordingly.
        if '}' in root.tag:
            ns_uri = root.tag.split('}')[0].strip('{')
            ns = {'ns': ns_uri}
            trans_unit_path = './/ns:trans-unit'
            source_path = 'ns:source'
            target_path = 'ns:target'
        else:
            ns = {}
            trans_unit_path = './/trans-unit'
            source_path = 'source'
            target_path = 'target'

        translations = []
        for trans_unit in root.findall(trans_unit_path, ns):
            source_el = trans_unit.find(source_path, ns)
            target_el = trans_unit.find(target_path, ns)
            source = source_el.text if source_el is not None else ''
            target = target_el.text if target_el is not None else ''
            translations.append({'source': source, 'target': target})
        return translations
    except Exception as e:
        # Surface parsing errors back to the caller so they can be displayed in
        # the web interface.
        return [{'source': 'Error', 'target': str(e)}]
