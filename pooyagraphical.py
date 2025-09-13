# ==========================
# 💻 کتابخانه‌های استاندارد پایتون
# ==========================
import os
import time
import datetime
import subprocess
import webbrowser

# ==========================
# 🧠 کتابخانه‌های شخص ثالث
# ==========================
try:
    import cv2
except ImportError:
    cv2 = None
from PIL import Image, ImageTk
import numpy as np

# ==========================
# 🪟 کتابخانه گرافیکی
# ==========================
import tkinter as tk
from tkinter import Toplevel, filedialog, messagebox

# ==================== تنظیمات اولیه و i18n ====================
settings_file = "settings.txt"
default_settings = {
    "bg": "SystemButtonFace",
    "font": "Arial,10",
    "btn_color": "SystemButtonFace",
    "lang": "FA"  # EN یا FA
}
current_bg = default_settings["bg"]
current_font = ("Arial", 10)
current_btn_color = default_settings["btn_color"]
LANG = default_settings["lang"]
setting_enabled = True

texts = {
    "FA": {
        "app_title": "PG - Pooya Graphical",
        "boot_anim": "در حال راه‌اندازی پویا گرافیکال",
        "lock_title": "صفحه قفل",
        "unlock": "باز کردن قفل",
        "now": "اکنون",
        "settings": "تنظیمات",
        "toggle_settings_on": "غیرفعال کردن تنظیمات",
        "toggle_settings_off": "فعال کردن تنظیمات",
        "notepad": "دفترچه یادداشت",
        "clock": "ساعت",
        "calculator": "ماشین‌حساب",
        "image_viewer": "📷 نمایشگر تصویر",
        "video_player": "🎬 پخش ویدئو",
        "audio_player": "🎵 پخش صدا",
        "exe_runner": "اجرای EXE",
        "apk_runner": "اجرای APK",
        "vscode": "Visual Studio Code",
        "internet": "اینترنت",
        "info": "اطلاعات",
        "exit": "خروج",
        "bg_label": "🎨 پس‌زمینه:",
        "font_label": "🔤 فونت:",
        "btn_color_label": "🎨 رنگ دکمه:",
        "light_blue": "آبی روشن",
        "white": "سفید",
        "black": "مشکی",
        "green": "سبز",
        "red": "قرمز",
        "blue": "آبی",
        "default": "پیش‌فرض",
        "saved": "ذخیره شد",
        "saved_to": "ذخیره شد در:",
        "error": "خطا",
        "opencv_missing": "کتابخانه OpenCV نصب نشده است.",
        "pygame_missing": "کتابخانه pygame نصب نشده است.\nنصب: pip install pygame",
        "cant_run": "نمی‌توان اجرا کرد:",
        "audio_playing": "در حال پخش:",
        "pause": "⏸ توقف موقت",
        "resume": "▶ ادامه",
        "stop": "⏹ توقف کامل",
        "close": "❌ خروج",
        "add_exe": "➕ افزودن EXE",
        "run": "▶ اجرا",
        "remove": "❌ حذف",
        "add_apk": "➕ افزودن APK",
        "settings_title": "تنظیمات",
        "info_text": "Pooya Graphical - v1.2\nتمام حقوق محفوظ است.",
        "lang_label": "🌐 زبان:",
        "lang_fa": "فارسی",
        "lang_en": "English",
        "lock_time_fmt": "%Y-%m-%d %H:%M:%S",
    },
    "EN": {
        "app_title": "PG - Pooya Graphical",
        "boot_anim": "Pooya Graphical Booting",
        "lock_title": "Lock Screen",
        "unlock": "Unlock",
        "now": "Now",
        "settings": "Settings",
        "toggle_settings_on": "Disable Settings",
        "toggle_settings_off": "Enable Settings",
        "notepad": "Notepad",
        "clock": "Clock",
        "calculator": "Calculator",
        "image_viewer": "📷 Image Viewer",
        "video_player": "🎬 Video Player",
        "audio_player": "🎵 Audio Player",
        "exe_runner": "EXE Runner",
        "apk_runner": "APK Runner",
        "vscode": "Visual Studio Code",
        "internet": "Internet",
        "info": "Info",
        "exit": "Exit",
        "bg_label": "🎨 Background:",
        "font_label": "🔤 Font:",
        "btn_color_label": "🎨 Button Color:",
        "light_blue": "Light Blue",
        "white": "White",
        "black": "Black",
        "green": "Green",
        "red": "Red",
        "blue": "Blue",
        "default": "Default",
        "saved": "Saved",
        "saved_to": "Saved to:",
        "error": "Error",
        "opencv_missing": "OpenCV is not installed.",
        "pygame_missing": "pygame is not installed.\nInstall: pip install pygame",
        "cant_run": "Cannot run:",
        "audio_playing": "Now Playing:",
        "pause": "⏸ Pause",
        "resume": "▶ Resume",
        "stop": "⏹ Stop",
        "close": "❌ Close",
        "add_exe": "➕ Add EXE",
        "run": "▶ Run",
        "remove": "❌ Remove",
        "add_apk": "➕ Add APK",
        "settings_title": "Settings",
        "info_text": "Pooya Graphical - v1.2\nAll rights reserved.",
        "lang_label": "🌐 Language:",
        "lang_fa": "Persian",
        "lang_en": "English",
        "lock_time_fmt": "%Y-%m-%d %H:%M:%S",
    }
}

def tr(key):  # ترجمه
    return texts.get(LANG, texts["FA"]).get(key, key)

# ==================== تنظیمات ذخیره/لود ====================
def load_settings():
    global current_bg, current_font, current_btn_color, LANG
    if os.path.exists(settings_file):
        with open(settings_file, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            # پشتیبانی از نسخه قدیمی که 3 خط داشت
            if len(lines) >= 3:
                current_bg = lines[0] or default_settings["bg"]
                font_parts = (lines[1] or default_settings["font"]).split(",")
                current_font = (font_parts[0], int(font_parts[1])) if len(font_parts) >= 2 else ("Arial", 10)
                current_btn_color = lines[2] or default_settings["btn_color"]
            if len(lines) >= 4:
                LANG = lines[3] or default_settings["lang"]

def save_settings():
    with open(settings_file, "w", encoding="utf-8") as f:
        f.write(f"{current_bg}\n{current_font[0]},{current_font[1]}\n{current_btn_color}\n{LANG}")

load_settings()

# ==================== توابع رابط گرافیکی عمومی ====================
def update_all_fonts(root):
    for widget in root.winfo_children():
        try:
            widget.config(font=current_font)
        except Exception:
            pass
        update_all_fonts(widget) if isinstance(widget, (tk.Frame, Toplevel)) else None

def update_all_buttons_bg(root):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button):
            widget.config(bg=current_btn_color)
        update_all_buttons_bg(widget) if isinstance(widget, (tk.Frame, Toplevel)) else None

def change_bg(color):
    global current_bg
    current_bg = color
    t.configure(bg=color)
    save_settings()
    t.update_idletasks()

def change_font(font_tuple):
    global current_font
    current_font = font_tuple
    update_all_fonts(t)
    save_settings()

def change_btn_color(color):
    global current_btn_color
    current_btn_color = color
    update_all_buttons_bg(t)
    save_settings()

def set_language(lang_code):
    global LANG
    LANG = lang_code
    save_settings()
    rebuild_main_buttons()  # همه متن‌ها عوض بشن

# ==================== بوت اسکرین (تصویری + انیمیشنی) ====================
def show_image_boot():
    if cv2:
        try:
            boot_png = cv2.imread('pooyagraphical.png')
            if boot_png is not None:
                cv2.imshow('boot screen', boot_png)
                cv2.waitKey(500)
                cv2.destroyAllWindows()
        except Exception:
            pass

def animated_boot(root):
    boot = Toplevel(root)
    boot.overrideredirect(True)
    boot.configure(bg='black')
    w, h = 420, 200
    x = (boot.winfo_screenwidth() // 2) - (w // 2)
    y = (boot.winfo_screenheight() // 2) - (h // 2)
    boot.geometry(f"{w}x{h}+{x}+{y}")
    label = tk.Label(boot, text="", font=("Consolas", 16), fg='lime', bg='black')
    label.pack(expand=True, fill="both")

    def animate():
        for i in range(4):
            label.config(text=tr("boot_anim") + "." * i)
            boot.update()
            time.sleep(0.5)
        boot.destroy()
    boot.after(50, animate)
    boot.update()

# ==================== لاک اسکرین ====================
def show_lock_screen(root):
    lock_win = Toplevel(root)
    lock_win.title(tr("lock_title"))
    lock_win.geometry("320x180")
    lock_win.configure(bg=current_bg)
    lock_win.grab_set()  # تا باز نشده، دسترسی به اصلی نداره

    lbl = tk.Label(lock_win,
                   text=datetime.datetime.now().strftime(tr("lock_time_fmt")),
                   font=current_font, bg=current_bg)
    lbl.pack(pady=20)

    btn = tk.Button(lock_win, text=tr("unlock"),
                    command=lock_win.destroy, bg=current_btn_color, font=current_font, width=18)
    btn.pack(pady=10)

# ==================== پنجره‌های کاربردی ====================
def openinfo():
    info = Toplevel(t)
    info.geometry('320x220')
    info.title(tr("info"))
    info.configure(bg=current_bg)
    tk.Label(info, text=tr("pooya_graphical - PG all rights resevrd"), font=current_font, bg=current_bg).pack(pady=35)
    tk.Button(info, text=tr("exit"), command=info.destroy,
              font=current_font, bg=current_btn_color, width=14).pack(pady=8)

def open_settings():
    sett = Toplevel(t)
    sett.geometry('340x470')
    sett.title(tr("settings"))
    sett.configure(bg=current_bg)

    # زبان
    tk.Label(sett, text=tr("lang_label"), font=current_font, bg=current_bg).pack(pady=(8, 2))
    lang_frame = tk.Frame(sett, bg=current_bg)
    lang_frame.pack(pady=(0, 10))
    tk.Button(lang_frame, text=tr("lang_fa"),
              command=lambda: (set_language("FA"), sett.title(tr("settings_title"))),
              width=12, bg=current_btn_color).pack(side="left", padx=5)
    tk.Button(lang_frame, text=tr("lang_en"),
              command=lambda: (set_language("EN"), sett.title(tr("settings_title"))),
              width=12, bg=current_btn_color).pack(side="left", padx=5)

    # پس‌زمینه
    tk.Label(sett, text=tr("bg_label"), font=current_font, bg=current_bg).pack()
    for name, color in [(tr("light_blue"), 'lightblue'),
                        (tr("white"), 'white'),
                        (tr("black"), 'black'),
                        (tr("green"), 'green')]:
        tk.Button(sett, text=name, bg=color, command=lambda c=color: change_bg(c)).pack(pady=2, fill="x", padx=20)

    # فونت
    tk.Label(sett, text=tr("font_label"), font=current_font, bg=current_bg).pack(pady=10)
    tk.Button(sett, text='Arial 10', command=lambda: change_font(('Arial', 10))).pack(pady=2, fill="x", padx=20)
    tk.Button(sett, text='Arial 14 Bold', command=lambda: change_font(('Arial', 14, 'bold'))).pack(pady=2, fill="x", padx=20)
    tk.Button(sett, text='Courier 12 Italic', command=lambda: change_font(('Courier', 12, 'italic'))).pack(pady=2, fill="x", padx=20)

    # رنگ دکمه
    tk.Label(sett, text=tr("btn_color_label"), font=current_font, bg=current_bg).pack(pady=10)
    for name, color in [(tr("red"), 'red'),
                        (tr("blue"), 'blue'),
                        (tr("default"), 'SystemButtonFace')]:
        tk.Button(sett, text=name, bg=color, command=lambda c=color: change_btn_color(c)).pack(pady=2, fill="x", padx=20)

    # اطلاعات/خروج
    tk.Button(sett, text=tr("info"), command=openinfo, bg=current_btn_color).pack(pady=10)
    tk.Button(sett, text=tr("exit"), command=sett.destroy, bg=current_btn_color).pack(pady=5)

def notepad():
    nt = Toplevel(t)
    nt.geometry('420x420')
    nt.title(tr("notepad"))
    txt = tk.Text(nt, height=20, width=46, font=current_font)
    txt.pack(padx=10, pady=10)

    def save_note():
        file = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt")])
        if file:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(txt.get("1.0", tk.END))
            messagebox.showinfo(tr("saved"), f"{tr('saved_to')}\n{file}")

    btn_frame = tk.Frame(nt)
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text=tr("saved"), command=save_note, bg=current_btn_color, width=14).pack(side="left", padx=6)
    tk.Button(btn_frame, text=tr("exit"), command=nt.destroy, bg=current_btn_color, width=14).pack(side="left", padx=6)

def calculator():
    calc = Toplevel(t)
    calc.geometry("320x510")
    calc.title(tr("calculator"))
    expression = tk.StringVar()
    entry = tk.Entry(calc, textvariable=expression, font=("Arial", 18),
                     bd=10, insertwidth=2, width=14, borderwidth=4, justify="right")
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    def press(key): expression.set(expression.get() + str(key))
    def clear(): expression.set("")
    def equal():
        try:
            expression.set(str(eval(expression.get())))
        except Exception:
            expression.set("Error")

    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
    ]
    for (text, row, col) in buttons:
        cmd = equal if text == '=' else (lambda t=text: press(t))
        tk.Button(calc, text=text, padx=20, pady=20, font=("Arial", 12),
                  command=cmd, bg=current_btn_color).grid(row=row, column=col)
    tk.Button(calc, text='C', padx=85, pady=20, font=("Arial", 12),
              command=clear, bg=current_btn_color).grid(row=5, column=0, columnspan=4)

def exe_launcher():
    exe_win = Toplevel(t)
    exe_win.title(tr("exe_runner"))
    exe_win.geometry("420x420")

    listbox = tk.Listbox(exe_win, width=55, height=15)
    listbox.pack(pady=10)
    apps_file = "apps.txt"

    if os.path.exists(apps_file):
        with open(apps_file, "r", encoding="utf-8") as f:
            for line in f:
                path = line.strip()
                if path:
                    listbox.insert(tk.END, path)

    def save_apps():
        with open(apps_file, "w", encoding="utf-8") as f:
            for i in range(listbox.size()):
                f.write(listbox.get(i) + "\n")

    def add_exe():
        file = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])
        if file:
            listbox.insert(tk.END, file)
            save_apps()

    def run_exe():
        selected = listbox.curselection()
        if selected:
            exe_path = listbox.get(selected[0])
            try:
                            os.startfile(exe_path)
            except Exception as e:
                messagebox.showerror(tr("error"), f"{tr('cant_run')}\n{e}")

    def remove_exe():
        selected = listbox.curselection()
        if selected:
            listbox.delete(selected[0])
            save_apps()

    btn_frame = tk.Frame(exe_win)
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text=tr("add_exe"), command=add_exe, bg=current_btn_color, width=14).pack(side="left", padx=5)
    tk.Button(btn_frame, text=tr("run"), command=run_exe, bg=current_btn_color, width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text=tr("remove"), command=remove_exe, bg=current_btn_color, width=12).pack(side="left", padx=5)

def apk_launcher():
    apk_win = Toplevel(t)
    apk_win.title(tr("apk_runner"))
    apk_win.geometry("420x420")

    listbox = tk.Listbox(apk_win, width=55, height=15)
    listbox.pack(pady=10)
    apk_file = "apk.txt"

    if os.path.exists(apk_file):
        with open(apk_file, "r", encoding="utf-8") as f:
            for line in f:
                path = line.strip()
                if path:
                    listbox.insert(tk.END, path)

    def save_apks():
        with open(apk_file, "w", encoding="utf-8") as f:
            for i in range(listbox.size()):
                f.write(listbox.get(i) + "\n")

    def add_apk():
        file = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
        if file:
            listbox.insert(tk.END, file)
            save_apks()

    def run_apk():
        selected = listbox.curselection()
        if selected:
            apk_path = listbox.get(selected[0])
            try:
                emulator_path = r"D:\LDPlayer\LDPlayer9\dnplayer.exe"
                subprocess.Popen([emulator_path, "-apk", apk_path])

            except Exception as e:
                messagebox.showerror(tr("error"), f"{tr('cant_run')}\n{e}")

    def remove_apk():
        selected = listbox.curselection()
        if selected:
            listbox.delete(selected[0])
            save_apks()

    btn_frame = tk.Frame(apk_win)
    btn_frame.pack(pady=6)
    tk.Button(btn_frame, text=tr("add_apk"), command=add_apk, bg=current_btn_color, width=14).pack(side="left", padx=5)
    tk.Button(btn_frame, text=tr("run"), command=run_apk, bg=current_btn_color, width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text=tr("remove"), command=remove_apk, bg=current_btn_color, width=12).pack(side="left", padx=5)

def image_viewer():
    file = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file:
        img_win = Toplevel(t)
        img_win.title(tr("image_viewer"))
        img = Image.open(file)
        img = img.resize((700, 500))
        img_tk = ImageTk.PhotoImage(img)
        lbl = tk.Label(img_win, image=img_tk)
        lbl.image = img_tk
        lbl.pack()

def video_player():
    if not cv2:
        messagebox.showerror(tr("error"), tr("opencv_missing"))
        return
    file = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov;*.mkv")])
    if file:
        cap = cv2.VideoCapture(file)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow(tr("video_player"), frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def audio_player():
    try:
        import pygame
    except ImportError:
        messagebox.showerror(tr("error"), tr("pygame_missing"))
        return

    file = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
    if file:
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()

            audio_win = Toplevel(t)
            audio_win.title(tr("audio_player"))
            audio_win.geometry("320x170")

            lbl = tk.Label(audio_win, text=f"{tr('audio_playing')}\n{os.path.basename(file)}", font=current_font)
            lbl.pack(pady=10)

            def stop_music():
                pygame.mixer.music.stop()

            def pause_music():
                pygame.mixer.music.pause()

            def unpause_music():
                pygame.mixer.music.unpause()

            tk.Button(audio_win, text=tr("pause"), command=pause_music, bg=current_btn_color).pack(pady=2)
            tk.Button(audio_win, text=tr("resume"), command=unpause_music, bg=current_btn_color).pack(pady=2)
            tk.Button(audio_win, text=tr("stop"), command=stop_music, bg=current_btn_color).pack(pady=2)
            tk.Button(audio_win, text=tr("close"),
                      command=lambda: (stop_music(), audio_win.destroy()), bg=current_btn_color).pack(pady=2)

        except Exception as e:
            messagebox.showerror(tr("error"), f"{tr('cant_run')}\n{e}")

# ==================== سوییچ تنظیمات ====================
def toggle_setting():
    global setting_enabled
    setting_enabled = not setting_enabled
    settings_button.config(state=tk.NORMAL if setting_enabled else tk.DISABLED)
    toggle_btn.config(text=tr("toggle_settings_on") if setting_enabled else tr("toggle_settings_off"))

# ==================== دکمه‌های اصلی GUI (دو ستونه) ====================
main_buttons_frame = None
settings_button = None
toggle_btn = None

def rebuild_main_buttons():
    global main_buttons_frame, settings_button, toggle_btn
    if main_buttons_frame and main_buttons_frame.winfo_exists():
        for w in main_buttons_frame.winfo_children():
            w.destroy()
        main_buttons_frame.destroy()

    main_buttons_frame = tk.Frame(t, bg=current_bg)
    main_buttons_frame.pack(pady=10, padx=10, fill="both", expand=True)

    button_defs = [
        (tr("settings"), open_settings),
        (tr("toggle_settings_on") if setting_enabled else tr("toggle_settings_off"), toggle_setting),
        (tr("notepad"), notepad),
        (tr("clock"), lambda: tk.Label(t, text=datetime.datetime.now().strftime(tr("lock_time_fmt")),
                                       font=current_font, bg=current_bg).pack()),
        (tr("calculator"), calculator),
        (tr("image_viewer"), image_viewer),
        (tr("video_player"), video_player),
        (tr("audio_player"), audio_player),
        (tr("exe_runner"), exe_launcher),
        (tr("apk_runner"), apk_launcher),
        (tr("vscode"), lambda : subprocess.Popen("code .", shell=True)),
        (tr("internet"), lambda: webbrowser.open("https://www.google.com")),
        (tr("info"), openinfo),
    ]

    # ساخت دکمه‌ها دو ستونه
    for i, (text, cmd) in enumerate(button_defs):
        row, col = divmod(i, 2)
        btn = tk.Button(main_buttons_frame, text=text, command=cmd, width=22, bg=current_btn_color, font=current_font)
        btn.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

    # برای دسترسی به دو دکمه‌ی خاص
    settings_button = main_buttons_frame.grid_slaves(row=0, column=0)[0]  # تنظیمات
    toggle_btn = main_buttons_frame.grid_slaves(row=0, column=1)[0]      # سوییچ تنظیمات

    # کشسانی سطر/ستون‌ها
    rows = (len(button_defs) + 1) // 2
    for r in range(rows):
        main_buttons_frame.grid_rowconfigure(r, weight=1)
    main_buttons_frame.grid_columnconfigure(0, weight=1)
    main_buttons_frame.grid_columnconfigure(1, weight=1)

# ==================== اجرای برنامه ====================
# فقط یک Tk اصلی
t = tk.Tk()
t.withdraw()  # تا پایان بوت و لاک نشان داده نشود
t.geometry("420x640+200+120")
t.title(tr("PG -pooya graphical v2.0"))
t.configure(bg=current_bg)

# بوت
show_image_boot()
animated_boot(t)

# لاک‌اسکرین
show_lock_screen(t)

# آماده‌سازی بدنه
t.deiconify()
rebuild_main_buttons()
update_all_fonts(t)
update_all_buttons_bg(t)

# شروع حلقه اصلی
t.mainloop()
