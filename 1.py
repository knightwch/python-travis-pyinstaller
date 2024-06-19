import os
import shutil
import subprocess
import logging
import sys
import tempfile
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("output.log"),
            logging.StreamHandler()
        ]
    )

def extract_resource(resource_name):
    """Extract a resource to a temporary file and return the file path."""
    current_dir = Path(sys._MEIPASS) if hasattr(sys, "_MEIPASS") else Path(__file__).parent
    resource_path = current_dir / resource_name
    temp_dir = tempfile.gettempdir()
    temp_path = Path(temp_dir) / resource_name
    shutil.copy(resource_path, temp_path)
    return temp_path

def delete_log_folders_and_copy_files(drive_letters, source_file, reg_file):
    for drive_letter in drive_letters:
        if not drive_letter.endswith(':'):
            drive_letter += ':'
        base_path = drive_letter + '\\'

        for root, dirs, files in os.walk(base_path):
            for dir_name in dirs:
                parent_dir = os.path.basename(root)
                
                if dir_name == 'log' and parent_dir.startswith('abc'):
                    log_folder_path = os.path.join(root, dir_name)
                    try:
                        shutil.rmtree(log_folder_path)
                        logging.info(f"Deleted: {log_folder_path}")
                    except Exception as e:
                        logging.error(f"Failed to delete {log_folder_path}. Reason: {e}")
                
                if dir_name == 'configuration' and parent_dir.startswith('abc'):
                    config_folder_path = os.path.join(root, dir_name)
                    try:
                        shutil.copy2(source_file, config_folder_path)
                        logging.info(f"Copied {source_file} to {config_folder_path}")
                    except Exception as e:
                        logging.error(f"Failed to copy {source_file} to {config_folder_path}. Reason: {e}")

                if dir_name == 'centerm' and parent_dir == 'driver' and os.path.basename(os.path.dirname(root)).startswith('abc'):
                    centerm_folder_path = os.path.join(root, dir_name)
                    try:
                        dest_reg_file_path = os.path.join(centerm_folder_path, os.path.basename(reg_file))
                        shutil.copy2(reg_file, dest_reg_file_path)
                        logging.info(f"Copied {reg_file} to {dest_reg_file_path}")

                        subprocess.run(['regedit.exe', '/s', dest_reg_file_path], check=True)
                        logging.info(f"Executed {dest_reg_file_path}")
                    except Exception as e:
                        logging.error(f"Failed to copy or execute {reg_file} in {centerm_folder_path}. Reason: {e}")

if __name__ == "__main__":
    setup_logging()

    drive_letters = ['C', 'D', 'E']  # 请将此列表替换为你想要遍历的盘符
    source_file = extract_resource('log4j.properties')
    reg_file = extract_resource('双击运行打开日志.reg')
    delete_log_folders_and_copy_files(drive_letters, source_file, reg_file)
#你的python代码
