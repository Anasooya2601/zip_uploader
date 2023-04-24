import os
import zipfile
from tkinter import *
from tkinter import filedialog

class FileZipper:
    def __init__(self, master):
        self.master = master
        master.title("File Zipper")
        self.file_paths = []
        self.current_page = 0

        # Create file selection button
        self.select_button = Button(master, text="Select Files", command=self.select_files)
        self.select_button.pack(pady=10)

        # Create file deletion button
        self.delete_button = Button(master, text="Delete Selected File", command=self.delete_file)
        self.delete_button.pack(pady=10)

        # Create zip button
        self.zip_button = Button(master, text="Zip Files", command=self.zip_files)
        self.zip_button.pack(pady=10)

        # Create navigation buttons
        self.back_button = Button(master, text="<<", command=self.previous_page)
        self.back_button.pack(side=LEFT, padx=10)
        self.forward_button = Button(master, text=">>", command=self.next_page)
        self.forward_button.pack(side=RIGHT, padx=10)

        # Create file listbox
        self.file_listbox = Listbox(master, width=50, height=10, selectmode=SINGLE)
        self.file_listbox.pack()

        # Create scrollbar for file listbox
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.file_listbox.yview)

    def select_files(self):
        file_types = [("PDF Files", "*.pdf"), ("JPEG Files", "*.jpg")]
        files = filedialog.askopenfilenames(filetypes=file_types)
        for file in files:
            if file.endswith(".pdf") or file.endswith(".jpg"):
                self.file_paths.append(file)
                self.file_listbox.insert(END, file)

    def delete_file(self):
        selected = self.file_listbox.curselection()
        if selected:
            index = int(selected[0])
            self.file_paths.pop(index)
            self.file_listbox.delete(selected)

    def zip_files(self):
        if not self.file_paths:
            messagebox.showwarning("No Files Selected", "Please select files to zip.")
        else:
            zip_file = filedialog.asksaveasfilename(defaultextension=".zip")
            with zipfile.ZipFile(zip_file, "w") as zip:
                for file in self.file_paths:
                    zip.write(file, os.path.basename(file))

    def next_page(self):
        if self.current_page < len(self.file_paths) - 1:
            self.current_page += 1
            self.file_listbox.select_clear(0, END)
            self.file_listbox.select_set(self.current_page)
            self.file_listbox.activate(self.current_page)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.file_listbox.select_clear(0, END)
            self.file_listbox.select_set(self.current_page)
            self.file_listbox.activate(self.current_page)

root = Tk()
file_zipper = FileZipper(root)
root.mainloop()


























