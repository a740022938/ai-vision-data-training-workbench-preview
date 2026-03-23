import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from core.config_manager import load_config, save_config
from ui.settings_window import SettingsWindow
from ui.training_window import TrainingWindow
from core.config_manager import load_config

def get_text(key):
    """根据当前语言配置获取文本"""
    config = load_config()
    lang = config.get("ui", {}).get("language", "zh_CN")
    if lang == "en_US":
        from config.texts import en_us as texts
    else:
        from config.texts import zh_cn as texts
    return getattr(texts, key, key)
from ui.style import get_basic_style
from ui.edit_box_window import EditBoxWindow
from ui.canvas_panel import CanvasPanel
from ui.right_panel import RightPanel
from core.context_builder import build_context
from core.plugin_api import get_canvas_menu_plugins
from core.external_api import send_context_to_external
from core.badcase_manager import mark_bad_case
from core.yolo_infer import infer_image
from core.dataset_exporter import export_dataset
from core.openclaw_bridge import analyze_with_openclaw
from core.badcase_manager import mark_bad_case
from core.yolo_infer import infer_image
from core.dataset_exporter import export_dataset
from core.openclaw_bridge import analyze_with_openclaw

CLASS_NAMES = [
    "1W","2W","3W","4W","5W","6W","7W","8W","9W",
    "1T","2T","3T","4T","5T","6T","7T","8T","9T",
    "1B","2B","3B","4B","5B","6B","7B","8B","9B",
    "DF","NF","XF","BF","HZ","FC","BL"
]


class MainWindow:
    def __init__(self, root):
        self.root = root
        self.ui_style = get_basic_style()
        self.canvas_panel = None
        self.right_panel = None
        self.CLASS_NAMES = CLASS_NAMES

        self.config_data = load_config()
        self.alpha_value = self.config_data.get("ui", {}).get("alpha", 0.96)

        self.valid_ext = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

        self.image_dir = self.config_data.get("paths", {}).get("image_dir", "")
        self.label_dir = self.config_data.get("paths", {}).get("label_dir", "")
        self.auto_save = self.config_data.get("behavior", {}).get("auto_save_on_navigate", True)

        self.image_files = []
        self.current_index = 0

        self.original_image = None
        self.display_image = None
        self.current_tk = None
        self.current_image_name = ""
        self.img_offset_x = 0
        self.img_offset_y = 0
        self.display_w = 0
        self.display_h = 0
        self.orig_w = 0
        self.orig_h = 0

        self.boxes = []
        self.selected_idx = None
        self._last_auto_infer_image = None

        self.drag_mode = None
        self.dragging = False
        self.start_x = 0
        self.start_y = 0
        self.temp_x = 0
        self.temp_y = 0
        self.move_offset_x = 0
        self.move_offset_y = 0
        self.active_handle = None
        self.handle_size = 8

        self.root.attributes("-alpha", self.alpha_value)
        self._build_ui()

        self.root.bind("<Control-0>", lambda e: self.set_view_fit())
        self.root.bind("<Control-1>", lambda e: self.set_view_original())
        self._bind_shortcuts()
        self.load_images()
        self.show_current_image()

    def _build_ui(self):
        # ====================
        # UI 区域一 顶部区域
        # ====================
        self.canvas_panel = CanvasPanel(self.root, app=self)
        self.right_panel = RightPanel(self.root, app=self)

        self.bg_main = "#16181d"
        self.bg_top = "#1b1f26"
        self.bg_card = "#20242c"
        self.bg_card_2 = "#252a33"
        self.text_main = "#f5f7fa"
        self.text_sub = "#aeb6c2"
        self.accent = "#6ea8fe"
        self.border = "#2d3440"
        self.btn_bg = "#2a303a"
        self.btn_hover = "#343b47"
        self.status_bg = "#171b22"

        self.root.configure(bg=self.bg_main)

        top_bar = tk.Frame(self.root, bg=self.bg_top, height=78)
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)

        title_wrap = tk.Frame(top_bar, bg=self.bg_top)
        title_wrap.pack(side="left", padx=18, pady=14)

        tk.Label(
            title_wrap,
            text=get_text("APP_TITLE"),
            bg=self.bg_top,
            fg=self.ui_style["text_fg"],
            font=self.ui_style["title_font"]
        ).pack(anchor="w", pady=(0, 2))

        tk.Label(
            title_wrap,
            text=get_text("APP_SUBTITLE"),
            bg=self.bg_top,
            fg=self.text_sub,
            font=("Microsoft YaHei", 9)
        ).pack(anchor="w")

        btn_wrap = tk.Frame(top_bar, bg=self.bg_top)
        btn_wrap.pack(side="right", padx=14)

        self._create_top_button(btn_wrap, get_text("BTN_OPEN_PROJECT"), self.open_project).pack(side="left", padx=5, pady=12)
        self._create_top_button(btn_wrap, get_text("BTN_SAVE"), self.save_current_labels).pack(side="left", padx=5, pady=12)
        self._create_top_button(btn_wrap, get_text("BTN_AUTO_DETECT"), self.not_ready_yolo).pack(side="left", padx=5, pady=12)
        self._create_top_button(btn_wrap, get_text("BTN_EXPORT"), self.export_dataset_action).pack(side="left", padx=5, pady=12)
        self.ai_analysis_btn = self._create_top_button(btn_wrap, get_text("BTN_AI_ANALYSIS"), self.run_openclaw_analysis)
        self.ai_analysis_btn.pack(side="left", padx=5, pady=12)
        if not self.config_data.get("inference", {}).get("enable_openclaw", True):
            self.ai_analysis_btn.config(state="disabled", fg="#7f8a99")
        self._create_top_button(btn_wrap, get_text("BTN_FIT_WINDOW"), self.set_view_fit).pack(side="left", padx=5, pady=12)
        self._create_top_button(btn_wrap, get_text("BTN_ORIGINAL_SCALE"), self.set_view_original).pack(side="left", padx=5, pady=12)
        self._create_top_button(btn_wrap, get_text("BTN_SETTINGS"), self.show_settings_tip).pack(side="left", padx=5, pady=12)

        body = tk.Frame(self.root, bg=self.bg_main)
        body.pack(fill="both", expand=True, padx=14, pady=14)

        left_card = tk.Frame(body, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        left_card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        left_header = tk.Frame(left_card, bg=self.bg_card, height=68)
        left_header.pack(fill="x", side="top")
        left_header.pack_propagate(False)

        tk.Label(
            left_header,
            text=get_text("LABEL_IMAGE_WORKSPACE"),
            bg=self.bg_card,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 13, "bold")
        ).pack(side="left", padx=14, pady=14)

        self.image_info_label = tk.Label(
            left_header,
            text=get_text("STATUS_WAITING_LOAD"),
            bg="#2b3240",
            fg="#d7deea",
            font=("Microsoft YaHei", 9),
            padx=12,
            pady=5
        )
        self.image_info_label.pack(side="right", padx=14, pady=12)

        self.canvas_area = tk.Frame(left_card, bg="#111318")
        self.canvas_area.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        # ====================
        # UI 区域二 画布区域
        # ====================
        self.image_canvas = tk.Canvas(self.canvas_area, bg="#111318", highlightthickness=0, bd=0)
        self.image_canvas.pack(fill="both", expand=True)
        self.image_canvas.bind("<Button-1>", self.on_mouse_down)
        self.image_canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.image_canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.image_canvas.bind("<Button-3>", self.on_right_click)

        right_card = tk.Frame(body, bg=self.bg_card, width=265, highlightthickness=1, highlightbackground=self.border)
        right_card.pack(side="right", fill="y")
        right_card.pack_propagate(False)

        right_header = tk.Frame(right_card, bg=self.bg_card, height=48)
        right_header.pack(fill="x", side="top")
        right_header.pack_propagate(False)

        tk.Label(
            right_header,
            text=get_text("LABEL_CONTROL_PANEL"),
            bg=self.bg_card,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 12, "bold")
        ).pack(side="left", padx=14, pady=10)

        # ====================
        # UI 区域三 右侧信息区域
        # ====================
        info_card = tk.Frame(right_card, bg=self.bg_card_2)
        info_card.pack(fill="x", padx=12, pady=(8, 8))

        tk.Label(
            info_card,
            text=get_text("LABEL_CURRENT_PROJECT"),
            bg=self.bg_card_2,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 2))

        self.project_info_label = tk.Label(
            info_card,
            text="等待接入图片目录与数据状态显示",
            bg=self.bg_card_2,
            fg=self.text_sub,
            justify="left",
            anchor="w",
            font=("Microsoft YaHei", 9)
        )
        self.project_info_label.pack(anchor="w", fill="x", padx=12, pady=(0, 10))

        class_card = tk.Frame(right_card, bg=self.bg_card_2)
        class_card.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            class_card,
            text=get_text("LABEL_CLASS_SETTINGS"),
            bg=self.bg_card_2,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 8))

        tk.Label(class_card, text=get_text("LABEL_SELECTED_CLASS"), bg=self.bg_card_2, fg=self.text_sub, font=("Microsoft YaHei", 9)).pack(anchor="w", padx=12)
        self.class_var = tk.StringVar(value=CLASS_NAMES[0])
        self.class_combo = ttk.Combobox(class_card, textvariable=self.class_var, values=CLASS_NAMES, state="readonly", width=14)
        self.class_combo.pack(fill="x", padx=12, pady=(4, 8))
        self.class_combo.bind("<<ComboboxSelected>>", self.change_selected_class)

        tk.Label(class_card, text=get_text("LABEL_SELECTED_BOX_LIST"), bg=self.bg_card_2, fg=self.text_sub, font=("Microsoft YaHei", 9)).pack(anchor="w", padx=12)
        list_wrap = tk.Frame(class_card, bg=self.bg_card_2)
        list_wrap.pack(fill="both", padx=12, pady=(4, 12))

        self.box_listbox = tk.Listbox(
            list_wrap,
            height=8,
            bg="#1b2028",
            fg=self.ui_style["text_fg"],
            selectbackground="#40516d",
            selectforeground="#ffffff",
            relief="flat",
            bd=0,
            font=("Consolas", 10)
        )
        self.box_listbox.pack(side="left", fill="both", expand=True)
        self.box_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        ysb = tk.Scrollbar(list_wrap, command=self.box_listbox.yview)
        ysb.pack(side="right", fill="y")
        self.box_listbox.config(yscrollcommand=ysb.set)

        selected_card = tk.Frame(right_card, bg=self.bg_card_2)
        selected_card.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            selected_card,
            text=get_text("LABEL_SELECTED_BOX"),
            bg=self.bg_card_2,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 8))

        self.selected_box_title = tk.Label(
            selected_card,
            text=get_text("LABEL_NO_BOX_SELECTED"),
            bg=self.bg_card_2,
            fg=self.text_sub,
            font=("Microsoft YaHei", 9)
        )
        self.selected_box_title.pack(anchor="w", padx=12, pady=(0, 8))

        # ====================
        # UI 区域四 选中框编辑区域
        # ====================
        self.info_vars = {
            "cx": tk.StringVar(value=""),
            "cy": tk.StringVar(value=""),
            "w": tk.StringVar(value=""),
            "h": tk.StringVar(value="")
        }

        self.info_entries = {}

        for field in ["cx", "cy", "w", "h"]:
            row = tk.Frame(selected_card, bg=self.bg_card_2)
            row.pack(fill="x", padx=12, pady=3)

            tk.Label(
                row,
                text=field,
                width=5,
                anchor="w",
                bg=self.bg_card_2,
                fg=self.text_sub,
                font=("Consolas", 10)
            ).pack(side="left")

            entry = tk.Entry(
                row,
                textvariable=self.info_vars[field],
                bg="#1b2028",
                fg=self.ui_style["text_fg"],
                insertbackground=self.text_main,
                relief="flat",
                font=("Consolas", 10)
            )
            entry.pack(side="left", fill="x", expand=True, ipady=5)
            self.info_entries[field] = entry

        info_btn_bar = tk.Frame(selected_card, bg=self.bg_card_2)
        info_btn_bar.pack(fill="x", padx=12, pady=(10, 12))

        self.apply_info_btn = tk.Button(
            info_btn_bar,
            text=get_text("BTN_APPLY_FINE_TUNE"),
            bg="#3a6df0",
            fg="white",
            relief="flat",
            activebackground="#4b7cff",
            activeforeground="white",
            command=self.apply_selected_box_info
        )
        self.apply_info_btn.pack(side="left")

        self.open_edit_btn = tk.Button(
            info_btn_bar,
            text=get_text("BTN_OPEN_EDIT_WINDOW"),
            bg=self.btn_bg,
            fg=self.ui_style["text_fg"],
            relief="flat",
            activebackground=self.btn_hover,
            activeforeground=self.text_main,
            command=self.open_edit_window
        )
        self.open_edit_btn.pack(side="left", padx=6)

        self.delete_info_btn = tk.Button(
            info_btn_bar,
            text=get_text("BTN_DELETE_CURRENT_BOX"),
            bg="#7a2e2e",
            fg="white",
            relief="flat",
            activebackground="#914141",
            activeforeground="white",
            command=self.delete_selected_box
        )
        self.delete_info_btn.pack(side="left")

        action_card = tk.Frame(right_card, bg=self.bg_card_2)
        action_card.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            action_card,
            text=get_text("LABEL_SHORTCUT_OPS"),
            bg=self.bg_card_2,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 8))

        self._create_side_button(action_card, get_text("BTN_DELETE_SELECTED"), self.delete_selected_box).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_PREV_IMAGE"), self.prev_image).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_NEXT_IMAGE"), self.next_image).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_SAVE_LABELS"), self.save_current_labels).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_BATCH_RENAME"), self.batch_rename).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_BACKUP"), self.backup_workspace).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_RESTORE"), self.restore_workspace).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, get_text("BTN_START_TRAINING"), self.show_training_window_placeholder).pack(fill="x", padx=12, pady=4)

        tip_card = tk.Frame(right_card, bg=self.bg_card_2)
        tip_card.pack_forget()

        tk.Label(
            tip_card,
            text="操作说明",
            bg=self.bg_card_2,
            fg=self.ui_style["text_fg"],
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 6))

        tk.Label(
            tip_card,
            text="空白处拖拽=新增框\n点中框内部=选中/移动\n拖四角手柄=缩放\n右键框=编辑窗口\nDelete=删除选中框\nCtrl+S=保存标签",
            bg=self.bg_card_2,
            fg=self.text_sub,
            justify="left",
            anchor="w",
            font=("Microsoft YaHei", 9)
        ).pack(anchor="w", padx=12, pady=(0, 10))

        appearance_card = tk.Frame(right_card, bg=self.bg_card_2)
        appearance_card.pack(fill="x", padx=12, pady=(0, 8))
        # 外观透明度标题已移入设置窗口

        self.alpha_scale = tk.Scale(
            appearance_card,
            from_=85,
            to=100,
            orient="horizontal",
            bg=self.bg_card_2,
            fg=self.text_sub,
            troughcolor="#151922",
            highlightthickness=0,
            bd=0,
            activebackground=self.accent,
            command=self.update_alpha
        )
        self.alpha_scale.set(int(self.alpha_value * 100))
        self.alpha_scale.pack_forget()

        status_bar = tk.Frame(self.root, bg="#171b22", height=30)
        status_bar.pack(fill="x", side="bottom")
        status_bar.pack_propagate(False)

        self.status_label = tk.Label(
            status_bar,
            text=get_text("STATUS_MAIN_LOADED"),
            bg="#171b22",
            fg=self.text_sub,
            font=("Microsoft YaHei", 9)
        )
        self.status_label.pack(side="left", padx=12)

    def _bind_shortcuts(self):
        self.root.bind("<Delete>", lambda e: self.delete_selected_box())
        self.root.bind("<Control-s>", lambda e: self.save_current_labels())
        self.root.bind("<Left>", lambda e: self.prev_image())
        self.root.bind("<Right>", lambda e: self.next_image())

    def _create_top_button(self, parent, text, command=None):
        btn = tk.Label(parent, text=text, bg="#2a303a", fg="#f5f7fa", font=("Microsoft YaHei", 9), padx=14, pady=7, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg="#343b47"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#2a303a"))
        if command:
            btn.bind("<Button-1>", lambda e: command())
        return btn

    def _create_side_button(self, parent, text, command=None):
        btn = tk.Label(parent, text=text, anchor="w", bg="#2a303a", fg="#f5f7fa", font=("Microsoft YaHei", 9), padx=12, pady=9, cursor="hand2")
        btn.bind("<Enter>", lambda e: btn.config(bg="#343b47"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#2a303a"))
        if command:
            btn.bind("<Button-1>", lambda e: command())
        return btn

    def update_alpha(self, value):
        alpha = max(0.85, min(1.0, float(value) / 100))
        self.root.attributes("-alpha", alpha)
        self.set_status(f"状态：当前透明度 {int(alpha * 100)}%")

    def set_status(self, text):
        self.status_label.config(text=text)


    def run_openclaw_analysis(self):
        if not self.current_image_name:
            messagebox.showwarning("提示", "当前没有图片可分析")
            return

        image_path = os.path.join(self.image_dir, self.current_image_name)
        label_path = self.get_label_path(self.current_image_name)

        # 先保存当前标签，保证 AI 看到的是最新内容
        if self.label_dir:
            self.save_current_labels()

        try:
            self.set_status("状态：正在调用 OpenClaw 分析...")
            self.root.update_idletasks()

            ok, result_text = analyze_with_openclaw(
                image_path=image_path,
                label_path=label_path,
                boxes=self.boxes,
                selected_idx=self.selected_idx,
                class_names=CLASS_NAMES,
                agent_name="main"
            )

            if ok:
                self.set_status("状态：OpenClaw 分析完成")
                messagebox.showinfo("OpenClaw 分析结果", result_text)
            else:
                self.set_status("状态：OpenClaw 分析失败")
                messagebox.showerror("OpenClaw 分析失败", result_text)

        except Exception as e:
            self.set_status("状态：OpenClaw 分析异常")
            messagebox.showerror("OpenClaw 分析异常", str(e))

    def open_project(self):
        folder = filedialog.askdirectory(title="选择图片目录", initialdir=self.image_dir or os.getcwd())
        if not folder:
            return
        self.image_dir = folder
        self.config_data["paths"]["image_dir"] = folder
        save_config(self.config_data)
        self.current_index = 0
        self.load_images()
        self.show_current_image()
        self.set_status("状态：图片目录已更新")

    def show_settings_tip(self):
        SettingsWindow(self.root, self.apply_settings)

    def apply_settings(self, new_config):
        self.config_data = new_config
        self.image_dir = self.config_data.get("paths", {}).get("image_dir", "")
        self.label_dir = self.config_data.get("paths", {}).get("label_dir", "")
        self.auto_save = self.config_data.get("behavior", {}).get("auto_save_on_navigate", True)

        alpha = self.config_data.get("ui", {}).get("alpha", 0.96)
        self.root.attributes("-alpha", alpha)
        self.alpha_scale.set(int(alpha * 100))

        self.current_index = 0
        
        if self.config_data.get("inference", {}).get("enable_openclaw", True):
            self.ai_analysis_btn.config(state="normal", fg="#f5f7fa")
        else:
            self.ai_analysis_btn.config(state="disabled", fg="#7f8a99")
        
        self.load_images()
        self.show_current_image()
        self.set_status("状态：设置已应用")

    def not_ready_yolo(self):
        self.run_yolo_infer()

    def run_yolo_infer(self):
        if not self.current_image_name:
            messagebox.showwarning("提示", "当前没有图片可识别")
            return

        model_path = self.config_data.get("paths", {}).get("model_path", "").strip()
        if not model_path:
            messagebox.showwarning("提示", "请先在设置里填写模型路径")
            return

        image_path = os.path.join(self.image_dir, self.current_image_name)
        if not os.path.exists(image_path):
            messagebox.showerror("错误", f"图片不存在：\n{image_path}")
            return

        conf = self.config_data.get("model", {}).get("conf", 0.25)

        try:
            self.set_status("状态：正在执行 YOLO 自动识别...")
            self.root.update_idletasks()

            yolo_boxes = infer_image(model_path, image_path, conf=conf)

            self.boxes = yolo_boxes
            self.selected_idx = None
            self.refresh_box_list()
            self.redraw_boxes()
            self.update_selected_box_panel()

            self.set_status(f"状态：自动识别完成，共 {len(self.boxes)} 个框")
        except Exception as e:
            messagebox.showerror("识别失败", f"YOLO 自动识别失败：\n{e}")
            self.set_status("状态：YOLO 自动识别失败")

    def get_label_path(self, image_name):
        if not self.label_dir:
            return ""
        return os.path.join(self.label_dir, os.path.splitext(image_name)[0] + ".txt")

    def load_images(self):
        self.image_files = []
        if self.image_dir and os.path.isdir(self.image_dir):
            self.image_files = sorted([f for f in os.listdir(self.image_dir) if f.lower().endswith(self.valid_ext)])
        self.project_info_label.config(text=f"图片目录：{self.image_dir or '未设置'}\n标签目录：{self.label_dir or '未设置'}\n图片数量：{len(self.image_files)}")

    def load_current_labels(self):
        self.boxes = []
        self.selected_idx = None
        if not self.current_image_name:
            return

        label_path = self.get_label_path(self.current_image_name)
        if not label_path or not os.path.exists(label_path):
            self.refresh_box_list()
            return

        try:
            with open(label_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) < 5:
                        continue
                    cls_id = int(float(parts[0]))
                    cx = float(parts[1]); cy = float(parts[2]); bw = float(parts[3]); bh = float(parts[4])
                    self.boxes.append([cls_id, cx, cy, bw, bh])
        except Exception as e:
            messagebox.showerror("错误", f"标签读取失败：\n{e}")
        self.refresh_box_list()

    def save_current_labels(self):
        if not self.current_image_name:
            return
        if not self.label_dir:
            messagebox.showwarning("提示", "config.json 里还没有设置 label_dir")
            return

        os.makedirs(self.label_dir, exist_ok=True)
        label_path = self.get_label_path(self.current_image_name)

        try:
            with open(label_path, "w", encoding="utf-8") as f:
                for cls_id, cx, cy, bw, bh in self.boxes:
                    f.write(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")
            self.set_status(f"状态：已保存 {os.path.basename(label_path)}")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：\n{e}")

    def maybe_autosave(self):
        if self.auto_save:
            self.save_current_labels()

    def show_current_image(self):
        if not self.image_files:
            self.image_canvas.delete("all")
            self.image_canvas.create_text(300, 200, text="未找到图片\n请检查 config.json 中的 image_dir", fill="#7f8a99", font=("Microsoft YaHei", 12))
            self.image_info_label.config(text="没有可显示的图片")
            self.set_status("状态：未找到图片")
            self.update_selected_box_panel()
            return

        self.current_image_name = self.image_files[self.current_index]
        image_path = os.path.join(self.image_dir, self.current_image_name)

        try:
            img = Image.open(image_path).convert("RGB")
            self.original_image = img
            self.orig_w, self.orig_h = img.size

            self.root.update_idletasks()
            area_w = max(self.canvas_area.winfo_width() - 20, 300)
            area_h = max(self.canvas_area.winfo_height() - 20, 300)

            scale = min(area_w / self.orig_w, area_h / self.orig_h)
            if scale <= 0:
                scale = 1.0

            self.display_w = max(1, int(self.orig_w * scale))
            self.display_h = max(1, int(self.orig_h * scale))

            self.display_image = img.resize((self.display_w, self.display_h), Image.LANCZOS)
            self.current_tk = ImageTk.PhotoImage(self.display_image)

            self.image_canvas.delete("all")

            canvas_w = self.image_canvas.winfo_width()
            canvas_h = self.image_canvas.winfo_height()
            if canvas_w <= 1: canvas_w = area_w
            if canvas_h <= 1: canvas_h = area_h

            self.img_offset_x = max((canvas_w - self.display_w) // 2, 0)
            self.img_offset_y = max((canvas_h - self.display_h) // 2, 0)

            self.image_canvas.create_image(self.img_offset_x, self.img_offset_y, anchor="nw", image=self.current_tk)
            self.load_current_labels()
            self.redraw_boxes()

            if self.config_data.get("inference", {}).get("auto_infer_on_open", False):
                if self.current_image_name != self._last_auto_infer_image:
                    self._last_auto_infer_image = self.current_image_name
                    self.root.after(100, self.run_yolo_infer)
                    self.image_info_label.config(text=f"{self.current_image_name}  [{self.current_index + 1}/{len(self.image_files)}]")
                    self.set_status(f"状态：当前图片 {self.current_index + 1}/{len(self.image_files)}，框数 {len(self.boxes)}")
                    self.update_selected_box_panel()
                    return

            self.image_info_label.config(text=f"{self.current_image_name}  [{self.current_index + 1}/{len(self.image_files)}]")
            self.set_status(f"状态：当前图片 {self.current_index + 1}/{len(self.image_files)}，框数 {len(self.boxes)}")
            self.update_selected_box_panel()
        except Exception as e:
            self.image_canvas.delete("all")
            self.image_canvas.create_text(300, 200, text=f"图片加载失败\n{e}", fill="#ff8080", font=("Microsoft YaHei", 12))
            self.set_status("状态：图片加载失败")
        self.update_selected_box_panel()

    def redraw_boxes(self, temp_rect=None):
        self.image_canvas.delete("box")

        for i, box in enumerate(self.boxes):
            x1, y1, x2, y2 = self.box_to_display_rect(box)
            color = "#ff6b6b" if i == self.selected_idx else "#6ea8fe"
            width = 3 if i == self.selected_idx else 2

            self.image_canvas.create_rectangle(
                x1 + self.img_offset_x, y1 + self.img_offset_y,
                x2 + self.img_offset_x, y2 + self.img_offset_y,
                outline=color, width=width, tags="box"
            )

            label = CLASS_NAMES[box[0]]
            text_y = y1 + self.img_offset_y - 10
            if text_y < 10:
                text_y = y1 + self.img_offset_y + 10

            self.image_canvas.create_text(
                x1 + self.img_offset_x + 4, text_y,
                text=label, fill=color, anchor="w",
                font=("Microsoft YaHei", 9, "bold"), tags="box"
            )

            if i == self.selected_idx:
                hs = self.handle_size
                for hx, hy in [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]:
                    self.image_canvas.create_rectangle(
                        hx - hs / 2 + self.img_offset_x,
                        hy - hs / 2 + self.img_offset_y,
                        hx + hs / 2 + self.img_offset_x,
                        hy + hs / 2 + self.img_offset_y,
                        fill="#ffd166", outline="#ffd166", tags="box"
                    )

        if temp_rect:
            x1, y1, x2, y2 = temp_rect
            self.image_canvas.create_rectangle(
                x1 + self.img_offset_x, y1 + self.img_offset_y,
                x2 + self.img_offset_x, y2 + self.img_offset_y,
                outline="#ffcc66", width=2, dash=(4, 2), tags="box"
            )

    def set_view_fit(self):
        self.view_mode = "fit"
        if self.current_image_name:
            self.show_current_image()

    def set_view_original(self):
        self.view_mode = "original"
        if self.current_image_name:
            self.show_current_image()

    def show_training_placeholder(self):
        messagebox.showinfo(
            "????",
            "?????????\n\n????? YOLO ?? ??? ????????"
        )

    def box_to_display_rect(self, box):
        cls_id, cx, cy, bw, bh = box
        x1 = (cx - bw / 2) * self.display_w
        y1 = (cy - bh / 2) * self.display_h
        x2 = (cx + bw / 2) * self.display_w
        y2 = (cy + bh / 2) * self.display_h
        return x1, y1, x2, y2

    def display_rect_to_box(self, x1, y1, x2, y2, cls_id=None):
        cls_id = 0 if cls_id is None else cls_id
        lx = max(0, min(self.display_w, min(x1, x2)))
        rx = max(0, min(self.display_w, max(x1, x2)))
        ty = max(0, min(self.display_h, min(y1, y2)))
        by = max(0, min(self.display_h, max(y1, y2)))
        if abs(rx - lx) < 8 or abs(by - ty) < 8:
            return None
        cx = ((lx + rx) / 2) / self.display_w
        cy = ((ty + by) / 2) / self.display_h
        bw = abs(rx - lx) / self.display_w
        bh = abs(by - ty) / self.display_h
        return [cls_id, cx, cy, bw, bh]

    def get_handle_hit(self, px, py, box):
        x1, y1, x2, y2 = self.box_to_display_rect(box)
        hs = self.handle_size
        handles = {"tl": (x1, y1), "tr": (x2, y1), "bl": (x1, y2), "br": (x2, y2)}
        for name, (hx, hy) in handles.items():
            if abs(px - hx) <= hs and abs(py - hy) <= hs:
                return name
        return None

    def hit_test_box(self, px, py):
        for i in range(len(self.boxes) - 1, -1, -1):
            handle = self.get_handle_hit(px, py, self.boxes[i])
            if handle:
                return i, "handle", handle

            x1, y1, x2, y2 = self.box_to_display_rect(self.boxes[i])
            if x1 <= px <= x2 and y1 <= py <= y2:
                return i, "inside", None

        return None, None, None

    def on_mouse_down(self, event):
        if not self.display_image:
            return
        px = event.x - self.img_offset_x
        py = event.y - self.img_offset_y
        if not (0 <= px <= self.display_w and 0 <= py <= self.display_h):
            return

        hit_idx, hit_type, handle = self.hit_test_box(px, py)

        if hit_idx is not None:
            self.selected_idx = hit_idx
            self.class_var.set(CLASS_NAMES[self.boxes[hit_idx][0]])
            self.refresh_box_list()

            if hit_type == "handle":
                self.drag_mode = "resize"
                self.active_handle = handle
                self.dragging = True
                self.set_status(f"状态：开始缩放框 {hit_idx}")
            else:
                self.drag_mode = "move"
                self.dragging = True
                x1, y1, x2, y2 = self.box_to_display_rect(self.boxes[hit_idx])
                self.move_offset_x = px - x1
                self.move_offset_y = py - y1
                self.set_status(f"状态：已选中框 {hit_idx}")

            self.redraw_boxes()
        else:
            self.selected_idx = None
            self.drag_mode = "add"
            self.dragging = True
            self.start_x = px
            self.start_y = py
            self.temp_x = px
            self.temp_y = py
            self.refresh_box_list()
            self.redraw_boxes()

    def on_mouse_drag(self, event):
        if not self.dragging or not self.display_image:
            return
        px = max(0, min(self.display_w, event.x - self.img_offset_x))
        py = max(0, min(self.display_h, event.y - self.img_offset_y))

        if self.drag_mode == "add":
            self.temp_x = px
            self.temp_y = py
            self.redraw_boxes((self.start_x, self.start_y, self.temp_x, self.temp_y))
            self.set_status(f"状态：正在新增框，当前框数 {len(self.boxes)}")

        elif self.drag_mode == "move" and self.selected_idx is not None:
            box = self.boxes[self.selected_idx]
            x1, y1, x2, y2 = self.box_to_display_rect(box)
            bw = x2 - x1
            bh = y2 - y1

            new_x1 = px - self.move_offset_x
            new_y1 = py - self.move_offset_y
            new_x2 = new_x1 + bw
            new_y2 = new_y1 + bh

            if new_x1 < 0:
                new_x2 -= new_x1
                new_x1 = 0
            if new_y1 < 0:
                new_y2 -= new_y1
                new_y1 = 0
            if new_x2 > self.display_w:
                shift = new_x2 - self.display_w
                new_x1 -= shift
                new_x2 = self.display_w
            if new_y2 > self.display_h:
                shift = new_y2 - self.display_h
                new_y1 -= shift
                new_y2 = self.display_h

            new_box = self.display_rect_to_box(new_x1, new_y1, new_x2, new_y2, box[0])
            if new_box:
                self.boxes[self.selected_idx] = new_box
                self.redraw_boxes()
                self.refresh_box_list()

        elif self.drag_mode == "resize" and self.selected_idx is not None:
            box = self.boxes[self.selected_idx]
            x1, y1, x2, y2 = self.box_to_display_rect(box)
            nx1, ny1, nx2, ny2 = x1, y1, x2, y2

            if self.active_handle == "tl":
                nx1, ny1 = px, py
            elif self.active_handle == "tr":
                nx2, ny1 = px, py
            elif self.active_handle == "bl":
                nx1, ny2 = px, py
            elif self.active_handle == "br":
                nx2, ny2 = px, py

            new_box = self.display_rect_to_box(nx1, ny1, nx2, ny2, box[0])
            if new_box:
                self.boxes[self.selected_idx] = new_box
                self.redraw_boxes()
                self.refresh_box_list()
                self.set_status(f"状态：正在缩放框 {self.selected_idx}")

    def on_mouse_up(self, event):
        if not self.dragging:
            return

        self.dragging = False

        if self.drag_mode == "add":
            new_box = self.display_rect_to_box(self.start_x, self.start_y, self.temp_x, self.temp_y, 0)
            if new_box:
                self.boxes.append(new_box)
                self.selected_idx = len(self.boxes) - 1
                self.class_var.set(CLASS_NAMES[new_box[0]])
                self.refresh_box_list()
                self.redraw_boxes()
                self.set_status(f"状态：新增框成功，当前框数 {len(self.boxes)}")
            else:
                self.redraw_boxes()
                self.set_status("状态：框太小，已取消新增")

        elif self.drag_mode == "move":
            self.redraw_boxes()
            self.set_status(f"状态：框移动完成，当前框数 {len(self.boxes)}")

        elif self.drag_mode == "resize":
            self.redraw_boxes()
            self.set_status(f"状态：框缩放完成，当前框数 {len(self.boxes)}")

        self.drag_mode = None
        self.active_handle = None

    def on_right_click(self, event):
        if not self.display_image:
            return

        px = event.x - self.img_offset_x
        py = event.y - self.img_offset_y

        hit_idx, hit_type, handle = self.hit_test_box(px, py)
        if hit_idx is None:
            return

        self.selected_idx = hit_idx
        self.class_var.set(CLASS_NAMES[self.boxes[hit_idx][0]])
        self.refresh_box_list()
        self.redraw_boxes()

        menu = tk.Menu(self.root, tearoff=0, bg="#252a33", fg="#f5f7fa", activebackground="#40516d", activeforeground="#ffffff")
        menu.add_command(label=get_text("MENU_EDIT_CURRENT_BOX"), command=self.open_edit_window)
        menu.add_command(label=get_text("MENU_DELETE_CURRENT_BOX"), command=self.delete_selected_box)
        menu.add_command(label=get_text("MENU_MARK_BAD_CASE"), command=self.mark_current_bad_case)
        menu.add_command(label=get_text("MENU_MARK_DUPLICATE"), command=self.mark_current_duplicate)
        menu.add_command(label=get_text("MENU_RESTORE_DUPLICATE"), command=self.restore_duplicate)
        menu.add_separator()

        context = build_context(self)
        plugins = get_canvas_menu_plugins(context)
        for item in plugins:
            menu.add_command(label=item.get("label", "插件功能"), command=item.get("callback"))

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_edit_window(self):
        if self.selected_idx is None or not (0 <= self.selected_idx < len(self.boxes)):
            messagebox.showinfo("提示", "请先选中一个框。")
            return

        EditBoxWindow(
            self.root,
            self.selected_idx,
            self.boxes[self.selected_idx],
            CLASS_NAMES,
            on_apply=self.apply_edit_box,
            on_delete=self.delete_box_by_index
        )

    def apply_edit_box(self, box_index, new_box):
        if not (0 <= box_index < len(self.boxes)):
            return
        self.boxes[box_index] = new_box
        self.selected_idx = box_index
        self.class_var.set(CLASS_NAMES[new_box[0]])
        self.refresh_box_list()
        self.redraw_boxes()
        self.set_status(f"状态：框 #{box_index} 已更新")

    def delete_box_by_index(self, box_index):
        if not (0 <= box_index < len(self.boxes)):
            return
        self.boxes.pop(box_index)
        self.selected_idx = None
        self.refresh_box_list()
        self.redraw_boxes()
        self.set_status("状态：已删除该框")

    def update_selected_box_panel(self):
        has_box = self.selected_idx is not None and 0 <= self.selected_idx < len(self.boxes)

        if not has_box:
            self.selected_box_title.config(text="当前未选中任何框")
            for field in ["cx", "cy", "w", "h"]:
                self.info_vars[field].set("")
                self.info_entries[field].config(state="disabled")

            self.apply_info_btn.config(state="disabled")
            self.open_edit_btn.config(state="disabled")
            self.delete_info_btn.config(state="disabled")
            return

        box = self.boxes[self.selected_idx]
        cls_name = CLASS_NAMES[box[0]]

        self.selected_box_title.config(text=f"框 #{self.selected_idx:02d}   类别：{cls_name}")

        self.info_vars["cx"].set(f"{box[1]:.6f}")
        self.info_vars["cy"].set(f"{box[2]:.6f}")
        self.info_vars["w"].set(f"{box[3]:.6f}")
        self.info_vars["h"].set(f"{box[4]:.6f}")

        for field in ["cx", "cy", "w", "h"]:
            self.info_entries[field].config(state="normal")

        self.apply_info_btn.config(state="normal")
        self.open_edit_btn.config(state="normal")
        self.delete_info_btn.config(state="normal")

    def apply_selected_box_info(self):
        if self.selected_idx is None or not (0 <= self.selected_idx < len(self.boxes)):
            messagebox.showinfo("提示", "请先选中一个框。")
            return

        try:
            old_box = self.boxes[self.selected_idx]
            cls_id = old_box[0]

            cx = max(0.0, min(1.0, float(self.info_vars["cx"].get().strip())))
            cy = max(0.0, min(1.0, float(self.info_vars["cy"].get().strip())))
            w = max(0.01, min(1.0, float(self.info_vars["w"].get().strip())))
            h = max(0.01, min(1.0, float(self.info_vars["h"].get().strip())))

            self.boxes[self.selected_idx] = [cls_id, cx, cy, w, h]
            self.redraw_boxes()
            self.refresh_box_list()
            self.update_selected_box_panel()
            self.set_status(f"状态：框 #{self.selected_idx} 已微调")
        except Exception as e:
            messagebox.showerror("输入错误", f"请检查 cx / cy / w / h：\n{e}")

    def mark_current_bad_case(self):
        bad_cases_dir = self.config_data.get("paths", {}).get("bad_cases_dir", "").strip()
        if not bad_cases_dir:
            messagebox.showwarning("提示", "请先在设置里填写 bad_cases 目录")
            return

        if not self.current_image_name:
            messagebox.showwarning("提示", "当前没有图片")
            return

        image_path = os.path.join(self.image_dir, self.current_image_name)
        label_path = self.get_label_path(self.current_image_name)

        # 先保存一下当前标签，保证归档的是最新修正结果
        if self.label_dir:
            self.save_current_labels()

        ok, msg = mark_bad_case(image_path, label_path, bad_cases_dir)
        if ok:
            self.set_status("状态：已标记为 bad case")
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("错误", msg)

    def mark_current_duplicate(self):
        import shutil
        dup_images_dir = r"C:\AI_Workbench\data\duplicate_cache\images"
        dup_labels_dir = r"C:\AI_Workbench\data\duplicate_cache\labels"
        
        if not self.current_image_name:
            self.set_status("状态：当前没有图片")
            return
        
        image_path = os.path.join(self.image_dir, self.current_image_name)
        if not os.path.exists(image_path):
            self.set_status("状态：图片文件不存在")
            return
        
        label_path = self.get_label_path(self.current_image_name)
        
        try:
            if self.label_dir:
                self.save_current_labels()
            
            os.makedirs(dup_images_dir, exist_ok=True)
            os.makedirs(dup_labels_dir, exist_ok=True)
            
            shutil.move(image_path, os.path.join(dup_images_dir, self.current_image_name))
            
            if label_path and os.path.exists(label_path):
                shutil.move(label_path, os.path.join(dup_labels_dir, os.path.basename(label_path)))
            
            self.set_status(f"状态：已标记为重复图并移入暂存")
            self.next_image()
        except Exception as e:
            self.set_status(f"状态：标记重复图失败")
            messagebox.showerror("错误", f"标记重复图失败：\n{e}")

    def restore_duplicate(self):
        import shutil
        dup_images_dir = r"C:\AI_Workbench\data\duplicate_cache\images"
        dup_labels_dir = r"C:\AI_Workbench\data\duplicate_cache\labels"
        
        if not self.image_dir:
            self.set_status("状态：请先设置图片目录")
            return
        
        filepath = filedialog.askopenfilename(
            title="选择要恢复的重复图",
            initialdir=dup_images_dir if os.path.exists(dup_images_dir) else os.getcwd(),
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.webp"), ("所有文件", "*.*")]
        )
        
        if not filepath:
            return
        
        filename = os.path.basename(filepath)
        label_name = os.path.splitext(filename)[0] + ".txt"
        dup_label_path = os.path.join(dup_labels_dir, label_name)
        
        try:
            os.makedirs(self.image_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(self.image_dir, filename))
            
            if os.path.exists(dup_label_path):
                if self.label_dir:
                    os.makedirs(self.label_dir, exist_ok=True)
                    shutil.move(dup_label_path, os.path.join(self.label_dir, label_name))
            
            self.load_images()
            self.set_status(f"状态：已恢复重复图 {filename}")
        except Exception as e:
            self.set_status("状态：恢复重复图失败")
            messagebox.showerror("错误", f"恢复失败：\n{e}")

    def batch_rename(self):
        if not self.image_dir or not os.path.isdir(self.image_dir):
            self.set_status("状态：请先设置图片目录")
            return

        files = sorted([f for f in os.listdir(self.image_dir) if f.lower().endswith(self.valid_ext)])
        if not files:
            self.set_status("状态：目录中没有图片文件")
            return

        temp_prefix = "_temp_"
        rename_map = []

        try:
            # 第一阶段：临时改名
            for i, old_name in enumerate(files):
                old_ext = os.path.splitext(old_name)[1]
                temp_name = f"{temp_prefix}{i:06d}{old_ext}"
                old_path = os.path.join(self.image_dir, old_name)
                temp_path = os.path.join(self.image_dir, temp_name)
                os.rename(old_path, temp_path)

                new_name = f"fbl{i+1:06d}{old_ext}"
                rename_map.append((temp_name, new_name, old_name))

                # 标签临时改名
                if self.label_dir:
                    old_label = os.path.splitext(old_name)[0] + ".txt"
                    temp_label = f"{temp_prefix}{i:06d}.txt"
                    old_label_path = os.path.join(self.label_dir, old_label)
                    temp_label_path = os.path.join(self.label_dir, temp_label)
                    if os.path.exists(old_label_path):
                        os.rename(old_label_path, temp_label_path)

            # 第二阶段：最终改名
            for temp_name, new_name, old_name in rename_map:
                temp_path = os.path.join(self.image_dir, temp_name)
                new_path = os.path.join(self.image_dir, new_name)
                os.rename(temp_path, new_path)

                # 标签最终改名
                if self.label_dir:
                    temp_label = os.path.splitext(temp_name)[0] + ".txt"
                    new_label = os.path.splitext(new_name)[0] + ".txt"
                    temp_label_path = os.path.join(self.label_dir, temp_label)
                    new_label_path = os.path.join(self.label_dir, new_label)
                    if os.path.exists(temp_label_path):
                        os.rename(temp_label_path, new_label_path)

            self.load_images()
            self.set_status(f"状态：批量重命名完成，共 {len(files)} 个文件")
        except Exception as e:
            self.set_status("状态：批量重命名失败")
            messagebox.showerror("错误", f"批量重命名失败：\n{e}")

    def backup_workspace(self):
        import shutil
        from datetime import datetime

        backup_root = r"C:\AI_Workbench\backups"
        files_to_backup = [
            r"C:\AI_Workbench\main.py",
            r"C:\AI_Workbench\ui\main_window.py",
            r"C:\AI_Workbench\ui\settings_window.py",
            r"C:\AI_Workbench\config.json"
        ]

        try:
            os.makedirs(backup_root, exist_ok=True)
            timestamp = datetime.now().strftime("backup_%Y%m%d_%H%M%S")
            backup_dir = os.path.join(backup_root, timestamp)
            os.makedirs(backup_dir, exist_ok=True)

            for filepath in files_to_backup:
                if os.path.exists(filepath):
                    shutil.copy2(filepath, backup_dir)

            self.set_status(f"状态：备份成功 {timestamp}")
            messagebox.showinfo("成功", f"工作台已备份到：\n{backup_dir}")
        except Exception as e:
            self.set_status("状态：备份失败")
            messagebox.showerror("错误", f"备份失败：\n{e}")

    def restore_workspace(self):
        import shutil
        
        backup_root = r"C:\AI_Workbench\backups"
        restore_targets = {
            "main.py": r"C:\AI_Workbench\main.py",
            "main_window.py": r"C:\AI_Workbench\ui\main_window.py",
            "settings_window.py": r"C:\AI_Workbench\ui\settings_window.py",
            "config.json": r"C:\AI_Workbench\config.json"
        }
        
        backup_dir = filedialog.askdirectory(title="选择备份目录", initialdir=backup_root if os.path.exists(backup_root) else os.getcwd())
        if not backup_dir:
            return
        
        try:
            restored_count = 0
            for filename, target_path in restore_targets.items():
                source_path = os.path.join(backup_dir, filename)
                if os.path.exists(source_path):
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    shutil.copy2(source_path, target_path)
                    restored_count += 1
            
            if restored_count > 0:
                self.set_status(f"状态：恢复成功，共 {restored_count} 个文件")
                messagebox.showinfo("成功", f"已从备份恢复 {restored_count} 个文件：\n{backup_dir}")
            else:
                self.set_status("状态：未找到备份文件")
                messagebox.showwarning("提示", "所选目录中没有找到备份文件")
        except Exception as e:
            self.set_status("状态：恢复失败")
            messagebox.showerror("错误", f"恢复失败：\n{e}")

    def show_training_window_placeholder(self):
        training_config = self.config_data.get("training", {})
        TrainingWindow(self.root, config=training_config)

    def refresh_box_list(self):
        self.box_listbox.delete(0, tk.END)
        for i, box in enumerate(self.boxes):
            cls_name = CLASS_NAMES[box[0]]
            self.box_listbox.insert(tk.END, f"[{i:02d}] {cls_name}")

        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.boxes):
            self.box_listbox.selection_set(self.selected_idx)
            self.box_listbox.see(self.selected_idx)

        self.update_selected_box_panel()

    def on_listbox_select(self, event):
        selection = self.box_listbox.curselection()
        if not selection:
            return
        self.selected_idx = selection[0]
        self.class_var.set(CLASS_NAMES[self.boxes[self.selected_idx][0]])
        self.redraw_boxes()
        self.set_status(f"状态：已选中框 {self.selected_idx}")

    def change_selected_class(self, event=None):
        if self.selected_idx is None or not (0 <= self.selected_idx < len(self.boxes)):
            return
        new_name = self.class_var.get().strip()
        if new_name not in CLASS_NAMES:
            return
        self.boxes[self.selected_idx][0] = CLASS_NAMES.index(new_name)
        self.refresh_box_list()
        self.redraw_boxes()
        self.set_status(f"状态：类别已修改为 {new_name}")

    def delete_selected_box(self):
        if self.selected_idx is None or not (0 <= self.selected_idx < len(self.boxes)):
            messagebox.showinfo("提示", "请先选中一个框。")
            return
        self.boxes.pop(self.selected_idx)
        self.selected_idx = None
        self.refresh_box_list()
        self.redraw_boxes()
        self.set_status(f"状态：已删除框，当前框数 {len(self.boxes)}")


    def export_dataset_action(self):
        output_dir = self.config_data.get("paths", {}).get("output_dataset_dir", "").strip()

        if not output_dir:
            messagebox.showwarning("提示", "请先在设置里填写输出数据集目录")
            return

        ok, msg = export_dataset(
            self.image_dir,
            self.label_dir,
            output_dir,
            CLASS_NAMES
        )

        if ok:
            self.set_status("状态：数据集导出完成")
            messagebox.showinfo("成功", msg)
        else:
            messagebox.showerror("错误", msg)

    def prev_image(self):
        if not self.image_files:
            return
        if self.current_index > 0:
            self.maybe_autosave()
            self.current_index -= 1
            self.show_current_image()

    def next_image(self):
        if not self.image_files:
            return
        if self.current_index < len(self.image_files) - 1:
            self.maybe_autosave()
            self.current_index += 1
            self.show_current_image()



















































