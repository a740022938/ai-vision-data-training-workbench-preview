import json
import os
from copy import deepcopy

# 获取项目根目录：C:\Ai
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")

DEFAULT_CONFIG = {
    "paths": {
        "image_dir": "",
        "label_dir": "",
        "bad_cases_dir": "",
        "model_path": "",
        "video_dir": "",
        "output_dataset_dir": ""
    },
    "model": {
        "conf": 0.25,
        "iou": 0.5,
        "imgsz": 640
    },
    "behavior": {
        "auto_save": True,
        "auto_save_on_navigate": True
    },
    "display": {
        "show_conf": True,
        "show_label": True
    }
}


def _merge_dict(default_dict, user_dict):
    """递归合并配置，确保缺失字段自动补齐"""
    result = deepcopy(default_dict)
    for key, value in user_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def save_config(config: dict) -> bool:
    """保存配置到 config.json"""
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8-sig") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[config_manager] 配置保存失败: {e}")
        return False


def load_config() -> dict:
    """读取配置；如果不存在或损坏，则自动恢复默认配置"""
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
        return deepcopy(DEFAULT_CONFIG)

    try:
        with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
            user_config = json.load(f)
        merged_config = _merge_dict(DEFAULT_CONFIG, user_config)
        return merged_config
    except Exception as e:
        print(f"[config_manager] 配置读取失败，已使用默认配置: {e}")
        save_config(DEFAULT_CONFIG)
        return deepcopy(DEFAULT_CONFIG)


def validate_config(config: dict) -> list:
    """校验配置，返回错误列表；为空表示通过"""
    errors = []

    paths = config.get("paths", {})
    model = config.get("model", {})

    for key in ["image_dir", "label_dir", "bad_cases_dir"]:
        value = paths.get(key, "")
        if value and not os.path.isdir(value):
            errors.append(f"目录不存在: {key} -> {value}")

    model_path = paths.get("model_path", "")
    if model_path and not os.path.isfile(model_path):
        errors.append(f"模型文件不存在: model_path -> {model_path}")

    conf = model.get("conf", 0.25)
    iou = model.get("iou", 0.5)
    imgsz = model.get("imgsz", 640)

    if not (0 <= conf <= 1):
        errors.append("model.conf 必须在 0 到 1 之间")

    if not (0 <= iou <= 1):
        errors.append("model.iou 必须在 0 到 1 之间")

    if not isinstance(imgsz, int) or imgsz <= 0:
        errors.append("model.imgsz 必须是大于 0 的整数")

    return errors


def get_path(key: str) -> str:
    """快捷获取 paths 里的某个路径"""
    config = load_config()
    return config.get("paths", {}).get(key, "")


def set_path(key: str, value: str) -> bool:
    """快捷设置 paths 里的某个路径"""
    config = load_config()
    if "paths" not in config:
        config["paths"] = {}
    config["paths"][key] = value
    return save_config(config)


def get_section(section_name: str) -> dict:
    """获取某个配置分组，比如 model / behavior / display"""
    config = load_config()
    return config.get(section_name, {})


if __name__ == "__main__":
    cfg = load_config()
    print("当前配置：")
    print(json.dumps(cfg, indent=4, ensure_ascii=False))

    errs = validate_config(cfg)
    if errs:
        print("\n检测到以下问题：")
        for err in errs:
            print("-", err)
    else:
        print("\n配置校验通过。")