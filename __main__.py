import game_master
import pygame

window_width = 1000  # display window width
window_height = 800  # display window height
target_x = 100  # x coord to target
target_y = 400  # y coord to target
dot_start_x = 800  # dot starting x coord
dot_start_y = 600  # dot starting y coord
num_dots = 30  # number of dots in each generation
num_steps = 20  # number of steps in each generation
pause_time = 0.1  # time inbetween steps in each generation
num_generations = 20  # number of generators to run


def main():
    gm = game_master.GameMaster(dot_start_x, dot_start_y, num_dots, target_x, target_y)

    # Starts pygame window
    pygame.init()
    window = pygame.display.set_mode((window_width, window_height))
    window.fill((255, 255, 255))
    pygame.display.flip()

    # Runs generations
    gm.run_generation(window, num_steps, pause_time)
    for i in range(num_generations - 1):
        gm.reproduce_dots()
        gm.run_generation(window, num_steps, pause_time)

    # Wait for window to  be closed
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False


if __name__ == "__main__":
    main()
