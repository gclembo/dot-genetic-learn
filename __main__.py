import game_master
import pygame

window_width = 1000
window_height = 800
target_x = 100
target_y = 400
dot_start_x = 800
dot_start_y = 600
num_dots = 30
num_steps = 20
pause_time = 0.1
num_generations = 20


def main():
    gm = game_master.GameMaster(dot_start_x, dot_start_y, num_dots, target_x, target_y)

    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    window.fill((255, 255, 255))
    pygame.display.flip()

    pygame.draw.circle(window, (255, 0, 0), (target_x, target_y), 5)
    pygame.display.update()

    gm.run_generation(window, num_steps, pause_time)

    for i in range(num_generations):
        gm.reproduce_dots()
        gm.run_generation(window, num_steps, pause_time)

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False


if __name__ == "__main__":
    main()
