import os
import shutil
from inquirer import prompt, List, Confirm, Text

class FileSorter:
    def __init__(self, source_dir):
        self.source_dir = source_dir
        self.extension_folders_created = False

    def create_extension_folders(self):
        # Créer des dossiers pour chaque extension dans le répertoire source
        if not self.extension_folders_created:
            for file in os.listdir(self.source_dir):
                if os.path.isfile(os.path.join(self.source_dir, file)):
                    extension = file.split('.')[-1].lower()
                    extension_folder = os.path.join(self.source_dir, extension)
                    if not os.path.exists(extension_folder):
                        os.makedirs(extension_folder)
            self.extension_folders_created = True

    def move_files(self):
        # Déplacer les fichiers dans les dossiers correspondants aux extensions
        for file in os.listdir(self.source_dir):
            if os.path.isfile(os.path.join(self.source_dir, file)):
                extension = file.split('.')[-1].lower()
                source_path = os.path.join(self.source_dir, file)
                destination_path = os.path.join(self.source_dir, extension, file)
                shutil.move(source_path, destination_path)
                print(f"Moved: {file} to {extension} folder")

    def move_small_files(self, size_threshold):
        # Déplacer les fichiers de moins de la taille minimal dans le dossier "A Mettre A Jour"
        update_folder = os.path.join(self.source_dir, "A Mettre A Jour")
        os.makedirs(update_folder, exist_ok=True)

        for file in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, file)
            if os.path.isfile(file_path) and os.path.getsize(file_path) < size_threshold:  
                destination_path = os.path.join(update_folder, file)
                shutil.move(file_path, destination_path)
                print(f"Moved: {file} to 'A Mettre A Jour' folder")

    def filter_files_by_extension(self, file_types=None):
        for file in os.listdir(self.source_dir):
            if os.path.isfile(os.path.join(self.source_dir, file)):
                if not file_types or any(file.lower().endswith(f".{ext}") for ext in file_types):
                    print(file)

def main():
    questions = [
        List('action',
             message="Choisissez une action",
             choices=['1. Filtrer les fichiers par extension', '2. Donner la liste des fichiers'],
        ),
    ]

    answers = prompt(questions)

    source_dir = input("Entrez le chemin du répertoire source : ")

    if "1. Filtrer les fichiers par extension" in answers['action']:
        file_sorter = FileSorter(source_dir)
        
        # Ajout d'une question pour spécifier la taille minimal en mégaoctets
        size_threshold_input = Text('size_threshold',
                                    message="Entrez la taille minimal en mégaoctets pour déplacer les fichiers dans 'A Mettre A Jour' (entrez 0 pour désactiver cette option) : ")
        size_threshold_answer = prompt([size_threshold_input])
        size_threshold = int(size_threshold_answer['size_threshold']) * 1e6  # Convertir en octets

        # Déplacer les fichiers de moins de la taille minimal vers "A Mettre A Jour"
        if size_threshold > 0:
            file_sorter.move_small_files(size_threshold)

        file_sorter.create_extension_folders()
        file_sorter.move_files()

    elif "2. Donner la liste des fichiers" in answers['action']:
        file_types_input = input("Entrez l'extension des fichiers à filtrer (séparées par des espaces, appuyez sur Entrée pour traiter toutes les extensions) : ")
        file_types = file_types_input.split() if file_types_input else None
        file_sorter = FileSorter(source_dir)
        file_sorter.filter_files_by_extension(file_types)

if __name__ == "__main__":
    main()