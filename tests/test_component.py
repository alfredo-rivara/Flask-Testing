import pytest
import sys
import os

# Ensure app is in path (handled by PYTHONPATH in docker-compose, but good for local)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app')))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"MC PRT EDITOR" in response.data

def test_clasificador_page(client):
    """Test that the clasificador page loads"""
    response = client.get('/clasificador')
    assert response.status_code == 200
    assert b"Clasificador" in response.data

def test_editor_page(client):
    """Test that the editor page loads"""
    response = client.get('/editor')
    assert response.status_code == 200
    assert b"Editor" in response.data

def test_visualizador_page(client):
    """Test that the visualizador page loads"""
    response = client.get('/visualizador')
    assert response.status_code == 200
    assert b"Visualizador" in response.data

def test_preproceso_duplicados_page(client):
    """Test that the preproceso duplicados page loads"""
    response = client.get('/preproceso-duplicados')
    assert response.status_code == 200
    assert b"Duplicados" in response.data
