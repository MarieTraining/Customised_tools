import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox

class ScreenScissors(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screenshot Tool")
        self.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        button_style = {'bg': 'navy', 'fg': 'white', 'font': ('Helvetica', 12, 'bold'), 'relief': 'flat'}
        capture_button = tk.Button(self, text="Capture Screenshot", command=self.capture_screenshot, **button_style)
        capture_button.pack(pady=20, fill='x', padx=20)

    def capture_screenshot(self):
        self.withdraw()  # skryt okno
        self.screen = tk.Toplevel(self)
        self.screen.attributes('-fullscreen', True)
        self.screen.attributes('-alpha', 0.3)  # pruhlednost
        self.canvas = tk.Canvas(self.screen, bg='gray', bd=0, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)

        self.start_x = self.start_y = 0
        self.rect = None

        self.canvas.bind('<Button-1>', self.start_selection)
        self.canvas.bind('<B1-Motion>', self.update_selection)
        self.canvas.bind('<ButtonRelease-1>', self.end_selection)

    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def update_selection(self, event):
        cur_x, cur_y = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def end_selection(self, event):
        end_x, end_y = event.x, event.y
        self.screen.destroy()  # zavri okno
        self.deiconify()  # ukaz hlavni okno

        # celou obrazovku
        screenshot = pyautogui.screenshot()
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        right = max(self.start_x, end_x)
        bottom = max(self.start_y, end_y)

        # nuzky
        cropped_image = screenshot.crop((left, top, right, bottom))

        # ulozeni vystrizku
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
        if file_path:
            try:
                cropped_image.save(file_path)
                messagebox.showinfo("Success", "Screenshot saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save screenshot: {e}")

if __name__ == "__main__":
    app = ScreenScissors()
    app.mainloop()
