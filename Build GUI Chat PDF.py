# Import required libraries
import tkinter as tk
from tkinter import filedialog
import requests
import json

# Class for UX GUI
class Chatter_Bot:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatavarayan")

        # API Key
        self.api_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'
        
        # docId
        self.doc_id = None
        
        # File Path
        self.file_path_var = tk.StringVar()
        #self.file_path_label = tk.Label(root, textvariable=self.file_path_var, width=50, anchor="w")
        #self.file_path_label.pack(pady=5)

        # Browse Button
        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # Delete Button
        self.delete_button = tk.Button(root, text = "Delete Document", command = self.delete_file)
        self.delete_button.pack(pady = 5)

        # Chat Display Box
        self.chat_display = tk.Text(root, height=20, width=50, font=("Helvetica", 16))
        self.chat_display.pack(fill='both', expand=True, pady=5)

        # Chat Entry Box
        self.chat_entry = tk.Entry(root, width=40)
        self.chat_entry.pack(fill='x', pady=5)

        # Send Button
        self.send_button = tk.Button(root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        # Bind Enter key to send_message function
        self.chat_entry.bind('<Return>', lambda event=None: self.send_message())

        self.display_message("Chatavarayan: Please upload a file in order to start our chat")
    
    def delete_file(self):
        headers = {'x-api-key': self.api_key}
        response = requests.delete(f'https://api.askyourpdf.com/v1/api/documents/{self.doc_id}', headers=headers)
        if response.status_code == 200:
            self.display_message(f'Document with {self.doc_id} deleted successfully')
        else:
            self.display_message('Failed to delete document. Error:', response.status_code)


    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.file_path_var.set(file_path)
            
            headers = {'x-api-key': self.api_key}
            with open(file_path, 'rb') as file_data:
                response = requests.post('https://api.askyourpdf.com/v1/api/upload', 
                                         headers=headers, files={'file': file_data})
                
            if response.status_code == 201:
                self.doc_id = response.json().get('docId')
                self.display_message(f"Document uploaded successfully. docId: {self.doc_id}")                
            else:
                self.display_message(f"Error: {response.status_code}. Failed to upload the document.")
                
    def send_message(self):
        message = self.chat_entry.get()
        headers = {'x-api-key': self.api_key}
        if message.strip():
            self.display_message("You: " + message)
            self.chat_entry.delete(0, tk.END)
            data = [
                {
                    "sender": "User",
                    "message": message
                }
            ]
            response = requests.post(f'https://api.askyourpdf.com/v1/chat/{self.doc_id}', headers=headers, data=json.dumps(data))
            response_message = response.json().get('answer', {}).get('message')
            if response.status_code == 200:
                self.display_message("Chatavarayan: " + response_message)
            else:
                self.display_message(f"Error: {response.status_code}. Failed to send the message.")

    def display_message(self, message):
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.insert(tk.END, '\n')
        self.chat_display.yview(tk.END)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = Chatter_Bot(root)
    root.mainloop()
