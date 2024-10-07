# Algorithms.py
import pygame
from Maze import Maze
from pygame.locals import *
from queue import PriorityQueue
from queue import PriorityQueue
import os  # Thêm thư viện os
def dijkstra(maze):
    # Thuật toán Dijkstra để tìm đường đi ngắn nhất trong mê cung
    start_node = (maze.start_x, maze.start_y)  # Điểm bắt đầu
    end_node = (maze.end_x, maze.end_y)  # Điểm kết thúc
    frontier = PriorityQueue()  # Hàng đợi ưu tiên để lưu các đỉnh cần kiểm tra
    frontier.put(start_node, 0)  # Thêm điểm bắt đầu vào hàng đợi ưu tiên với độ ưu tiên là 0
    came_from = {}  # Dùng để lưu lại đỉnh trước của mỗi đỉnh
    cost_so_far = {}  # Dùng để lưu lại chi phí tới mỗi đỉnh
    came_from[start_node] = None  # Khởi tạo điểm bắt đầu không có điểm trước đó
    cost_so_far[start_node] = 0  # Khởi tạo chi phí tới điểm bắt đầu là 0

    # Bắt đầu vòng lặp chính của thuật toán
    while not frontier.empty():
        current = frontier.get()  # Lấy ra đỉnh có độ ưu tiên nhỏ nhất từ hàng đợi

        if current == end_node:  # Nếu đỉnh hiện tại là điểm kết thúc, thoát khỏi vòng lặp
            break

        # Duyệt qua các đỉnh kề của đỉnh hiện tại
        # Kiểm tra nếu đỉnh kề tiếp theo chưa được xem xét trước đó hoặc chi phí mới để đến đỉnh này nhỏ hơn chi phí đã biết trước đó
        for next in maze.get_neighbors(current[0], current[1]):
             # Nếu điều kiện trên đúng, ta cập nhật chi phí mới và thêm đỉnh này vào hàng đợi ưu tiên để xem xét sau này
            new_cost = cost_so_far[current] + 1  # Tính chi phí mới đến đỉnh kề
            # Kiểm tra xem ô tiếp theo chưa được xem xét trước đó hoặc chi phí mới để đến ô này nhỏ hơn chi phí đã biết trước đó
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost  # Cập nhật chi phí mới cho đỉnh kề
                priority = new_cost + heuristic(end_node, next)  # Tính độ ưu tiên mới
                frontier.put(next, priority)  # Thêm đỉnh kề vào hàng đợi với độ ưu tiên mới
                came_from[next] = current  # Lưu lại đỉnh trước của đỉnh kề

    # Sau khi thuật toán kết thúc, ta lấy đường đi từ điểm kết thúc về điểm bắt đầu
    current = end_node
    path = []
    while current != start_node:
        path.append(current)
        current = came_from[current]
    path.append(start_node)
    path.reverse()  # Đảo ngược đường đi để được theo thứ tự từ điểm bắt đầu đến điểm kết thúc
    return path

def heuristic(a, b):
    # Hàm heuristic để ước lượng khoảng cách từ một điểm đến điểm khác
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def play_next_music():
    # Hàm để phát nhạc tiếp theo
    base_path = os.path.dirname(__file__)  # Lấy đường dẫn thư mục hiện tại
    music_path = os.path.join(base_path, "assets/music/nhac.mp3")  # Đường dẫn tương đối tới file nhạc
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
