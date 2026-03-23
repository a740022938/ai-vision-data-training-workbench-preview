import tkinter as tk


class CanvasPanel:
    """
    画布容器模块
    当前阶段只负责：
    1 画布外层 frame
    2 返回画布主体区域 body

    后续再继续接：
    图像显示
    缩放
    框选
    坐标换算
    """

    def __init__(self, parent, app=None):
        self.parent = parent
        self.app = app

        self.frame = tk.Frame(parent, bg="#111318")
        self.body = self.frame

    def get_frame(self):
        return self.frame

    def get_body(self):
        return self.body
