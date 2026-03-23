from pathlib import Path

path = Path(r"C:\Ai\ui\main_window.py")
text = path.read_text(encoding="utf-8")

# 1) 删除重复的 selected_card 区块（保留第一块，删第二块）
dup_block = '''
        selected_card = tk.Frame(right_card, bg=self.bg_card_2)
        selected_card.pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(
            selected_card,
            text="当前选中框",
            bg=self.bg_card_2,
            fg=self.text_main,
            font=("Microsoft YaHei", 10, "bold")
        ).pack(anchor="w", padx=12, pady=(10, 8))

        self.selected_box_title = tk.Label(
            selected_card,
            text="当前未选中任何框",
            bg=self.bg_card_2,
            fg=self.text_sub,
            font=("Microsoft YaHei", 9)
        )
        self.selected_box_title.pack(anchor="w", padx=12, pady=(0, 8))

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
                fg=self.text_main,
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
            text="应用微调",
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
            text="打开编辑窗口",
            bg=self.btn_bg,
            fg=self.text_main,
            relief="flat",
            activebackground=self.btn_hover,
            activeforeground=self.text_main,
            command=self.open_edit_window
        )
        self.open_edit_btn.pack(side="left", padx=6)

        self.delete_info_btn = tk.Button(
            info_btn_bar,
            text="删除当前框",
            bg="#7a2e2e",
            fg="white",
            relief="flat",
            activebackground="#914141",
            activeforeground="white",
            command=self.delete_selected_box
        )
        self.delete_info_btn.pack(side="left")
'''

# 如果出现两次，只保留一次
first = text.find(dup_block)
if first != -1:
    second = text.find(dup_block, first + len(dup_block))
    if second != -1:
        text = text[:second] + text[second + len(dup_block):]

# 2) 顶部按钮栏加入 导出数据集（如果还没有）
anchor = '        self._create_top_button(btn_wrap, "设置", self.show_settings_tip).pack(side="left", padx=5, pady=12)'
insert = '        self._create_top_button(btn_wrap, "导出数据集", self.export_dataset_action).pack(side="left", padx=5, pady=12)\n'
if 'self._create_top_button(btn_wrap, "导出数据集", self.export_dataset_action)' not in text:
    text = text.replace(anchor, insert + anchor)

# 3) 右侧快捷操作区如果有“导出数据集”按钮，删掉，避免重复
right_btn = '        self._create_side_button(action_card, "导出数据集", self.export_dataset_action).pack(fill="x", padx=12, pady=(4, 12))\n'
text = text.replace(right_btn, '')
right_btn2 = '        self._create_side_button(action_card, "导出数据集", self.export_dataset_action).pack(fill="x", padx=12, pady=4)\n'
text = text.replace(right_btn2, '')

path.write_text(text, encoding="utf-8")
print("已修复：删除重复选中框卡片，并把导出数据集按钮移到顶部。")
