# Algorithms.py
import pygame  # Nhập thư viện pygame để làm việc với game và âm thanh
from Maze import Maze  # Nhập lớp Maze từ tệp Maze
from pygame.locals import *  # Nhập các hằng số từ pygame.locals
from queue import PriorityQueue  # Nhập hàng đợi ưu tiên
import os  # Nhập thư viện os để làm việc với hệ thống tệp

def dijkstra(maze):
    # Thuật toán Dijkstra để tìm đường đi ngắn nhất trong mê cung
    start_node = (maze.start_x, maze.start_y)  # Thiết lập điểm bắt đầu của mê cung
    end_node = (maze.end_x, maze.end_y)  # Thiết lập điểm kết thúc của mê cung
    frontier = PriorityQueue()  # Tạo hàng đợi ưu tiên để lưu các điểm cần kiểm tra
    frontier.put(start_node, 0)  # Thêm điểm bắt đầu vào hàng đợi với độ ưu tiên là 0
    came_from = {}  # Dictionary lưu trữ đỉnh trước của mỗi đỉnh (đường đi)
    cost_so_far = {}  # Dictionary lưu trữ chi phí từ điểm bắt đầu đến các đỉnh
    came_from[start_node] = None  # Điểm bắt đầu không có đỉnh trước
    cost_so_far[start_node] = 0  # Chi phí đến điểm bắt đầu là 0

    # Vòng lặp chính của thuật toán Dijkstra
    while not frontier.empty():  # Tiếp tục khi hàng đợi không rỗng
        current = frontier.get()  # Lấy điểm có độ ưu tiên cao nhất từ hàng đợi

        if current == end_node:  # Nếu đã đến điểm kết thúc thì thoát vòng lặp
            break

        # Duyệt qua các điểm lân cận của điểm hiện tại
        for next in maze.get_neighbors(current[0], current[1]):  # Lấy các điểm lân cận
            new_cost = cost_so_far[current] + 1  # Tính chi phí đến đỉnh lân cận
            # Nếu đỉnh lân cận chưa được xem xét hoặc có chi phí thấp hơn
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost  # Cập nhật chi phí mới cho đỉnh lân cận
                priority = new_cost + heuristic(end_node, next)  # Tính độ ưu tiên dựa trên chi phí và heuristic
                frontier.put(next, priority)  # Thêm đỉnh lân cận vào hàng đợi với độ ưu tiên mới
                came_from[next] = current  # Lưu trữ đỉnh trước của đỉnh lân cận

    # Xây dựng đường đi từ điểm kết thúc về điểm bắt đầu
    current = end_node  # Bắt đầu từ điểm kết thúc
    path = []  # Tạo danh sách lưu trữ đường đi
    while current != start_node:  # Lặp lại cho đến khi trở về điểm bắt đầu
        path.append(current)  # Thêm điểm hiện tại vào đường đi
        current = came_from[current]  # Di chuyển đến đỉnh trước
    path.append(start_node)  # Thêm điểm bắt đầu vào đường đi
    path.reverse()  # Đảo ngược danh sách để có đường đi từ điểm bắt đầu đến điểm kết thúc
    return path  # Trả về đường đi

def heuristic(a, b):
    # Hàm heuristic để ước lượng khoảng cách giữa hai điểm
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Sử dụng khoảng cách Manhattan

def play_next_music():
    # Hàm để phát nhạc tiếp theo
    base_path = os.path.dirname(__file__)  # Lấy đường dẫn thư mục hiện tại
    music_path = os.path.join(base_path, "assets/music/nhac.mp3")  # Tạo đường dẫn đến file nhạc
    pygame.mixer.music.load(music_path)  # Tải file nhạc vào pygame mixer
    pygame.mixer.music.play()  # Phát nhạc
