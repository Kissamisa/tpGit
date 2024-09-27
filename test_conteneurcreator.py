import pytest
import platform
from conteneurcreator import display_message, is_docker_installed, create_container

# Test de display_message sans mock (capture de la sortie)
def test_display_message(capsys):
    display_message("Test message", pause=0)
    captured = capsys.readouterr()
    assert "Test message" in captured.out

# Test de l'OS détecté (fonctionne seulement sur la machine actuelle)
def test_detect_system():
    system = platform.system()
    assert system in ["Linux", "Windows", "Darwin"]  # On s'attend à un système valide

# Test de Docker installé (fonctionne seulement si Docker est installé sur la machine)
def test_is_docker_installed():
    result = is_docker_installed()
    assert isinstance(result, bool)  # Doit renvoyer un booléen

# Test de la création de conteneur (en simulant directement le choix)
""" def test_create_container(monkeypatch):
    # Simuler le choix direct '1' pour Ubuntu/Debian
    monkeypatch.setattr('builtins.input', lambda _: '1')
    
    # Ce test exécutera la création d'un conteneur réel si Docker est installé.
    # Soyez prudent car cela peut affecter votre environnement Docker.
    try:
        create_container()
        assert True  # Si la création réussit, le test passe
    except Exception as e:
        pytest.fail(f"Erreur lors de la création du conteneur : {e}")
 """