import tkinter as tk
import os
import sys
import traceback
from datetime import datetime
from tkinter import messagebox

from config.texts.zh_cn import APP_TITLE
from ui.main_window import MainWindow


def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    log_path = r"C:\AI_Workbench\logs\startup_error.log"
    try:
        main()
    except Exception as e:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        error_info = f"[{datetime.now()}]\n"
        error_info += f"Exception Type: {type(e).__name__}\n"
        error_info += f"Exception Message: {e}\n"
        error_info += f"Traceback:\n{traceback.format_exc()}"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(error_info)
        print("=" * 50)
        print("启动失败！")
        print(error_info)
        print("=" * 50)
        try:
            messagebox.showerror(
                "启动失败",
                f"程序启动时发生错误。\n\n日志已保存到:\n{log_path}"
            )
        except:
            pass
        sys.exit(1)
