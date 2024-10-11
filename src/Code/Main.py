import pygame  # Nhập thư viện Pygame để phát triển game
from Maze import Maze  # Nhập lớp Maze từ tệp Maze
from pygame.locals import *  # Nhập các hằng số từ pygame.locals
from queue import PriorityQueue  # Nhập hàng đợi ưu tiên
import time  # Nhập thư viện time để làm việc với thời gian
from ControlPanel import ControlPanel  # Nhập lớp ControlPanel từ tệp ControlPanel
from AI import AI  # Nhập lớp AI từ tệp AI
from Algorithms import dijkstra, heuristic  # Nhập thuật toán dijkstra và heuristic từ tệp Algorithms

def main():
    pygame.init()  # Khởi tạo pygame
    width, height = 1000, 500  # Đặt kích thước cửa sổ game
    screen = pygame.display.set_mode((width, height))  # Tạo cửa sổ game với kích thước đã định
    pygame.mixer.init()  # Khởi tạo mixer cho âm thanh
    pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nhac.mp3")  # Tải nhạc từ đường dẫn
    pygame.mixer.music.set_volume(1.0)  # Đặt âm lượng của nhạc
    music_start_time = None  # Biến để lưu thời gian bắt đầu phát nhạc
    control_panel = ControlPanel(300, 500)  # Khởi tạo bảng điều khiển ControlPanel với kích thước
    maze = Maze(35, 25)  # Tạo mê cung với số hàng và số cột
    ai = AI(maze)  # Tạo AI và truyền mê cung vào
    auto_play = False  # Biến trạng thái tự động chơi
    shortest_path = None  # Biến để lưu đường đi ngắn nhất
    ai.maze = maze  # Gán mê cung cho AI
    start_time = None  # Biến lưu thời gian bắt đầu
    countdown_time = 120  # Đếm ngược thời gian (120 giây)
    running = True  # Biến theo dõi trạng thái trò chơi (đang chạy hay dừng)
    game_over = False  # Biến theo dõi trạng thái kết thúc trò chơi
    game_over_time = None  # Biến lưu thời gian khi game kết thúc
    maze_completed = False  # Biến theo dõi trạng thái hoàn thành mê cung
    congrats_display_time = None  # Biến lưu thời gian hiển thị thông báo chúc mừng
    game_over_display_time = None  # Biến lưu thời gian hiển thị thông báo game over

    while running:  # Vòng lặp chính của trò chơi
        current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại
        if ai.x == maze.end_x and ai.y == maze.end_y:  # Kiểm tra nếu AI đã đến điểm cuối của mê cung
            maze_completed = True  # Đặt biến hoàn thành mê cung thành True
        for event in pygame.event.get():  # Lấy tất cả các sự kiện
            if event.type == QUIT:  # Nếu nhấn nút thoát
                running = False  # Dừng trò chơi
            elif event.type == MOUSEBUTTONDOWN:  # Nếu nhấn chuột
                maze, ai = control_panel.handle_event(event, maze, ai)  # Xử lý sự kiện trên bảng điều khiển
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí chuột
                if 750 <= mouse_x <= 950 and 50 <= mouse_y <= 100:  # Nếu nhấn vào nút Auto Play
                    auto_play = True  # Bật chế độ tự động chơi
                    start_time = time.time()  # Lưu thời gian bắt đầu
                    pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nhac.mp3")  # Tải nhạc từ đường dẫn
                    pygame.mixer.music.play()  # Phát nhạc
                elif 750 <= mouse_x <= 950 and 150 <= mouse_y <= 200:  # Nếu nhấn vào nút AI Play
                    auto_play = True  # Bật chế độ AI chơi
                    shortest_path = dijkstra(maze)  # Tìm đường đi ngắn nhất với thuật toán Dijkstra
                    start_time = time.time()  # Lưu thời gian bắt đầu
                    pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nhac.mp3")  # Tải nhạc từ đường dẫn
                    pygame.mixer.music.play()  # Phát nhạc
                elif 750 <= mouse_x <= 950 and 250 <= mouse_y <= 300:  # Nếu nhấn vào nút Reset
                    maze = Maze(35, 25)  # Tạo lại mê cung mới
                    ai = AI(maze)  # Tạo lại AI cho mê cung mới
                    auto_play = False  # Tắt chế độ tự động chơi
                    shortest_path = None  # Đặt lại đường đi ngắn nhất
                    start_time = None  # Đặt lại thời gian bắt đầu
                    game_over = False  # Đặt lại trạng thái game over
                    game_over_time = None  # Đặt lại thời gian game over
                    pygame.mixer.music.stop()  # Dừng nhạc
                elif 750 <= mouse_x <= 950 and 350 <= mouse_y <= 400:  # Nếu nhấn vào nút Thoát
                    running = False  # Dừng trò chơi

            elif event.type == KEYDOWN and auto_play:  # Nếu nhấn phím và đang ở chế độ tự động chơi
                if not game_over:  # Kiểm tra nếu chưa game over
                    if event.key == K_UP:  # Nếu nhấn phím mũi tên lên
                        ai.move_towards(ai.x, ai.y - 1)  # Di chuyển AI lên trên
                    elif event.key == K_DOWN:  # Nếu nhấn phím mũi tên xuống
                        ai.move_towards(ai.x, ai.y + 1)  # Di chuyển AI xuống dưới
                    elif event.key == K_LEFT:  # Nếu nhấn phím mũi tên trái
                        ai.move_towards(ai.x - 1, ai.y)  # Di chuyển AI sang trái
                    elif event.key == K_RIGHT:  # Nếu nhấn phím mũi tên phải
                        ai.move_towards(ai.x + 1, ai.y)  # Di chuyển AI sang phải

            if ai.x == maze.end_x and ai.y == maze.end_y:  # Nếu AI đã đến điểm cuối
                if not game_over:  # Nếu chưa game over
                    game_over_time = time.time()  # Lưu thời gian khi game over
                    game_over = True  # Đặt trạng thái game over thành True
                    total_time = game_over_time - start_time  # Tính tổng thời gian chơi
                    start_time = None  # Dừng đếm thời gian
                    pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/dendich.mp3")  # Tải nhạc khi đến đích
                    pygame.mixer.music.play()  # Phát nhạc
                    congrats_display_time = pygame.time.get_ticks()  # Lưu thời gian hiển thị thông báo chúc mừng

        screen.fill((0, 0, 0))  # Tô màu nền đen cho màn hình
        maze.display_maze(screen, ai)  # Hiển thị mê cung
        control_panel.display(screen)  # Hiển thị bảng điều khiển

        if auto_play:  # Nếu đang ở chế độ tự động chơi
            if shortest_path:  # Nếu có đường đi ngắn nhất
                if len(shortest_path) > 1:  # Nếu đường đi còn nhiều bước
                    next_step = shortest_path.pop(1)  # Lấy bước tiếp theo
                    ai.move_towards(next_step[0], next_step[1])  # Di chuyển AI theo bước tiếp theo
            player_image = pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/icon.png")  # Tải hình ảnh người chơi
            cell_size = 20  # Kích thước mỗi ô trong mê cung
            player_image = pygame.transform.scale(player_image, (cell_size, cell_size))  # Thu nhỏ hình ảnh người chơi
            screen.blit(player_image, (ai.x * cell_size, ai.y * cell_size))  # Vẽ hình ảnh người chơi tại vị trí mới

        rewards_to_remove = []  # Danh sách để lưu các phần thưởng cần xóa
        play_reward_music = False  # Biến để theo dõi việc phát nhạc khi nhận phần thưởng

        for reward in maze.rewards:  # Duyệt qua tất cả các phần thưởng
            if (ai.x, ai.y) == reward:  # Nếu AI đến vị trí phần thưởng
                start_time += 3  # Cộng thêm 3 giây vào thời gian chơi
                rewards_to_remove.append(reward)  # Thêm phần thưởng vào danh sách cần xóa
                play_reward_music = True  # Đánh dấu phát nhạc

        for reward in rewards_to_remove:  # Loại bỏ phần thưởng đã thu thập
            maze.rewards.remove(reward)  # Xóa phần thưởng khỏi mê cung

        if play_reward_music:  # Nếu cần phát nhạc phần thưởng
            reward_channel = pygame.mixer.Channel(1)  # Tạo kênh riêng để phát nhạc
            reward_channel.play(pygame.mixer.Sound("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/trungthuong.mp3"))  # Phát nhạc phần thưởng

        if start_time is not None and not game_over:  # Nếu trò chơi chưa kết thúc và đang đếm thời gian
            elapsed_time = countdown_time - int(time.time() - start_time)  # Tính thời gian còn lại
            elapsed_time = max(0, elapsed_time)  # Đảm bảo thời gian không âm
            font = pygame.font.Font(None, 36)  # Thiết lập phông chữ
            time_text = font.render(f"TIME: {elapsed_time} S", True, (0, 0, 0))  # Tạo chuỗi hiển thị thời gian
            text_rect = time_text.get_rect()  # Tạo hình chữ nhật chứa văn bản
            text_rect.topright = (width - 100, 10)  # Đặt vị trí cho văn bản thời gian
            screen.blit(time_text, text_rect)  # Vẽ thời gian lên màn hình

            if elapsed_time == 0 and not maze_completed:  # Nếu hết thời gian và chưa hoàn thành mê cung
                game_over = True  # Đặt trạng thái game over thành True
                game_over_time = time.time()  # Lưu thời gian game over
                game_over_display_time = pygame.time.get_ticks()  # Lưu thời gian hiển thị thông báo game over
                pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/gameover.mp3")  # Tải nhạc game over
                pygame.mixer.music.play()  # Phát nhạc game over

        if congrats_display_time is not None:  # Nếu cần hiển thị thông báo chúc mừng
            elapsed_congrats_time = current_time - congrats_display_time  # Tính thời gian hiển thị thông báo
            if elapsed_congrats_time < 3000:  # Nếu đã dưới 3 giây
                pygame.draw.rect(screen, (0, 0, 0), (width // 2 - 150, height // 2 - 50, 300, 100))  # Vẽ nền đen
                font = pygame.font.Font(None, 48)  # Thiết lập phông chữ
                congrats_text = font.render("Congratulations!", True, (255, 255, 255))  # Hiển thị chữ "Congratulations"
                text_rect = congrats_text.get_rect(center=(width // 2, height // 2))  # Đặt vị trí cho văn bản
                screen.blit(congrats_text, text_rect)  # Vẽ văn bản lên màn hình
            else:
                congrats_display_time = None  # Dừng hiển thị thông báo chúc mừng

        if game_over_display_time is not None:  # Nếu cần hiển thị thông báo game over
            elapsed_game_over_time = current_time - game_over_display_time  # Tính thời gian hiển thị
            if elapsed_game_over_time < 3000:  # Nếu đã dưới 3 giây
                pygame.draw.rect(screen, (0, 0, 0), (width // 2 - 150, height // 2 - 50, 300, 100))  # Vẽ nền đen
                font = pygame.font.Font(None, 48)  # Thiết lập phông chữ
                game_over_text = font.render("Game Over!", True, (255, 255, 255))  # Hiển thị chữ "Game Over"
                text_rect = game_over_text.get_rect(center=(width // 2, height // 2))  # Đặt vị trí cho văn bản
                screen.blit(game_over_text, text_rect)  # Vẽ văn bản lên màn hình
            else:
                game_over_display_time = None  # Dừng hiển thị thông báo game over

        pygame.display.flip()  # Cập nhật màn hình
        pygame.time.delay(100)  # Dừng một chút giữa mỗi lần cập nhật

    pygame.quit()  # Thoát Pygame

if __name__ == "__main__":  # Điểm bắt đầu chương trình
    main()  # Gọi hàm main
