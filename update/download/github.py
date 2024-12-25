import os
import zipfile
import requests

def download():
    try:
        response = requests.get('https://github.com/fluffy-melli/sclat/archive/refs/heads/main.zip')
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"HTTP GET Fail: {e}")
        return
    try:
        with open('-install.zip', 'wb') as out_file:
            out_file.write(response.content)
    except IOError as e:
        print(f"File Creation Fail: {e}")
        return
    if not unzip('-install.zip'):
        return

def unzip(filename):
    dest_dir = os.path.join(".install")
    try:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(dest_dir)
    except zipfile.BadZipFile as e:
        print(f"Can't open zip file: {e}")
        return False
    except Exception as e:
        print(f"Error extracting zip file: {e}")
        return False
    return True

def extract_file(zip_ref, file_info, dest_path):
    try:
        with zip_ref.open(file_info) as source_file:
            with open(dest_path, 'wb') as dest_file:
                dest_file.write(source_file.read())
        os.chmod(dest_path, file_info.external_attr >> 16)
    except Exception as e:
        print(f"Can't extract file: {e}")
        return False
    return True