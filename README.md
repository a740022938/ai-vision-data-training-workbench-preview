# AI Vision Data and Training Workbench Preview v0.2.0
# AI视觉数据与训练工作台 预览版 v0.2.0

A local-first visual data and training workbench preview focused on UI demonstration, structured settings, and YOLO26-based workflow presentation.
一个本地优先的视觉数据与训练工作台预览版，当前重点展示界面结构、设置体系，以及基于 YOLO26 的工作流能力。

This release is a display-enhanced preview version. It is designed to make the project easier to understand, easier to run, and easier to evaluate for users who want to try the UI and the current workflow direction.
本次发布属于展示增强版预览，不是全功能正式版。目标是让用户更容易理解项目、更容易运行界面，并更清楚地看到当前版本的整体方向。

---

## What's New in v0.2.0-preview / 更新重点

- Improved release presentation with clearer bilingual structure
- Added UI preview screenshots for the current workbench interface
- Refined project path configuration presentation
- Added clearer inference, training, and language settings preview
- Improved readability for first-time users
- Continued to keep the project in a realistic preview-stage scope

- 优化了发布页展示结构，采用更清晰的中英文双语说明
- 增加了当前工作台界面的 UI 截图展示
- 优化了项目路径配置展示方式
- 补充了推理设置、训练设置、语言设置的界面预览
- 提升了首次访问用户对项目的理解和可用性感知
- 保持项目仍处于真实的预览阶段，不夸大未完成能力

---

## UI Preview / 界面预览

### 01 - Main UI / 主界面
![Main UI](assets/screenshots/01_main_ui.png)
Current running UI preview with YOLO26-based inference display integrated into the workbench interface.
当前运行中的主界面预览，已展示基于 YOLO26 的推理结果接入工作台界面。

### 02 - Path Settings / 路径设置
![Path Settings](assets/screenshots/02_path_settings.png)
Configurable image, label, model, dataset output, and bad cases paths for local workflow organization.
支持本地图片、标签、模型、输出数据集和 bad_cases 路径配置，便于管理本地工作流。

### 03 - Inference Settings / 推理设置
![Inference Settings](assets/screenshots/03_inference_settings.png)
Inference-related settings preview for local model-based workflow expansion.
推理相关设置页预览，用于展示本地模型工作流扩展方向。

### 04 - Training Settings / 训练设置
![Training Settings](assets/screenshots/04_training_settings.png)
Training-oriented settings page preview for future workflow expansion.
训练相关设置页预览，为后续训练工作流扩展预留入口。

### 05 - Language Settings / 语言设置
![Language Settings](assets/screenshots/05_language_settings.png)
Language configuration page preview showing the bilingual direction of the project.
语言设置页预览，展示项目的双语界面方向。

---

## Current Highlights / 当前亮点

- Local-first UI workbench preview
- Configurable local project paths
- YOLO26 model path integration preview
- Inference settings page
- Training settings page
- Language settings page
- OpenClaw-assisted workflow direction
- Structured UI presentation for early evaluation

- 本地优先的工作台界面预览
- 可配置的本地项目路径
- YOLO26 模型路径接入展示
- 推理设置页
- 训练设置页
- 语言设置页
- 预留 OpenClaw 协同工作流方向
- 已具备早期评估所需的结构化界面展示能力

---

## Quick Start / 快速开始

> **Recommended for most users:** download the preview zip package and start with the packaged UI first. Manual setup is mainly for advanced users who want to reproduce the environment or modify the workflow.
>
> **建议大多数用户优先下载预览版 zip 压缩包并直接体验打包好的 UI。**手动安装方式主要面向希望复现环境或自行修改工作流的进阶用户。

---

### Route A: For most users / 路线 A：普通用户

**Quick steps:**

1. Download the preview zip package.
2. Extract it to a local folder.
3. Run the launcher or start the packaged UI.
4. Open Settings and confirm your local paths.
5. Load an image and preview the current workflow.

**快速步骤：**

1. 下载预览版 zip 压缩包。
2. 解压到本地目录。
3. 运行启动器或直接打开打包好的 UI。
4. 打开设置页并确认本地路径。
5. 加载图片并预览当前工作流。

---

### Route B: For advanced users / 路线 B：进阶用户

**Prerequisites:** Python 3.10, Conda or Miniconda

**Step-by-step:**

1. Prepare Python and Conda or Miniconda.
2. Create and activate a Python environment.
3. Install Ultralytics for YOLO26 support.
4. Install project dependencies (including GUI libraries).
5. Run the project manually.

**前置条件：** Python 3.10、Conda 或 Miniconda

**分步安装：**

1. 准备 Python 与 Conda 或 Miniconda。
2. 创建并激活 Python 虚拟环境。
3. 安装 Ultralytics 以支持 YOLO26。
4. 安装项目依赖（包含 GUI 库）。
5. 手动运行项目。

**Example commands / 命令示例：**

```bash
# Create and activate environment / 创建并激活环境
conda create -n ai_workbench python=3.10 -y
conda activate ai_workbench

# Upgrade pip / 升级 pip
python -m pip install --upgrade pip

# Install YOLO26 support / 安装 YOLO26 支持
pip install ultralytics

# Install dependencies / 安装依赖
pip install -r requirements.txt

# Note: If you encounter GUI display issues, you may need to install Tkinter separately.
# 注意：如果遇到 GUI 显示问题，可能需要单独安装 Tkinter。

# Run the project / 运行项目
python main.py
```

**GUI Dependency Note / GUI 依赖说明：**

This project currently uses a Tkinter-based desktop GUI.
Most standard Python installations already include Tkinter.
If your environment does not include it, please install the Tkinter component for your current Python distribution before running the UI.

本项目当前使用基于 Tkinter 的桌面 GUI。
大多数标准 Python 安装通常已自带 Tkinter。
如果你的环境缺少 Tkinter，请先为当前 Python 发行版补装对应的 Tkinter 组件，再运行图形界面。

---

## Recommended Environment / 推荐环境

- OS: Windows 10 / Windows 11
- Python: 3.10
- Conda / Miniconda (recommended env name: ai_workbench or yolo)
- Core Dependencies:
  - Ultralytics (for YOLO26)
  - OpenCV (image processing)
  - Tkinter (GUI framework, usually bundled with Python)

- 操作系统: Windows 10 / Windows 11
- Python: 3.10
- Conda / Miniconda（推荐环境名: ai_workbench 或 yolo）
- 核心依赖:
  - Ultralytics（用于 YOLO26）
  - OpenCV（图像处理）
  - Tkinter（GUI 框架，通常随 Python 捆绑）

---

## Not Fully Included Yet / 当前尚未完全开放

This is a preview release. The following features are planned but not yet fully implemented:
- Real training execution pipeline
- Dynamic training curves visualization
- GPU monitoring and multi-GPU support
- Deeper OpenClaw automation workflows
- Complete plugin system architecture
- Some windows and dialogs are still being polished

这是预览版。以下功能已规划但尚未完全实现：
- 真实训练执行链路
- 动态训练曲线可视化
- GPU 监控和多 GPU 支持
- 更深层 OpenClaw 自动化工作流
- 完整插件系统架构
- 部分窗口和对话框仍在打磨

---

## Next Steps / 下一步计划

1. Stabilize editor workflow
2. Improve training integration
3. Improve bilingual consistency
4. Refine plugin boundaries

1. 稳定编辑工作流
2. 完善训练集成
3. 提升双语一致性
4. 明确插件边界

---

## Download
## 下载

Download the attached preview package and start exploring.

下载附带的预览版压缩包，开始探索。

**Latest Release:** [v0.2.0-preview](https://github.com/a740022938/ai-vision-data-training-workbench-preview/releases/tag/v0.2.0-preview)
