import pygame  # Nhập thư viện Pygame, hỗ trợ phát triển game, giao diện đồ họa.
import random  # Nhập thư viện random, hỗ trợ sinh số ngẫu nhiên.

class Maze:
    def __init__(self, width, height):  # Hàm khởi tạo đối tượng mê cung với chiều rộng và chiều cao.
        self.width = width  # Lưu trữ chiều rộng của mê cung.
        self.height = height  # Lưu trữ chiều cao của mê cung.
        self.grid = [[1] * width for _ in range(height)]  # Tạo lưới mê cung, khởi đầu tất cả các ô là tường (1).
        self.start_x, self.start_y = 1, 1  # Thiết lập điểm bắt đầu tại tọa độ (1, 1).
        self.end_x, self.end_y = width - 2, height - 2  # Thiết lập điểm kết thúc tại tọa độ (width-2, height-2).
        self.generate_maze()  # Gọi hàm generate_maze để tạo mê cung.
        self.grid[self.start_y][self.start_x] = 0  # Đặt ô bắt đầu là đường đi (0).
        self.grid[self.end_y][self.end_x] = 0  # Đặt ô kết thúc là đường đi (0).
        self.path = []  # Tạo danh sách lưu đường đi của người chơi.
        self.obstacles = set()  # Tạo tập hợp chứa chướng ngại vật.
        self.create_obstacles()  # Gọi hàm tạo chướng ngại vật.
        self.load_images()  # Gọi hàm tải hình ảnh các đối tượng trong mê cung.
        self.rewards = set()  # Tạo tập hợp chứa phần thưởng.
        self.create_rewards()  # Gọi hàm tạo phần thưởng.

    def load_images(self):  # Hàm tải hình ảnh từ các file trên hệ thống.
        cell_size = 20  # Kích thước mỗi ô trong mê cung là 20 pixel.
        self.obstacle_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/iconbom.png"), (cell_size, cell_size))  # Tải và thu nhỏ hình ảnh chướng ngại vật.
        self.reward_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/phanthuong.jpg"), (cell_size, cell_size))  # Tải và thu nhỏ hình ảnh phần thưởng.
        self.end_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/dautay.jpg"), (cell_size, cell_size))  # Tải và thu nhỏ hình ảnh điểm kết thúc.
        self.wall_image = pygame.transform.scale(pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/hangrao.jpg"), (cell_size, cell_size))  # Tải và thu nhỏ hình ảnh tường.

    def create_rewards(self):  # Hàm tạo phần thưởng.
        reward_count = 0  # Biến đếm số phần thưởng đã tạo.
        while reward_count < 10:  # Tạo 10 phần thưởng ngẫu nhiên.
            x = random.randint(1, self.width - 2)  # Chọn ngẫu nhiên tọa độ x trong mê cung.
            y = random.randint(1, self.height - 2)  # Chọn ngẫu nhiên tọa độ y trong mê cung.
            if self.grid[y][x] == 0 and (x, y) not in self.rewards and not self.has_adjacent_reward(x, y):  # Kiểm tra ô trống và không có phần thưởng lân cận.
                self.rewards.add((x, y))  # Thêm tọa độ phần thưởng vào tập hợp.
                reward_count += 1  # Tăng biến đếm phần thưởng lên.

    def has_adjacent_reward(self, x, y):  # Hàm kiểm tra có phần thưởng lân cận hay không.
        for dy in range(-1, 2):  # Duyệt các ô xung quanh.
            for dx in range(-1, 2):  # Duyệt các ô xung quanh.
                if (dx != 0 or dy != 0) and (x + dx, y + dy) in self.rewards:  # Nếu có phần thưởng ở lân cận thì trả về True.
                    return True
        return False  # Nếu không có thì trả về False.

    def create_obstacles(self):  # Hàm tạo chướng ngại vật.
        obstacle_count = 0  # Biến đếm số chướng ngại vật đã tạo.
        while obstacle_count < 20:  # Tạo 20 chướng ngại vật ngẫu nhiên.
            x = random.randint(1, self.width - 2)  # Chọn ngẫu nhiên tọa độ x.
            y = random.randint(1, self.height - 2)  # Chọn ngẫu nhiên tọa độ y.
            if self.grid[y][x] == 1 and (x, y) != (self.start_x, self.start_y) and (x, y) != (self.end_x, self.end_y) and self.is_far_from_obstacles(x, y):  # Kiểm tra ô có hợp lệ để đặt chướng ngại vật không.
                self.obstacles.add((x, y))  # Thêm tọa độ chướng ngại vật vào tập hợp.
                obstacle_count += 1  # Tăng biến đếm chướng ngại vật lên.

    def is_far_from_obstacles(self, x, y):  # Hàm kiểm tra chướng ngại vật có xa các chướng ngại vật khác không.
        min_distance = 5  # Khoảng cách tối thiểu giữa các chướng ngại vật.
        for obstacle in self.obstacles:  # Duyệt qua tất cả các chướng ngại vật đã có.
            obstacle_x, obstacle_y = obstacle  # Lấy tọa độ chướng ngại vật.
            distance = abs(x - obstacle_x) + abs(y - obstacle_y)  # Tính khoảng cách Manhattan.
            if distance < min_distance:  # Nếu khoảng cách nhỏ hơn khoảng cách tối thiểu.
                return False  # Không hợp lệ, trả về False.
        return True  # Hợp lệ, trả về True.

    def generate_maze(self):  # Hàm sinh mê cung ngẫu nhiên.
        for x in range(self.width):  # Thiết lập tường trên và dưới của mê cung.
            self.grid[0][x] = 1
            self.grid[self.height - 1][x] = 1
        for y in range(self.height):  # Thiết lập tường trái và phải của mê cung.
            self.grid[y][0] = 1
            self.grid[y][self.width - 1] = 1

        stack = [(1, 1)]  # Sử dụng ngăn xếp để lưu trữ các ô đã thăm.
        while stack:  # Lặp lại cho đến khi ngăn xếp trống.
            x, y = stack[-1]  # Lấy ô hiện tại từ ngăn xếp.
            neighbors = [(x + dx, y + dy) for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)] if 0 < x + dx < self.width - 1 and 0 < y + dy < self.height - 1]  # Lấy các ô lân cận chưa thăm.
            unvisited_neighbors = [neighbor for neighbor in neighbors if self.grid[neighbor[1]][neighbor[0]] == 1]  # Lọc các ô chưa thăm.
            if unvisited_neighbors:  # Nếu có ô chưa thăm.
                nx, ny = random.choice(unvisited_neighbors)  # Chọn ngẫu nhiên một ô chưa thăm.
                self.grid[ny][nx] = 0  # Đặt ô đó thành đường đi (0).
                self.grid[y + (ny - y) // 2][x + (nx - x) // 2] = 0  # Đặt ô trung gian giữa hai ô làm đường đi.
                stack.append((nx, ny))  # Thêm ô mới vào ngăn xếp.
            else:
                stack.pop()  # Nếu không có ô nào chưa thăm, loại bỏ ô hiện tại khỏi ngăn xếp.

    def display_maze(self, screen, ai):  # Hàm hiển thị mê cung lên màn hình.
        cell_size = 20  # Kích thước mỗi ô trong mê cung là 20 pixel.
        START_COLOR = (135, 206, 250)  # Màu cho điểm bắt đầu.
        END_COLOR = (34, 139, 34)  # Màu cho điểm kết thúc.
        PLAYER_PATH_COLOR = (255, 99, 71)  # Màu cho đường đi của người chơi.
        AI_PATH_COLOR = (100, 149, 237)  # Màu cho đường đi của AI.
        OBSTACLE_COLOR = (80, 80, 80)  # Màu cho chướng ngại vật.
        REWARD_COLOR = (255, 215, 0)  # Màu cho phần thưởng.
        WALL_COLOR = (112, 128, 144)  # Màu cho tường.
        EMPTY_COLOR = (245, 245, 245)  # Màu cho ô trống.
        VISITED_COLOR = (144, 238, 144)  # Màu cho các ô đã thăm.

        for y in range(self.height):  # Duyệt qua từng ô của mê cung.
            for x in range(self.width):
                rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)  # Tạo một hình chữ nhật đại diện cho ô.
                if (x, y) == (self.start_x, self.start_y):  # Nếu là điểm bắt đầu.
                    pygame.draw.rect(screen, START_COLOR, rect)  # Vẽ ô với màu bắt đầu.
                elif (x, y) == (self.end_x, self.end_y):  # Nếu là điểm kết thúc.
                    screen.blit(self.end_image, rect.topleft)  # Vẽ hình ảnh kết thúc.
                elif (x, y) in self.path:  # Nếu là đường đi của người chơi.
                    pygame.draw.rect(screen, PLAYER_PATH_COLOR, rect)  # Vẽ ô với màu đường đi.
                elif (x, y) in ai.path:  # Nếu là đường đi của AI.
                    pygame.draw.rect(screen, AI_PATH_COLOR, rect)  # Vẽ ô với màu đường đi của AI.
                elif (x, y) in self.obstacles:  # Nếu là chướng ngại vật.
                    screen.blit(self.obstacle_image, rect.topleft)  # Vẽ hình ảnh chướng ngại vật.
                elif (x, y) in self.rewards:  # Nếu là phần thưởng.
                    screen.blit(self.reward_image, rect.topleft)  # Vẽ hình ảnh phần thưởng.
                elif self.grid[y][x] == 1:  # Nếu là tường.
                    screen.blit(self.wall_image, rect.topleft)  # Vẽ hình ảnh tường.
                else:
                    pygame.draw.rect(screen, EMPTY_COLOR, rect)  # Vẽ ô trống.

        path_color = VISITED_COLOR  # Màu cho các ô đã thăm.
        if ai.x == self.end_x and ai.y == self.end_y:  # Nếu AI đã đến điểm kết thúc.
            for step in ai.path:  # Vẽ lại toàn bộ đường đi của AI.
                x, y = step
                pygame.draw.rect(screen, path_color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
        else:
            for step in self.path:  # Vẽ lại toàn bộ đường đi của người chơi.
                x, y = step
                pygame.draw.rect(screen, path_color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

    def get_neighbors(self, x, y):  # Hàm lấy các ô lân cận có thể đi qua.
        neighbors = []  # Danh sách các ô lân cận.
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Duyệt các ô lân cận theo 4 hướng.
            nx, ny = x + dx, y + dy  # Tính tọa độ lân cận.
            if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] == 0:  # Nếu ô lân cận hợp lệ và là đường đi.
                neighbors.append((nx, ny))  # Thêm ô vào danh sách.
        return neighbors  # Trả về danh sách ô lân cận có thể đi qua.
