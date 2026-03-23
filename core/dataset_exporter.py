import os
import shutil


def export_dataset(image_dir, label_dir, output_dir, class_names):
    if not image_dir or not os.path.isdir(image_dir):
        return False, f"image_dir not found: {image_dir}"

    if not label_dir or not os.path.isdir(label_dir):
        return False, f"label_dir not found: {label_dir}"

    if not output_dir:
        return False, "output_dir is empty"

    images_out = os.path.join(output_dir, "images")
    labels_out = os.path.join(output_dir, "labels")

    os.makedirs(images_out, exist_ok=True)
    os.makedirs(labels_out, exist_ok=True)

    count = 0
    valid_ext = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

    for file in os.listdir(image_dir):
        if not file.lower().endswith(valid_ext):
            continue

        img_path = os.path.join(image_dir, file)
        label_name = os.path.splitext(file)[0] + ".txt"
        label_path = os.path.join(label_dir, label_name)

        if os.path.exists(label_path):
            shutil.copy2(img_path, os.path.join(images_out, file))
            shutil.copy2(label_path, os.path.join(labels_out, label_name))
            count += 1

    yaml_path = os.path.join(output_dir, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write(f"path: {output_dir}\n")
        f.write("train: images\n")
        f.write("val: images\n\n")
        f.write("names:\n")
        for i, name in enumerate(class_names):
            f.write(f"  {i}: {name}\n")

    return True, f"export done, total {count}"