from pathlib import Path

path = Path(r"C:\Ai\ui\main_window.py")
text = path.read_text(encoding="utf-8")

# 1) 补 import
import_line = "from core.openclaw_bridge import analyze_with_openclaw"
if import_line not in text:
    anchor = "from core.dataset_exporter import export_dataset"
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + import_line)
    else:
        raise SystemExit("没有找到 dataset_exporter 导入锚点，停止修改。")

# 2) 顶部加按钮
button_line = '        self._create_top_button(btn_wrap, "AI分析", self.run_openclaw_analysis).pack(side="left", padx=5, pady=12)'
if button_line not in text:
    anchor = '        self._create_top_button(btn_wrap, "设置", self.show_settings_tip).pack(side="left", padx=5, pady=12)'
    if anchor in text:
        text = text.replace(anchor, button_line + "\n" + anchor)
    else:
        raise SystemExit("没有找到顶部 设置 按钮锚点，停止修改。")

# 3) 增加方法
if "def run_openclaw_analysis(self):" not in text:
    method_code = '''
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

'''
    anchor = "    def open_project(self):"
    if anchor in text:
        text = text.replace(anchor, method_code + anchor)
    else:
        raise SystemExit("没有找到 open_project 方法锚点，停止修改。")

path.write_text(text, encoding="utf-8")
print("main_window.py 已接入 AI分析 按钮和 OpenClaw 调用")
