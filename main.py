import os
import shutil
from inquirer import prompt, List, Confirm

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

    def move_large_files(self):
        # Déplacer les fichiers de plus de 1 Go dans le dossier "A Mettre A Jour"
        update_folder = os.path.join(self.source_dir, "A Mettre A Jour")
        os.makedirs(update_folder, exist_ok=True)

        for file in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, file)
            if os.path.isfile(file_path) and os.path.getsize(file_path) < 1e9:  # Taille < 1 Go
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
        move_large_files_question = Confirm('move_large_files',
                                            message="Voulez-vous mettre les fichiers de moins de 1 Go dans un dossier séparé ?")
        move_large_files_answer = prompt([move_large_files_question])
        if move_large_files_answer['move_large_files']:
            file_sorter.move_large_files()
        file_sorter.create_extension_folders()
        file_sorter.move_files()  # Déplace toujours les fichiers dans des dossiers par extension

    elif "2. Donner la liste des fichiers" in answers['action']:
        file_types_input = input("Entrez l'extension des fichiers à filtrer (séparées par des espaces, appuyez sur Entrée pour traiter toutes les extensions) : ")
        file_types = file_types_input.split() if file_types_input else None
        file_sorter = FileSorter(source_dir)
        file_sorter.filter_files_by_extension(file_types)

if __name__ == "__main__":
    main()