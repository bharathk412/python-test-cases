from your_flask_app import app  # Import your Flask app instance
from unittest.mock import patch

def test_entity_extraction_success():
    client = app.test_client()
    response = client.post('/extract_entities', data={'pdf_path': 'path/to/valid/pdf.pdf'})
    assert response.status_code == 200
    assert b'entity_name' in response.data
    assert b'entity_place' in response.data
    assert b'entity_cost' in response.data

def test_missing_pdf_path():
    client = app.test_client()
    response = client.post('/extract_entities', data={})
    assert response.status_code == 400
    assert b'Missing PDF path' in response.data

def test_invalid_pdf_path():
    client = app.test_client()
    response = client.post('/extract_entities', data={'pdf_path': 'invalid/path/to/pdf.pdf'})
    assert response.status_code == 400
    assert b'Invalid PDF path' in response.data

@patch('your_flask_app.extract_entities_from_pdf')
def test_pdf_extraction_failure(mock_extract_entities_from_pdf):
    mock_extract_entities_from_pdf.side_effect = Exception('PDF extraction error')
    client = app.test_client()
    response = client.post('/extract_entities', data={'pdf_path': 'path/to/valid/pdf.pdf'})
    assert response.status_code == 500
    assert b'PDF extraction error' in response.data

@patch('your_flask_app.extract_entities_from_pdf')
def test_empty_pdf_content(mock_extract_entities_from_pdf):
    mock_extract_entities_from_pdf.return_value = None
    client = app.test_client()
    response = client.post('/extract_entities', data={'pdf_path': 'path/to/valid/pdf.pdf'})
    assert response.status_code == 200
    assert b'No entities found' in response.data

@patch('your_flask_app.extract_entities_from_pdf')
def test_unexpected_response_format(mock_extract_entities_from_pdf):
    mock_extract_entities_from_pdf.return_value = {'invalid_key': 'value'}
    client = app.test_client()
    response = client.post('/extract_entities', data={'pdf_path': 'path/to/valid/pdf.pdf'})
    assert response.status_code == 500
    assert b'Unexpected response format' in response.data
