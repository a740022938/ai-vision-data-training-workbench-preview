import tkinter as tk
from tkinter import messagebox, ttk


class EditBoxWindow(tk.Toplevel):
    def __init__(self, master, box_index, box_data, class_names, on_apply=None, on_delete=None):
        super().__init__(master)
        self.box_index = box_index
        self.box_data = box_data[:]   # [cls_id, cx, cy, w, h]
        self.class_names = class_names
        self.on_apply = on_apply
        self.on_delete = on_delete

        self.title(f"编辑标注框 #{box_index}")
        self.geometry("420x360")
        self.resizable(False, False)
        self.configure(bg="#1b1f26")
        self.transient(master)
        self.grab_set()

        self._build_ui()
        self.bind("<Return>", lambda e: self.apply_changes())
        self.bind("<Escape>", lambda e: self.destroy())

    def _build_ui(self):
        bg = "#1b1f26"
        card = "#252a33"
        text_main = "#f5f7fa"
        text_sub = "#aeb6c2"
        border = "#2d3440"

        container = tk.Frame(self, bg=bg)
        container.pack(fill="both", expand=True, padx=14, pady=14)

        tk.Label(
            container,
            text=f"📦 标注编辑器（框 #{self.box_index}）",
            bg=bg,
            fg=text_main,
            font=("Microsoft YaHei", 13, "bold")
        ).pack(anchor="w", pady=(0, 10))

        form = tk.Frame(container, bg=card, highlightthickness=1, highlightbackground=border)
        form.pack(fill="both", expand=True)

        self.class_var = tk.StringVar(value=self.class_names[self.box_data[0]])
        self.cx_var = tk.StringVar(value=f"{self.box_data[1]:.6f}")
        self.cy_var = tk.StringVar(value=f"{self.box_data[2]:.6f}")
        self.w_var = tk.StringVar(value=f"{self.box_data[3]:.6f}")
        self.h_var = tk.StringVar(value=f"{self.box_data[4]:.6f}")

        self._add_row(form, "类别", combo=True)
        self._add_row(form, "cx")
        self._add_row(form, "cy")
        self._add_row(form, "w")
        self._add_row(form, "h")

        btn_bar = tk.Frame(container, bg=bg)
        btn_bar.pack(fill="x", pady=(12, 0))

        tk.Button(
            btn_bar,
            text="取消",
            bg="#2a303a",
            fg=text_main,
            relief="flat",
            activebackground="#343b47",
            activeforeground=text_main,
            command=self.destroy
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            btn_bar,
            text="删除该框",
            bg="#7a2e2e",
            fg="white",
            relief="flat",
            activebackground="#914141",
            activeforeground="white",
            command=self.delete_box
        ).pack(side="right", padx=(8, 0))

        tk.Button(
            btn_bar,
            text="应用修改",
            bg="#3a6df0",
            fg="white",
            relief="flat",
            activebackground="#4b7cff",
            activeforeground="white",
            command=self.apply_changes
        ).pack(side="right")

    def _add_row(self, parent, field_name, combo=False):
        row = tk.Frame(parent, bg=parent["bg"])
        row.pack(fill="x", padx=14, pady=8)

        tk.Label(
            row,
            text=f"{field_name}",
            width=8,
            anchor="w",
            bg=parent["bg"],
            fg="#f5f7fa",
            font=("Microsoft YaHei", 10)
        ).pack(side="left")

        if combo:
            self.class_combo = ttk.Combobox(
                row,
                textvariable=self.class_var,
                values=self.class_names,
                state="readonly",
                width=22
            )
            self.class_combo.pack(side="left", fill="x", expand=True)
        else:
            var = getattr(self, f"{field_name}_var")
            entry = tk.Entry(
                row,
                textvariable=var,
                bg="#1b2028",
                fg="#f5f7fa",
                insertbackground="#f5f7fa",
                relief="flat",
                font=("Consolas", 11)
            )
            entry.pack(side="left", fill="x", expand=True, ipady=6)

    def _clamp(self, value, min_v=0.0, max_v=1.0):
        return max(min_v, min(max_v, value))

    def apply_changes(self):
        try:
            cls_name = self.class_var.get().strip()
            if cls_name not in self.class_names:
                raise ValueError("类别无效")

            cls_id = self.class_names.index(cls_name)
            cx = self._clamp(float(self.cx_var.get().strip()))
            cy = self._clamp(float(self.cy_var.get().strip()))
            w = self._clamp(float(self.w_var.get().strip()))
            h = self._clamp(float(self.h_var.get().strip()))

            if w < 0.01 or h < 0.01:
                raise ValueError("w 和 h 不能小于 0.01")

            new_box = [cls_id, cx, cy, w, h]

            if self.on_apply:
                self.on_apply(self.box_index, new_box)

            self.destroy()

        except Exception as e:
            messagebox.showerror("输入错误", f"请检查输入内容：\n{e}")

    def delete_box(self):
        if self.on_delete:
            self.on_delete(self.box_index)
        self.destroy()
