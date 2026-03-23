from pathlib import Path

path = Path(r"C:\Ai\ui\main_window.py")
text = path.read_text(encoding="utf-8")

# 1) 补 import
import_line = "from core.dataset_exporter import export_dataset"
if import_line not in text:
    anchor = "from core.yolo_infer import infer_image"
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + import_line)
    else:
        raise SystemExit("没有找到 yolo_infer 导入锚点，停止修改。")

# 2) 补 export_dataset_action 方法
method_code = '''
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

'''
if "def export_dataset_action(self):" not in text:
    anchor = "    def prev_image(self):"
    if anchor in text:
        text = text.replace(anchor, method_code + anchor)
    else:
        raise SystemExit("没有找到 prev_image 锚点，停止修改。")

# 3) 补按钮
button_line = '        self._create_side_button(action_card, "导出数据集", self.export_dataset_action).pack(fill="x", padx=12, pady=4)'
if button_line not in text:
    anchor = '        self._create_side_button(action_card, "保存标签", self.save_current_labels).pack(fill="x", padx=12, pady=(4, 12))'
    replacement = '''        self._create_side_button(action_card, "保存标签", self.save_current_labels).pack(fill="x", padx=12, pady=4)
        self._create_side_button(action_card, "导出数据集", self.export_dataset_action).pack(fill="x", padx=12, pady=(4, 12))'''
    if anchor in text:
        text = text.replace(anchor, replacement)
    else:
        raise SystemExit("没有找到 保存标签 按钮锚点，停止修改。")

path.write_text(text, encoding="utf-8")
print("main_window.py 已稳定补上：导出数据集 import / 方法 / 按钮")
