import pygame
import sys
import subprocess

# Khởi tạo Pygame
pygame.init()

# Đường dẫn đến file nhạc nền
music_path = "C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nenstart.mp3"
# Đường dẫn đến file âm thanh hiệu ứng cho nút START
start_sound_path = "C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/button_click.mp3"

# Kích thước màn hình
SCREEN_WIDTH = 1000 
SCREEN_HEIGHT = 500
# Tạo cửa sổ game với kích thước đã chỉ định
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Đặt tiêu đề cho cửa sổ game
pygame.display.set_caption("WELCOME THE MAZE GAME")

# Phát nhạc nền
pygame.mixer.music.load(music_path)  # Tải file nhạc nền
pygame.mixer.music.play(-1)  # Phát nhạc lặp vô hạn

# Tải âm thanh hiệu ứng khi nhấn nút START
start_sound = pygame.mixer.Sound(start_sound_path)

# Màu sắc được sử dụng trong game
WHITE = (255, 255, 255)  # Màu trắng
BLACK = (0, 0, 0)  # Màu đen

# Font chữ
font = pygame.font.SysFont(None, 36)  # Khởi tạo font chữ với kích thước 36

# Định nghĩa biến start_button ở đây để trở thành biến toàn cục và căn giữa màn hình
button_width = 200  # Chiều rộng nút START
button_height = 50  # Chiều cao nút START
start_button_x = (SCREEN_WIDTH - button_width) // 2  # Tính toán vị trí ngang của nút START
start_button_y = (SCREEN_HEIGHT - button_height) // 2  # Tính toán vị trí dọc của nút START
start_button = pygame.Rect(start_button_x, start_button_y, button_width, button_height)  # Tạo hình chữ nhật cho nút START

# Hàm vẽ màn hình bắt đầu
def draw_start_screen():
    # Load hình nền cho màn hình bắt đầu
    background = pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/wellcome.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Thay đổi kích thước hình nền cho khớp với kích thước màn hình
    
    # Vẽ hình nền
    screen.blit(background, (0, 0))  # Vẽ hình nền lên màn hình
    
    # Vẽ văn bản và nút START lên màn hình
    text = font.render("Welcome to the maze game", True, BLACK)  # Tạo văn bản chào mừng
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))  # Căn giữa văn bản
    screen.blit(text, text_rect)  # Vẽ văn bản lên màn hình
    
    # Vẽ nút START
    pygame.draw.rect(screen, BLACK, start_button)  # Vẽ hình chữ nhật đại diện cho nút START
    start_text = font.render("START", True, WHITE)  # Tạo văn bản "START" cho nút
    start_text_rect = start_text.get_rect(center=start_button.center)  # Căn chỉnh văn bản vào giữa nút
    screen.blit(start_text, start_text_rect)  # Vẽ văn bản lên nút
    
    pygame.display.flip()  # Cập nhật màn hình hiển thị

# Hàm chính của game
def main():
    running = True  # Biến điều khiển vòng lặp chính
    transition_started = False  # Kiểm soát việc hiệu ứng chuyển cảnh có bắt đầu hay không
    
    # Khởi tạo và phát nhạc nền cho màn hình bắt đầu
    pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nenstart.mp3")
    pygame.mixer.music.play(-1)  # Phát nhạc nền lặp vô hạn
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Khi người dùng đóng cửa sổ
                running = False  # Kết thúc vòng lặp và đóng ứng dụng
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Khi người dùng nhấp chuột
                if start_button.collidepoint(event.pos):  # Kiểm tra xem vị trí nhấp chuột có nằm trong nút START không
                    start_sound.play()  # Phát âm thanh khi nút START được nhấp
                    pygame.mixer.music.fadeout(500)  # Giảm dần âm lượng nhạc nền trong 0.5 giây
                    transition_started = True  # Bắt đầu hiệu ứng chuyển cảnh
        
        # Kiểm tra nếu hiệu ứng chuyển cảnh đã bắt đầu
        if transition_started:
            transition_effect()  # Thực hiện hiệu ứng chuyển cảnh
            if run_external_script():  # Nếu script bên ngoài được chạy thành công
                running = False  # Kết thúc vòng lặp chính
        
        draw_start_screen()  # Vẽ màn hình bắt đầu trong mỗi vòng lặp
    
    quit_game()  # Thoát game sau khi vòng lặp kết thúc

# Hàm để chạy script bên ngoài (ví dụ: Main.py)
def run_external_script():
    try:
        # Đường dẫn đến file Main.py và chạy nó bằng subprocess
        main_py_path = r"C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Code/Main.py"
        subprocess.Popen(["python", "-u", main_py_path])  # Chạy file Main.py
        return True  # Trả về True nếu chạy thành công
    except Exception as e:
        # Hiển thị lỗi nếu có vấn đề khi chạy script
        print(f"Đã xảy ra lỗi khi chạy Main.py: {e}")
        return False

# Hàm tạo hiệu ứng chuyển cảnh
def transition_effect():
    # Thêm hiệu ứng chuyển cảnh (ví dụ: fade out, trượt màn hình)
    for alpha in range(0, 255, 5):  # Tăng dần giá trị alpha để tạo hiệu ứng mờ dần
        overlay = pygame.Surface(screen.get_size())  # Tạo bề mặt mới có kích thước bằng màn hình
        overlay.set_alpha(alpha)  # Đặt độ trong suốt cho bề mặt
        overlay.fill((0, 0, 0))  # Tô bề mặt với màu đen
        screen.blit(overlay, (0, 0))  # Vẽ bề mặt lên màn hình
        pygame.display.update()  # Cập nhật màn hình
        pygame.time.delay(10)  # Tạo độ trễ giữa các lần cập nhật để tạo hiệu ứng mượt mà

# Hàm thoát game
def quit_game():
    # Thoát game và đóng ứng dụng
    pygame.quit()  # Thoát khỏi Pygame
    sys.exit()  # Đóng ứng dụng

# Chạy hàm main khi chương trình bắt đầu
if __name__ == "__main__":
    main()  # Chạy hàm main
