import pygame  # Nhập thư viện pygame để hỗ trợ phát triển game và âm thanh
from Maze import Maze  # Nhập lớp Maze từ tệp Maze
from pygame.locals import *  # Nhập các hằng số từ pygame.locals
import threading  # Nhập thư viện threading để tạo và quản lý luồng
import os  # Nhập thư viện os để làm việc với hệ thống tệp và đường dẫn

class AI:
    
    def __init__(self, maze):
        self.maze = maze  # Khởi tạo mê cung
        self.x, self.y = maze.start_x, maze.start_y  # Vị trí ban đầu của AI trong mê cung
        self.start_x = maze.start_x  # Lưu trữ vị trí ban đầu của AI theo trục X
        self.start_y = maze.start_y  # Lưu trữ vị trí ban đầu của AI theo trục Y
        self.path = []  # Danh sách lưu đường đi của AI
        self.move_history = []  # Danh sách lưu lịch sử các bước đã di chuyển

    # Phương thức di chuyển AI tới tọa độ chỉ định (target_x, target_y)
    def move_towards(self, target_x, target_y):
        dx = target_x - self.x  # Tính khoảng cách trên trục X
        dy = target_y - self.y  # Tính khoảng cách trên trục Y
        if dx != 0:
            dx //= abs(dx)  # Điều chỉnh hướng di chuyển theo trục X
        if dy != 0:
            dy //= abs(dy)  # Điều chỉnh hướng di chuyển theo trục Y

        next_x = self.x + dx  # Tính tọa độ X tiếp theo
        next_y = self.y + dy  # Tính tọa độ Y tiếp theo

        # Kiểm tra xem ô tiếp theo có phải là ô trống hoặc chứa chướng ngại vật không
        if self.maze.grid[next_y][next_x] == 0 or (next_x, next_y) in self.maze.obstacles:
            # Nếu ô tiếp theo chứa chướng ngại vật
            if (next_x, next_y) in self.maze.obstacles:
                # Nếu có đủ 3 bước trong lịch sử di chuyển, lùi lại 3 bước
                if len(self.move_history) >= 4:
                    for i in range(3):
                        x, y = self.move_history.pop()  # Lấy bước cuối cùng từ lịch sử di chuyển
                        self.path.remove((x, y))  # Xóa bước này khỏi đường đi
                        # Đặt lại giá trị ô đã đi thành 0 (màu trắng)
                        self.maze.grid[y][x] = 0

                    # Lấy tọa độ của ô trước đó
                    next_x, next_y = self.move_history[-1]  
                else:
                    # Nếu không đủ 3 bước, di chuyển về điểm xuất phát
                    next_x, next_y = self.maze.start_x, self.maze.start_y

                # Cập nhật vị trí của AI
                self.x = next_x
                self.y = next_y
                self.path.append((self.x, self.y))  # Thêm bước lùi vào đường đi
                self.move_history.append((self.x, self.y))  # Thêm bước lùi vào lịch sử di chuyển

                # Tạo một luồng mới để phát nhạc khi lùi
                threading.Thread(target=self.play_sound_after_reverse).start()

                return  # Kết thúc phương thức sau khi xử lý lùi

            # Nếu ô tiếp theo là ô trống, di chuyển bình thường
            self.x = next_x
            self.y = next_y
            self.path.append((self.x, self.y))  # Thêm bước di chuyển vào đường đi
            self.move_history.append((self.x, self.y))  # Thêm bước di chuyển vào lịch sử di chuyển

    # Phương thức phát nhạc khi AI lùi lại do va chạm với chướng ngại vật
    def play_sound_after_reverse(self):
        pygame.mixer.init()  # Khởi tạo mixer của pygame để phát nhạc

        # Đường dẫn tương đối tới file nhạc
        base_path = os.path.dirname(__file__)  # Lấy đường dẫn thư mục hiện tại
        sound1_path = os.path.join(base_path, "assets/music/trungchuongngaivat.mp3")  # Đường dẫn tới file nhạc va chạm
        sound2_path = os.path.join(base_path, "assets/music/nhac.mp3")  # Đường dẫn tới file nhạc nền

        pygame.mixer.music.load(sound1_path)  # Tải file nhạc va chạm
        pygame.mixer.music.play()  # Phát nhạc va chạm

        pygame.time.wait(3000)  # Đợi 3 giây cho nhạc va chạm phát xong

        pygame.mixer.music.load(sound2_path)  # Tải file nhạc nền
        pygame.mixer.music.play()  # Phát nhạc nền
