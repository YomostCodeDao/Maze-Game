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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("WELCOME THE MAZE GAME")

# Phát nhạc nền
pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)  # Phát liên tục

# Tải âm thanh hiệu ứng
start_sound = pygame.mixer.Sound(start_sound_path)

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 36)

# Định nghĩa biến start_button ở đây để trở thành biến toàn cục và căn giữa màn hình
button_width = 200
button_height = 50
start_button_x = (SCREEN_WIDTH - button_width) // 2
start_button_y = (SCREEN_HEIGHT - button_height) // 2
start_button = pygame.Rect(start_button_x, start_button_y, button_width, button_height)

def draw_start_screen():
    # Load hình nền
    background = pygame.image.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Picture/wellcome.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Vẽ hình nền
    screen.blit(background, (0, 0))
    
    # Vẽ văn bản và nút bắt đầu trên hình nền
    text = font.render("Welcome to the maze game", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    
    pygame.draw.rect(screen, BLACK, start_button)
    start_text = font.render("START", True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    pygame.display.flip()


def main():
    running = True
    transition_started = False  # Để kiểm soát hiệu ứng chuyển cảnh
    # Khởi tạo âm thanh nền cho màn hình bắt đầu
    pygame.mixer.music.load("C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Music/nenstart.mp3")
    pygame.mixer.music.play(-1)  # Phát lặp vô hạn
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    # Phát âm thanh khi nút START được nhấp
                    start_sound.play()
                    # Dừng âm thanh nền
                    pygame.mixer.music.fadeout(500)  # Tắt dần âm thanh nền trong 0.5 giây
                    # Bắt đầu hiệu ứng chuyển cảnh
                    transition_started = True
        # Kiểm soát hiệu ứng chuyển cảnh
        if transition_started:
            # Vẽ hiệu ứng fade hoặc bất kỳ hiệu ứng nào
            transition_effect()
            # Sau khi hoàn thành hiệu ứng, khởi chạy tệp Main.py
            if run_external_script():
                running = False  # Kết thúc vòng lặp nếu script khởi chạy thành công
        draw_start_screen()
    # Thoát game sau khi kết thúc vòng lặp
    quit_game()

def run_external_script():
    try:
        main_py_path = r"C:/Users/ASUS/Desktop/Yomost File/CDIO/GameTTNT/src/Code/Main.py"
        subprocess.Popen(["python", "-u", main_py_path])
        return True
    except Exception as e:
        print(f"Đã xảy ra lỗi khi chạy Main.py: {e}")
        return False

def transition_effect():
    # Thêm các hiệu ứng chuyển cảnh (ví dụ: fade out, trượt màn hình, v.v.)
    # Ví dụ hiệu ứng fade ra màn hình đen
    for alpha in range(0, 255, 5):
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(alpha)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)

def quit_game():
    pygame.quit()
    sys.exit()



if __name__ == "__main__":
    main()
