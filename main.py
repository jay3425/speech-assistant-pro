import tkinter as tk
from tkinter import filedialog
import pyttsx3
import speech_recognition as sr
import threading

# ---------- INIT ----------
engine = pyttsx3.init()

# ---------- VOICES ----------
voices = engine.getProperty('voices')

# ---------- FUNCTIONS ----------

def speak_text():
    text = text_box.get("1.0", tk.END)
    if text.strip():
        apply_voice_settings()
        set_status("Speaking...")
        engine.say(text)
        engine.runAndWait()
        set_status("Done ✅")

def save_audio():
    text = text_box.get("1.0", tk.END)
    if text.strip():
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3")
        if file_path:
            apply_voice_settings()
            engine.save_to_file(text, file_path)
            engine.runAndWait()
            set_status("Audio saved 🎧")

def listen_speech():
    threading.Thread(target=_listen_thread).start()

def _listen_thread():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        animate_mic(True)
        set_status("Listening...")

        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)

            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, text)

            set_status("Recognized ✅")

        except Exception:
            set_status("Error ❌")

        animate_mic(False)

def save_text():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_box.get("1.0", tk.END))
        set_status("Text saved 💾")

def load_text():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, f.read())
        set_status("Text loaded 📂")

def apply_voice_settings():
    engine.setProperty('rate', speed_slider.get())
    engine.setProperty('volume', volume_slider.get())

    selected_voice = voice_var.get()
    engine.setProperty('voice', voices[selected_voice].id)

def set_status(msg):
    status_var.set(msg)

# ---------- MIC ANIMATION ----------
def animate_mic(active):
    if active:
        mic_canvas.itemconfig(mic_circle, fill="#ef4444")
    else:
        mic_canvas.itemconfig(mic_circle, fill="#334155")

# ---------- UI ----------
window = tk.Tk()
window.title("Speech Assistant Pro")
window.geometry("520x550")
window.configure(bg="#0f172a")

main = tk.Frame(window, bg="#0f172a")
main.pack(fill="both", expand=True, padx=20, pady=20)

# Title
tk.Label(main, text="🎙 Speech Assistant", font=("Segoe UI", 18, "bold"),
         fg="white", bg="#0f172a").pack(pady=10)

# Card
card = tk.Frame(main, bg="#1e293b")
card.pack(fill="both", expand=True)

# Text box
text_box = tk.Text(card, height=6, font=("Segoe UI", 11),
                   bg="#0f172a", fg="white", insertbackground="white",
                   bd=0, padx=10, pady=10)
text_box.pack(fill="both", expand=True, padx=15, pady=10)

# ---------- CONTROLS ----------
controls = tk.Frame(card, bg="#1e293b")
controls.pack(pady=10)

# Speed
tk.Label(controls, text="Speed", fg="white", bg="#1e293b").grid(row=0, column=0)
speed_slider = tk.Scale(controls, from_=100, to=250, orient="horizontal",
                        bg="#1e293b", fg="white", highlightthickness=0)
speed_slider.set(170)
speed_slider.grid(row=1, column=0)

# Volume
tk.Label(controls, text="Volume", fg="white", bg="#1e293b").grid(row=0, column=1)
volume_slider = tk.Scale(controls, from_=0.0, to=1.0, resolution=0.1,
                         orient="horizontal", bg="#1e293b", fg="white",
                         highlightthickness=0)
volume_slider.set(1.0)
volume_slider.grid(row=1, column=1)

# Voice selection
tk.Label(controls, text="Voice", fg="white", bg="#1e293b").grid(row=2, column=0)

voice_var = tk.IntVar(value=0)
voice_menu = tk.OptionMenu(controls, voice_var, *range(len(voices)))
voice_menu.config(bg="#334155", fg="white", bd=0)
voice_menu.grid(row=3, column=0, pady=5)

# ---------- BUTTONS ----------
btn_frame = tk.Frame(card, bg="#1e293b")
btn_frame.pack(pady=10)

def btn(text, cmd, color):
    return tk.Button(btn_frame, text=text, command=cmd,
                     bg=color, fg="white", bd=0,
                     padx=12, pady=6, font=("Segoe UI", 10, "bold"))

btn("🔊 Speak", speak_text, "#2563eb").grid(row=0, column=0, padx=5)
btn("🎤 Listen", listen_speech, "#16a34a").grid(row=0, column=1, padx=5)
btn("💾 Save Text", save_text, "#475569").grid(row=1, column=0, padx=5, pady=5)
btn("📂 Load Text", load_text, "#475569").grid(row=1, column=1, padx=5, pady=5)
btn("🎧 Save Audio", save_audio, "#9333ea").grid(row=2, column=0, columnspan=2, pady=5)

# ---------- MIC ANIMATION ----------
mic_canvas = tk.Canvas(main, width=20, height=20, bg="#0f172a", highlightthickness=0)
mic_canvas.pack()

mic_circle = mic_canvas.create_oval(2, 2, 18, 18, fill="#334155")

# ---------- STATUS ----------
status_var = tk.StringVar(value="Status: Idle")
tk.Label(main, textvariable=status_var, fg="#94a3b8", bg="#0f172a").pack(pady=5)

# ---------- RUN ----------
window.mainloop()