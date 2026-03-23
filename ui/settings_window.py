import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from core.config_manager import load_config, save_config

def get_text(key):
    """根据当前语言配置获取文本"""
    config = load_config()
    lang = config.get("ui", {}).get("language", "zh_CN")
    if lang == "en_US":
        from config.texts import en_us as texts
    else:
        from config.texts import zh_cn as texts
    return getattr(texts, key, key)


class SettingsWindow(tk.Toplevel):
    def __init__(self, master, on_saved_callback=None):
        super().__init__(master)
        self.master = master
        self.on_saved_callback = on_saved_callback

        self.title(get_text("BTN_SETTINGS"))
        self.geometry("820x560")
        self.minsize(760, 520)
        self.configure(bg="#16181d")
        self.transient(master)
        self.grab_set()

        self.config_data = load_config()

        self.bg_main = "#16181d"
        self.bg_left = "#1b1f26"
        self.bg_right = "#20242c"
        self.bg_card = "#252a33"
        self.text_main = "#f5f7fa"
        self.text_sub = "#aeb6c2"
        self.border = "#2d3440"
        self.btn_bg = "#2a303a"
        self.btn_hover = "#343b47"

        self.current_page = None
        self.pages = {}

        self._build_ui()
        self.show_page("paths")

    def _build_ui(self):
        container = tk.Frame(self, bg=self.bg_main)
        container.pack(fill="both", expand=True, padx=14, pady=14)

        left_nav = tk.Frame(container, bg=self.bg_left, width=180, highlightthickness=1, highlightbackground=self.border)
        left_nav.pack(side="left", fill="y", padx=(0, 8))
        left_nav.pack_propagate(False)

        tk.Label(left_nav, text=get_text("BTN_SETTINGS"), bg=self.bg_left, fg=self.text_main, font=("Microsoft YaHei", 14, "bold")).pack(anchor="w", padx=14, pady=(16, 10))

        self.nav_buttons = {}
        self.nav_buttons["paths"] = self._create_nav_button(left_nav, get_text("NAV_PATHS"), lambda: self.show_page("paths"))
        self.nav_buttons["behavior"] = self._create_nav_button(left_nav, get_text("NAV_BEHAVIOR"), lambda: self.show_page("behavior"))
        self.nav_buttons["inference"] = self._create_nav_button(left_nav, get_text("NAV_INFERENCE"), lambda: self.show_page("inference"))
        self.nav_buttons["training"] = self._create_nav_button(left_nav, get_text("NAV_TRAINING"), lambda: self.show_page("training"))
        self.nav_buttons["appearance"] = self._create_nav_button(left_nav, get_text("NAV_APPEARANCE"), lambda: self.show_page("appearance"))
        self.nav_buttons["language"] = self._create_nav_button(left_nav, get_text("NAV_LANGUAGE"), lambda: self.show_page("language"))

        self.nav_buttons["paths"].pack(fill="x", padx=10, pady=4)
        self.nav_buttons["behavior"].pack(fill="x", padx=10, pady=4)
        self.nav_buttons["inference"].pack(fill="x", padx=10, pady=4)
        self.nav_buttons["training"].pack(fill="x", padx=10, pady=4)
        self.nav_buttons["appearance"].pack(fill="x", padx=10, pady=4)
        self.nav_buttons["language"].pack(fill="x", padx=10, pady=4)

        right_area = tk.Frame(container, bg=self.bg_right, highlightthickness=1, highlightbackground=self.border)
        right_area.pack(side="right", fill="both", expand=True)

        self.content_frame = tk.Frame(right_area, bg=self.bg_right)
        self.content_frame.pack(fill="both", expand=True, padx=16, pady=16)

        bottom_bar = tk.Frame(right_area, bg=self.bg_right)
        bottom_bar.pack(fill="x", padx=16, pady=(0, 16))

        tk.Button(bottom_bar, text=get_text("BTN_CANCEL"), bg=self.btn_bg, fg=self.text_main, relief="flat", activebackground=self.btn_hover, activeforeground=self.text_main, command=self.destroy).pack(side="right", padx=(8, 0))
        tk.Button(bottom_bar, text=get_text("BTN_SAVE_SETTINGS"), bg="#3a6df0", fg="white", relief="flat", activebackground="#4b7cff", activeforeground="white", command=self.save_settings).pack(side="right")

        self._build_pages()

    def _create_nav_button(self, parent, text, command):
        btn = tk.Label(parent, text=text, bg=self.btn_bg, fg=self.text_main, anchor="w", padx=12, pady=10, cursor="hand2", font=("Microsoft YaHei", 10))
        btn.bind("<Enter>", lambda e: btn.config(bg=self.btn_hover))
        btn.bind("<Leave>", lambda e: self._reset_nav_button(btn))
        btn.bind("<Button-1>", lambda e: command())
        return btn

    def _reset_nav_button(self, btn):
        if getattr(btn, "is_active", False):
            btn.config(bg="#40516d")
        else:
            btn.config(bg=self.btn_bg)

    def show_page(self, page_name):
        if self.current_page:
            self.pages[self.current_page].pack_forget()

        self.current_page = page_name
        self.pages[page_name].pack(fill="both", expand=True)

        for name, btn in self.nav_buttons.items():
            btn.is_active = (name == page_name)
            self._reset_nav_button(btn)

    def _build_pages(self):
        self.pages["paths"] = self._build_paths_page()
        self.pages["behavior"] = self._build_behavior_page()
        self.pages["inference"] = self._build_inference_page()
        self.pages["training"] = self._build_training_page()
        self.pages["appearance"] = self._build_appearance_page()
        self.pages["language"] = self._build_language_page()
        self.pages["language"] = self._build_language_page()

    def _page_title(self, parent, title, subtitle):
        tk.Label(parent, text=title, bg=self.bg_right, fg=self.text_main, font=("Microsoft YaHei", 13, "bold")).pack(anchor="w")
        tk.Label(parent, text=subtitle, bg=self.bg_right, fg=self.text_sub, font=("Microsoft YaHei", 9)).pack(anchor="w", pady=(4, 14))

    def _build_paths_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_right)
        self._page_title(page, get_text("TITLE_PATHS"), get_text("SUBTITLE_PATHS"))

        self.path_vars = {
            "image_dir": tk.StringVar(value=self.config_data["paths"].get("image_dir", "")),
            "label_dir": tk.StringVar(value=self.config_data["paths"].get("label_dir", "")),
            "model_path": tk.StringVar(value=self.config_data["paths"].get("model_path", "")),
            "output_dataset_dir": tk.StringVar(value=self.config_data["paths"].get("output_dataset_dir", "")),
            "bad_cases_dir": tk.StringVar(value=self.config_data["paths"].get("bad_cases_dir", "")),
        }

        self._add_path_row(page, get_text("LABEL_IMAGE_DIR"), self.path_vars["image_dir"], False)
        self._add_path_row(page, get_text("LABEL_LABEL_DIR"), self.path_vars["label_dir"], False)
        self._add_path_row(page, get_text("LABEL_MODEL_PATH"), self.path_vars["model_path"], True)
        self._add_path_row(page, get_text("LABEL_OUTPUT_DIR"), self.path_vars["output_dataset_dir"], False)
        self._add_path_row(page, get_text("LABEL_BAD_CASE_DIR"), self.path_vars["bad_cases_dir"], False)
        return page

    def _add_path_row(self, parent, title, var, is_file):
        card = tk.Frame(parent, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        card.pack(fill="x", pady=6)

        tk.Label(card, text=title, bg=self.bg_card, fg=self.text_main, font=("Microsoft YaHei", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 4))

        row = tk.Frame(card, bg=self.bg_card)
        row.pack(fill="x", padx=12, pady=(0, 12))

        entry = tk.Entry(row, textvariable=var, bg="#1b2028", fg=self.text_main, insertbackground=self.text_main, relief="flat", font=("Consolas", 10))
        entry.pack(side="left", fill="x", expand=True, ipady=6)

        def browse():
            if is_file:
                path = filedialog.askopenfilename(title=f"{get_text('BTN_SELECT')}{title}", filetypes=[("模型文件", "*.pt *.onnx *.pth"), ("所有文件", "*.*")])
            else:
                path = filedialog.askdirectory(title=f"{get_text('BTN_SELECT')}{title}")
            if path:
                var.set(path)

        tk.Button(row, text=get_text("BTN_SELECT"), bg=self.btn_bg, fg=self.text_main, relief="flat", activebackground=self.btn_hover, activeforeground=self.text_main, command=browse).pack(side="left", padx=(8, 0))

    def _build_training_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_right)
        self._page_title(page, get_text("TITLE_TRAINING"), get_text("SUBTITLE_TRAINING"))

        self.training_vars = {
            "epochs": tk.StringVar(value=str(self.config_data.get("training", {}).get("epochs", 100))),
            "batch_size": tk.StringVar(value=str(self.config_data.get("training", {}).get("batch_size", 16))),
            "imgsz": tk.StringVar(value=str(self.config_data.get("training", {}).get("imgsz", 640))),
            "device": tk.StringVar(value=self.config_data.get("training", {}).get("device", "0")),
            "project": tk.StringVar(value=self.config_data.get("training", {}).get("project", "runs/train")),
            "name": tk.StringVar(value=self.config_data.get("training", {}).get("name", "exp"))
        }

        for key, label in [("epochs", get_text("LABEL_EPOCHS")), ("batch_size", get_text("LABEL_BATCH_SIZE")), ("imgsz", get_text("LABEL_IMGSZ")), ("device", get_text("LABEL_DEVICE")), ("project", get_text("LABEL_PROJECT")), ("name", get_text("LABEL_NAME"))]:
            card = tk.Frame(page, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
            card.pack(fill="x", pady=6)
            tk.Label(card, text=label, bg=self.bg_card, fg=self.text_main, font=("Microsoft YaHei", 10, "bold")).pack(anchor="w", padx=12, pady=(10, 4))
            row = tk.Frame(card, bg=self.bg_card)
            row.pack(fill="x", padx=12, pady=(0, 12))
            entry = tk.Entry(row, textvariable=self.training_vars[key], bg="#1b2028", fg=self.text_main, insertbackground=self.text_main, relief="flat", font=("Consolas", 10))
            entry.pack(side="left", fill="x", expand=True, ipady=6)
        return page

    def _build_behavior_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_right)
        self._page_title(page, get_text("TITLE_BEHAVIOR"), get_text("SUBTITLE_BEHAVIOR"))

        self.auto_save_var = tk.BooleanVar(value=self.config_data["behavior"].get("auto_save", True))
        self.auto_save_nav_var = tk.BooleanVar(value=self.config_data["behavior"].get("auto_save_on_navigate", True))

        card = tk.Frame(page, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        card.pack(fill="x", pady=6)

        tk.Checkbutton(card, text=get_text("CHECK_AUTO_SAVE"), variable=self.auto_save_var, bg=self.bg_card, fg=self.text_main, activebackground=self.bg_card, activeforeground=self.text_main, selectcolor="#1b2028", font=("Microsoft YaHei", 10)).pack(anchor="w", padx=12, pady=(12, 8))
        tk.Checkbutton(card, text=get_text("CHECK_AUTO_SAVE_NAV"), variable=self.auto_save_nav_var, bg=self.bg_card, fg=self.text_main, activebackground=self.bg_card, activeforeground=self.text_main, selectcolor="#1b2028", font=("Microsoft YaHei", 10)).pack(anchor="w", padx=12, pady=(0, 12))
        return page

    def _build_inference_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_right)
        self._page_title(page, get_text("TITLE_INFERENCE"), get_text("SUBTITLE_INFERENCE"))

        self.auto_infer_var = tk.BooleanVar(value=self.config_data.get("inference", {}).get("auto_infer_on_open", False))
        self.enable_openclaw_var = tk.BooleanVar(value=self.config_data.get("inference", {}).get("enable_openclaw", True))

        card = tk.Frame(page, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        card.pack(fill="x", pady=6)

        tk.Checkbutton(card, text=get_text("CHECK_AUTO_INFER"), variable=self.auto_infer_var, bg=self.bg_card, fg=self.text_main, activebackground=self.bg_card, activeforeground=self.text_main, selectcolor="#1b2028", font=("Microsoft YaHei", 10)).pack(anchor="w", padx=12, pady=(12, 8))
        tk.Checkbutton(card, text=get_text("CHECK_ENABLE_OPENCLAW"), variable=self.enable_openclaw_var, bg=self.bg_card, fg=self.text_main, activebackground=self.bg_card, activeforeground=self.text_main, selectcolor="#1b2028", font=("Microsoft YaHei", 10)).pack(anchor="w", padx=12, pady=(0, 12))
        return page

    def _build_appearance_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_right)
        self._page_title(page, get_text("TITLE_APPEARANCE"), get_text("SUBTITLE_APPEARANCE"))

        self.alpha_var = tk.DoubleVar(value=self.config_data.get("ui", {}).get("alpha", 0.96))

        card = tk.Frame(page, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        card.pack(fill="x", pady=6)

        tk.Label(card, text=get_text("LABEL_OPACITY"), bg=self.bg_card, fg=self.text_main, font=("Microsoft YaHei", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 6))

        self.alpha_value_label = tk.Label(card, text=f"{int(self.alpha_var.get() * 100)}%", bg=self.bg_card, fg=self.text_sub, font=("Microsoft YaHei", 9))
        self.alpha_value_label.pack(anchor="w", padx=12, pady=(0, 4))

        scale = tk.Scale(card, from_=85, to=100, orient="horizontal", bg=self.bg_card, fg=self.text_sub, troughcolor="#151922", highlightthickness=0, bd=0, activebackground="#6ea8fe", command=self._on_alpha_change)
        scale.set(int(self.alpha_var.get() * 100))
        scale.pack(fill="x", padx=12, pady=(0, 12))
        return page

    def _on_alpha_change(self, value):
        alpha = float(value) / 100
        self.alpha_var.set(alpha)
        self.alpha_value_label.config(text=f"{int(alpha * 100)}%")

    def _build_language_page(self):
        page = tk.Frame(self.content_frame, bg=self.bg_right)
        self._page_title(page, get_text("TITLE_LANGUAGE"), get_text("SUBTITLE_LANGUAGE"))

        lang_map_display = {"zh_CN": "简体中文", "en_US": "English"}
        lang_map_value = {"简体中文": "zh_CN", "English": "en_US"}
        self._lang_map_value = lang_map_value

        current_lang = self.config_data.get("ui", {}).get("language", "zh_CN")
        display_value = lang_map_display.get(current_lang, "简体中文")

        self.language_var = tk.StringVar(value=display_value)

        card = tk.Frame(page, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        card.pack(fill="x", pady=6)

        tk.Label(card, text=get_text("LABEL_UI_LANGUAGE"), bg=self.bg_card, fg=self.text_main, font=("Microsoft YaHei", 10, "bold")).pack(anchor="w", padx=12, pady=(12, 6))

        combo = ttk.Combobox(card, textvariable=self.language_var, values=["简体中文", "English"], state="readonly", width=20)
        combo.pack(anchor="w", padx=12, pady=(0, 12))

        return page

    def save_settings(self):
        try:
            self.config_data["paths"]["image_dir"] = self.path_vars["image_dir"].get().strip()
            self.config_data["paths"]["label_dir"] = self.path_vars["label_dir"].get().strip()
            self.config_data["paths"]["model_path"] = self.path_vars["model_path"].get().strip()
            self.config_data["paths"]["output_dataset_dir"] = self.path_vars["output_dataset_dir"].get().strip()
            self.config_data["paths"]["bad_cases_dir"] = self.path_vars["bad_cases_dir"].get().strip()

            self.config_data["behavior"]["auto_save"] = self.auto_save_var.get()
            self.config_data["behavior"]["auto_save_on_navigate"] = self.auto_save_nav_var.get()

            if "inference" not in self.config_data:
                self.config_data["inference"] = {}
            self.config_data["inference"]["auto_infer_on_open"] = self.auto_infer_var.get()
            self.config_data["inference"]["enable_openclaw"] = self.enable_openclaw_var.get()

            if "training" not in self.config_data:
                self.config_data["training"] = {}
            self.config_data["training"]["epochs"] = int(self.training_vars["epochs"].get() or 100)
            self.config_data["training"]["batch_size"] = int(self.training_vars["batch_size"].get() or 16)
            self.config_data["training"]["imgsz"] = int(self.training_vars["imgsz"].get() or 640)
            self.config_data["training"]["device"] = self.training_vars["device"].get().strip() or "0"
            self.config_data["training"]["project"] = self.training_vars["project"].get().strip() or "runs/train"
            self.config_data["training"]["name"] = self.training_vars["name"].get().strip() or "exp"

            if "ui" not in self.config_data:
                self.config_data["ui"] = {}
            self.config_data["ui"]["alpha"] = round(self.alpha_var.get(), 2)
            self.config_data["ui"]["language"] = self._lang_map_value.get(self.language_var.get(), "zh_CN")

            save_config(self.config_data)

            if self.on_saved_callback:
                self.on_saved_callback(self.config_data)

            messagebox.showinfo("成功", "设置已保存")
            self.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"设置保存失败：\n{e}")
