import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import json

class WorkflowToJsonApp:
    def __init__(self, root, config_file):
        self.root = root
        self.root.title("Workflow to JSON Converter")
        
        self.input_blocks = {}
        self.generated_json = None
        
        # Read and parse the configuration file
        self.parse_config(config_file)
        
        # Convert Button
        self.convert_button = tk.Button(root, text="Convert to JSON", command=self.convert_to_json)
        self.convert_button.pack(pady=10)
        
        # Save Button
        self.save_button = tk.Button(root, text="Save JSON", command=self.save_json, state=tk.DISABLED)
        self.save_button.pack(pady=10)
        
        # JSON Output
        self.json_label = tk.Label(root, text="Generated JSON:")
        self.json_label.pack(pady=10)
        self.json_text = tk.Text(root, height=15, width=60, state=tk.DISABLED)
        self.json_text.pack(pady=10)

    def parse_config(self, config_file):
        with open(config_file, 'r') as file:
            lines = file.readlines()
            
        for line in lines:
            if line.strip():
                key, label = line.split(":")
                key = key.strip()
                label = label.strip()
                self.create_input_block(key, label)

    def create_input_block(self, key, label):
        self.input_blocks[key] = {}
        self.input_blocks[key]['label'] = tk.Label(self.root, text=label)
        self.input_blocks[key]['label'].pack(pady=5)
        self.input_blocks[key]['text'] = tk.Text(self.root, height=5, width=60)
        self.input_blocks[key]['text'].pack(pady=5)
    
    def convert_to_json(self):
        json_output = {}
        for key, widgets in self.input_blocks.items():
            text = widgets['text'].get("1.0", tk.END).strip()
            if text:
                json_output[key] = text
            else:
                messagebox.showerror("Input Error", f"{widgets['label'].cget('text')} cannot be empty.")
                return
        
        try:
            # Add metadata
            metadata = {
                "generated_on": datetime.now().isoformat()
            }
            json_output["metadata"] = metadata

            self.generated_json = json_output
            self.json_text.config(state=tk.NORMAL)
            self.json_text.delete("1.0", tk.END)
            self.json_text.insert(tk.END, json.dumps(json_output, indent=4))
            self.json_text.config(state=tk.DISABLED)
            self.save_button.config(state=tk.NORMAL)
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))
    
    def save_json(self):
        if not self.generated_json:
            messagebox.showerror("Save Error", "No JSON data to save.")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json"),
                                                            ("All files", "*.*")],
                                                 initialdir="./")
        if file_path:
            try:
                with open(file_path, 'w') as json_file:
                    json.dump(self.generated_json, json_file, indent=4)
                messagebox.showinfo("Save Success", f"JSON file saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

if __name__ == "__main__":
    config_file = 'workflow_config.txt'
    root = tk.Tk()
    app = WorkflowToJsonApp(root, config_file)
    root.mainloop()
