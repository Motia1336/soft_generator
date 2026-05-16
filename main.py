"""
main.py - Mobile Device Profile Manager
Portable, self-contained GUI application.
"""

import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import os
import glob
import sys

import database as db
import generator as gen

# ─── Theme ────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT     = "#3B8BEB"
ACCENT2    = "#7C3AED"
BG_DARK    = "#0F1117"
BG_CARD    = "#1A1D27"
BG_CARD2   = "#21253A"
TEXT_MAIN  = "#EAEAEA"
TEXT_MUTED = "#7A8299"
SUCCESS    = "#22C55E"
WARNING    = "#F59E0B"
DANGER     = "#EF4444"

FONT_TITLE  = ("Inter", 22, "bold")
FONT_HEAD   = ("Inter", 14, "bold")
FONT_BODY   = ("Inter", 12)
FONT_SMALL  = ("Inter", 10)
FONT_MONO   = ("Consolas", 10)

PAGE_SIZE = 50   # rows per page


APP_VERSION = "1.2.1"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        db.init_db()

        self.title(f"Менеджер Профилей SunBrowser v{APP_VERSION}")
        self.geometry("1300x820")
        self.minsize(1024, 700)
        self.configure(fg_color=BG_DARK)

        self._current_page = 0
        self._current_platform = "all"
        self._search_term = ""
        self._selected_ids: list[str] = []

        self._build_layout()
        self._load_table()
        self._update_stats()

    def _build_layout(self):
        self._sidebar = ctk.CTkFrame(self, width=240, fg_color=BG_CARD, corner_radius=0)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)
        self._build_sidebar()

        self._content = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=0)
        self._content.pack(side="left", fill="both", expand=True)

        self._tabs = ctk.CTkTabview(
            self._content,
            fg_color=BG_CARD,
            segmented_button_fg_color=BG_CARD2,
            segmented_button_selected_color=ACCENT,
            text_color=TEXT_MAIN,
        )
        self._tabs.pack(fill="both", expand=True, padx=12, pady=12)

        self._tabs.add("📋 Профили")
        self._tabs.add("⚡ Генерация БД")
        self._tabs.add("📤 Экспорт всё")
        self._tabs.add("📊 Статистика")

        self._build_profiles_tab(self._tabs.tab("📋 Профили"))
        self._build_generate_tab(self._tabs.tab("⚡ Генерация БД"))
        self._build_export_tab(self._tabs.tab("📤 Экспорт всё"))
        self._build_stats_tab(self._tabs.tab("📊 Статистика"))

    def _build_sidebar(self):
        logo_frame = ctk.CTkFrame(self._sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=16, pady=(24, 8))
        ctk.CTkLabel(logo_frame, text="📱", font=("Inter", 36)).pack()
        ctk.CTkLabel(logo_frame, text="Profile Manager", font=FONT_HEAD, text_color=TEXT_MAIN).pack()

        ctk.CTkFrame(self._sidebar, height=1, fg_color=BG_CARD2).pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(self._sidebar, text="ФИЛЬТР", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=20)

        self._platform_var = ctk.StringVar(value="all")
        for label, val in [("🌐 Все", "all"), ("🤖 Android", "Android"), ("🍎 iOS", "iOS")]:
            btn = ctk.CTkRadioButton(
                self._sidebar, text=label, variable=self._platform_var, value=val,
                command=self._on_filter_change, font=FONT_BODY, text_color=TEXT_MAIN,
                fg_color=ACCENT, hover_color="#2563EB",
            )
            btn.pack(anchor="w", padx=20, pady=4)

        ctk.CTkFrame(self._sidebar, height=1, fg_color=BG_CARD2).pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(self._sidebar, text="БАЗА", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=20)
        self._lbl_total   = ctk.CTkLabel(self._sidebar, text="Всего: 0", font=FONT_BODY, text_color=TEXT_MAIN)
        self._lbl_android = ctk.CTkLabel(self._sidebar, text="Android: 0", font=FONT_BODY, text_color="#4ADE80")
        self._lbl_ios     = ctk.CTkLabel(self._sidebar, text="iOS: 0", font=FONT_BODY, text_color="#60A5FA")
        for lbl in (self._lbl_total, self._lbl_android, self._lbl_ios):
            lbl.pack(anchor="w", padx=20, pady=2)

        ctk.CTkFrame(self._sidebar, height=1, fg_color=BG_CARD2).pack(fill="x", padx=16, pady=12)
        ctk.CTkLabel(self._sidebar, text="ОПАСНАЯ ЗОНА", font=FONT_SMALL, text_color=DANGER).pack(anchor="w", padx=20)
        ctk.CTkButton(
            self._sidebar, text="🗑 Удалить выделенные", font=FONT_BODY,
            fg_color="#7F1D1D", hover_color=DANGER, text_color=TEXT_MAIN, command=self._delete_selected,
        ).pack(fill="x", padx=16, pady=4)
        ctk.CTkButton(
            self._sidebar, text="💣 ОЧИСТИТЬ БАЗУ", font=FONT_BODY,
            fg_color="#450A0A", hover_color="#991B1B", text_color=TEXT_MUTED, command=self._wipe_all,
        ).pack(fill="x", padx=16, pady=4)

    def _build_profiles_tab(self, parent):
        toolbar = ctk.CTkFrame(parent, fg_color="transparent")
        toolbar.pack(fill="x", padx=8, pady=(8, 4))
        self._search_var = ctk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search())
        search = ctk.CTkEntry(
            toolbar, textvariable=self._search_var, placeholder_text="🔍 Поиск по модели, User-Agent...",
            font=FONT_BODY, width=320, height=36, fg_color=BG_CARD2, border_color=ACCENT,
        )
        search.pack(side="left", padx=(0, 8))
        self._lbl_count = ctk.CTkLabel(toolbar, text="", font=FONT_SMALL, text_color=TEXT_MUTED)
        self._lbl_count.pack(side="left", padx=8)

        pg_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        pg_frame.pack(side="right")
        ctk.CTkButton(pg_frame, text="◀", width=36, height=32, command=self._prev_page, fg_color=BG_CARD2).pack(side="left", padx=2)
        self._lbl_page = ctk.CTkLabel(pg_frame, text="Стр 1", font=FONT_SMALL, width=80)
        self._lbl_page.pack(side="left")
        ctk.CTkButton(pg_frame, text="▶", width=36, height=32, command=self._next_page, fg_color=BG_CARD2).pack(side="left", padx=2)

        table_container = ctk.CTkFrame(parent, fg_color=BG_CARD2, corner_radius=12)
        table_container.pack(fill="both", expand=True, padx=8, pady=4)

        cols = ("Платформа", "Модель", "Система", "ОЗУ", "ЦП", "Экран", "User-Agent", "Имя устройства")
        col_widths = (80, 160, 100, 50, 50, 90, 420, 150)

        import tkinter.ttk as ttk
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview", background=BG_CARD2, foreground=TEXT_MAIN, rowheight=28, fieldbackground=BG_CARD2, borderwidth=0)
        style.configure("Custom.Treeview.Heading", background=BG_DARK, foreground=TEXT_MUTED, font=("Inter", 10, "bold"))
        style.map("Custom.Treeview", background=[("selected", ACCENT)])

        scroll_y = tk.Scrollbar(table_container, orient="vertical")
        scroll_x = tk.Scrollbar(table_container, orient="horizontal")
        self._tree = ttk.Treeview(table_container, columns=cols, show="headings", style="Custom.Treeview",
                                  yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, selectmode="extended")
        scroll_y.config(command=self._tree.yview)
        scroll_x.config(command=self._tree.xview)

        for col, w in zip(cols, col_widths):
            self._tree.heading(col, text=col, anchor="w")
            self._tree.column(col, width=w, minwidth=w, anchor="w")

        scroll_x.pack(side="bottom", fill="x")
        scroll_y.pack(side="right", fill="y")
        self._tree.pack(fill="both", expand=True)

        self._tree.bind("<<TreeviewSelect>>", self._on_row_select)
        self._tree.tag_configure("even", background="#1A1D27")
        self._tree.tag_configure("odd",  background="#21253A")

    def _build_generate_tab(self, parent):
        # Using ScrollableFrame to ensure all settings are visible on smaller resolutions
        left = ctk.CTkScrollableFrame(parent, fg_color=BG_CARD2, corner_radius=12, label_text="Настройки генерации", label_font=FONT_HEAD, label_text_color=ACCENT)
        left.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(left, text="⚡ Генерация базы устройств", font=FONT_TITLE, text_color=TEXT_MAIN).pack(pady=(30, 10))
        ctk.CTkLabel(left, text="Вы можете сгенерировать до 10,000 профилей в мастер-базу.", font=FONT_BODY, text_color=TEXT_MUTED).pack()

        ctk.CTkLabel(left, text="Платформа", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=40, pady=(20,2))
        self._gen_platform = ctk.CTkSegmentedButton(left, values=["Mix (Случайно)", "Андроид", "Айос"], font=FONT_BODY)
        self._gen_platform.set("Mix (Случайно)")
        self._gen_platform.pack(fill="x", padx=40, pady=(0, 15))

        ctk.CTkLabel(left, text="Регион (опционально)", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=40, pady=(6,2))
        self._region_group = ctk.CTkSegmentedButton(left, values=["Любой", "СНГ", "Европа"], font=FONT_BODY)
        self._region_group.set("Любой")
        self._region_group.pack(fill="x", padx=40, pady=(0, 8))

        ctk.CTkLabel(left, text="Выбрать страну (опционально) — перекрывает группу", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=40, pady=(6,2))
        countries = sorted(gen.ALL_GEO)
        try:
            self._country_combo = ctk.CTkComboBox(left, values=countries)
        except Exception:
            self._country_combo = ctk.CTkOptionMenu(left, values=countries)
        self._country_combo.set("")
        self._country_combo.pack(fill="x", padx=40, pady=(0, 12))

        # Language selection checkboxes
        langs_frame = ctk.CTkFrame(left, fg_color="transparent")
        langs_frame.pack(fill="x", padx=40, pady=(6, 6))
        self._lang_en_var = ctk.BooleanVar(value=True)
        self._lang_ru_var = ctk.BooleanVar(value=True)
        self._lang_country_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(langs_frame, text="Английский (en-GB)", variable=self._lang_en_var, onvalue=True, offvalue=False).pack(anchor="w")
        ctk.CTkCheckBox(langs_frame, text="Русский (ru)", variable=self._lang_ru_var, onvalue=True, offvalue=False).pack(anchor="w")
        ctk.CTkCheckBox(langs_frame, text="Язык страны (если выбран)", variable=self._lang_country_var, onvalue=True, offvalue=False).pack(anchor="w")
        ctk.CTkLabel(langs_frame, text="Подсказка: если выбран русский — system=ru ~60%, country ~35%, en-GB ~5% (учитываются только отмеченные языки).", font=FONT_SMALL, text_color=TEXT_MUTED, wraplength=520).pack(anchor="w", pady=(6,0))

        # --- User-Agent Mode Selection ---
        ctk.CTkLabel(left, text="Режим User-Agent (Android)", font=FONT_SMALL, text_color=TEXT_MUTED).pack(anchor="w", padx=40, pady=(15, 2))
        self._ua_mode_var = ctk.StringVar(value="frozen")
        ua_frame = ctk.CTkFrame(left, fg_color="transparent")
        ua_frame.pack(fill="x", padx=40)
        
        for text, val in [("Замороженный", "frozen"), ("Реальный", "real"), ("Микс", "mix")]:
            ctk.CTkRadioButton(ua_frame, text=text, variable=self._ua_mode_var, value=val, font=FONT_BODY).pack(side="left", padx=(0, 20))
            
        # Mix Percentage Slider
        self._ua_mix_frame = ctk.CTkFrame(left, fg_color="transparent")
        self._ua_mix_frame.pack(fill="x", padx=40, pady=(5, 0))
        ctk.CTkLabel(self._ua_mix_frame, text="Процент реальных UA:", font=FONT_SMALL, text_color=TEXT_MUTED).pack(side="left")
        self._ua_mix_slider = ctk.CTkSlider(self._ua_mix_frame, from_=0, to=100, number_of_steps=100, width=200)
        self._ua_mix_slider.set(50)
        self._ua_mix_slider.pack(side="left", padx=10)
        self._ua_mix_lbl = ctk.CTkLabel(self._ua_mix_frame, text="50%", font=FONT_SMALL)
        self._ua_mix_lbl.pack(side="left")
        self._ua_mix_slider.configure(command=lambda v: self._ua_mix_lbl.configure(text=f"{int(v)}%"))

        self._gen_count = ctk.CTkEntry(left, placeholder_text="Сколько сгенерировать? (напр. 1000)", font=FONT_BODY)
        self._gen_count.pack(fill="x", padx=40, pady=10)

        self._gen_btn = ctk.CTkButton(left, text="🚀 Запустить генерацию", font=FONT_HEAD, height=48, command=self._do_generate)
        self._gen_btn.pack(fill="x", padx=40, pady=20)

        self._gen_status = ctk.CTkLabel(left, text="", font=FONT_BODY)
        self._gen_status.pack()

    def _build_export_tab(self, parent):
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=40, pady=40)

        ctk.CTkLabel(wrap, text="📤 Пакованный экспорт для работы", font=FONT_TITLE, text_color=TEXT_MAIN).pack(anchor="w")
        ctk.CTkLabel(wrap, text="Берет ВСЕ профили из базы данных и сохраняет их в текстовый документ.\nПри каждом нажатии номер файла увеличивается: devise_1.txt, devise_2.txt и т.д.\nПосле экспорта профили удаляются из базы.", font=FONT_BODY, text_color=TEXT_MUTED, justify="left").pack(anchor="w", pady=(5, 30))

        btn = ctk.CTkButton(wrap, text="📥 Экспортировать все устройства", font=FONT_HEAD, height=60, width=400, fg_color=SUCCESS, hover_color="#16A34A", command=self._do_export_all)
        btn.pack(anchor="w", pady=10)

        self._exp_status = ctk.CTkLabel(wrap, text="", font=("Inter", 14), text_color=TEXT_MAIN)
        self._exp_status.pack(anchor="w", pady=10)

    def _build_stats_tab(self, parent):
        self._stats_frame = ctk.CTkFrame(parent, fg_color="transparent")
        self._stats_frame.pack(fill="both", expand=True, padx=20, pady=20)
        # Refreshed when switched manually or periodically over load
        self._refresh_stats_view()

    def _refresh_stats_view(self):
        for w in self._stats_frame.winfo_children(): w.destroy()
        stats = db.get_stats()
        cum_stats = db.get_cumulative_stats()

        ctk.CTkLabel(self._stats_frame, text="📊 Текущая база", font=FONT_TITLE).pack(anchor="w", pady=(10, 5))
        
        row1 = ctk.CTkFrame(self._stats_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        for name, val, c in [("Всего в базе", stats['total'], TEXT_MAIN), ("Android", stats['android'], "#4ADE80"), ("iOS", stats['ios'], "#60A5FA")]:
            f = ctk.CTkFrame(row1, fg_color=BG_CARD2, corner_radius=10)
            f.pack(side="left", fill="both", expand=True, padx=5)
            ctk.CTkLabel(f, text=name, text_color=TEXT_MUTED).pack(pady=(10,0))
            ctk.CTkLabel(f, text=str(val), font=("Inter", 24, "bold"), text_color=c).pack(pady=(0,10))

        ctk.CTkLabel(self._stats_frame, text="📈 Общая статистика за все время", font=FONT_TITLE).pack(anchor="w", pady=(20, 5))
        
        row2 = ctk.CTkFrame(self._stats_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        for name, val, c in [
            ("Сгенерировано", cum_stats.get('total_generated', 0), TEXT_MAIN), 
            ("Экспортировано", cum_stats.get('total_exported', 0), SUCCESS), 
            ("Ген. Android", cum_stats.get('android_generated', 0), "#4ADE80"), 
            ("Ген. iOS", cum_stats.get('ios_generated', 0), "#60A5FA")
        ]:
            f = ctk.CTkFrame(row2, fg_color=BG_CARD2, corner_radius=10)
            f.pack(side="left", fill="both", expand=True, padx=5)
            ctk.CTkLabel(f, text=name, text_color=TEXT_MUTED).pack(pady=(10,0))
            ctk.CTkLabel(f, text=str(val), font=("Inter", 20, "bold"), text_color=c).pack(pady=(0,10))

    def _load_table(self):
        for item in self._tree.get_children(): self._tree.delete(item)
        self._selected_ids.clear()
        total = db.count_profiles(self._current_platform, self._search_term)
        start = self._current_page * PAGE_SIZE
        profiles = db.get_profiles(self._current_platform, self._search_term, PAGE_SIZE, start)
        pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        self._lbl_page.configure(text=f"Стр {self._current_page + 1} / {pages}")
        self._lbl_count.configure(text=f"{total:,} найдено")

        for i, p in enumerate(profiles):
            tag = "even" if i % 2 == 0 else "odd"
            self._tree.insert("", "end", iid=p.get("id"), tags=(tag,), values=(
                p.get("platform", ""), p.get("model", ""), p.get("os_display", ""), p.get("ram", ""), p.get("cpu", ""),
                p.get("screen", ""), p.get("user_agent", ""), p.get("device_name", "")
            ))

    def _update_stats(self):
        stats = db.get_stats()
        self._lbl_total.configure(text=f"Всего: {stats['total']:,}")
        self._lbl_android.configure(text=f"Android: {stats['android']:,}")
        self._lbl_ios.configure(text=f"iOS: {stats['ios']:,}")
        if hasattr(self, '_stats_frame'): 
            self._refresh_stats_view()

    def _on_filter_change(self):
        self._current_platform = self._platform_var.get()
        self._current_page = 0
        self._load_table()

    def _on_search(self):
        self._search_term = self._search_var.get()
        self._current_page = 0
        self._load_table()

    def _prev_page(self):
        if self._current_page > 0: self._current_page -= 1; self._load_table()

    def _next_page(self):
        if (self._current_page + 1) * PAGE_SIZE < db.count_profiles(self._current_platform, self._search_term):
            self._current_page += 1; self._load_table()

    def _on_row_select(self, _event):
        self._selected_ids = list(self._tree.selection())

    def _delete_selected(self):
        if not self._selected_ids: return messagebox.showinfo("Пусто", "Выберите профили в таблице")
        if messagebox.askyesno("Подтверждение", f"Удалить {len(self._selected_ids)} профилей?"):
            db.delete_profiles(self._selected_ids)
            self._load_table()
            self._update_stats()

    def _wipe_all(self):
        if messagebox.askyesno("ОЧИСТКА", "Удалить ВСЕ профили? Это нельзя отменить."):
            db.delete_all()
            self._load_table()
            self._update_stats()

    def _do_generate(self):
        try: cnt = int(self._gen_count.get())
        except ValueError: return messagebox.showerror("Ошибка", "Введите нормальное число")
        
        plat_map = {"Mix (Случайно)": "random", "Андроид": "Android", "Айос": "iOS"}
        plat = plat_map[self._gen_platform.get()]

        self._gen_btn.configure(state="disabled")
        self._gen_status.configure(text=f"Идет генерация {cnt} профилей. Подождите...", text_color=WARNING)

        def work():
            # Build region filter
            sel_country = ""
            try:
                sel_country = self._country_combo.get()
            except Exception:
                sel_country = ""
            region = None
            if sel_country:
                region = sel_country
            else:
                grp = self._region_group.get()
                if grp == "СНГ":
                    region = gen.CIS_COUNTRIES
                elif grp == "Европа":
                    region = gen.EUROPE_COUNTRIES

            # build languages_allowed list from checkboxes
            langs_allowed = []
            if self._lang_en_var.get():
                langs_allowed.append("en-GB")
            if self._lang_ru_var.get():
                langs_allowed.append("ru")
            if self._lang_country_var.get() and sel_country:
                # include country primary language code if available
                cl, _ = gen.COUNTRY_LANG.get(sel_country, (None, None))
                if cl:
                    langs_allowed.append(cl)

            # UA Settings
            ua_mode = self._ua_mode_var.get()
            ua_percent = int(self._ua_mix_slider.get())

            profiles = gen.generate_batch(cnt, plat, region=region, languages_allowed=(langs_allowed or None), ua_mode=ua_mode, ua_mix_percent=ua_percent)
            db.insert_profiles(profiles)
            db.record_generation(profiles)
            self.after(0, lambda: self._on_gen_done(len(profiles)))

        threading.Thread(target=work, daemon=True).start()

    def _on_gen_done(self, cnt):
        self._gen_btn.configure(state="normal")
        self._gen_status.configure(text=f"✅ Успешно добавлено {cnt} профилей в базу!", text_color=SUCCESS)
        self._gen_count.delete(0, 'end')
        self._load_table()
        self._update_stats()

    def _get_next_devise_filename(self) -> str:
        # Check current devise_X.txt files in current directory to figure out next X
        files = glob.glob("devise_*.txt")
        max_num = 0
        for f in files:
            name = os.path.basename(f)
            num_part = name.replace("devise_", "").replace(".txt", "")
            if num_part.isdigit():
                max_num = max(max_num, int(num_part))
        return f"devise_{max_num + 1}.txt"

    def _do_export_all(self):
        stats = db.get_stats()
        total = stats['total']
        if total == 0:
            messagebox.showwarning("База пустая", "В базе нет профилей! Сначала сгенерируйте их.")
            return

        # Export ALL profiles in the database filtered by current platform selection
        platform = self._platform_var.get()
        profiles = db.get_all_profiles(platform)

        if not profiles:
            messagebox.showwarning("Нет данных", "Нет профилей для экспорта с текущим фильтром.")
            return

        filename = self._get_next_devise_filename()

        with open(filename, "w", encoding="utf-8") as f:
            for i, p in enumerate(profiles):
                f.write(f"УСТРОЙСТВО {i+1}\n")
                f.write(gen.format_profile_text(p))
                f.write("\n\n")

        db.delete_profiles([p["id"] for p in profiles])
        db.record_export(profiles)
        self._load_table()
        self._update_stats()

        self._exp_status.configure(
            text=f"✅ Экспортировано {len(profiles)} устройств → {filename} (удалены из базы)"
        )




if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = App()
    app.mainloop()
