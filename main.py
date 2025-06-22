import tkinter as tk
from tkinter import messagebox
from lunarcalendar import Converter, Solar
from datetime import datetime

# === Kéo cửa sổ ===
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    x = root.winfo_x() + deltax
    y = root.winfo_y() + deltay
    root.geometry(f"+{x}+{y}")

# === Nút chức năng ===
def minimize():
    root.overrideredirect(False)  # Tạm bật lại viền
    root.iconify()
    root.after(200, lambda: root.overrideredirect(True))  # Bật lại sau khi từ dock mở lại

def toggle_maximize():
    if not hasattr(root, "maximized") or not root.maximized:
        root.original_geometry = root.geometry()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}+0+0")
        root.maximized = True
    else:
        root.geometry(root.original_geometry)
        root.maximized = False

# === Xử lý lịch âm ===
def convert_today_to_lunar():
    today = datetime.now()
    solar = Solar(today.year, today.month, today.day)
    lunar = Converter.Solar2Lunar(solar)
    result = f"Hôm nay (Âm lịch): {lunar.day}/{lunar.month}/{lunar.year}"
    if lunar.isleap:
        result += " (Nhuận)"
    result_label.config(text=result)

def convert_to_lunar():
    try:
        day = int(day_entry.get())
        month = int(month_entry.get())
        year = int(year_entry.get())

        solar = Solar(year, month, day)
        lunar = Converter.Solar2Lunar(solar)

        result = f"{day}/{month}/{year} → Âm lịch: {lunar.day}/{lunar.month}/{lunar.year}"
        if lunar.isleap:
            result += " (Nhuận)"
        result_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể chuyển đổi ngày.\nChi tiết: {e}")

# === Tạo giao diện ===
root = tk.Tk()
root.title("Lịch Âm")
root.geometry("520x360+60+60")
root.configure(bg="#f5f5f5")
root.overrideredirect(True)
root.attributes("-topmost", True)

# === Thanh tiêu đề giả (để kéo + chứa nút) ===
drag_area = tk.Frame(root, bg="#dddddd", height=40)
drag_area.pack(fill=tk.X, side=tk.TOP)
drag_area.bind("<Button-1>", start_move)
drag_area.bind("<B1-Motion>", do_move)

# === Nút kiểu macOS ===
circle_radius = 12

btn_close = tk.Canvas(drag_area, width=circle_radius*2, height=circle_radius*2, highlightthickness=0, bg="#dddddd")
btn_close.create_oval(2, 2, 2*circle_radius, 2*circle_radius, fill="#FF5F56", outline="")
btn_close.place(x=10, y=10)
btn_close.bind("<Button-1>", lambda e: root.destroy())

btn_min = tk.Canvas(drag_area, width=circle_radius*2, height=circle_radius*2, highlightthickness=0, bg="#dddddd")
btn_min.create_oval(2, 2, 2*circle_radius, 2*circle_radius, fill="#FFBD2E", outline="")
btn_min.place(x=35, y=10)
btn_min.bind("<Button-1>", lambda e: minimize())

btn_max = tk.Canvas(drag_area, width=circle_radius*2, height=circle_radius*2, highlightthickness=0, bg="#dddddd")
btn_max.create_oval(2, 2, 2*circle_radius, 2*circle_radius, fill="#27C93F", outline="")
btn_max.place(x=60, y=10)
btn_max.bind("<Button-1>", lambda e: toggle_maximize())

# === Nội dung chính ===
font_label = ("Arial", 18)
tk.Label(root, text="Ngày:", bg="#f5f5f5", font=font_label).place(x=20, y=60)
tk.Label(root, text="Tháng:", bg="#f5f5f5", font=font_label).place(x=20, y=120)
tk.Label(root, text="Năm:", bg="#f5f5f5", font=font_label).place(x=20, y=180)

day_entry = tk.Entry(root, width=5, font=("Arial", 18))
month_entry = tk.Entry(root, width=5, font=("Arial", 18))
year_entry = tk.Entry(root, width=8, font=("Arial", 18))

day_entry.place(x=130, y=60)
month_entry.place(x=130, y=120)
year_entry.place(x=130, y=180)

convert_button = tk.Button(root, text="→ Âm lịch", command=convert_to_lunar, font=("Arial", 16))
convert_button.place(x=300, y=120)

result_label = tk.Label(root, text="", fg="blue", font=("Arial", 18), wraplength=460, bg="#f5f5f5")
result_label.place(x=20, y=260)

# === Hiển thị âm lịch hôm nay khi mở ===
convert_today_to_lunar()

root.mainloop()
