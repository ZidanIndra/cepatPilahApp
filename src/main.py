import os
import shutil
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk

class cepatPilahApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CepatPilahApp")
        self.root.state("zoomed")  # Full-screen mode
        self.root.configure(bg="#1E1E1E")  # Dark theme background
        
        # Initialize variables
        self.source_folder = ""
        self.current_image_index = 0
        self.image_files = []
        self.folder_names = {"Folder1": "Folder1", "Folder2": "Folder2", "Folder3": "Folder3", "Trash": "Trash"}
        self.zoom_level = 0.5
        
        # Bind keyboard shortcuts
        self.root.bind("<Up>", lambda e: self.zoom_in())
        self.root.bind("<Down>", lambda e: self.zoom_out())
        self.root.bind("<Right>", lambda e: self.next_image())
        self.root.bind("<Left>", lambda e: self.previous_image())
        for i in range(1, 10):  # Bind keys 1-9 to move images to folders
            self.root.bind(str(i), lambda e, idx=i-1: self.move_to_folder_by_key(idx))
        
        self.show_start_menu()

    def show_start_menu(self):
        """Display the start menu with options."""
        self.clear_window()
        center_frame = Frame(self.root, bg="#1E1E1E")
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        Label(center_frame, text="CepatPilah", font=("Consolas", 24, "bold"), fg="#569CD6", bg="#1E1E1E").pack(pady=20)
        Button(center_frame, text="Mulai Sorting", command=self.start_sorting,
               bg="#007ACC", fg="white", font=("Consolas", 14, "bold"), relief=FLAT).pack(pady=10)
        Button(center_frame, text="Reset Settings", command=self.reset_settings,
               bg="#CE9178", fg="black", font=("Consolas", 14, "bold"), relief=FLAT).pack(pady=10)
        Button(center_frame, text="Credits", command=self.show_credits,
               bg="#007ACC", fg="white", font=("Consolas", 14, "bold"), relief=FLAT).pack(pady=10)

    def start_sorting(self):
        """Start the photo sorting interface."""
        self.clear_window()
        self.create_main_interface()

    def show_credits(self):
        """Show the credits page."""
        self.clear_window()
        center_frame = Frame(self.root, bg="#1E1E1E")
        center_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(center_frame, text="Dibuat oleh Zidan Indra Nugraha\nhttps://github.com/ZidanIndra",
              font=("Consolas", 16), fg="#569CD6", bg="#1E1E1E").pack(pady=20)
        Button(center_frame, text="Kembali", command=self.show_start_menu,
               bg="#007ACC", fg="white", font=("Consolas", 14, "bold"), relief=FLAT).pack(pady=10)

    def create_main_interface(self):
        """Create the main photo sorting interface."""
        Label(self.root, text="CepatPilah", font=("Consolas", 20, "bold"), fg="#569CD6", bg="#1E1E1E").pack(pady=10)
        self.canvas = Canvas(self.root, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.filename_label = Label(self.root, text="", font=("Consolas", 12), fg="#D4D4D4", bg="#1E1E1E")
        self.filename_label.pack(pady=5)
        
        self.zoom_slider = Scale(self.root, from_=0.2, to=3.0, resolution=0.1, orient=HORIZONTAL, label="Zoom Level",
                                 bg="#1E1E1E", fg="#D4D4D4", troughcolor="#569CD6", sliderrelief="flat",
                                 command=self.update_zoom)
        self.zoom_slider.set(0.5)
        self.zoom_slider.pack(pady=5, fill=X, padx=10)
        
        self.button_frame = Frame(self.root, bg="#1E1E1E")
        self.button_frame.pack(pady=10, fill=X)
        Button(self.button_frame, text="Select Folder", command=self.select_folder,
               bg="#007ACC", fg="white", font=("Consolas", 10, "bold"), relief=FLAT).pack(side=LEFT, padx=5)
        self.create_folder_buttons()
        Button(self.button_frame, text="Add Folder", command=self.add_folder,
               bg="#007ACC", fg="white", font=("Consolas", 10, "bold"), relief=FLAT).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Rename File", command=self.rename_file,
               bg="#CE9178", fg="black", font=("Consolas", 10, "bold"), relief=FLAT).pack(side=LEFT, padx=5)
        Button(self.button_frame, text="Back to Home", command=self.show_start_menu,
               bg="#CE9178", fg="black", font=("Consolas", 10, "bold"), relief=FLAT).pack(side=LEFT, padx=5)

    def create_folder_buttons(self):
        """Create buttons for moving images to folders."""
        for widget in self.button_frame.winfo_children():
            if isinstance(widget, Frame):
                widget.destroy()
        for key, name in self.folder_names.items():
            frame = Frame(self.button_frame, bg="#1E1E1E")
            frame.pack(side=LEFT, padx=5)
            Button(frame, text=f"Move to {name}", command=lambda k=key: self.move_image(k),
                   bg="#007ACC", fg="white", font=("Consolas", 10, "bold"), relief=FLAT).pack(side=LEFT, padx=2)
            Button(frame, text="...", command=lambda k=key: self.rename_folder(k),
                   bg="#CE9178", fg="black", font=("Consolas", 8, "bold"), width=3, relief=FLAT).pack(side=LEFT, padx=2)

    def select_folder(self):
        """Select a folder containing images."""
        self.source_folder = filedialog.askdirectory()
        if self.source_folder:
            self.image_files = [f for f in os.listdir(self.source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.current_image_index = 0
            self.show_image()

    def show_image(self):
        """Display the current image on the canvas."""
        if self.image_files:
            image_path = os.path.join(self.source_folder, self.image_files[self.current_image_index])
            try:
                img = Image.open(image_path)
                img = img.resize((int(img.width * self.zoom_level), int(img.height * self.zoom_level)), Image.Resampling.LANCZOS)
                self.img_tk = ImageTk.PhotoImage(img)
                self.canvas.delete("all")
                canvas_width, canvas_height = self.canvas.winfo_width(), self.canvas.winfo_height()
                x, y = (canvas_width - img.width) // 2, (canvas_height - img.height) // 2
                self.canvas.create_image(x, y, anchor=NW, image=self.img_tk)
                self.filename_label.config(text=self.image_files[self.current_image_index])
            except Exception as e:
                print(f"Error loading image: {e}")

    def move_image(self, destination):
        """Move the current image to the specified folder."""
        if self.image_files:
            source_path = os.path.join(self.source_folder, self.image_files[self.current_image_index])
            destination_folder = os.path.join(self.source_folder, self.folder_names[destination])
            os.makedirs(destination_folder, exist_ok=True)
            shutil.move(source_path, os.path.join(destination_folder, self.image_files[self.current_image_index]))
            self.image_files.pop(self.current_image_index)
            if self.image_files:
                self.current_image_index %= len(self.image_files)
                self.show_image()
            else:
                self.canvas.delete("all")
                self.filename_label.config(text="")
                self.label.config(text="All images sorted!")

    def update_zoom(self, value):
        """Update zoom level based on slider."""
        self.zoom_level = float(value)
        self.show_image()

    def zoom_in(self):
        """Zoom in using keyboard shortcut."""
        if self.zoom_level < 3.0:
            self.zoom_level += 0.1
            self.zoom_slider.set(self.zoom_level)
            self.show_image()

    def zoom_out(self):
        """Zoom out using keyboard shortcut."""
        if self.zoom_level > 0.2:
            self.zoom_level -= 0.1
            self.zoom_slider.set(self.zoom_level)
            self.show_image()

    def next_image(self):
        """Skip to the next image."""
        if self.image_files:
            self.current_image_index = (self.current_image_index + 1) % len(self.image_files)
            self.show_image()

    def previous_image(self):
        """Go back to the previous image."""
        if self.image_files:
            self.current_image_index = (self.current_image_index - 1) % len(self.image_files)
            self.show_image()

    def move_to_folder_by_key(self, idx):
        """Move image to folder using keyboard shortcut (keys 1-9)."""
        if idx < len(self.folder_names):
            key = list(self.folder_names.keys())[idx]
            self.move_image(key)

    def rename_folder(self, key):
        """Rename a folder."""
        new_name = simpledialog.askstring("Rename Folder", f"Enter new name for {self.folder_names[key]}:", initialvalue=self.folder_names[key])
        if new_name:
            self.folder_names[key] = new_name
            self.create_folder_buttons()

    def add_folder(self):
        """Add a new folder."""
        new_folder_name = simpledialog.askstring("Add Folder", "Enter new folder name:")
        if new_folder_name:
            new_key = f"Folder{len(self.folder_names)}"
            self.folder_names[new_key] = new_folder_name
            self.create_folder_buttons()

    def rename_file(self):
        """Rename the current file."""
        if self.image_files:
            current_file = self.image_files[self.current_image_index]
            base_name, ext = os.path.splitext(current_file)
            new_name = simpledialog.askstring("Rename File", "Enter new file name:", initialvalue=base_name)
            if new_name:
                new_name_with_ext = f"{new_name}{ext}"
                old_path = os.path.join(self.source_folder, current_file)
                new_path = os.path.join(self.source_folder, new_name_with_ext)
                os.rename(old_path, new_path)
                self.image_files[self.current_image_index] = new_name_with_ext
                self.show_image()

    def reset_settings(self):
        """Reset all application settings."""
        confirmation = messagebox.askyesno("Reset Settings", "Apakah Anda yakin ingin mereset semua pengaturan?")
        if confirmation:
            self.source_folder = ""
            self.current_image_index = 0
            self.image_files = []
            self.folder_names = {"Folder1": "Folder1", "Folder2": "Folder2", "Folder3": "Folder3", "Trash": "Trash"}
            self.zoom_level = 0.5
            messagebox.showinfo("Reset Settings", "Pengaturan telah berhasil direset.")
            self.show_start_menu()

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Main Application
if __name__ == "__main__":
    root = Tk()
    app = cepatPilahApp(root)
    root.mainloop()