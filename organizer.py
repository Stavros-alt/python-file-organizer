#!/usr/bin/env python3

import shutil
from pathlib import Path

# File type categorization mapping
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mov", ".avi"],
    "Others": []  # Catch-all for other extensions
}

def get_category(file_extension):
    """Determine file category based on extension"""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"

def organize_files(src_path, dest_path):
    """Organize files from source to destination folders"""
    moved_files = {category: 0 for category in FILE_CATEGORIES.keys()}
    
    for item in src_path.iterdir():
        if item.is_dir() or item.name.startswith('.'):
            continue
            
        file_ext = item.suffix
        category = get_category(file_ext)
        dest_dir = dest_path / category
        
        try:
            dest_dir.mkdir(exist_ok=True)
            dest_file = dest_dir / item.name
            
            if dest_file.exists():
                overwrite = input(f"Overwrite {dest_file}? (y/n): ").lower()
                if overwrite != 'y':
                    continue
            
            shutil.move(str(item), str(dest_file))
            moved_files[category] += 1
            print(f"Moved {item.name} to {category}")
            
        except Exception as e:
            print(f"Error processing {item.name}: {e}")
    
    return moved_files

def main():
    """Main function to handle user input and file organization"""
    print("=== File Organizer ===")
    
    src_input = input("Enter source folder path: ").strip()
    dest_input = input("Enter destination folder path (leave empty to use source): ").strip()
    
    try:
        src_path = Path(src_input)
        if not src_path.exists() or not src_path.is_dir():
            raise ValueError("Invalid source path")
            
        dest_path = Path(dest_input) if dest_input else src_path
        
        print(f"\nOrganizing files from {src_path} to {dest_path}")
        moved_files = organize_files(src_path, dest_path)
        
        print("\n=== Summary ===")
        for category, count in moved_files.items():
            print(f"{category}: {count} files")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()