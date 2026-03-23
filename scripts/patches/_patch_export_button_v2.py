from pathlib import Path
import re

path = Path(r"C:\Ai\ui\main_window.py")
text = path.read_text(encoding="utf-8")

print("=== 修改前检查 ===")
print("has import export_dataset:", "from core.dataset_exporter import export_dataset" in text)
print("has method export_dataset_action:", "def export_dataset_action(self):" in text)
print("has button 导出数据集:", '"导出数据集"' in text)

# 1) 导入
import_line = "from core.dataset_exporter import export_dataset"
if import_line not in text:
    anchor = "from core.yolo_infer import infer_image"
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + import_line)
    else:
        raise SystemExit("没有找到导入锚点：from core.yolo_infer import infer_image")

# 2) 方法
if "def export_dataset_action(self):" not in text:
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
    anchor = "    def prev_image(self):"
    if anchor in text:
        text = text.replace(anchor, method_code + anchor)
    else:
        raise SystemExit("没有找到方法锚点：def prev_image(self)")

# 3) 按钮
button_line = '        self._create_side_button(action_card, "导出数据集", self.export_dataset_action).pack(fill="x", padx=12, pady=(4, 12))'
if '"导出数据集"' not in text:
    # 用正则匹配“保存标签”那一行，更稳
    pattern = r'(\s*self\._create_side_button\(action_card,\s*"保存标签",\s*self\.save_current_labels\)\.pack\(fill="x",\s*padx=12,\s*pady=\([^\)]*\)\))'
    m = re.search(pattern, text)
    if not m:
        raise SystemExit("没有找到“保存标签”按钮锚点")
    save_line = m.group(1)
    replacement = save_line + '\n        self._create_side_button(action_card, "导出数据集", self.export_dataset_action).pack(fill="x", padx=12, pady=(4, 12))'
    text = text.replace(save_line, replacement, 1)

path.write_text(text, encoding="utf-8")

print("=== 修改后检查 ===")
print("has import export_dataset:", "from core.dataset_exporter import export_dataset" in text)
print("has method export_dataset_action:", "def export_dataset_action(self):" in text)
print("has button 导出数据集:", '"导出数据集"' in text)
print("补丁完成")
