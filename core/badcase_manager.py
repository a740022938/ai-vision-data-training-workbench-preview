import os
import shutil
from datetime import datetime


def mark_bad_case(image_path, label_path, bad_cases_dir):
    if not bad_cases_dir:
        return False, "bad_cases_dir 未设置"

    images_dir = os.path.join(bad_cases_dir, "images")
    labels_dir = os.path.join(bad_cases_dir, "labels")
    logs_dir = os.path.join(bad_cases_dir, "logs")

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    if not image_path or not os.path.exists(image_path):
        return False, "图片不存在"

    image_name = os.path.basename(image_path)
    target_image = os.path.join(images_dir, image_name)
    shutil.copy2(image_path, target_image)

    label_name = ""
    if label_path and os.path.exists(label_path):
        label_name = os.path.basename(label_path)
        target_label = os.path.join(labels_dir, label_name)
        shutil.copy2(label_path, target_label)

    log_path = os.path.join(logs_dir, "bad_cases_log.txt")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{now}] image={image_name} label={label_name or 'NONE'} reason=manual_mark\n")

    return True, f"已归档到 {bad_cases_dir}"
