# ControlPanel.py
import pygame  # Nhập thư viện pygame để phát triển giao diện game
from Maze import Maze  # Nhập lớp Maze từ tệp Maze
from pygame.locals import *  # Nhập các hằng số từ pygame.locals
from queue import PriorityQueue  # Nhập hàng đợi ưu tiên

class ControlPanel:
    def __init__(self, width, height):
        # Tải hình nền từ tệp và thay đổi kích thước của nó
        self.background_image = pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/selectbackground.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (300, 500))  # Chỉnh kích thước hình nền
        self.font = pygame.font.Font('freesansbold.ttf', 24)  # Thiết lập phông chữ cho các nút
        # Thiết lập các phím điều hướng cho di chuyển
        self.direction_keys = {K_UP: (0, -1), K_DOWN: (0, 1), K_LEFT: (-1, 0), K_RIGHT: (1, 0)}
        self.current_direction = None  # Hướng di chuyển hiện tại
        self.move_continuous = False  # Biến theo dõi xem có đang di chuyển liên tục hay không
        self.auto_play = False  # Trạng thái tự động chơi
        self.levels_displayed = False  # Trạng thái hiển thị các mức độ của trò chơi
        
    # Đặt lại vị trí của biểu tượng AI về vị trí ban đầu
    def reset_icon_position(self, ai):
        ai.x, ai.y = ai.start_x, ai.start_y  # Đặt lại vị trí của icon về vị trí ban đầu
    
    # Xử lý di chuyển liên tục khi giữ phím điều hướng
    def handle_continuous_movement(self, maze, ai):
        if self.move_continuous and self.current_direction:  # Nếu đang di chuyển liên tục và có hướng di chuyển
            dx, dy = self.current_direction
            # Kiểm tra xem có thể di chuyển đến ô tiếp theo không (ô trống)
            if maze.grid[ai.y + dy][ai.x + dx] == 0:
                ai.move_towards(ai.x + dx, ai.y + dy)  # Di chuyển AI
        return maze, ai  # Trả về mê cung và đối tượng AI sau khi di chuyển

    # Phương thức để hiển thị giao diện của bảng điều khiển
    def display(self, screen):
        # Hiển thị hình nền và các nút chức năng
        bg_width, bg_height = self.background_image.get_size()  # Lấy kích thước của hình nền
        x = 700  # Vị trí căn lề phải của hình nền
        y = 0  # Vị trí từ trên xuống của hình nền

        screen.blit(self.background_image, (x, y))  # Vẽ hình nền lên màn hình
        text_color = (255, 255, 255)  # Màu trắng cho chữ trên các nút

        # Tạo các văn bản cho các nút
        auto_play_text = self.font.render("Auto Play", True, text_color)  # Tạo văn bản cho nút "Auto Play"
        ai_play_text = self.font.render("AI Play", True, text_color)  # Tạo văn bản cho nút "AI Play"
        reset_text = self.font.render("Reset Maze", True, text_color)  # Tạo văn bản cho nút "Reset Maze"
        exit_text = self.font.render("Exit", True, text_color)  # Tạo văn bản cho nút "Exit"

        # Thiết lập màu cho nút và khi di chuột qua
        button_color = (0, 153, 204)  # Màu nền mặc định của nút
        hover_color = (0, 102, 153)  # Màu nền của nút khi di chuột qua

        # Vẽ các nút và viền
        buttons = [
            (750, 50, 200, 50, auto_play_text),  # Nút "Auto Play"
            (750, 150, 200, 50, ai_play_text),  # Nút "AI Play"
            (750, 250, 200, 50, reset_text),  # Nút "Reset Maze"
            (750, 350, 200, 50, exit_text),  # Nút "Exit"
        ]
        mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí của chuột

        # Vẽ nút và xác định vị trí của chuột để thay đổi màu nút khi hover
        for button in buttons:
            x, y, width, height, text = button
            # Kiểm tra xem chuột có nằm trên nút hay không để thay đổi màu sắc
            if x < mouse_x < x + width and y < mouse_y < y + height:
                pygame.draw.rect(screen, hover_color, (x, y, width, height))  # Màu nền khi di chuột qua
            else:
                pygame.draw.rect(screen, button_color, (x, y, width, height))  # Màu nền mặc định của nút

            # Vẽ viền trắng của nút
            pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 1)

            # Vị trí văn bản nằm giữa trên nút
            text_rect = text.get_rect(center=(x + width // 2, y + height // 2))
            screen.blit(text, text_rect)  # Hiển thị văn bản lên nút

    # Xử lý các sự kiện chuột và bàn phím
    def handle_event(self, event, maze, ai):
        if event.type == pygame.MOUSEBUTTONDOWN:  # Kiểm tra nếu chuột được nhấn
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí chuột khi nhấn
            # Kiểm tra xem chuột có nhấn vào nút "Auto Play" không
            if 750 < mouse_x < 950 and 50 < mouse_y < 100:  
                self.auto_play = True  # Bật chế độ tự động chơi
                self.reset_icon_position(ai)  # Đặt lại vị trí của biểu tượng AI về vị trí ban đầu
            # Kiểm tra xem chuột có nhấn vào nút "AI Play" không
            elif 750 < mouse_x < 950 and 150 < mouse_y < 200:  
                self.auto_play = False  # Tắt chế độ tự động chơi
                self.reset_icon_position(ai)  # Đặt lại vị trí của biểu tượng AI về vị trí ban đầu

        elif event.type == KEYDOWN:  # Kiểm tra nếu phím được nhấn
            if event.key in self.direction_keys:  # Nếu phím nhấn là một trong các phím điều hướng
                dx, dy = self.direction_keys[event.key]  # Lấy hướng di chuyển tương ứng
                # Kiểm tra ô tiếp theo có phải là đường đi hợp lệ (không phải tường) không
                if maze.grid[ai.y + dy][ai.x + dx] == 0:
                    self.current_direction = (dx, dy)  # Lưu hướng di chuyển hiện tại
                    self.move_continuous = True  # Bật chế độ di chuyển liên tục
                    if self.auto_play:  # Nếu chế độ tự động chơi đang bật
                        maze, ai = self.handle_continuous_movement(maze, ai)  # Xử lý di chuyển liên tục cho AI

        elif event.type == KEYUP:  # Kiểm tra nếu phím được nhả ra
            if event.key in self.direction_keys:  # Nếu phím nhả là một trong các phím điều hướng
                if self.current_direction == self.direction_keys[event.key]:  # Kiểm tra nếu hướng nhả là hướng hiện tại
                    self.move_continuous = False  # Tắt chế độ di chuyển liên tục
                    self.current_direction = None  # Xóa hướng di chuyển hiện tại

        return maze, ai  # Trả về mê cung và đối tượng AI sau khi xử lý sự kiện
