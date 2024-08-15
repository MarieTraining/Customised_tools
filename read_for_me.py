"""přečte nahlas hlavni odstavec ze stranky, zatim neumi stop/pause """
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
import pyttsx3

# Inicializace pyttsx3 engine
engine = pyttsx3.init()

# Nastavení rychlosti řeči (nižší hodnota = pomalejší řeč)
current_rate = engine.getProperty('rate')  # Získání aktuální rychlosti řeči
engine.setProperty('rate', current_rate - 50)  # Snížení rychlosti řeči o 50 (přizpůsobit podle potřeby)

# Globální proměnné
stop_reading = False

def read_text_aloud(text):
    global stop_reading

    sentences = text.split('. ')  # Rozdělení textu na věty
    for sentence in sentences:
        if stop_reading:
            print("Čtení zastaveno.")
            break

        print(f"Čtení věty: {sentence}")
        engine.say(sentence)
        engine.runAndWait()

def fetch_webpage(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Selhalo načtení stránky. Status kód: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Došlo k chybě: {e}")
        return None

def extract_text(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    # Extrakce textu z <p> tagů === odstavce, ne menu
    paragraphs = soup.find_all('p')
    text = ' '.join(p.get_text() for p in paragraphs)
    return text

def load_and_read():
    global stop_reading
    stop_reading = False  # Resetování stavu zastavení
    url = url_entry.get()
    html_content = fetch_webpage(url)
    if html_content:
        page_text = extract_text(html_content)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, page_text)
        # Spuštění TTS
        read_text_aloud(page_text)
    else:
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.INSERT, "Selhalo načtení webové stránky.")

# Tkinter GUI
root = tk.Tk()
root.title("Čtečka webových stránek")

url_label = tk.Label(root, text="Zadejte URL:", font=("Arial", 14))
url_label.pack(pady=10)

url_entry = tk.Entry(root, font=("Arial", 14), width=50)
url_entry.pack(pady=10)

load_button = tk.Button(root, text="Načíst a Přečíst", command=load_and_read, font=("Arial", 14))
load_button.pack(pady=10)

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 18), width=80, height=20)
text_area.pack(pady=10)

# Spuštění hlavní smyčky Tkinter
root.mainloop()
