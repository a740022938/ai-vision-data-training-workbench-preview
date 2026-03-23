import tkinter as tk


class RightPanel:
    """
    右侧面板壳子
    后续用于承接信息区 选中框编辑区 按钮区等逻辑
    """

    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg="#2B2D31")

        self.placeholder = tk.Label(
            self.frame,
            text="RightPanel 模块占位",
            bg="#2B2D31",
            fg="#F1F3F4"
        )
        self.placeholder.pack(padx=8, pady=8)

    def get_frame(self):
        return self.frame
