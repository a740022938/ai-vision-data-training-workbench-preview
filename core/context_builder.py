import os


def build_context(main_window):
    image_name = getattr(main_window, "current_image_name", "")
    image_dir = getattr(main_window, "image_dir", "")
    image_path = os.path.join(image_dir, image_name) if image_name else ""

    return {
        "image_name": image_name,
        "image_path": image_path,
        "image_dir": image_dir,
        "label_dir": getattr(main_window, "label_dir", ""),
        "boxes": getattr(main_window, "boxes", []),
        "selected_idx": getattr(main_window, "selected_idx", None),
        "config": getattr(main_window, "config_data", {}),
        "class_names": getattr(main_window, "CLASS_NAMES", None),
    }
