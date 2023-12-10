import unittest
import tempfile
import os
import io 
import shutil 
from unittest.mock import patch
from main import FileSorter 

class TestFileSorter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.file_sorter = FileSorter(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_create_extension_folders(self):
        # Créez quelques fichiers de test dans le répertoire source
        open(os.path.join(self.temp_dir, 'file1.txt'), 'a').close()
        open(os.path.join(self.temp_dir, 'file2.py'), 'a').close()
        open(os.path.join(self.temp_dir, 'file3.txt'), 'a').close()

        self.file_sorter.create_extension_folders()

        # Vérifiez si les dossiers d'extension ont été créés correctement
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'txt')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'py')))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'A Mettre A Jour')))

    def test_move_files(self):
        # Créez quelques fichiers de test dans le répertoire source
        open(os.path.join(self.temp_dir, 'file1.txt'), 'a').close()
        open(os.path.join(self.temp_dir, 'file2.py'), 'a').close()

        # Créez les dossiers d'extension
        self.file_sorter.create_extension_folders()

        self.file_sorter.move_files()

        # Vérifiez si les fichiers ont été déplacés correctement
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'file1.txt')))
        self.assertFalse(os.path.exists(os.path.join(self.temp_dir, 'file2.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'txt', 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'py', 'file2.py')))

    def test_move_small_files(self):
        # Créez quelques fichiers de test dans le répertoire source avec différentes tailles
        small_file_path = os.path.join(self.temp_dir, 'small_file.txt')
        large_file_path = os.path.join(self.temp_dir, 'large_file.txt')

        with open(small_file_path, 'w') as small_file:
            small_file.write('Small content')

        with open(large_file_path, 'w') as large_file:
            large_file.write('Larger content' * 1000)  # Un fichier plus grand

        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Définissez une taille seuil pour les fichiers à déplacer vers "A Mettre A Jour"
        size_threshold = 100  # Taille en octets (choisissez une valeur appropriée)

        # Appelez la méthode move_small_files
        file_sorter.move_small_files(size_threshold)

        # Vérifiez si les fichiers ont été déplacés correctement
        self.assertFalse(os.path.exists(small_file_path))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'A Mettre A Jour', 'small_file.txt')))
        self.assertTrue(os.path.exists(large_file_path))  # Le fichier plus grand ne devrait pas être déplacé

    def test_filter_files_by_extension(self):
        # Créez quelques fichiers de test dans le répertoire source avec différentes extensions
        txt_file_path = os.path.join(self.temp_dir, 'file1.txt')
        py_file_path = os.path.join(self.temp_dir, 'file2.py')
        md_file_path = os.path.join(self.temp_dir, 'file3.md')

        with open(txt_file_path, 'w') as txt_file:
            txt_file.write('Text content')

        with open(py_file_path, 'w') as py_file:
            py_file.write('Python content')

        with open(md_file_path, 'w') as md_file:
            md_file.write('Markdown content')

        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode filter_files_by_extension pour filtrer les fichiers par extension
        file_sorter.filter_files_by_extension(['txt', 'py'])

        # Capturer la sortie standard pour vérifier les résultats
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            file_sorter.filter_files_by_extension(['txt', 'py'])
            output = mock_stdout.getvalue()

        # Vérifiez si la sortie standard contient les noms des fichiers filtrés
        self.assertIn('file1.txt', output)
        self.assertIn('file2.py', output)
        self.assertNotIn('file3.md', output)

    def test_delete_file(self):
        # Créez un fichier de test dans le répertoire source
        file_path = os.path.join(self.temp_dir, 'file_to_delete.txt')
        with open(file_path, 'w') as test_file:
            test_file.write('Content to delete')

        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode delete_file pour supprimer le fichier
        file_sorter.delete_file('file_to_delete.txt')

        # Vérifiez si le fichier a été supprimé
        self.assertFalse(os.path.exists(file_path))

    def test_delete_nonexistent_file(self):
        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode delete_file pour supprimer un fichier inexistant
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            file_sorter.delete_file('nonexistent_file.txt')
            output = mock_stdout.getvalue()

        # Vérifiez si un message d'erreur approprié est affiché
        self.assertIn("Error: File 'nonexistent_file.txt' not found.", output)
    
    def test_rename_file(self):
        # Créez un fichier de test dans le répertoire source
        old_file_path = os.path.join(self.temp_dir, 'old_name.txt')
        new_file_path = os.path.join(self.temp_dir, 'new_name.txt')

        with open(old_file_path, 'w') as test_file:
            test_file.write('Content to rename')

        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode rename_file pour renommer le fichier
        file_sorter.rename_file('old_name.txt', 'new_name.txt')

        # Vérifiez si le fichier a été renommé
        self.assertFalse(os.path.exists(old_file_path))
        self.assertTrue(os.path.exists(new_file_path))

    def test_rename_nonexistent_file(self):
        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode rename_file pour renommer un fichier inexistant
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            file_sorter.rename_file('nonexistent_file.txt', 'new_name.txt')
            output = mock_stdout.getvalue()

        # Vérifiez si un message d'erreur approprié est affiché
        self.assertIn("Error: File 'nonexistent_file.txt' not found.", output)

    def test_duplicate_file(self):
        # Créez un fichier de test dans le répertoire source
        original_file_path = os.path.join(self.temp_dir, 'original_file.txt')

        with open(original_file_path, 'w') as original_file:
            original_file.write('Content to duplicate')

        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode duplicate_file pour dupliquer le fichier
        file_sorter.duplicate_file('original_file.txt')

        # Vérifiez si le fichier a été dupliqué
        self.assertTrue(os.path.exists(original_file_path))
        self.assertTrue(os.path.exists(os.path.join(self.temp_dir, 'Copy_of_original_file.txt')))

    def test_duplicate_nonexistent_file(self):
        # Instanciez un objet FileSorter avec le répertoire temporaire de test
        file_sorter = FileSorter(self.temp_dir)

        # Appelez la méthode duplicate_file pour dupliquer un fichier inexistant
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            file_sorter.duplicate_file('nonexistent_file.txt')
            output = mock_stdout.getvalue()

        # Vérifiez si un message d'erreur approprié est affiché
        self.assertIn("Error: File 'nonexistent_file.txt' not found.", output)


if __name__ == '__main__':
    unittest.main()
