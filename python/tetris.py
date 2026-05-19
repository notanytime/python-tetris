import pygame
import random
import sys
import ctypes
import json
import os

# Windows 下禁用输入法，防止字母键被 IME 拦截
if sys.platform == 'win32':
    try:
        ctypes.windll.imm32.ImmDisableIME(-1)
    except Exception:
        pass

pygame.init()

# 游戏常量
CELL_SIZE = 32
COLS = 10
ROWS = 20
SIDEBAR_WIDTH = 220
SCREEN_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = ROWS * CELL_SIZE
FPS = 60
HIGHSCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tetris_highscore.json")

# 颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (40, 40, 45)
DARK_GRAY = (22, 22, 28)
DARK_BG = (15, 15, 20)
BORDER_COLOR = (60, 60, 70)
GRID_COLOR = (30, 30, 36)

# 方块颜色 (I, O, T, S, Z, J, L) - 更鲜艳的配色
COLORS = [
    (0, 220, 230),   # I - 青色
    (230, 220, 0),   # O - 黄色
    (180, 60, 220),  # T - 紫色
    (80, 220, 30),   # S - 绿色
    (230, 40, 40),   # Z - 红色
    (50, 80, 230),   # J - 蓝色
    (230, 140, 20),  # L - 橙色
]

# 方块形状定义
SHAPES = [
    [[(0, 1), (1, 1), (2, 1), (3, 1)],
     [(2, 0), (2, 1), (2, 2), (2, 3)],
     [(0, 2), (1, 2), (2, 2), (3, 2)],
     [(1, 0), (1, 1), (1, 2), (1, 3)]],
    [[(1, 0), (2, 0), (1, 1), (2, 1)],
     [(1, 0), (2, 0), (1, 1), (2, 1)],
     [(1, 0), (2, 0), (1, 1), (2, 1)],
     [(1, 0), (2, 0), (1, 1), (2, 1)]],
    [[(0, 1), (1, 1), (2, 1), (1, 0)],
     [(1, 0), (1, 1), (1, 2), (2, 1)],
     [(0, 1), (1, 1), (2, 1), (1, 2)],
     [(1, 0), (1, 1), (1, 2), (0, 1)]],
    [[(1, 0), (2, 0), (0, 1), (1, 1)],
     [(1, 0), (1, 1), (2, 1), (2, 2)],
     [(1, 1), (2, 1), (0, 2), (1, 2)],
     [(0, 0), (0, 1), (1, 1), (1, 2)]],
    [[(0, 0), (1, 0), (1, 1), (2, 1)],
     [(2, 0), (1, 1), (2, 1), (1, 2)],
     [(0, 1), (1, 1), (1, 2), (2, 2)],
     [(1, 0), (0, 1), (1, 1), (0, 2)]],
    [[(0, 0), (0, 1), (1, 1), (2, 1)],
     [(1, 0), (2, 0), (1, 1), (1, 2)],
     [(0, 1), (1, 1), (2, 1), (2, 2)],
     [(1, 0), (1, 1), (0, 2), (1, 2)]],
    [[(2, 0), (0, 1), (1, 1), (2, 1)],
     [(1, 0), (1, 1), (1, 2), (2, 2)],
     [(0, 1), (1, 1), (2, 1), (0, 2)],
     [(0, 0), (1, 0), (1, 1), (1, 2)]],
]

WALL_KICKS = {
    'default': [
        [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
        [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
        [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    ],
    'I': [
        [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)],
        [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)],
        [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)],
        [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)],
    ],
}

# 中英文文本
TEXTS = {
    'zh': {
        'title': '俄罗斯方块',
        'next': '下一个',
        'score': '分数',
        'level': '等级',
        'lines': '消行',
        'restarts': '重开',
        'best': '最高纪录',
        'controls': '操作',
        'ctrl_left_right': '移动',
        'ctrl_up': '旋转',
        'ctrl_down': '加速',
        'ctrl_space': '硬降',
        'ctrl_p': '暂停',
        'ctrl_r': '重来(双击)',
        'ctrl_tab': '中/英',
        'confirm_r': '再按一次R确认重开',
        'game_over': '游戏结束',
        'final_score': '最终得分',
        'press_r': '按 R 重新开始',
        'paused': '暂停',
        'press_p': '按 P 继续',
        'tetris': 'TETRIS!',
    },
    'en': {
        'title': 'TETRIS',
        'next': 'NEXT',
        'score': 'SCORE',
        'level': 'LEVEL',
        'lines': 'LINES',
        'restarts': 'RESETS',
        'best': 'BEST',
        'controls': 'CONTROLS',
        'ctrl_left_right': 'Move',
        'ctrl_up': 'Rotate',
        'ctrl_down': 'Soft Drop',
        'ctrl_space': 'Hard Drop',
        'ctrl_p': 'Pause',
        'ctrl_r': 'Reset(2x)',
        'ctrl_tab': 'Lang',
        'confirm_r': 'Press R again to confirm',
        'game_over': 'GAME OVER',
        'final_score': 'Final Score',
        'press_r': 'Press R to restart',
        'paused': 'PAUSED',
        'press_p': 'Press P to continue',
        'tetris': 'TETRIS!',
    },
}


class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=1.0, size=3):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-3, 3)
        self.vy = vy if vy is not None else random.uniform(-5, -1)
        self.life = life
        self.max_life = life
        self.size = size

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.vy += 0.15 * dt * 60
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        alpha = max(0, min(255, alpha))
        size = max(1, int(self.size * (self.life / self.max_life)))
        s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (size, size), size)
        surface.blit(s, (int(self.x) - size, int(self.y) - size))


class LineFlash:
    def __init__(self, row):
        self.row = row
        self.time = 0
        self.duration = 0.4

    def update(self, dt):
        self.time += dt

    def draw(self, surface):
        progress = self.time / self.duration
        if progress >= 1:
            return False
        alpha = int(255 * (1 - progress))
        brightness = int(200 + 55 * (1 - progress))
        flash_color = (brightness, brightness, brightness, alpha)
        s = pygame.Surface((COLS * CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        s.fill(flash_color)
        surface.blit(s, (0, self.row * CELL_SIZE))
        return True


class Piece:
    def __init__(self, shape_idx=None):
        if shape_idx is None:
            shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape_idx = shape_idx
        self.rotation = 0
        self.x = COLS // 2 - 2
        self.y = 0
        self.color = COLORS[shape_idx]

    def cells(self):
        return [(self.x + cx, self.y + cy) for cx, cy in SHAPES[self.shape_idx][self.rotation]]

    def rotated(self, direction):
        return (self.rotation + direction) % 4


class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("俄罗斯方块")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.SysFont("microsoftyahei", 38, bold=True)
        self.font_medium = pygame.font.SysFont("microsoftyahei", 22)
        self.font_small = pygame.font.SysFont("microsoftyahei", 16)
        self.font_score = pygame.font.SysFont("consolas", 28, bold=True)

        # 预渲染方块表面
        self.block_cache = {}
        self._build_block_cache()

        # 动画状态
        self.particles = []
        self.line_flashes = []
        self.shake_offset = [0, 0]
        self.shake_timer = 0
        self.score_popups = []
        self._pending_clear = []
        self._clear_delay = 0
        self._clear_timer = 0
        self._just_reset = False
        self.prev_keys = pygame.key.get_pressed()
        self.restart_count = 0

        # 高分记录
        self.best_score = 0
        self.best_level = 1
        self.best_lines = 0
        self._load_highscore()

        # 语言
        self.lang = 'zh'

        # 防误触：双击 R 确认重开
        self._r_confirm_timer = 0
        self._r_waiting_confirm = False

        # 按键重复延迟（防止下键过快导致连续生成方块）
        self._down_held = False
        self._down_repeat_timer = 0
        self._down_initial_delay = 170   # 首次按下延迟(ms)
        self._down_repeat_rate = 50      # 重复速率(ms)

        self.reset_game()

    def t(self, key):
        return TEXTS[self.lang].get(key, key)

    def _build_block_cache(self):
        for idx, color in enumerate(COLORS):
            s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            bevel = 4
            # 主体
            pygame.draw.rect(s, color, (0, 0, CELL_SIZE, CELL_SIZE))
            # 内部暗色框
            inner = tuple(max(c - 60, 0) for c in color)
            pygame.draw.rect(s, inner, (bevel, bevel, CELL_SIZE - bevel * 2, CELL_SIZE - bevel * 2))
            # 内部填充
            inner_fill = tuple(max(c - 20, 0) for c in color)
            pygame.draw.rect(s, inner_fill, (bevel + 1, bevel + 1, CELL_SIZE - bevel * 2 - 2, CELL_SIZE - bevel * 2 - 2))
            # 高光 (左上)
            lighter = tuple(min(c + 80, 255) for c in color)
            pygame.draw.line(s, lighter, (1, 1), (CELL_SIZE - 2, 1), 2)
            pygame.draw.line(s, lighter, (1, 1), (1, CELL_SIZE - 2), 2)
            # 阴影 (右下)
            darker = tuple(max(c - 80, 0) for c in color)
            pygame.draw.line(s, darker, (1, CELL_SIZE - 2), (CELL_SIZE - 1, CELL_SIZE - 2), 2)
            pygame.draw.line(s, darker, (CELL_SIZE - 2, 1), (CELL_SIZE - 2, CELL_SIZE - 1), 2)
            # 中心高光点
            highlight = pygame.Surface((8, 8), pygame.SRCALPHA)
            hl_color = tuple(min(c + 120, 255) for c in color)
            pygame.draw.circle(highlight, (*hl_color, 60), (4, 4), 4)
            s.blit(highlight, (bevel + 2, bevel + 2))
            self.block_cache[idx] = s

    def reset_game(self):
        if hasattr(self, 'restart_count'):
            self.restart_count += 1
        self.board = [[None] * COLS for _ in range(ROWS)]
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 1000
        self.lock_delay = 500
        self.lock_timer = 0
        self.locking = False
        self.particles.clear()
        self.line_flashes.clear()
        self.score_popups.clear()
        self.shake_offset = [0, 0]
        self.shake_timer = 0
        self._pending_clear = []
        self._clear_delay = 0
        self._clear_timer = 0
        self._just_reset = True
        self.prev_keys = pygame.key.get_pressed()

    def _load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.best_score = data.get('score', 0)
                self.best_level = data.get('level', 1)
                self.best_lines = data.get('lines', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            self.best_score = 0
            self.best_level = 1
            self.best_lines = 0

    def _save_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    'score': self.best_score,
                    'level': self.best_level,
                    'lines': self.best_lines,
                }, f, ensure_ascii=False)
        except Exception:
            pass

    def _update_highscore(self):
        changed = False
        if self.score > self.best_score:
            self.best_score = self.score
            changed = True
        if self.level > self.best_level:
            self.best_level = self.level
            changed = True
        if self.lines_cleared > self.best_lines:
            self.best_lines = self.lines_cleared
            changed = True
        if changed:
            self._save_highscore()

    def valid_position(self, piece, x=None, y=None, rotation=None):
        px = x if x is not None else piece.x
        py = y if y is not None else piece.y
        rot = rotation if rotation is not None else piece.rotation
        for cx, cy in SHAPES[piece.shape_idx][rot]:
            nx, ny = px + cx, py + cy
            if nx < 0 or nx >= COLS or ny >= ROWS:
                return False
            if ny >= 0 and self.board[ny][nx] is not None:
                return False
        return True

    def spawn_particles(self, x, y, color, count=8, spread=3, speed=3):
        px = x * CELL_SIZE + CELL_SIZE // 2
        py = y * CELL_SIZE + CELL_SIZE // 2
        for _ in range(count):
            self.particles.append(Particle(
                px, py, color,
                vx=random.uniform(-spread, spread),
                vy=random.uniform(-speed, 0),
                life=random.uniform(0.3, 0.8),
                size=random.randint(2, 4)
            ))

    def spawn_line_particles(self, row):
        for x in range(COLS):
            color = self.board[row][x] if self.board[row][x] else WHITE
            px = x * CELL_SIZE + CELL_SIZE // 2
            py = row * CELL_SIZE + CELL_SIZE // 2
            for _ in range(3):
                self.particles.append(Particle(
                    px, py, color,
                    vx=random.uniform(-4, 4),
                    vy=random.uniform(-6, -1),
                    life=random.uniform(0.5, 1.0),
                    size=random.randint(2, 5)
                ))

    def trigger_shake(self, intensity=4, duration=0.15):
        self.shake_timer = duration
        self.shake_offset = [random.uniform(-intensity, intensity),
                             random.uniform(-intensity, intensity)]

    def add_score_popup(self, x, y, text, color=(255, 255, 100)):
        self.score_popups.append({
            'x': x * CELL_SIZE + CELL_SIZE // 2,
            'y': y * CELL_SIZE,
            'text': text,
            'color': color,
            'time': 0,
            'duration': 1.0
        })

    def lock_piece(self):
        cells = SHAPES[self.current_piece.shape_idx][self.current_piece.rotation]
        placed_any = False
        for cx, cy in cells:
            nx = self.current_piece.x + cx
            ny = self.current_piece.y + cy
            if 0 <= ny < ROWS and 0 <= nx < COLS:
                self.board[ny][nx] = self.current_piece.color
                self.spawn_particles(nx, ny, self.current_piece.color, count=3, spread=1.5, speed=1.5)
                placed_any = True

        if not placed_any:
            self.game_over = True
            self._update_highscore()
            return

        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        self.locking = False
        self.lock_timer = 0
        if not self.valid_position(self.current_piece):
            self.game_over = True
            self._update_highscore()

    def clear_lines(self):
        lines = []
        for y in range(ROWS):
            if all(cell is not None for cell in self.board[y]):
                lines.append(y)

        if lines:
            for y in lines:
                self.spawn_line_particles(y)
                self.line_flashes.append(LineFlash(y))

            # 延迟后实际清除（通过动画时间控制）
            self._pending_clear = lines
            self._clear_delay = 0.35
            self._clear_timer = 0

    def _do_clear(self):
        if not hasattr(self, '_pending_clear') or not self._pending_clear:
            return
        lines = self._pending_clear
        for y in sorted(lines, reverse=True):
            del self.board[y]
            self.board.insert(0, [None] * COLS)

        count = len(lines)
        self.lines_cleared += count
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        pts = points.get(count, 800) * self.level
        self.score += pts
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(80, 1000 - (self.level - 1) * 80)

        # 分数弹出
        center_x = COLS // 2
        center_y = min(lines)
        label = {1: "+100", 2: "+300", 3: "+500", 4: "+800"}.get(count, "+800")
        self.add_score_popup(center_x, center_y, label)
        if count >= 4:
            self.add_score_popup(center_x, center_y - 1, self.t('tetris'), (255, 215, 0))

        self._pending_clear = []
        self.trigger_shake(intensity=2 + count * 2, duration=0.1 + count * 0.05)

    def try_wall_kick(self, piece, new_rotation):
        kick_table = WALL_KICKS['I'] if piece.shape_idx == 0 else WALL_KICKS['default']
        for dx, dy in kick_table[piece.rotation]:
            if self.valid_position(piece, piece.x + dx, piece.y - dy, new_rotation):
                return piece.x + dx, piece.y - dy
        return None

    def rotate_piece(self, direction):
        new_rotation = self.current_piece.rotated(direction)
        if self.valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece.rotation = new_rotation
            self.reset_lock_timer()
            return True
        kick = self.try_wall_kick(self.current_piece, new_rotation)
        if kick:
            self.current_piece.x, self.current_piece.y = kick
            self.current_piece.rotation = new_rotation
            self.reset_lock_timer()
            return True
        return False

    def move_piece(self, dx, dy):
        if self.valid_position(self.current_piece, self.current_piece.x + dx, self.current_piece.y + dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            self.reset_lock_timer()
            return True
        return False

    def hard_drop(self):
        drop_dist = 0
        while self.move_piece(0, 1):
            self.score += 2
            drop_dist += 1
        # 硬降尾迹粒子
        cells = SHAPES[self.current_piece.shape_idx][self.current_piece.rotation]
        for cx, cy in cells:
            px = self.current_piece.x + cx
            py_start = self.current_piece.y + cy - drop_dist
            py_end = self.current_piece.y + cy
            for i in range(3):
                t = i / 3
                py = py_start + (py_end - py_start) * t
                self.particles.append(Particle(
                    px * CELL_SIZE + CELL_SIZE // 2,
                    py * CELL_SIZE + CELL_SIZE // 2,
                    self.current_piece.color,
                    vx=random.uniform(-0.5, 0.5),
                    vy=random.uniform(-1, 1),
                    life=0.3,
                    size=2
                ))
        self.trigger_shake(intensity=3 + drop_dist // 3, duration=0.12)
        self.lock_piece()

    def get_ghost_y(self):
        ghost_y = self.current_piece.y
        while self.valid_position(self.current_piece, y=ghost_y + 1):
            ghost_y += 1
        return ghost_y

    def reset_lock_timer(self):
        if self.locking:
            self.lock_timer = 0

    def draw_block(self, x, y, color_idx):
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if color_idx in self.block_cache:
            self.screen.blit(self.block_cache[color_idx], rect)

    def draw_block_at(self, x, y, color, size=CELL_SIZE):
        rect = pygame.Rect(x, y, size, size)
        bevel = max(2, size // 8)
        pygame.draw.rect(self.screen, color, rect)
        inner = tuple(max(c - 50, 0) for c in color)
        pygame.draw.rect(self.screen, inner, (rect.x + bevel, rect.y + bevel, size - bevel * 2, size - bevel * 2))
        inner_fill = tuple(max(c - 15, 0) for c in color)
        pygame.draw.rect(self.screen, inner_fill, (rect.x + bevel + 1, rect.y + bevel + 1, size - bevel * 2 - 2, size - bevel * 2 - 2))
        lighter = tuple(min(c + 70, 255) for c in color)
        pygame.draw.line(self.screen, lighter, (rect.x + 1, rect.y + 1), (rect.x + size - 2, rect.y + 1), 1)
        pygame.draw.line(self.screen, lighter, (rect.x + 1, rect.y + 1), (rect.x + 1, rect.y + size - 2), 1)

    def draw_board(self):
        game_rect = pygame.Rect(0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE)
        pygame.draw.rect(self.screen, DARK_BG, game_rect)

        # 网格点（更轻量的网格）
        for x in range(COLS):
            for y in range(ROWS):
                dot_x = x * CELL_SIZE + CELL_SIZE // 2
                dot_y = y * CELL_SIZE + CELL_SIZE // 2
                self.screen.set_at((dot_x, dot_y), GRID_COLOR)

        # 已锁定的方块
        for y in range(ROWS):
            for x in range(COLS):
                if self.board[y][x] is not None:
                    color_idx = COLORS.index(self.board[y][x]) if self.board[y][x] in COLORS else -1
                    if color_idx >= 0:
                        self.draw_block(x, y, color_idx)
                    else:
                        self.draw_block_at(x * CELL_SIZE, y * CELL_SIZE, self.board[y][x])

        # 幽灵方块（轮廓样式）
        if not self.game_over:
            ghost_y = self.get_ghost_y()
            if ghost_y != self.current_piece.y:
                for cx, cy in SHAPES[self.current_piece.shape_idx][self.current_piece.rotation]:
                    gx = self.current_piece.x + cx
                    gy = ghost_y + cy
                    if gy >= 0:
                        rect = pygame.Rect(gx * CELL_SIZE + 1, gy * CELL_SIZE + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                        ghost_color = (*self.current_piece.color[:3],)
                        pygame.draw.rect(self.screen, ghost_color, rect, 2)

        # 当前方块
        if not self.game_over:
            for cx, cy in SHAPES[self.current_piece.shape_idx][self.current_piece.rotation]:
                px = self.current_piece.x + cx
                py = self.current_piece.y + cy
                if py >= 0:
                    color_idx = COLORS.index(self.current_piece.color)
                    self.draw_block(px, py, color_idx)

        # 游戏区域边框（带发光效果）
        glow_rect = pygame.Rect(-1, -1, COLS * CELL_SIZE + 2, ROWS * CELL_SIZE + 2)
        pygame.draw.rect(self.screen, (80, 80, 100), glow_rect, 2)
        pygame.draw.rect(self.screen, BORDER_COLOR, game_rect, 1)

    def draw_sidebar(self):
        sidebar_x = COLS * CELL_SIZE
        # 侧边栏背景（渐变效果）
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(22 + t * 8)
            g = int(22 + t * 6)
            b = int(28 + t * 10)
            pygame.draw.line(self.screen, (r, g, b), (sidebar_x, y), (SCREEN_WIDTH, y))

        pygame.draw.line(self.screen, (60, 60, 80), (sidebar_x, 0), (sidebar_x, SCREEN_HEIGHT), 2)

        # 标题
        title = self.font_large.render(self.t('title'), True, (220, 220, 240))
        title_shadow = self.font_large.render(self.t('title'), True, (40, 40, 60))
        self.screen.blit(title_shadow, (sidebar_x + 12, 17))
        self.screen.blit(title, (sidebar_x + 10, 15))

        # 分隔线
        pygame.draw.line(self.screen, (50, 50, 70), (sidebar_x + 15, 58), (SCREEN_WIDTH - 15, 58), 1)

        # 下一个方块
        next_label = self.font_medium.render(self.t('next'), True, (160, 160, 180))
        self.screen.blit(next_label, (sidebar_x + 15, 68))

        # 预览框
        preview_box = pygame.Rect(sidebar_x + 20, 95, 160, 90)
        pygame.draw.rect(self.screen, (18, 18, 24), preview_box, border_radius=6)
        pygame.draw.rect(self.screen, (50, 50, 70), preview_box, 1, border_radius=6)

        preview_cx = sidebar_x + 100
        preview_cy = 140
        block_size = 22
        cells = SHAPES[self.next_piece.shape_idx][0]
        min_x = min(c[0] for c in cells)
        max_x = max(c[0] for c in cells)
        min_y = min(c[1] for c in cells)
        max_y = max(c[1] for c in cells)
        offset_x = preview_cx - (min_x + max_x + 1) * block_size // 2
        offset_y = preview_cy - (min_y + max_y + 1) * block_size // 2
        for cx, cy in cells:
            self.draw_block_at(offset_x + cx * block_size, offset_y + cy * block_size,
                               self.next_piece.color, block_size)

        # 分隔线
        pygame.draw.line(self.screen, (50, 50, 70), (sidebar_x + 15, 195), (SCREEN_WIDTH - 15, 195), 1)

        # 分数信息
        stats = [
            (self.t('score'), str(self.score), (255, 215, 100)),
            (self.t('level'), str(self.level), (100, 200, 255)),
            (self.t('lines'), str(self.lines_cleared), (120, 255, 140)),
            (self.t('restarts'), str(self.restart_count), (200, 160, 255)),
        ]
        y_offset = 200
        for label, value, color in stats:
            label_text = self.font_small.render(label, True, (120, 120, 140))
            self.screen.blit(label_text, (sidebar_x + 15, y_offset))
            val_text = self.font_score.render(value, True, color)
            self.screen.blit(val_text, (sidebar_x + 15, y_offset + 18))
            y_offset += 50

        # 分隔线
        pygame.draw.line(self.screen, (50, 50, 70), (sidebar_x + 15, 410), (SCREEN_WIDTH - 15, 410), 1)

        # 历史最高
        best_title = self.font_small.render(self.t('best'), True, (255, 200, 80))
        self.screen.blit(best_title, (sidebar_x + 15, 420))
        best_stats = [
            (self.t('score'), str(self.best_score), (255, 215, 100)),
            (self.t('level'), str(self.best_level), (100, 200, 255)),
            (self.t('lines'), str(self.best_lines), (120, 255, 140)),
        ]
        bx = sidebar_x + 15
        for i, (label, value, color) in enumerate(best_stats):
            lx = bx + i * 65
            lt = self.font_small.render(label, True, (100, 100, 120))
            self.screen.blit(lt, (lx, 440))
            vt = self.font_small.render(value, True, color)
            self.screen.blit(vt, (lx, 456))

        # 分隔线
        pygame.draw.line(self.screen, (50, 50, 70), (sidebar_x + 15, 478), (SCREEN_WIDTH - 15, 478), 1)

        # 操作说明
        controls_y = 488
        controls = [
            ("← →", self.t('ctrl_left_right')),
            ("  ↑ ", self.t('ctrl_up')),
            ("  ↓ ", self.t('ctrl_down')),
            ("空格" if self.lang == 'zh' else "SPC ", self.t('ctrl_space')),
            (" P  ", self.t('ctrl_p')),
            (" R  ", self.t('ctrl_r')),
            ("Tab ", self.t('ctrl_tab')),
        ]
        help_title = self.font_small.render(self.t('controls'), True, (120, 120, 140))
        self.screen.blit(help_title, (sidebar_x + 15, controls_y))
        for i, (key, desc) in enumerate(controls):
            y = controls_y + 18 + i * 18
            key_text = self.font_small.render(key, True, (180, 180, 200))
            desc_text = self.font_small.render(desc, True, (130, 130, 150))
            self.screen.blit(key_text, (sidebar_x + 20, y))
            self.screen.blit(desc_text, (sidebar_x + 75, y))

        # 防误触确认提示
        if self._r_waiting_confirm:
            confirm_text = self.font_small.render(self.t('confirm_r'), True, (255, 180, 60))
            ct_rect = confirm_text.get_rect(center=(sidebar_x + SIDEBAR_WIDTH // 2, SCREEN_HEIGHT - 22))
            self.screen.blit(confirm_text, ct_rect)
            # 倒计时条
            bar_w = 140
            bar_h = 4
            bar_x = sidebar_x + (SIDEBAR_WIDTH - bar_w) // 2
            bar_y = SCREEN_HEIGHT - 8
            ratio = max(0, self._r_confirm_timer / 2.0)
            pygame.draw.rect(self.screen, (40, 40, 50), (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(self.screen, (255, 180, 60), (bar_x, bar_y, int(bar_w * ratio), bar_h))

    def draw_game_over(self):
        overlay = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE), pygame.SRCALPHA)
        for y in range(ROWS * CELL_SIZE):
            alpha = min(200, int(150 * (y / (ROWS * CELL_SIZE)) + 50))
            pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (COLS * CELL_SIZE, y))
        self.screen.blit(overlay, (0, 0))

        # 游戏结束文字（带描边）
        go_text = self.font_large.render(self.t('game_over'), True, (255, 60, 60))
        go_rect = go_text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2 - 40))
        for dx, dy in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            shadow = self.font_large.render(self.t('game_over'), True, (80, 0, 0))
            self.screen.blit(shadow, (go_rect.x + dx, go_rect.y + dy))
        self.screen.blit(go_text, go_rect)

        score_text = self.font_medium.render(f"{self.t('final_score')}: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2 + 15))
        self.screen.blit(score_text, score_rect)

        restart_text = self.font_small.render(self.t('press_r'), True, (180, 180, 200))
        restart_rect = restart_text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2 + 55))
        self.screen.blit(restart_text, restart_rect)

    def draw_pause(self):
        overlay = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.screen.blit(overlay, (0, 0))

        pause_text = self.font_large.render(self.t('paused'), True, (200, 200, 220))
        pause_rect = pause_text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2))
        self.screen.blit(pause_text, pause_rect)

        hint_text = self.font_small.render(self.t('press_p'), True, (150, 150, 170))
        hint_rect = hint_text.get_rect(center=(COLS * CELL_SIZE // 2, ROWS * CELL_SIZE // 2 + 40))
        self.screen.blit(hint_text, hint_rect)

    def draw_particles(self):
        for p in self.particles:
            p.draw(self.screen)

    def draw_line_flashes(self):
        for flash in self.line_flashes:
            flash.draw(self.screen)

    def draw_score_popups(self):
        for popup in self.score_popups:
            progress = popup['time'] / popup['duration']
            alpha = int(255 * (1 - progress))
            y_offset = -30 * progress
            scale = 1 + 0.3 * progress
            text = self.font_medium.render(popup['text'], True, popup['color'])
            scaled = pygame.transform.scale(text, (int(text.get_width() * scale), int(text.get_height() * scale)))
            scaled.set_alpha(alpha)
            rect = scaled.get_rect(center=(popup['x'], popup['y'] + y_offset))
            self.screen.blit(scaled, rect)

    def update_animations(self, dt):
        # 粒子更新
        for p in self.particles:
            p.update(dt)
        self.particles = [p for p in self.particles if p.life > 0]

        # 消行闪烁
        for flash in self.line_flashes:
            flash.update(dt)
        self.line_flashes = [f for f in self.line_flashes if f.time < f.duration]

        # 屏幕震动
        if self.shake_timer > 0:
            self.shake_timer -= dt
            fade = self.shake_timer / 0.15
            self.shake_offset[0] *= fade
            self.shake_offset[1] *= fade
        else:
            self.shake_offset = [0, 0]

        # 分数弹出
        for popup in self.score_popups:
            popup['time'] += dt
        self.score_popups = [p for p in self.score_popups if p['time'] < p['duration']]

        # 消行延迟
        if self._pending_clear:
            self._clear_timer += dt
            if self._clear_timer >= self._clear_delay:
                self._do_clear()

    def handle_input(self, dt):
        # 只处理退出事件，其余全部用轮询
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        just_pressed = lambda k: keys[k] and not self.prev_keys[k]

        # R 键：双击确认重开，防误触
        if just_pressed(pygame.K_r):
            if self._r_waiting_confirm:
                # 第二次按下，确认重开
                self._r_waiting_confirm = False
                self._r_confirm_timer = 0
                self.prev_keys = keys
                self.reset_game()
                return
            else:
                # 第一次按下，进入等待确认
                self._r_waiting_confirm = True
                self._r_confirm_timer = 2.0

        # 以下只在游戏进行中生效
        if not self.game_over and not self.paused:
            # 方向键 - 左右移动
            if just_pressed(pygame.K_LEFT):
                self.move_piece(-1, 0)
            elif just_pressed(pygame.K_RIGHT):
                self.move_piece(1, 0)
            # 下键 - 加速（带重复延迟，防止过快）
            if keys[pygame.K_DOWN]:
                if not self._down_held:
                    # 首次按下，立即移动一次
                    self._down_held = True
                    self._down_repeat_timer = self._down_initial_delay / 1000.0
                    if self.move_piece(0, 1):
                        self.score += 1
                else:
                    # 持续按住，按重复速率移动
                    self._down_repeat_timer -= dt
                    if self._down_repeat_timer <= 0:
                        self._down_repeat_timer = self._down_repeat_rate / 1000.0
                        if self.move_piece(0, 1):
                            self.score += 1
            else:
                self._down_held = False
                self._down_repeat_timer = 0
            # 上键 - 旋转
            if just_pressed(pygame.K_UP):
                self.rotate_piece(1)
            # 空格 - 硬降
            if just_pressed(pygame.K_SPACE):
                self.hard_drop()

        # P 键 - 暂停
        if just_pressed(pygame.K_p):
            self.paused = not self.paused

        # Tab 键 - 切换中英文
        if just_pressed(pygame.K_TAB):
            self.lang = 'en' if self.lang == 'zh' else 'zh'

        self.prev_keys = keys

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            self.handle_input(dt)

            # 防误触确认计时器
            if self._r_waiting_confirm:
                self._r_confirm_timer -= dt
                if self._r_confirm_timer <= 0:
                    self._r_waiting_confirm = False

            # 重置后跳过本帧游戏逻辑，防止立即 game_over
            if self._just_reset:
                self._just_reset = False
                self.screen.fill(DARK_BG)
                self.draw_board()
                self.draw_sidebar()
                pygame.display.flip()
                continue

            self.update_animations(dt)

            if not self.game_over and not self.paused:
                self.fall_time += dt * 1000
                if self.fall_time >= self.fall_speed:
                    self.fall_time = 0
                    if not self.move_piece(0, 1):
                        self.locking = True
                if self.locking:
                    self.lock_timer += dt * 1000
                    if self.lock_timer >= self.lock_delay:
                        self.lock_piece()
                if not self.locking and not self.valid_position(self.current_piece, y=self.current_piece.y + 1):
                    self.locking = True
                    self.lock_timer = 0

            # 绘制
            self.screen.fill(DARK_BG)
            game_surface = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE))
            old_screen = self.screen
            self.screen = game_surface
            self.draw_board()
            self.draw_line_flashes()
            self.draw_particles()
            self.draw_score_popups()
            self.screen = old_screen

            self.screen.blit(game_surface, (int(self.shake_offset[0]), int(self.shake_offset[1])))
            self.draw_sidebar()

            if self.game_over:
                self.draw_game_over()
            elif self.paused:
                self.draw_pause()

            pygame.display.flip()


if __name__ == "__main__":
    game = Tetris()
    game.run()