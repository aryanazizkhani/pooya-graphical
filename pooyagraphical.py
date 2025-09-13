import os, datetime, subprocess, webbrowser, tkinter as tk
from tkinter import Toplevel, filedialog, messagebox
from PIL import Image, ImageTk
try:
    import cv2
except ImportError:
    cv2 = None

# =================== تنظیمات و ذخیره فایل‌ها
current_bg = "SystemButtonFace"
current_font = ("Arial", 10)
current_btn_color = "lightgray"

EXE_FILE = "exes.txt"
APK_FILE = "apks.txt"
LDPLAYER_PATH = r"C:\Program Files\LDPlayer\LDPlayer9\ldconsole.exe"  # مسیر LDPlayer

def save_list(file_path, items):
    with open(file_path, "w", encoding="utf-8") as f:
        for item in items: f.write(item+"\n")

def load_list(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

exe_items = load_list(EXE_FILE)
apk_items = load_list(APK_FILE)

# =================== اپلیکیشن‌های ساده
def notepad():
    nt = Toplevel(m); nt.title("📝")
    txt = tk.Text(nt, font=current_font); txt.pack(expand=True, fill="both")
    tk.Button(nt, text="💾", command=lambda: save_note(txt)).pack()

def save_note(txt):
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, "w", encoding="utf-8") as f: f.write(txt.get("1.0", "end"))

def calculator():
    calc = Toplevel(m); calc.title("🧮")
    expr = tk.StringVar(); e = tk.Entry(calc, textvariable=expr, font=("Arial",18))
    e.grid(row=0, column=0, columnspan=4)
    def press(x): expr.set(expr.get()+str(x))
    def equal(): 
        try: expr.set(eval(expr.get()))
        except: expr.set("Err")
    for i,ch in enumerate("789/456*123-0.+="):
        cmd = equal if ch=="=" else (lambda c=ch: press(c))
        tk.Button(calc, text=ch, command=cmd, relief="flat").grid(row=1+i//4, column=i%4, sticky="nsew")

def image_viewer():
    f = filedialog.askopenfilename(filetypes=[("Images","*.png;*.jpg")])
    if f:
        win = Toplevel(m); win.title("📷")
        img = Image.open(f).resize((400,300)); tkimg = ImageTk.PhotoImage(img)
        tk.Label(win,image=tkimg).pack(); win.mainloop()

def video_player():
    if not cv2: return messagebox.showerror("Error","cv2 missing")
    f = filedialog.askopenfilename(filetypes=[("Videos","*.mp4;*.avi")])
    if f:
        cap=cv2.VideoCapture(f)
        while cap.isOpened():
            r,frame=cap.read()
            if not r: break
            cv2.imshow("🎬",frame)
            if cv2.waitKey(25)&0xFF==ord('q'):break
        cap.release(); cv2.destroyAllWindows()

def audio_player():
    try: import pygame
    except: return messagebox.showerror("Error","pygame missing")
    f=filedialog.askopenfilename(filetypes=[("Audio","*.mp3;*.wav")])
    if f:
        pygame.mixer.init(); pygame.mixer.music.load(f); pygame.mixer.music.play()
        win=Toplevel(m); win.title("🎵")
        tk.Button(win,text="⏸",command=pygame.mixer.music.pause,relief="flat").pack()
        tk.Button(win,text="▶",command=pygame.mixer.music.unpause,relief="flat").pack()
        tk.Button(win,text="⏹",command=pygame.mixer.music.stop,relief="flat").pack()

# =================== EXE Launcher پیشرفته

# ===== EXE Launcher =====
def exe_launcher():
    exe_win = Toplevel()
    exe_win.title("EXE Launcher")
    exe_win.geometry("420x420")

    listbox = tk.Listbox(exe_win, width=55, height=15)
    listbox.pack(pady=10)

    btn_frame = tk.Frame(exe_win)
    btn_frame.pack(pady=6)

    tk.Button(btn_frame, text="➕ Add EXE", command=lambda: add_exe(listbox), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="▶️ Run", command=lambda: run_exe(listbox), width=12).pack(side="left", padx=5)
    tk.Button(btn_frame, text="❌ Remove", command=lambda: remove_exe(listbox), width=12).pack(side="left", padx=5)

def add_exe(listbox):
    file = filedialog.askopenfilename(filetypes=[("EXE files", "*.exe")])
    if file:
        listbox.insert(tk.END, file)

def run_exe(listbox):
    selected = listbox.curselection()
    if selected:
        exe_path = listbox.get(selected[0])
        try:
            os.startfile(exe_path)
        except Exception as e:
            messagebox.showerror("Error", f"Cannot run EXE:\n{e}")

def remove_exe(listbox):
    selected = listbox.curselection()
    if selected:
        listbox.delete(selected[0])



    tk.Button(exe_launcher, text=tr("add_exe"), command=add_exe, bg=current_btn_color, width=14).pack(side="left", padx=5)
    tk.Button(exe_launcher, text=tr("run"), command=run_exe, bg=current_btn_color, width=10).pack(side="left", padx=5)
    tk.Button(exe_launcher, text=tr("remove"), command=remove_exe, bg=current_btn_color, width=12).pack(side="left", padx=5)


# ===== APK Launcher =====
def apk_launcher(m):
    apk_win = Toplevel(m)
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
                emulator_path = r"D:\LDPlayer\LDPlayer9\dnplayer.exe"  # مسیر LDPlayer
                subprocess.Popen([emulator_path, "-apk", apk_path])
            except Exception as e:
                messagebox.showerror(tr("error"), f"{tr('cant_run')}\n{e}")
        else:
            messagebox.showwarning(tr("warning"), "هیچ فایل انتخاب نشده است!")

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



# =================== APK Launcher پیشرفته
def open_apk_launcher():
    apk_win = Toplevel(m); apk_win.title("📱 APK Launcher"); apk_win.geometry("400x300")
    lb = tk.Listbox(apk_win, width=50, height=10); lb.pack(pady=10)
    for item in apk_items: lb.insert(tk.END, item)

    def add_apk():
        file = filedialog.askopenfilename(filetypes=[("APK files","*.apk")])
        if file: apk_items.append(file); lb.insert(tk.END,file); save_list(APK_FILE,apk_items)

    def run_apk():
        sel = lb.curselection()
        if sel:
            apk_path = lb.get(sel[0])
            try:
                cmd = f'"{LDPLAYER_PATH}" installapp --name LDPlayer9 --file "{apk_path}"'
                subprocess.Popen(cmd,shell=True)
                messagebox.showinfo("📱 APK Runner", f"APK اجرا شد:\n{apk_path}")
            except Exception as e:
                messagebox.showerror("خطا", f"اجرا نشد:\n{e}")

    def remove_apk():
        sel = lb.curselection()
        if sel:
            idx = sel[0]; lb.delete(idx); del apk_items[idx]; save_list(APK_FILE,apk_items)

    tk.Button(apk_win,text="➕",command=add_apk).pack(side="left",padx=5)
    tk.Button(apk_win,text="▶️",command=run_apk).pack(side="left",padx=5)
    tk.Button(apk_win,text="❌",command=remove_apk).pack(side="left",padx=5)

# =================== تنظیمات و اطلاعات
def open_settings():
    sett=Toplevel(m); sett.title("⚙ تنظیمات")
    tk.Label(sett,text="🎨 پس‌زمینه:").pack()
    for name,color in [("آبی روشن","lightblue"),("سفید","white"),("مشکی","black"),
                       ("سبز","green"),("قرمز","red"),("آبی","blue")]:
        tk.Button(sett,text=f"🎨 {name}",bg=color,relief="flat",
                  command=lambda c=color: m.configure(bg=c)).pack(fill="x",pady=2,padx=20)
    tk.Label(sett,text="🌐 زبان:").pack(pady=5)
    tk.Button(sett,text="🌐 فارسی",relief="flat").pack()
    tk.Button(sett,text="🌐 English",relief="flat").pack()

def openinfo():
    info=Toplevel(m); info.title("ℹ")
    tk.Label(info,text="Pooya Graphical - v1.2").pack(pady=20)
    tk.Button(info,text="❌",command=info.destroy,relief="flat").pack()

# =================== منو اصلی
def open_menu():
    menu=Toplevel(m); menu.title("📋 فهرست")
    btns=[("📝",notepad),("🧮",calculator),("📷",image_viewer),("🎬",video_player),
          ("🎵",audio_player),("💻",exe_launcher),("📱",open_apk_launcher),
          ("🌐",lambda: webbrowser.open("https://google.com")),
          ("⚙",open_settings),("ℹ",openinfo)]
    for i,(ic,cmd) in enumerate(btns):
        tk.Button(menu,text=ic,command=cmd,font=("Arial",18),
                  width=4,height=2,relief="flat",bg="lightgray").grid(row=i//3,column=i%3,padx=8,pady=8)

# =================== پنجره اصلی
m=tk.Tk(); m.title("PG"); m.geometry("240x320")
time_label=tk.Label(m,font=("Arial",16)); time_label.pack(pady=50)
def tick(): time_label.config(text=datetime.datetime.now().strftime("%H:%M:%S")); m.after(1000,tick)
tick()

# نوار پایین
bar=tk.Frame(m,bg="darkblue",height=40); bar.pack(side="bottom",fill="x")
tk.Button(bar,text="📋",command=open_menu,font=("Arial",16),relief="flat",bg="lightgray").pack(side="left",padx=10,pady=5)
tk.Button(bar,text="⚙",command=open_settings,font=("Arial",16),relief="flat",bg="lightgray").pack(side="right",padx=10,pady=5)

m.mainloop()
