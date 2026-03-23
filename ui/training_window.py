import tkinter as tk
from tkinter import ttk

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


class TrainingWindow(tk.Toplevel):
    def __init__(self, master, config=None):
        super().__init__(master)
        self.config = config or {}
        
        self.title(get_text("TITLE_TRAINING_WINDOW"))
        self.geometry("700x500")
        self.minsize(600, 400)
        self.configure(bg="#16181d")
        self.transient(master)
        self.grab_set()
        
        self.bg_main = "#16181d"
        self.bg_card = "#252a33"
        self.text_main = "#f5f7fa"
        self.text_sub = "#aeb6c2"
        self.border = "#2d3440"
        
        self._build_ui()
    
    def _build_ui(self):
        container = tk.Frame(self, bg=self.bg_main)
        container.pack(fill="both", expand=True, padx=14, pady=14)
        
        # 标题
        tk.Label(container, text=get_text("TITLE_TRAINING_WINDOW"), bg=self.bg_main, fg=self.text_main, font=("Microsoft YaHei", 14, "bold")).pack(anchor="w", pady=(0, 10))
        
        # 状态占位
        self.status_label = tk.Label(container, text=get_text("LABEL_STATUS"), bg=self.bg_main, fg=self.text_sub, font=("Microsoft YaHei", 10))
        self.status_label.pack(anchor="w", pady=4)
        
        # Epoch 占位
        self.epoch_label = tk.Label(container, text=get_text("LABEL_CURRENT_EPOCH"), bg=self.bg_main, fg=self.text_sub, font=("Microsoft YaHei", 10))
        self.epoch_label.pack(anchor="w", pady=4)
        
        # Loss 占位
        self.loss_label = tk.Label(container, text=get_text("LABEL_CURRENT_LOSS"), bg=self.bg_main, fg=self.text_sub, font=("Microsoft YaHei", 10))
        self.loss_label.pack(anchor="w", pady=4)
        
        # best.pt 路径占位
        self.best_pt_label = tk.Label(container, text=get_text("LABEL_BEST_MODEL"), bg=self.bg_main, fg=self.text_sub, font=("Microsoft YaHei", 10))
        self.best_pt_label.pack(anchor="w", pady=4)
        
        # 日志区域
        log_frame = tk.Frame(container, bg=self.bg_card, highlightthickness=1, highlightbackground=self.border)
        log_frame.pack(fill="both", expand=True, pady=(10, 10))
        
        tk.Label(log_frame, text=get_text("LABEL_TRAINING_LOGS"), bg=self.bg_card, fg=self.text_main, font=("Microsoft YaHei", 10, "bold")).pack(anchor="w", padx=10, pady=(8, 4))
        
        text_frame = tk.Frame(log_frame, bg=self.bg_card)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.log_text = tk.Text(text_frame, bg="#1b2028", fg=self.text_sub, relief="flat", font=("Consolas", 9), wrap="word")
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.log_text.yview, bg=self.bg_card)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        self.log_text.insert("1.0", "[日志占位] 训练日志将在后续版本显示...\n")
        self.log_text.config(state="disabled")
        
        # 关闭按钮
        tk.Button(container, text=get_text("BTN_CLOSE"), bg="#3a6df0", fg="white", relief="flat", activebackground="#4b7cff", activeforeground="white", command=self.destroy).pack(anchor="e")
