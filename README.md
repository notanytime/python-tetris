完全AI生成，只提出问题AI修改，下文也是

Completely AI-generated, only questions are modified by AI, the following text is the same

# 俄罗斯方块 / Tetris

基于 Python + Pygame 开发的经典俄罗斯方块游戏，拥有精美的画面效果和流畅的操作体验。

A classic Tetris game built with Python + Pygame, featuring polished visuals and smooth gameplay.

<img width="406" height="504" alt="屏幕截图 2026-05-19 213810" src="https://github.com/user-attachments/assets/9ffd7ab0-97f9-4a4c-9f64-ee6d89a9980b" />


## 游戏特性 / Features

- 7种标准方块（I/O/T/S/Z/J/L），支持SRS旋转踢墙系统
- 幽灵方块预览落点
- 下一个方块预览
- 消行动画（闪光 + 粒子爆炸）
- 硬降尾迹粒子 + 屏幕震动反馈
- 历史最高分记录（分数/等级/消行，自动保存到本地文件）
- 重开次数统计
- 防误触：双击 R 确认重开（2秒超时，带倒计时条）
- 中英文切换（Tab 键）
- 按键重复延迟（防止下键过快导致连续生成方块）
- 禁用中文输入法，确保按键响应正常

---

- 7 standard tetrominoes (I/O/T/S/Z/J/L) with SRS rotation & wall kick
- Ghost piece showing drop preview
- Next piece preview
- Line clear animation (flash + particle explosion)
- Hard drop trail particles + screen shake
- High score tracking (score/level/lines, auto-saved to local file)
- Restart counter
- Anti-mispress: double-tap R to confirm restart (2s timeout with progress bar)
- Chinese / English language toggle (Tab key)
- Key repeat delay to prevent rapid piece spawning
- Chinese IME disabled for reliable key input

## 操作方式 / Controls

| 按键 Key | 功能 Function                            |
|----------|-----------------------------------------|
| ← →      | 左右移动            Move left/right      |
| ↑        | 旋转                Rotate               |
| ↓        | 加速下落            Soft drop            |
| 空格 Space | 硬降              Hard drop            |
| P        | 暂停/继续           Pause/Resume         |
| R        | 重新开始（双击确认） Restart (double-tap) |
| Tab      | 切换中英文          Switch language      |

## 安装与运行 / Installation

```bash
# 安装依赖 Install dependencies
pip install pygame

# 运行游戏 Run the game
python tetris.py
```

## 环境要求 / Requirements

- Python 3.8+
- Pygame 2.0+
- Windows / macOS / Linux

## 文件说明 / Project Structure

```
├── tetris.py              # 游戏主程序 Main game
├── tetris_highscore.json  # 历史最高记录 High scores (auto-generated)
├── .gitignore             # Git 忽略配置
└── README.md              # 项目说明
```

## 许可证 / License

MIT License
