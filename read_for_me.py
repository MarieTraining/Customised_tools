import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3

# Funkce pro načtení webové stránky
def fetch_webpage(url):
    try:
        # Odeslání HTTP GET požadavku na URL
        response = requests.get(url)
        
        # Kontrola, zda byl požadavek úspěšný
        if response.status_code == 200:
            return response.text
        else:
            print(f"Selhalo načtení stránky. Status kód: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Došlo k chybě: {e}")
        return None

# Funkce pro extrakci textu z HTML obsahu
def extract_text(html_content):
    # Parsování HTML obsahu pomocí BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extrakce veškerého textu ze stránky
    text = soup.get_text()
    
    return text

# Funkce pro předčítání textu nahlas
def read_text_aloud(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Funkce pro zobrazení a čtení textu z URL
def load_and_read():
    url = url_entry.get()
    
    # Načtení obsahu webové stránky
    html_content = fetch_webpage(url)
    
    if html_content:
        # Extrakce textu z webové stránky
        page_text = extract_text(html_content)
        
        # Zobrazení textu ve velkém textovém poli
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, page_text)
        
        # Předčítání textu nahlas
        read_text_aloud(page_text)
    else:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, "Selhalo načtení webové stránky.")

# Nastavení Tkinter GUI
root = tk.Tk()
root.title("Čtečka webových stránek")

# Vytvoření vstupního pole pro URL
url_label = tk.Label(root, text="Zadejte URL:", font=("Arial", 14))
url_label.pack(pady=10)

url_entry = tk.Entry(root, font=("Arial", 14), width=50)
url_entry.pack(pady=10)

# Vytvoření tlačítka pro načtení a čtení textu
load_button = tk.Button(root, text="Načíst a Přečíst", command=load_and_read, font=("Arial", 14))
load_button.pack(pady=10)

# Vytvoření textového pole pro zobrazení načteného textu
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 18), width=80, height=20)
text_area.pack(pady=10)

# Spuštění hlavní smyčky Tkinter
root.mainloop()
