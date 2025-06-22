import tkinter as tk
from tkinter import messagebox
from lunarcalendar import Converter, Solar
from datetime import datetime, timedelta
import calendar

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

# === Zoom ===
scale = 1.0
def on_mousewheel(event):
    global scale
    if event.delta > 0 or event.num == 4:
        scale += 0.1
    elif event.delta < 0 or event.num == 5:
        scale = max(0.5, scale - 0.1)
    root.tk.call('tk', 'scaling', scale)

# === Resize bằng mép ===
resizing = False
def start_resize(event):
    global resizing
    resizing = True
    root.start_x = event.x_root
    root.start_y = event.y_root
    root.start_width = root.winfo_width()
    root.start_height = root.winfo_height()

def do_resize(event):
    if resizing:
        dx = event.x_root - root.start_x
        dy = event.y_root - root.start_y
        new_w = max(400, root.start_width + dx)
        new_h = max(300, root.start_height + dy)
        root.geometry(f"{new_w}x{new_h}")

def stop_resize(event):
    global resizing
    resizing = False

# === Nút chức năng ===
def minimize():
    root.overrideredirect(False)
    root.iconify()
    root.after(200, lambda: root.overrideredirect(True))

def toggle_maximize():
    if not hasattr(root, "maximized") or not root.maximized:
        root.original_geometry = root.geometry()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f"{sw}x{sh-30}+0+30")
        root.maximized = True
    else:
        root.geometry(root.original_geometry)
        root.maximized = False

# === Lấy ngày âm ===
def get_lunar_str(date):
    solar = Solar(date.year, date.month, date.day)
    lunar = Converter.Solar2Lunar(solar)
    return f"{lunar.day}/{lunar.month}"

# === Cửa sổ chính ===
root = tk.Tk()
root.title("Lịch Âm")
root.geometry("700x600+100+100")
root.configure(bg="#f9f9f9")
root.overrideredirect(True)
root.attributes("-topmost", True)

root.bind("<MouseWheel>", on_mousewheel)
root.bind("<Button-4>", on_mousewheel)
root.bind("<Button-5>", on_mousewheel)

# === Thanh kéo ===
drag_area = tk.Frame(root, bg="#e0e0e0", height=40)
drag_area.pack(fill=tk.X, side=tk.TOP)
drag_area.bind("<Button-1>", start_move)
drag_area.bind("<B1-Motion>", do_move)

# === Nút macOS ===
def create_mac_button(parent, color, x, symbol, command):
    frame = tk.Frame(parent, width=16, height=16, bg=parent["bg"])
    frame.place(x=x, y=12)
    circle = tk.Canvas(frame, width=14, height=14, highlightthickness=0, bg=parent["bg"])
    circle.create_oval(0, 0, 14, 14, fill=color, outline=color)
    circle.pack()
    label = tk.Label(frame, text=symbol, font=("Arial", 8, "bold"), fg="white", bg=color)
    label.place(relx=0.5, rely=0.5, anchor="center")
    label.lower()
    def on_enter(event): label.lift()
    def on_leave(event): label.lower()
    frame.bind("<Enter>", on_enter)
    frame.bind("<Leave>", on_leave)
    circle.bind("<Enter>", on_enter)
    circle.bind("<Leave>", on_leave)
    label.bind("<Button-1>", lambda e: command())
    circle.bind("<Button-1>", lambda e: command())

create_mac_button(drag_area, "#FF5F56", 8, "×", root.destroy)
create_mac_button(drag_area, "#FFBD2E", 28, "–", minimize)
create_mac_button(drag_area, "#27C93F", 48, "⤢", toggle_maximize)

# === Resize handle ===
resize_handle = tk.Frame(root, cursor="bottom_right_corner", bg="#dddddd", width=10, height=10)
resize_handle.place(relx=1.0, rely=1.0, anchor="se")
resize_handle.bind("<Button-1>", start_resize)
resize_handle.bind("<B1-Motion>", do_resize)
resize_handle.bind("<ButtonRelease-1>", stop_resize)

# === Lịch tháng dạng lưới đẹp ===
today = datetime.now()
year = today.year
month = today.month
cal = calendar.Calendar(firstweekday=0)  # Thứ 2 là ngày đầu tuần

calendar_frame = tk.Frame(root, bg="#f9f9f9")
calendar_frame.pack(pady=10, expand=True, fill=tk.BOTH)

# Tiêu đề tháng
tk.Label(calendar_frame, text=f"Tháng {month} / {year}", font=("Arial", 22, "bold"), bg="#f9f9f9", fg="#333333").grid(row=0, column=0, pady=10)

# Tên thứ (dùng grid để hỗ trợ co giãn)
weekdays_frame = tk.Frame(calendar_frame, bg="#f9f9f9")
weekdays_frame.grid(row=1, column=0, sticky="nsew")

for i, wd in enumerate(["T2", "T3", "T4", "T5", "T6", "T7", "CN"]):
    tk.Label(weekdays_frame, text=wd, font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#555555", pady=5).grid(row=0, column=i, padx=1, sticky="nsew")
    weekdays_frame.columnconfigure(i, weight=1)

calendar_frame.rowconfigure(1, weight=0)
calendar_frame.columnconfigure(0, weight=1)

# Lưới ngày
grid_frame = tk.Frame(calendar_frame, bg="#f0f0f0", bd=1, relief=tk.FLAT)
grid_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
for i in range(7):
    grid_frame.columnconfigure(i, weight=1)

row = 0
col = 0
for date in cal.itermonthdates(year, month):
    is_current_month = date.month == month
    is_today = date == today.date()

    bg_color = "#ffffff" if is_current_month else "#eeeeee"
    border_color = "#e0e0e0"
    highlight_color = "#FF6B6B" if is_today else "#333333"

    frame = tk.Frame(grid_frame, width=90, height=70, bg=bg_color, highlightbackground=border_color, highlightthickness=1)
    frame.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

    day_label = tk.Label(frame, text=date.day, font=("Arial", 14, "bold"), fg=highlight_color if is_today else "#222222", bg=bg_color)
    day_label.pack(anchor="n", pady=4)

    if is_current_month:
        lunar = get_lunar_str(date)
        lunar_label = tk.Label(frame, text=lunar, font=("Arial", 10), fg="#888888", bg=bg_color)
        lunar_label.pack(anchor="s", pady=2)

    col += 1
    if col == 7:
        col = 0
        row += 1

root.mainloop()