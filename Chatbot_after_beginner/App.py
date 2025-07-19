import subprocess

def main():
    # Pfad zur main.py Datei
    main_file_path = 'bin/main.py'

    # Führe main.py aus
    subprocess.run(['python', main_file_path])

if __name__ == "__main__":
    main()