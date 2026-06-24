# main.py - Подчасть 1 из 5
import tkinter as tk
from tkinter import ttk
import logic
import random

button_references = {}
canvas_references = []
initial_buttons_order = []

show_castle_view = True
show_mine_view = False
show_barracks_view = False

def click_money():
    logic.process_money_click()
    update_display()

def click_crystals():
    logic.process_crystal_click()
    update_display()

def buy_upgrade(upg_id):
    if logic.try_buy_upgrade(upg_id):
        update_display()
        repack_buttons()
        draw_graphics_area()

def auto_click_loop():
    logic.process_auto_tick()
    update_display()
    root.after(1000, auto_click_loop)
# main.py - Подчасть 2 из 5
def update_display():
    st = logic.state
    f_money = logic.format_number(st["money"])
    f_crystals = logic.format_number(st["crystals"])
    
    # Отображаем текущий феодальный Титул и казну королевства
    main_balance_label.config(text=f"👑 Титул: {st['title']}  |  💵 Казна: {f_money} $  |  💎 Кристаллы: {f_crystals}")
    
    # Обновление текста характеристик армии в меню Казармы
    army_stats_label.config(
        text=f"⚔️ Сила Королевства:  ⚔️ Урон: {st['army_damage']}  |  🛡️ Защита: {st['army_defense']}\n"
             f"👥 Состав: Сн: {st['soldier_count']} | Рц: {st['knight_count']} | Лч: {st['archer_count']} | Кт: {st['catapult_count']}"
    )
    
    for upg_id, btn in button_references.items():
        upg = logic.upgrades[upg_id]
        
        if upg["type"] == "interior":
            currency_sign = "💎"
            effect_text = "✨ Повышает престиж"
            f_cost = "МАКС." if upg["cost"] > 999999999999 else logic.format_number(upg["cost"])
        elif "tech" in upg["type"]:
            currency_sign = "💎"
            f_cost = "ИЗУЧЕНО" if upg["cost"] > 999999999 else logic.format_number(upg["cost"])
            if upg["type"] == "tech_swords": effect_text = f"⚔️ Урон армии +50%"
            elif upg["type"] == "tech_walls": effect_text = f"🛡️ Защита армии +50%"
            elif upg["type"] == "tech_taxes": effect_text = f"💵 Сбор налогов x2"
        elif upg["type"] == "title_rank":
            currency_sign = "$"
            f_cost = "МАКС." if st["title_stage"] >= 3 else logic.format_number(upg["cost"])
            effect_text = "👑 Продвижение по феодальной лестнице"
        else:
            currency_sign = "$"
            f_cost = logic.format_number(upg["cost"])
            f_power = logic.format_number(upg["power"])
            if upg["type"] in ["soldier", "knight"]:
                effect_text = f"+{f_power}$ к клику | ⚔️+{upg['dmg']} 🛡️+{upg['dfn']}"
            elif upg["type"] == "archer":
                effect_text = f"+{f_power}$ в сек | ⚔️+{upg['dmg']} 🛡️+{upg['dfn']}"
            elif upg["type"] == "catapult_crystal":
                effect_text = f"+{f_power}💎 в сек | ⚔️+{upg['dmg']} 🛡️+{upg['dfn']}"
            
        btn.config(text=f"{upg['name']}\n{effect_text} | Цена: {f_cost} {currency_sign}")
# main.py - Подчасть 3 из 5
def draw_graphics_area():
    graphics_canvas.delete("all")
    
    if show_castle_view:
        bi = logic.state["bought_interiors"]
        stone_colors = ["#78909C", "#708691", "#617680", "#546E7A", "#455A64"]
        block_w, block_h = 38, 20
        for row in range(11):
            y1 = 20 + (row * block_h)
            y2 = y1 + block_h
            shift = (block_w // 2) if row % 2 == 0 else 0
            for col in range(12):
                x1 = 40 + (col * block_w) - shift
                x2 = x1 + block_w
                cx1 = max(40, min(x1, 420))
                cx2 = max(40, min(x2, 420))
                if cx2 - cx1 > 2:
                    graphics_canvas.create_rectangle(cx1, y1, cx2, y2, fill=random.choice(stone_colors), outline="#37474F")
                    for _ in range(random.randint(4, 9)):
                        px = random.randint(cx1 + 1, cx2 - 1)
                        py = random.randint(y1 + 1, y2 - 1)
                        graphics_canvas.create_line(px, py, px + 1, py, fill="#90A4AE" if random.random() > 0.5 else "#263238")
        # Знамена королевства
        graphics_canvas.create_rectangle(50, 30, 80, 110, fill="#4A0E17", outline="#D4AF37", width=2)
        graphics_canvas.create_polygon(50, 110, 65, 130, 80, 110, fill="#4A0E17", outline="#D4AF37", width=2)
        graphics_canvas.create_text(65, 65, text="⚜️", font=("Arial", 12), fill="#D4AF37")
        graphics_canvas.create_rectangle(380, 30, 410, 110, fill="#4A0E17", outline="#D4AF37", width=2)
        graphics_canvas.create_polygon(380, 110, 395, 130, 410, 110, fill="#4A0E17", outline="#D4AF37", width=2)
        graphics_canvas.create_text(395, 65, text="⚜️", font=("Arial", 12), fill="#D4AF37")
        graphics_canvas.create_line(40, 180, 420, 180, fill="#3E2723", width=4)
        graphics_canvas.create_rectangle(40, 20, 420, 220, fill="", outline="#1A237E", width=4)
        
        # Предметы Замка
        if "interior_chair" in bi: graphics_canvas.create_text(75, 160, text="👑🪑", font=("Arial", 22))
        if "interior_carpet" in bi: graphics_canvas.create_rectangle(140, 180, 320, 195, fill="#E1BEE7", outline="#BA68C8")
        if "interior_fireplace" in bi: graphics_canvas.create_text(380, 145, text="🪨🔥", font=("Arial", 20))
        if "interior_chandelier" in bi: graphics_canvas.create_text(230, 45, text="🔱🔥", font=("Arial", 16))

    elif show_mine_view:
        mine_colors = ["#37474F", "#263238", "#212121", "#424242"]
        graphics_canvas.create_rectangle(40, 20, 420, 220, fill="#1A0F0A")
        for _ in range(1200):
            rx = random.randint(40, 420)
            ry = random.randint(20, 220)
            graphics_canvas.create_line(rx, ry, rx + random.randint(2, 6), ry + random.randint(1, 3), fill=random.choice(mine_colors))
        graphics_canvas.create_polygon(170, 220, 170, 100, 230, 70, 290, 100, 290, 220, fill="#000000", outline="#5D4037", width=4)
        graphics_canvas.create_line(170, 220, 170, 100, fill="#8D6E63", width=6)
        graphics_canvas.create_line(290, 220, 290, 100, fill="#8D6E63", width=6)
        graphics_canvas.create_line(167, 100, 293, 100, fill="#8D6E63", width=8)
        # Вывеска
        graphics_canvas.create_rectangle(180, 45, 280, 75, fill="#D7CCC8", outline="#5D4037", width=2)
        graphics_canvas.create_text(230, 60, text="⛏️ ШАХТА", font=("Arial", 11, "bold"), fill="#3E2723")
        graphics_canvas.create_rectangle(40, 20, 420, 220, fill="", outline="#A73A00", width=4)
# main.py - Подчасть 4 из 5
def toggle_castle_tab():
    global show_castle_view, show_mine_view, show_barracks_view
    show_castle_view = not show_castle_view
    if show_castle_view:
        show_mine_view = show_barracks_view = False
        main_notebook.pack_forget()
    draw_graphics_area()

def toggle_mine_tab():
    global show_mine_view, show_castle_view, show_barracks_view
    show_mine_view = not show_mine_view
    if show_mine_view:
        show_castle_view = show_barracks_view = False
        main_notebook.pack_forget()
    draw_graphics_area()

def toggle_barracks_tab():
    global show_barracks_view, show_castle_view, show_mine_view
    show_barracks_view = not show_barracks_view
    if show_barracks_view:
        show_castle_view = show_mine_view = False
        main_notebook.pack(fill="x", expand=False, padx=10, pady=5)
        repack_buttons()
    else:
        main_notebook.pack_forget()
    draw_graphics_area()

def repack_buttons():
    for btn in button_references.values():
        btn.pack_forget()
    for upg_id in initial_buttons_order:
        button_references[upg_id].pack(pady=4, fill="x", padx=10)

def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent, bg="#F4ECD8", highlightthickness=0)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#F4ECD8")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas_references.append(canvas)
    return scrollable_frame

def on_closing():
    logic.save_game()
    root.destroy()
# main.py - Подчасть 5 из 5 (Финальная сборка и запуск)

# Изолированная фабрика для безопасной привязки скролла мыши к кнопкам
def bind_mousewheel_safely(target_button, target_canvas):
    target_button.bind(
        "<MouseWheel>", 
        lambda event: target_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    )

# --- Инициализация главного графического окна Tkinter ---
root = tk.Tk()
root.title("Python Эпический Средневековый Кликер 3.0")
root.geometry("480x820")
root.configure(bg="#2D1A12") # Цвет темного дуба

# Связываем системный крестик закрытия окна с автосохранением прогресса
root.protocol("WM_DELETE_WINDOW", on_closing)

# Верхняя золотая панель Казны Королевства
main_balance_label = tk.Label(root, text="", font=("Arial", 11, "bold"), bg="#D4AF37", fg="#2D1A12", pady=10, relief="groove")
main_balance_label.pack(fill="x", padx=10, pady=10)

# Главный интерактивный холст для Замка и Шахты
graphics_canvas = tk.Canvas(root, bg="#2D1A12", height=240, highlightthickness=0)
graphics_canvas.pack(fill="x", padx=10)

# Панель навигации (Кнопки-переключатели экранов)
actions_frame = tk.Frame(root, bg="#2D1A12")
actions_frame.pack(fill="x", padx=10, pady=5)

tk.Button(actions_frame, text="🏰 ЗАМОК", font=("Arial", 9, "bold"), bg="#4A0E17", fg="white", width=14, command=toggle_castle_tab).grid(row=0, column=0, padx=4)
tk.Button(actions_frame, text="⛏️ ШАХТА", font=("Arial", 9, "bold"), bg="#1A365D", fg="white", width=14, command=toggle_mine_tab).grid(row=0, column=1, padx=4)
tk.Button(actions_frame, text="⚔️ КАЗАРМА", font=("Arial", 9, "bold"), bg="#3E2723", fg="white", width=14, command=toggle_barracks_tab).grid(row=0, column=2, padx=4)

# Панель ручного сбора ресурсов (Налоги и Кристаллы)
clicks_frame = tk.Frame(root, bg="#2D1A12")
clicks_frame.pack(fill="x", padx=10, pady=2)
tk.Button(clicks_frame, text="💰 Собрать налоги ($)", font=("Arial", 10, "bold"), bg="#5D4037", fg="white", width=22, command=click_money).grid(row=0, column=0, padx=5)
tk.Button(clicks_frame, text="💎 Добыть Кристалл", font=("Arial", 10, "bold"), bg="#008CBA", fg="white", width=22, command=click_crystals).grid(row=0, column=1, padx=5)

# Кнопка продвижения по феодальной лестнице (Повышение Титула)
tk.Button(root, text="👑 ПОВЫСИТЬ ТИТУЛ", font=("Arial", 10, "bold"), bg="#D4AF37", fg="#2D1A12", command=lambda: buy_upgrade("title_rank")).pack(fill="x", padx=15, pady=4)

# Создание и стилизация системы вкладок под пергамент
main_notebook = ttk.Notebook(root)
style = ttk.Style()
style.configure("TNotebook", background="#2D1A12")
style.configure("TNotebook.Tab", background="#DBCEB4", font=("Arial", 8, "bold"))

tab_soldier = tk.Frame(main_notebook, bg="#F4ECD8")
tab_knight = tk.Frame(main_notebook, bg="#F4ECD8")
tab_archer = tk.Frame(main_notebook, bg="#F4ECD8")
tab_catapult = tk.Frame(main_notebook, bg="#F4ECD8")
tab_alchemy = tk.Frame(main_notebook, bg="#F4ECD8")
tab_inventory = tk.Frame(main_notebook, bg="#F4ECD8")

main_notebook.add(tab_soldier, text="🗡️ Солдаты ")
main_notebook.add(tab_knight, text="🐴 Рыцари ")
main_notebook.add(tab_archer, text="🏹 Лучники ")
main_notebook.add(tab_catapult, text="☄️ Катапульты ")
main_notebook.add(tab_alchemy, text="🧪 Алхимия ")
main_notebook.add(tab_inventory, text="🏰 Замок ")

# Информационный свиток военных характеристик Армии
army_stats_label = tk.Label(root, text="", font=("Arial", 9, "bold"), bg="#DBCEB4", fg="#2D1A12", height=2, relief="sunken")
army_stats_label.pack(fill="x", padx=15, pady=5)

# Картография фреймов магазинов
containers = {}
frames_map = {
    "soldier_tab": tab_soldier, "knight_tab": tab_knight,
    "archer_tab": tab_archer, "catapult_tab": tab_catapult, 
    "alchemy_tech": tab_alchemy, "inventory": tab_inventory
}

# ЖЕСТКАЯ ОПТИМИЗАЦИЯ ГЕОМЕТРИИ (Фиксируем высоту height=180 под 5 кнопок)
for name, f_obj in frames_map.items():
    c_box = tk.Frame(f_obj, bg="#F4ECD8", height=180)
    c_box.pack_propagate(False)
    c_box.pack(fill="x", padx=10, pady=5)
    containers[name] = create_scrollable_frame(c_box)

# Замеряем изначальную стоимость для статичной сортировки при старте
initial_buttons_order = sorted(logic.upgrades.keys(), key=lambda uid: logic.upgrades[uid]["cost"])

# Сборка кнопок и безопасное распределение по прокручиваемым слоям
for upg_id in initial_buttons_order:
    upg = logic.upgrades[upg_id]
    target_frame = containers[upg["tab"]]
    
    # Стилизация цветов кнопок под средневековый тип
    if upg["tab"] == "inventory": bg, fg = "#D2B48C", "#4A2E00" # Дерево/Кожа
    elif "tech" in upg["type"]: bg, fg = "#4A148C", "#FFFFFF" # Магическая алхимия
    elif "click" in upg["type"] or upg["type"] == "soldier": bg, fg = "#8C7B6E", "#FFFFFF" # Пехота
    else: bg, fg = "#708090", "#FFFFFF" # Осада/Сталь
        
    btn = tk.Button(target_frame, font=("Arial", 9, "bold"), bg=bg, fg=fg, height=2, width=45, command=lambda uid=upg_id: buy_upgrade(uid))
    
    # Находим точный родительский холст (Canvas) для данной кнопки
    associated_canvas = target_frame.master
    
    # Безопасно изолируем событие прокрутки мыши в фабрике, предотвращая вылеты
    bind_mousewheel_safely(btn, associated_canvas)
    
    button_references[upg_id] = btn

# Скрываем блок магазинов до клика по кнопке "КАЗАРМА"
main_notebook.pack_forget()

# Запуск стартовой отрисовки и фонового таймера доходов
update_display()
repack_buttons()
draw_graphics_area()
root.after(1000, auto_click_loop)
root.mainloop()

# --- КОНЕЦ КОДА ИГРЫ ---
