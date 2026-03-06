import os
import shutil
from app.core.settings import settings

class FileUtils:
    
    @staticmethod
    def save_file(file, uuuid, file_extension):
        # Create the directory if it doesn't exist
        os.makedirs(settings.FILES_PATH, exist_ok=True)
        
        # Save the file with the UUID as its name
        print(f'uuid: {uuuid}, file_extension: {file_extension}')
        file_path = os.path.join(settings.FILES_PATH, f"{uuuid}{file_extension}")
        with open(file_path, "wb") as buffer:
             shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    @staticmethod
    def extract_file_extension(filename):
        return os.path.splitext(filename)[1].lower()
