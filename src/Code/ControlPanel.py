# ControlPanel.py
import pygame
from Maze import Maze
from pygame.locals import *
from queue import PriorityQueue


class ControlPanel:
    def __init__(self, width, height):
        self.background_image = pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/selectbackground.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (300, 500))  # Chỉnh kích thước hình nền
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.direction_keys = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}
        self.current_direction = None
        self.move_continuous = False
        self.auto_play = False  # Thêm thuộc tính auto_play để theo dõi trạng thái auto play
        self.levels_displayed = False  # Thêm thuộc tính để theo dõi trạng thái hiển thị của các mức độ
        
    def reset_icon_position(self, ai):
        ai.x, ai.y = ai.start_x, ai.start_y  # Đặt lại vị trí của icon về vị trí ban đầu
    def handle_continuous_movement(self, maze, ai):
        if self.move_continuous and self.current_direction:
            dx, dy = self.current_direction
            # Kiểm tra xem có thể di chuyển đến ô tiếp theo không
            if maze.grid[ai.y + dy][ai.x + dx] == 0:
                ai.move_towards(ai.x + dx, ai.y + dy)  # Di chuyển
        return maze, ai

    # Phương thức để hiển thị giao diện
    def display(self, screen):
        # Hiển thị hình nền và các nút chức năng
        bg_width, bg_height = self.background_image.get_size()  # Lấy kích thước của hình nền
        x = 700  # Vị trí căn lề phải
        y = 0  

        screen.blit(self.background_image, (x, y))  # Vẽ hình nền
        text_color = (255, 255, 255)  # Màu chữ

        # Tạo các văn bản cho các nút
        auto_play_text = self.font.render("Auto Play", True, text_color)  # Tạo văn bản cho nút "Auto Play"
        ai_play_text = self.font.render("AI Play", True, text_color)  # Tạo văn bản cho nút "AI Play"
        reset_text = self.font.render("Reset Maze", True, text_color)  # Tạo văn bản cho nút "Reset Maze"
        exit_text = self.font.render("Exit", True, text_color)  # Tạo văn bản cho nút "Exit"

        # Màu và hiệu ứng nút khi di chuột qua
        button_color = (0, 153, 204)  # Màu nền của nút
        hover_color = (0, 102, 153)  # Màu nền của nút khi di chuột qua

        # Vẽ các nút và viền
        buttons = [
            (750, 50, 200, 50, auto_play_text),  # Nút "Auto Play"
            (750, 150, 200, 50, ai_play_text),  # Nút "AI Play"
            (750, 250, 200, 50, reset_text),  # Nút "Reset Maze"
            (750, 350, 200, 50, exit_text),  # Nút "Exit"
        ]
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí của chuột

        # Vẽ nút và xác định vị trí của chuột
        for button in buttons:
            x, y, width, height, text = button
            # Kiểm tra vị trí của chuột để thay đổi màu của nút
            if x < mouse_x < x + width and y < mouse_y < y + height:
                pygame.draw.rect(screen, hover_color, (x, y, width, height))  # Màu nền khi di chuột qua
            else:
                pygame.draw.rect(screen, button_color, (x, y, width, height))  # Màu nền mặc định của nút

            # Vẽ viền của nút
            pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 1)

            # Vị trí văn bản căng giữa trên nút
            text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
            screen.blit(text, text_rect)

        # Xử lý các sự kiện từ chuột và bàn phím
    def handle_event(self, event, maze, ai):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí chuột khi nhấn
            # Kiểm tra xem chuột có nhấn vào nút "Auto Play" không
            if 750 < mouse_x < 950 and 50 < mouse_y < 100:  
                self.auto_play = True  # Kích hoạt chế độ tự động chơi
                self.reset_icon_position(ai)  # Đặt lại vị trí của biểu tượng AI về vị trí ban đầu
            # Kiểm tra xem chuột có nhấn vào nút "AI Play" không
            elif 750 < mouse_x < 950 and 150 < mouse_y < 200:  
                self.auto_play = False  # Tắt chế độ tự động chơi
                self.reset_icon_position(ai)  # Đặt lại vị trí của biểu tượng AI về vị trí ban đầu

        elif event.type == KEYDOWN:
            if event.key in self.direction_keys:
                dx, dy = self.direction_keys[event.key]
                # Kiểm tra ô tiếp theo có là chướng ngại vật không
                if maze.grid[ai.y + dy][ai.x + dx] == 0:
                    self.current_direction = (dx, dy)
                    self.move_continuous = True
                    if self.auto_play:  
                        maze, ai = self.handle_continuous_movement(maze, ai) 

        elif event.type == KEYUP:
            if event.key in self.direction_keys:
                if self.current_direction == self.direction_keys[event.key]:
                    self.move_continuous = False
                    self.current_direction = None

        return maze, ai
