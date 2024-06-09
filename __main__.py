import pygame, game_master

height = 800
width = 1000
target_x = 400
target_y = 400


def main():
    gm = game_master.GameMaster(600, 600, 30, target_x, target_y)

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

    best = gm.dots[0]

    best.reset(200, 400)
    window.fill((255, 255, 255))

    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False


if __name__ == "__main__":
    main()
