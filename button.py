import pygame


class Button():
    def __init__(self, x, y, image, single_click_button):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.single_click_button = single_click_button

    def draw(self, surface):
        action = False
        # get mouse pos
        pos = pygame.mouse.get_pos()
        # check mouseover and click
        if self.rect.collidepoint(pos) and self.clicked == False:
            if pygame.mouse.get_pressed()[0]:
                action = True
                if self.single_click_button:
                    self.clicked = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, self.rect)

        return action
