# Preview Releases Overview
# 预览版发布总览

This document consolidates and clarifies the two public preview releases of this repository.
本文档用于统一整理并澄清本仓库当前两个公开预览版的定位与差异。

---

## Project Positioning / 项目定位

**AI Vision Data and Training Workbench Preview** is a **local-first desktop preview project**.
It is currently aimed at:

- UI structure demonstration
- local path and workflow organization
- early inference and training workflow presentation
- OpenClaw-assisted direction preview
- iterative evaluation before a more complete stable version

**AI Vision Data and Training Workbench Preview** 当前是一个 **本地优先的桌面预览项目**。
当前主要面向：

- 界面结构展示
- 本地路径与工作流组织
- 早期推理与训练工作流展示
- OpenClaw 协同方向预览
- 在更完整稳定版之前进行迭代评估

> Note / 说明：
> The current codebase uses a **Tkinter-based desktop GUI** in `main.py`, and the current `requirements.txt` is intentionally lightweight.
> 当前代码基于 `main.py` 中的 **Tkinter 桌面 GUI**，且当前 `requirements.txt` 保持轻量化。

---

## Release Summary / 版本概览

| Version | Date | Positioning | Main Focus |
|---|---|---|---|
| `v0.1.0-preview` | 2026-03-23 | first public preview | workflow direction and feature foundation |
| `v0.2.0-preview` | 2026-03-24 | display-enhanced preview | bilingual presentation, screenshots, onboarding clarity |

| 版本 | 日期 | 定位 | 重点 |
|---|---|---|---|
| `v0.1.0-preview` | 2026-03-23 | 首个公开预览版 | 工作流方向与功能地基 |
| `v0.2.0-preview` | 2026-03-24 | 展示增强版预览 | 双语展示、截图说明、上手清晰度 |

---

## v0.1.0-preview

### English

The first public preview established the project's early desktop-workbench direction.
Its emphasis was not visual polish, but proving that the repository already had a meaningful structure for local data work and future workflow expansion.

**Highlights**
- OpenClaw-assisted workflow direction
- duplicate image cache and restore
- batch rename for images and paired labels
- workspace backup and restore
- bilingual UI foundation
- inference settings page
- training settings page
- training entry and monitor scaffold
- startup error logging

**Status**
This version is best understood as a capability-foundation preview.
It shows the project's intended operating model, but it is not yet a complete production workflow.

### 中文

首个公开预览版主要用于建立这个项目的早期桌面工作台方向。
它的重点不是界面包装，而是证明仓库已经具备本地数据处理与后续工作流扩展的基础结构。

**亮点**
- OpenClaw 协同工作流方向
- 重复图片缓存与恢复
- 图片及配对标签批量重命名
- 工作区备份与恢复
- 双语界面基础
- 推理设置页
- 训练设置页
- 训练入口与监控界面骨架
- 启动错误日志

**当前判断**
这个版本更适合被理解为“能力地基预览版”。
它已经展示了项目未来要怎么运作，但还不是完整生产级工作流。

---

## v0.2.0-preview

### English

The second public preview focuses on presentation clarity and first-time user understanding.
Compared with `v0.1.0-preview`, it improves how the project is explained and evaluated, especially for users arriving through the repository or release page for the first time.

**Highlights**
- clearer bilingual release structure
- UI preview screenshots
- clearer path configuration presentation
- improved inference, training, and language settings explanation
- more readable quick-start guidance
- more realistic preview-stage framing without overstating unfinished features

**Status**
This version is best understood as a display-enhanced preview.
It is more polished for public viewing, sharing, and evaluation, while still honestly remaining in preview scope.

### 中文

第二个公开预览版更偏向“展示清晰度”和“首次访问用户理解成本”的优化。
相较于 `v0.1.0-preview`，它更强调项目是如何被解释、被展示、被评估的，尤其适合第一次从仓库页或发布页进入项目的人。

**亮点**
- 更清晰的双语发布结构
- 补充 UI 预览截图
- 更清楚的路径配置展示
- 更好的推理设置 训练设置 语言设置说明
- 更易理解的快速开始引导
- 更真实地保持预览版定位 不夸大未完成能力

**当前判断**
这个版本更适合被理解为“展示增强版预览”。
它更适合公开展示 分享和评估，同时依然诚实地保持在预览版范围内。

---

## What Actually Changed Between v0.1.0 and v0.2.0
## v0.1.0 与 v0.2.0 到底变化了什么

### English

From `v0.1.0-preview` to `v0.2.0-preview`, the biggest change is **how the project is communicated**, not a full jump in backend maturity.

In plain words:
- `v0.1.0-preview` proved the project had real structure
- `v0.2.0-preview` made that structure easier to understand
- the repository became more presentation-ready for public sharing
- the preview remained honest about what is and is not implemented yet

### 中文

从 `v0.1.0-preview` 到 `v0.2.0-preview`，最大的变化是 **项目表达方式更清楚了**，而不是底层成熟度一下子跨越到正式版。

直白一点说：
- `v0.1.0-preview` 证明这个项目已经不是空壳
- `v0.2.0-preview` 让别人更容易看懂这个项目
- 仓库整体更适合公开展示和分享
- 同时仍然保持了对“已实现”和“未实现”的诚实边界

---

## Recommended Release Description Style Going Forward
## 后续发布文案建议风格

### English

For future preview releases, keep this structure:
1. one-sentence project positioning
2. what changed in this version
3. what users can try now
4. what is intentionally not complete yet
5. what comes next

### 中文

后续预览版建议固定采用这个顺序：
1. 一句话说明项目定位
2. 这一版具体更新了什么
3. 用户现在能体验什么
4. 当前刻意还没做完什么
5. 下一步会做什么

---

## Suggested Short Release Taglines
## 推荐短标题文案

### For v0.1.0-preview
- First public preview focused on workflow foundation
- 首个公开预览版 聚焦工作流地基

### For v0.2.0-preview
- Display-enhanced preview with clearer bilingual onboarding
- 展示增强版预览 双语说明与上手引导更清晰

---

## Repository Guidance
## 仓库建议

If this repository continues evolving publicly, the next documentation upgrades worth adding are:

- `CHANGELOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/ROADMAP.md`
- release-page text templates for each version

如果这个仓库继续对外迭代，下一步很值得补的文档有：

- `CHANGELOG.md`
- `docs/KNOWN_LIMITATIONS.md`
- `docs/ROADMAP.md`
- 每个版本的发布页文案模板
