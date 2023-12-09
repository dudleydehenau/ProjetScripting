import os
import shutil

class FileSorter:
    def __init__(self, source_dir, update_folder=False):
        self.source_dir = source_dir
        self.update_folder = update_folder

    def create_extension_folders(self):
        # Créer des dossiers pour chaque extension dans le répertoire source
        for file in os.listdir(self.source_dir):
            if os.path.isfile(os.path.join(self.source_dir, file)):
                extension = file.split('.')[-1].lower()
                extension_folder = os.path.join(self.source_dir, extension)
                if not os.path.exists(extension_folder):
                    os.makedirs(extension_folder)

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

def main():
    # Demander à l'utilisateur d'entrer le chemin du répertoire source
    source_dir = input("Entrez le chemin du répertoire source à trier (exemple : C:\Chemin\Repertoire) : ")

    # Vérifier si le répertoire source existe
    if not os.path.exists(source_dir):
        print(f"Erreur: Le repertoire spécifié '{source_dir}' semble ne pas exister.")
        return

    # Demander à l'utilisateur s'il veut déplacer les fichiers de moins de 1 Go vers "A Mettre A Jour"
    update_folder = input("Voulez-vous déplacer les fichiers de moins de 1 Go vers 'A Mettre A Jour'? (Oui/Non): ").lower()
    update_folder = update_folder == "oui"

    # Instancier la classe FileSorter
    file_sorter = FileSorter(source_dir, update_folder)

    # Déplacer les fichiers de moins de 1 Go vers "A Mettre A Jour"
    if update_folder:
        file_sorter.move_large_files()

    # Créer des dossiers pour chaque extension
    file_sorter.create_extension_folders()

    # Déplacer les fichiers dans les dossiers correspondants
    file_sorter.move_files()

if __name__ == "__main__":
    main()