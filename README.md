# AI Vision Data and Training Workbench Preview v0.2.0

**Display-Enhanced Preview | 展示增强版预览**

Integrated with an OpenClaw-assisted workflow.  
已接入 OpenClaw 协同工作流。

---

## Quick Preview

This is a local-first visual data workbench preview. Download, extract, and run to explore the complete UI and available settings.

这是一个本地优先的视觉数据工作台预览版。下载、解压、运行，即可探索完整 UI 和可用设置。

---

## Main Interface | 主界面

![Main UI](assets/screenshots/01_main_ui.png)

---

## Settings Pages | 设置页面

### Path Settings | 路径设置
Configure dataset paths, model paths, and output directories.

配置数据集路径、模型路径和输出目录。

![Path Settings](assets/screenshots/02_path_settings.png)

### Inference Settings | 推理设置
Set confidence threshold, IoU threshold, and device selection.

设置置信度阈值、IoU 阈值和设备选择。

![Inference Settings](assets/screenshots/03_inference_settings.png)

### Training Settings | 训练设置
Configure training epochs, batch size, learning rate, and model selection.

配置训练轮数、批次大小、学习率和模型选择。

![Training Settings](assets/screenshots/04_training_settings.png)

### Language Settings | 语言设置
Switch between English and Chinese interface.

在英文和中文界面之间切换。

![Language Settings](assets/screenshots/05_language_settings.png)

---

## Current Highlights | 当前亮点

**English:**
- Local-first UI preview – run immediately after extraction
- Configurable project paths for datasets and models
- YOLO26 model path integration (preparation for training)
- Inference settings page (confidence, IoU, device)
- Training settings page (epochs, batch size, learning rate)
- Language settings (English / 中文)
- OpenClaw-assisted workflow direction – designed for AI collaboration

**中文：**
- 本地优先 UI 预览 – 解压即可运行
- 可配置的数据集和模型项目路径
- YOLO26 模型路径接入（为训练做准备）
- 推理设置页（置信度、IoU、设备）
- 训练设置页（轮数、批次、学习率）
- 语言设置（English / 中文）
- OpenClaw 协同工作流方向 – 为 AI 协作设计

---

## Quick Start | 快速开始

### For Most Users | 普通用户

1. Download the attached ZIP package from the [Releases](https://github.com/a740022938/ai-vision-data-training-workbench-preview/releases) page
2. Extract to a local folder (no installation required)
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python main.py`
5. Explore the UI and settings

1. 从 [Releases](https://github.com/a740022938/ai-vision-data-training-workbench-preview/releases) 页面下载 ZIP 包
2. 解压到本地文件夹（无需安装）
3. 安装依赖：`pip install -r requirements.txt`
4. 运行：`python main.py`
5. 探索界面和设置

### For Advanced Users | 高级用户

- Configure paths in the Path Settings tab before importing datasets
- Set your YOLO26 model path in Inference/Training settings
- Modify `config.json` for custom configurations
- Check `config.json.example` for all available options

- 导入数据集前先在路径设置页配置路径
- 在推理/训练设置中设置 YOLO26 模型路径
- 修改 `config.json` 进行自定义配置
- 参考 `config.json.example` 了解所有可用选项

---

## Recommended Environment | 推荐环境

- **OS**: Windows 10 / Windows 11
- **Python**: 3.10
- **Environment Manager**: Conda / Miniconda (recommended: env name `yolo`)
- **Dependencies**: 
  - PyQt5
  - Ultralytics YOLO26 (auto-download on first run)
  - OpenCV (cv2)

---

## Not Fully Included Yet | 暂未完全开放

**English:**
This is a preview release. The following features are planned but not yet fully implemented:
- Real training execution pipeline (training entry and monitor UI exist, execution in progress)
- Dynamic training curves visualization
- GPU monitoring and multi-GPU support
- Deeper OpenClaw automation workflows
- Complete plugin system architecture
- Some windows and dialogs are still being polished

**中文：**
这是预览版。以下功能已规划但尚未完全实现：
- 真实训练执行链路（训练入口和监控 UI 已存在，执行功能开发中）
- 动态训练曲线可视化
- GPU 监控和多 GPU 支持
- 更深层 OpenClaw 自动化工作流
- 完整插件系统架构
- 部分窗口和对话框仍在打磨

---

## Next Steps | 下一步路线

1. **Stabilize editor workflow** – improve dataset import and annotation experience
2. **Improve training integration** – connect settings UI to actual training execution
3. **Improve bilingual consistency** – refine all UI text and documentation
4. **Refine plugin boundaries** – clarify what can be extended vs. core functionality

1. **稳定编辑工作流** – 改进数据集导入和标注体验
2. **完善训练集成** – 将设置 UI 连接到实际训练执行
3. **提升双语一致性** – 优化所有界面文本和文档
4. **明确插件边界** – 厘清可扩展部分与核心功能

---

## About This Preview | 关于本预览版

This v0.2.0-preview is focused on **display enhancement** – making sure users can see the complete UI and understand the direction of the project. It is not a full-featured release, but a demonstration of where we're heading.

本次 v0.2.0-preview 重点在于**展示增强** – 确保用户能看到完整 UI 并理解项目方向。这不是全功能正式版，而是展示我们前进方向的演示版。

For questions or feedback, open an issue or discuss in the repository.

如有问题或反馈，请在仓库中提交 Issue 或讨论。

---

**Version**: v0.2.0-preview  
**Release Date**: 2026-03-24  
**Status**: Display-Enhanced Preview
