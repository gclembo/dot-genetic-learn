import game_master
import pygame

width = 1000
height = 800
target_x = 200
target_y = 200
dot_start_x = width - 200
dot_start_y = height - 200


def main():
    gm = game_master.GameMaster(dot_start_x, dot_start_y, 30, target_x, target_y)

    pygame.init()
    window = pygame.display.set_mode((width, height))
    window.fill((255, 255, 255))
    pygame.display.flip()

    pygame.draw.circle(window, (255, 0, 0), (target_x, target_y), 5)
    pygame.display.update()

    gm.run_generation(window, 20, 0.1)

    for i in range(30):
        gm.reproduce_dots()
        gm.run_generation(window, 20, 0.1)

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False


if __name__ == "__main__":
    main()
