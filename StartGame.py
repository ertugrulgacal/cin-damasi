import pygame
import sys

# Initialize the game engine
pygame.init()

# Set display screen size
screen = pygame.display.set_mode((512, 512))

# Set caption for the game window
pygame.display.set_caption("Pygame Input Example")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (126, 126, 126)

# Initialize font for the buttons
font = pygame.font.Font(None, 36)

# Function to render text for buttons
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

# Function to create button
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    textSurf, textRect = text_objects(msg, font)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

# Function to initialize white screen
def init_white_screen():
    print(input_text)

# Function to quit the game
def quit():
    pygame.quit()
    sys.exit()

# Initialize text input field
input_field = pygame.Rect(100, 150, 140, 32)

# Initialize input text
input_text = ""

# Game loop
running = True
while running:
    screen.fill((30, 30, 30))
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Set the `START_GAME_CONSTANT` variable to the value entered in the text input field
                START_GAME_CONSTANT = input_text
                print(START_GAME_CONSTANT)
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                input_text += event.unicode

    # Render text input field
    pygame.draw.rect(screen, white, input_field)
    input_text_surface = font.render(input_text, True, black)
    input_field.w = max(100, input_text_surface.get_width()+10)
    screen.blit(input_text_surface, (input_field.x+5, input_field.y+5))

    # Create buttons
    button("Initialize White Screen", 10, 10, 180, 50, black, gray, init_white_screen)
    button("Quit", 210, 10, 180, 50, black, gray, quit)

    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()

# import pygame
# import sys
#
# # pygame.init() will initialize all
# # imported module
# pygame.init()
#
# clock = pygame.time.Clock()
#
# # it will display on screen
# screen = pygame.display.set_mode([600, 500])
#
# # basic font for user typed
# base_font = pygame.font.Font(None, 32)
# user_text = ''
#
# # create rectangle
# input_rect = pygame.Rect(200, 200, 140, 32)
#
# # color_active stores color(lightskyblue3) which
# # gets active when input box is clicked by user
# color_active = pygame.Color('lightskyblue3')
#
# # color_passive store color(chartreuse4) which is
# # color of input box.
# color_passive = pygame.Color('chartreuse4')
# color = color_passive
#
# active = False
#
# while True:
#     for event in pygame.event.get():
#
#         # if user types QUIT then the screen will close
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if input_rect.collidepoint(event.pos):
#                 active = True
#             else:
#                 active = False
#
#         if event.type == pygame.KEYDOWN:
#
#             # Check for backspace
#             if event.key == pygame.K_BACKSPACE:
#
#                 # get text input from 0 to -1 i.e. end.
#                 user_text = user_text[:-1]
#
#             # Unicode standard is used for string
#             # formation
#             else:
#                 user_text += event.unicode
#
#     # it will set background color of screen
#     screen.fill((255, 255, 255))
#
#     if active:
#         color = color_active
#     else:
#         color = color_passive
#
#     # draw rectangle and argument passed which should
#     # be on screen
#     pygame.draw.rect(screen, color, input_rect)
#
#     text_surface = base_font.render(user_text, True, (255, 255, 255))
#
#     # render at position stated in arguments
#     screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
#
#     # set width of textfield so that text cannot get
#     # outside of user's text input
#     input_rect.w = max(100, text_surface.get_width() + 10)
#
#     # display.flip() will update only a portion of the
#     # screen to updated, not full area
#     pygame.display.flip()
#
#     # clock.tick(60) means that for every second at most
#     # 60 frames should be passed.
#     clock.tick(60)