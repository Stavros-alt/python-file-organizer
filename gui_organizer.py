import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# --- 1. THE CORE LOGIC (from my original script with some extra) ---
# Mapping of file extensions to folder names
EXT_TO_FOLDER_MAP = {
    # Images
    '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images', '.gif': 'Images', '.bmp': 'Images', '.svg': 'Images',
    # Documents
    '.pdf': 'Documents', '.docx': 'Documents', '.txt': 'Documents', '.pptx': 'Documents', '.xlsx': 'Documents',
    # Audio
    '.mp3': 'Audio', '.wav': 'Audio', '.aac': 'Audio',
    # Video
    '.mp4': 'Video', '.mov': 'Video', '.avi': 'Video', '.mkv': 'Video',
    # Archives
    '.zip': 'Archives', '.rar': 'Archives', '.7z': 'Archives',
    # Code & Scripts
    '.py': 'Code', '.js': 'Code', '.html': 'Code', '.css': 'Code',
    # Executables
    '.exe': 'Executables', '.msi': 'Executables'
}

def organize_folder(target_folder):
    """Organizes files in the target_folder into subdirectories based on their extension."""
    if not target_folder:
        return 0, "No folder selected."

    file_count = 0
    try:
        for filename in os.listdir(target_folder):
            # Skip directories
            if os.path.isdir(os.path.join(target_folder, filename)):
                continue

            file_ext = os.path.splitext(filename)[1].lower()
            
            # Get the destination folder name from the map, default to 'Other'
            dest_folder_name = EXT_TO_FOLDER_MAP.get(file_ext, 'Other')
            dest_path = os.path.join(target_folder, dest_folder_name)
            
            # Create destination folder if it doesn't exist
            os.makedirs(dest_path, exist_ok=True)
            
            # Move the file
            shutil.move(os.path.join(target_folder, filename), os.path.join(dest_path, filename))
            file_count += 1
            
        return file_count, "Success"
    except Exception as e:
        return 0, f"An error occurred: {e}"

# --- 2. THE GUI APPLICATION ---

class App:
    def __init__(self, root):
        self.root = root
        self.target_directory = ""

        # --- Window Configuration ---
        self.root.title("File Organizer v1.0")
        self.root.geometry("500x350")
        self.root.configure(bg="#2c3e50")

        # --- Widget Creation ---
        main_frame = tk.Frame(root, bg="#2c3e50", padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Select Folder Button
        self.select_btn = tk.Button(main_frame, text="Select Folder to Organize", command=self.select_directory, font=("Helvetica", 12), bg="#3498db", fg="white", relief=tk.FLAT, width=30)
        self.select_btn.pack(pady=10)
        
        # Label to show the selected path
        self.path_label = tk.Label(main_frame, text="No folder selected", font=("Helvetica", 10), bg="#2c3e50", fg="#ecf0f1", wraplength=450)
        self.path_label.pack(pady=10)

        # Organize Now Button
        self.organize_btn = tk.Button(main_frame, text="ORGANIZE NOW", command=self.run_organization, font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white", relief=tk.FLAT, width=20, height=2)
        self.organize_btn.pack(pady=20)

        # Status Bar
        self.status_label = tk.Label(main_frame, text="Status: Ready", font=("Helvetica", 10), bg="#2c3e50", fg="#bdc3c7")
        self.status_label.pack(pady=10, side=tk.BOTTOM)

    # --- Widget Functions ---
    def select_directory(self):
        """Opens a dialog to select a directory and updates the path label."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.target_directory = folder_selected
            self.path_label.config(text=f"Selected: {self.target_directory}")
            self.status_label.config(text="Status: Folder selected. Ready to organize.")
    
    def run_organization(self):
        """Runs the main organization logic when the button is pressed."""
        if not self.target_directory:
            messagebox.showwarning("Warning", "Please select a folder first.")
            return

        count, status = organize_folder(self.target_directory)
        
        if status == "Success":
            messagebox.showinfo("Success", f"Organization complete! \nOrganized {count} files successfully.")
            self.status_label.config(text=f"Status: Organized {count} files successfully.")
        else:
            messagebox.showerror("Error", status)
            self.status_label.config(text=f"Status: {status}")

# --- 3. RUN THE APPLICATION ---
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()