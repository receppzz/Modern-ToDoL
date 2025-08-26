# todo_app.py
# Basit ama "elle tutulur" To-Do masaüstü uygulaması
# - Tkinter (standart kütüphane) ile GUI
# - tasks.json dosyasına otomatik kaydetme/yükleme
# - Çift tıkla: tamamlandı/geri al
# - Seçileni sil / Tamamlananları temizle / Tümünü temizle

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------
# Kalıcı veri (JSON dosyası)
# -----------------------
DATA_FILE = Path(__file__).with_name("tasks.json")

def load_tasks():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Beklenen yapı: [{"text": str, "done": bool}, ...]
                if isinstance(data, list):
                    return [t for t in data if "text" in t and "done" in t]
        except Exception:
            pass
    return []

def save_tasks():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Kayıt Hatası", f"Dosyaya yazılamadı:\n{e}")

# -----------------------
# GUI işlevleri
# -----------------------
def render():
    """Listbox'ı bellekteki görevlerle yeniden doldur."""
    listbox.delete(0, tk.END)
    for t in tasks:
        prefix = "✓ " if t["done"] else "• "
        listbox.insert(tk.END, prefix + t["text"])

def add_task(event=None):
    text = entry.get().strip()
    if not text:
        messagebox.showwarning("Uyarı", "Boş görev ekleyemezsin.")
        return
    tasks.append({"text": text, "done": False})
    save_tasks()
    entry.delete(0, tk.END)
    render()

def delete_selected():
    sel = listbox.curselection()
    if not sel:
        messagebox.showinfo("Bilgi", "Lütfen listeden bir görev seç.")
        return
    # Birden fazla seçimde indexler bozulmasın diye tersten sil
    for idx in sorted(sel, reverse=True):
        tasks.pop(idx)
    save_tasks()
    render()

def toggle_done(event=None):
    """Seçili görevi tamamlandı/geri al (çift tıkla)."""
    sel = listbox.curselection()
    if not sel:
        return
    for idx in sel:
        tasks[idx]["done"] = not tasks[idx]["done"]
    save_tasks()
    render()

def clear_completed():
    if not any(t["done"] for t in tasks):
        messagebox.showinfo("Bilgi", "Tamamlanan görev yok.")
        return
    if messagebox.askyesno("Onay", "Tamamlanan görevler silinsin mi?"):
        remaining = [t for t in tasks if not t["done"]]
        tasks.clear()
        tasks.extend(remaining)
        save_tasks()
        render()

def clear_all():
    if not tasks:
        return
    if messagebox.askyesno("Onay", "TÜM görevler silinsin mi?"):
        tasks.clear()
        save_tasks()
        render()

def on_enter_focus(event=None):
    entry.focus_set()

# -----------------------
# Uygulama Penceresi
# -----------------------
root = tk.Tk()
root.title("Görev Listesi (To-Do)")
root.geometry("520x540")
root.minsize(480, 460)

# ttk stil (hafif modern görünüm)
style = ttk.Style(root)
try:
    style.theme_use("clam")
except Exception:
    pass
style.configure("TButton", padding=8)
style.configure("TLabel", padding=4)
style.configure("TEntry", padding=4)

# Üst çerçeve: başlık
header = ttk.Frame(root)
header.pack(fill="x", padx=14, pady=(14, 8))

title = ttk.Label(header, text="✅ Görev Listem", font=("Segoe UI", 16, "bold"))
title.pack(side="left")

# Giriş çerçevesi: entry + ekle butonu
entry_frame = ttk.Frame(root)
entry_frame.pack(fill="x", padx=14, pady=(4, 8))

entry = ttk.Entry(entry_frame)
entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
entry.bind("<Return>", add_task)   # Enter ile ekle

add_btn = ttk.Button(entry_frame, text="➕ Ekle", command=add_task)
add_btn.pack(side="left")

# Liste + kaydırma
list_frame = ttk.Frame(root)
list_frame.pack(fill="both", expand=True, padx=14, pady=(6, 8))

listbox = tk.Listbox(
    list_frame,
    selectmode=tk.EXTENDED,     # çoklu seçim
    activestyle="none",
    font=("Segoe UI", 11),
)
listbox.pack(side="left", fill="both", expand=True)

scroll = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
scroll.pack(side="right", fill="y")
listbox.configure(yscrollcommand=scroll.set)

# Alt butonlar
btns = ttk.Frame(root)
btns.pack(fill="x", padx=14, pady=(4, 14))

done_btn = ttk.Button(btns, text="✓ Tamamlandı / Geri Al", command=toggle_done)
done_btn.pack(side="left")

del_btn = ttk.Button(btns, text="🗑 Seçileni Sil", command=delete_selected)
del_btn.pack(side="left", padx=8)

clear_done_btn = ttk.Button(btns, text="🧹 Tamamlananları Temizle", command=clear_completed)
clear_done_btn.pack(side="left")

clear_all_btn = ttk.Button(btns, text="❌ Tümünü Temizle", command=clear_all)
clear_all_btn.pack(side="right")

# Kısayollar
root.bind("<Control-n>", on_enter_focus)   # Ctrl+N ile girişe odaklan
listbox.bind("<Double-Button-1>", toggle_done)  # çift tıkla tamamlandı/geri

# Veri: yükle ve ekrana bas
tasks = load_tasks()
render()
entry.focus()

root.mainloop()
