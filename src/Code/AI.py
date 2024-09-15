import pygame
from Maze import Maze
from pygame.locals import *
import threading

class AI:
    
    def __init__(self, maze):
        self.maze = maze
        self.x, self.y = maze.start_x, maze.start_y
        self.start_x = maze.start_x  # Lưu trữ vị trí ban đầu của icon theo trục X
        self.start_y = maze.start_y  # Lưu trữ vị trí ban đầu của icon theo trục Y
        self.path = []  # Thêm thuộc tính path vào đối tượng AI
        self.move_history = []  # Lịch sử các bước đã di chuyển
    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        if dx != 0:
            dx //= abs(dx)
        if dy != 0:
            dy //= abs(dy)

        next_x = self.x + dx
        next_y = self.y + dy

        # Kiểm tra xem ô tiếp theo có phải là ô màu trắng hoặc chứa chướng ngại vật không
        if self.maze.grid[next_y][next_x] == 0 or (next_x, next_y) in self.maze.obstacles:
            # Nếu ô tiếp theo không hợp lệ, kiểm tra xem ô tiếp theo có phải là ô chứa chướng ngại vật hay không
            if (next_x, next_y) in self.maze.obstacles:
                # Nếu là ô chứa chướng ngại vật, lùi lại 3 bước đã đi trước đó
                if len(self.move_history) >= 4:
                    # Lùi lại 3 bước
                    for i in range(3):
                        x, y = self.move_history.pop()
                        self.path.remove((x, y))
                        # Đặt lại giá trị của ô đã đi trước đó thành 0 (màu trắng)
                        self.maze.grid[y][x] = 0

                    # Lấy tọa độ của ô đã đi trước đó
                    next_x, next_y = self.move_history[-1]  
                else:
                    # Nếu không đủ 3 ô trong lịch sử di chuyển, thì di chuyển về điểm xuất phát
                    next_x, next_y = self.maze.start_x, self.maze.start_y

                # Lưu lại tọa độ lùi
                self.x = next_x
                self.y = next_y
                self.path.append((self.x, self.y))
                self.move_history.append((self.x, self.y))

                # Tạo một thread mới để phát nhạc
                threading.Thread(target=self.play_sound_after_reverse).start()

                return  # Kết thúc phương thức sau khi xử lý va chạm

            # Nếu ô tiếp theo là ô màu trắng, tiến hành di chuyển bình thường
            self.x = next_x
            self.y = next_y
            self.path.append((self.x, self.y))
            self.move_history.append((self.x, self.y))

    def play_sound_after_reverse(self):
        # Khởi tạo mixer của pygame
        pygame.mixer.init()

        # Phát nhạc 'trungchuongngaivat.mp3'
        pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/trungchuongngaivat.mp3")
        pygame.mixer.music.play()

        # Đợi cho nhạc phát xong
        pygame.time.wait(3000)  # Chờ 3 giây

        # Phát nhạc 'nhac.mp3'
        pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nhac.mp3")
        pygame.mixer.music.play()

        