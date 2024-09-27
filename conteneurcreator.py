import platform
import subprocess
import os
import time
from colorama import init, Fore, Style

# Initialiser colorama pour la coloration du texte
init(autoreset=True)

# Définition de l'exception personnalisée
class NotRootException(Exception):
    pass

# Fonction pour afficher des messages avec pauses
def display_message(message, color=Fore.WHITE, pause=2):
    print(color + message)
    time.sleep(pause)

# 1. Détecter si on est sur Windows ou Linux
def main():
    system = platform.system()
    if system == "Linux":
        display_message("Vous êtes sur Linux.", Fore.GREEN)

        # Vérifier si l'utilisateur est root
        if os.geteuid() == 0:
            display_message("Vous êtes root.", Fore.GREEN)
        else:
            display_message("Vous n'êtes pas root.", Fore.RED)
            raise NotRootException("Vous devez être root pour exécuter ce script.")

        # Détection de la famille Linux (Debian/RedHat)
        with open("/etc/os-release", "r") as f:
            os_info = f.read()
        if "debian" in os_info.lower() or "ubuntu" in os_info.lower():
            linux_family = "debian"
            display_message("Famille Linux: Debian/Ubuntu", Fore.BLUE)
        elif "rhel" in os_info.lower() or "fedora" in os_info.lower():
            linux_family = "redhat"
            display_message("Famille Linux: RedHat/Fedora", Fore.BLUE)
        else:
            display_message("Famille Linux inconnue.", Fore.RED)
            raise Exception("Famille Linux inconnue.")

    elif system == "Windows":
        display_message("Vous êtes sur Windows.", Fore.GREEN)

    else:
        display_message("Système d'exploitation non supporté.", Fore.RED)
        raise Exception("Système d'exploitation non supporté.")

    # 2. Docker est-il installé ?
    if not is_docker_installed():
        display_message("Docker n'est pas installé.", Fore.RED)
        install_docker(linux_family)
    
    # 3. Le service Docker est-il actif ?
    if system == "Linux":
        if not is_docker_active():
            display_message("Le service Docker est inactif. Démarrage...", Fore.YELLOW)
            subprocess.run(["systemctl", "start", "docker"], check=True)
            display_message("Service Docker démarré.", Fore.GREEN)

    # 4. Créer un conteneur
    create_container()

def is_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except FileNotFoundError:
        return False

def install_docker(linux_family):
    if linux_family == "debian":
        display_message("Installation de Docker via apt...", Fore.YELLOW)
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "-y", "docker.io"], check=True)
    elif linux_family == "redhat":
        display_message("Installation de Docker via dnf...", Fore.YELLOW)
        subprocess.run(["dnf", "install", "-y", "docker"], check=True)

def is_docker_active():
    try:
        subprocess.run(["systemctl", "is-active", "--quiet", "docker"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def create_container():
    # Votre logique pour créer un conteneur ici
    pass

# Lancer le processus principal si le script est exécuté directement
if __name__ == "__main__":
    try:
        main()
    except NotRootException as e:
        display_message(str(e), Fore.RED)
