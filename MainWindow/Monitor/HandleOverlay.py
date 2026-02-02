import os
import configparser
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, QPoint, Signal


class HandleOverlay(QWidget):
    ratioChanged = Signal(dict)

    CONFIG_PATH = "config/line.ini"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self._draw_enabled = False
        self._ratios = {
            'top': 0.2,
            'bottom': 0.8,
            'left': 0.25,
            'right': 0.75
        }
        self._drag_mode = None
        self._drag_start_pos = QPoint()
        self._tolerance = 6
        self._line_positions = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0}

        self._load_from_config()
        self._update_line_positions()

    def _load_from_config(self):
        if not os.path.exists(self.CONFIG_PATH):
            return

        config = configparser.ConfigParser()
        try:
            config.read(self.CONFIG_PATH)
            if 'Lines' in config:
                section = config['Lines']
                self._ratios['top']    = float(section.get('top',    '0.2'))
                self._ratios['bottom'] = float(section.get('bottom', '0.8'))
                self._ratios['left']   = float(section.get('left',   '0.25'))
                self._ratios['right']  = float(section.get('right',  '0.75'))

                # 简单范围校验
                for k in self._ratios:
                    self._ratios[k] = max(0.0, min(1.0, self._ratios[k]))
        except Exception as e:
            print(f"加载 {self.CONFIG_PATH} 失败: {e}，使用默认值")

    def save_to_config(self):
        os.makedirs(os.path.dirname(self.CONFIG_PATH), exist_ok=True)

        config = configparser.ConfigParser()
        config['Lines'] = {
            'top':    f"{self._ratios['top']:.4f}",
            'bottom': f"{self._ratios['bottom']:.4f}",
            'left':   f"{self._ratios['left']:.4f}",
            'right':  f"{self._ratios['right']:.4f}"
        }

        try:
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                config.write(f)
            print(f"已保存四线位置到 {self.CONFIG_PATH}")
        except Exception as e:
            print(f"保存 {self.CONFIG_PATH} 失败: {e}")

    # ================== 绘制 ==================
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        if w <= 1 or h <= 1:
            return

        if self._draw_enabled:
            # 四条可拖动辅助线
            pen = QPen(QColor(0, 255, 255), 2)
            painter.setPen(pen)
            pos = self._line_positions
            painter.drawLine(0, pos['top'],    w, pos['top'])
            painter.drawLine(0, pos['bottom'], w, pos['bottom'])
            painter.drawLine(pos['left'],  0, pos['left'],  h)
            painter.drawLine(pos['right'], 0, pos['right'], h)

            # 固定中心十字线
            cx, cy = w // 2, h // 2
            pen = QPen(QColor(255, 0, 0, 128), 1)
            painter.setPen(pen)
            painter.drawLine(0, cy, w, cy)
            painter.drawLine(cx, 0, cx, h)

    # ================== 鼠标交互 ==================
    def mousePressEvent(self, event):
        if not self._draw_enabled:
            return
        pos = event.pos()
        p = self._line_positions
        tol = self._tolerance

        if abs(pos.y() - p['top'])    <= tol: self._drag_mode = 'top'
        elif abs(pos.y() - p['bottom']) <= tol: self._drag_mode = 'bottom'
        elif abs(pos.x() - p['left'])   <= tol: self._drag_mode = 'left'
        elif abs(pos.x() - p['right'])  <= tol: self._drag_mode = 'right'

        if self._drag_mode:
            self._drag_start_pos = pos
            self.setCursor(Qt.ArrowCursor)

    def mouseMoveEvent(self, event):
        pos = event.pos()
        w, h = self.width(), self.height()

        if self._drag_mode:
            delta = pos - self._drag_start_pos

            if self._drag_mode in ('top', 'bottom'):
                key = self._drag_mode
                new_ratio = self._ratios[key] + (delta.y() / h)
                self._ratios[key] = max(0.0, min(1.0, new_ratio))

                # 防止上下线交叉
                if self._drag_mode == 'top' and self._ratios['top'] > self._ratios['bottom'] - 0.01:
                    self._ratios['bottom'] = self._ratios['top'] + 0.01
                elif self._drag_mode == 'bottom' and self._ratios['bottom'] < self._ratios['top'] + 0.01:
                    self._ratios['top'] = self._ratios['bottom'] - 0.01

            else:  # left / right
                key = self._drag_mode
                new_ratio = self._ratios[key] + (delta.x() / w)
                self._ratios[key] = max(0.0, min(1.0, new_ratio))

                # 防止左右线交叉
                if self._drag_mode == 'left' and self._ratios['left'] > self._ratios['right'] - 0.01:
                    self._ratios['right'] = self._ratios['left'] + 0.01
                elif self._drag_mode == 'right' and self._ratios['right'] < self._ratios['left'] + 0.01:
                    self._ratios['left'] = self._ratios['right'] - 0.01

            self._update_line_positions()
            self.update()
            self._drag_start_pos = pos  # 支持连续拖动
            return

        # 未拖拽时更新光标
        self._update_cursor(pos)

    def mouseReleaseEvent(self, event):
        self._drag_mode = None
        if self._draw_enabled:
            self.save_to_config()

    def _update_cursor(self, pos):
        if not self._draw_enabled:
            self.setCursor(Qt.ArrowCursor)
            return

        tol = self._tolerance
        p = self._line_positions

        if abs(pos.y() - p['top']) <= tol or abs(pos.y() - p['bottom']) <= tol:
            self.setCursor(Qt.SizeVerCursor)
        elif abs(pos.x() - p['left']) <= tol or abs(pos.x() - p['right']) <= tol:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    # ================== 窗口大小变化 ==================
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_line_positions()

    # ================== 核心更新逻辑 ==================
    def _update_line_positions(self):
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return

        self._line_positions['top']    = max(0, min(int(self._ratios['top']    * h), h))
        self._line_positions['bottom'] = max(self._line_positions['top'], min(int(self._ratios['bottom'] * h), h))
        self._line_positions['left']   = max(0, min(int(self._ratios['left']   * w), w))
        self._line_positions['right']  = max(self._line_positions['left'], min(int(self._ratios['right'] * w), w))

        # 防止比例交叉（再次强制约束）
        if self._ratios['top'] >= self._ratios['bottom']:
            mid = (self._ratios['top'] + self._ratios['bottom']) / 2
            self._ratios['top'] = mid - 0.1
            self._ratios['bottom'] = mid + 0.1

        if self._ratios['left'] >= self._ratios['right']:
            mid = (self._ratios['left'] + self._ratios['right']) / 2
            self._ratios['left'] = mid - 0.05
            self._ratios['right'] = mid + 0.05

        self.ratioChanged.emit(self._ratios.copy())

    # ================== 对外接口 ==================
    def set_draw_mode(self, enabled: bool):
        """启用/禁用四线绘制"""
        self._draw_enabled = enabled
        if enabled:
            self._update_line_positions()
        self.update()

    def get_line_positions(self):
        """获取当前像素位置 (top, bottom, left, right)"""
        return (self._line_positions['top'],
                self._line_positions['bottom'],
                self._line_positions['left'],
                self._line_positions['right'])

    def get_ratios(self):
        """获取当前比例字典"""
        return self._ratios.copy()

    def get_4_line(self):
        return self.get_line_positions()
