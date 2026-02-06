import os
import time
import zipfile
import py7zr
import rarfile
import tarfile
from pathlib import Path
from utils import get_readable_file_size, get_readable_time

class UnzipHelper:
    def __init__(self):
        self.supported_formats = {
            '.zip': self.extract_zip,
            '.rar': self.extract_rar,
            '.7z': self.extract_7z,
            '.tar': self.extract_tar,
            '.tar.gz': self.extract_tar,
            '.tgz': self.extract_tar,
            '.tar.bz2': self.extract_tar,
        }

    async def extract_zip(self, file_path, extract_path, progress_callback=None):
        """Extract ZIP files"""
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                total_files = len(file_list)
                
                for index, file in enumerate(file_list):
                    zip_ref.extract(file, extract_path)
                    if progress_callback:
                        await progress_callback(index + 1, total_files)
            
            return True, "Extraction completed successfully"
        except Exception as e:
            return False, f"Error extracting ZIP: {str(e)}"

    async def extract_rar(self, file_path, extract_path, progress_callback=None):
        """Extract RAR files"""
        try:
            with rarfile.RarFile(file_path, 'r') as rar_ref:
                file_list = rar_ref.namelist()
                total_files = len(file_list)
                
                for index, file in enumerate(file_list):
                    rar_ref.extract(file, extract_path)
                    if progress_callback:
                        await progress_callback(index + 1, total_files)
            
            return True, "Extraction completed successfully"
        except Exception as e:
            return False, f"Error extracting RAR: {str(e)}"

    async def extract_7z(self, file_path, extract_path, progress_callback=None):
        """Extract 7Z files"""
        try:
            with py7zr.SevenZipFile(file_path, 'r') as archive:
                file_list = archive.getnames()
                total_files = len(file_list)
                archive.extractall(path=extract_path)
                
                if progress_callback:
                    await progress_callback(total_files, total_files)
            
            return True, "Extraction completed successfully"
        except Exception as e:
            return False, f"Error extracting 7Z: {str(e)}"

    async def extract_tar(self, file_path, extract_path, progress_callback=None):
        """Extract TAR files"""
        try:
            with tarfile.open(file_path, 'r:*') as tar_ref:
                members = tar_ref.getmembers()
                total_files = len(members)
                
                for index, member in enumerate(members):
                    tar_ref.extract(member, extract_path)
                    if progress_callback:
                        await progress_callback(index + 1, total_files)
            
            return True, "Extraction completed successfully"
        except Exception as e:
            return False, f"Error extracting TAR: {str(e)}"

    async def extract_archive(self, file_path, extract_path, progress_callback=None):
        """Extract any supported archive format"""
        file_ext = ''.join(Path(file_path).suffixes).lower()
        
        # Handle compound extensions
        if file_ext not in self.supported_formats:
            file_ext = Path(file_path).suffix.lower()
        
        if file_ext in self.supported_formats:
            extractor = self.supported_formats[file_ext]
            return await extractor(file_path, extract_path, progress_callback)
        else:
            return False, f"Unsupported file format: {file_ext}"

    def get_archive_info(self, file_path):
        """Get information about the archive"""
        try:
            file_ext = ''.join(Path(file_path).suffixes).lower()
            if file_ext not in ['.zip', '.rar', '.7z', '.tar', '.tar.gz', '.tgz', '.tar.bz2']:
                file_ext = Path(file_path).suffix.lower()
            
            info = {
                'format': file_ext,
                'size': os.path.getsize(file_path),
                'files': 0,
                'file_list': []
            }
            
            if file_ext == '.zip':
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    info['files'] = len(zip_ref.namelist())
                    info['file_list'] = zip_ref.namelist()[:10]  # First 10 files
            
            elif file_ext == '.rar':
                with rarfile.RarFile(file_path, 'r') as rar_ref:
                    info['files'] = len(rar_ref.namelist())
                    info['file_list'] = rar_ref.namelist()[:10]
            
            elif file_ext == '.7z':
                with py7zr.SevenZipFile(file_path, 'r') as archive:
                    file_list = archive.getnames()
                    info['files'] = len(file_list)
                    info['file_list'] = file_list[:10]
            
            elif file_ext in ['.tar', '.tar.gz', '.tgz', '.tar.bz2']:
                with tarfile.open(file_path, 'r:*') as tar_ref:
                    members = tar_ref.getmembers()
                    info['files'] = len(members)
                    info['file_list'] = [m.name for m in members[:10]]
            
            return info
        except Exception as e:
            return {'error': str(e)}

    async def create_zip(self, source_dir, output_path, progress_callback=None):
        """Create a ZIP archive from a directory"""
        try:
            files_to_zip = []
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    files_to_zip.append(file_path)
            
            total_files = len(files_to_zip)
            
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for index, file_path in enumerate(files_to_zip):
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                    if progress_callback:
                        await progress_callback(index + 1, total_files)
            
            return True, "ZIP created successfully"
        except Exception as e:
            return False, f"Error creating ZIP: {str(e)}"

unzip_helper = UnzipHelper()
