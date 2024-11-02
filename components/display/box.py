import pygame


class Box:
    id_counter = 0

    def __init__(
        self,
        width,
        height,
        bg_color,
        border_color,
    ):
        self.id = Box.id_counter
        Box.id_counter += 1
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.bg_color = bg_color
        self.border_color = border_color
        self.child_boxes = {}
        self.box_content = None

    def draw(self):
        if self.bg_color:
            self.surface.fill(self.bg_color)

        if isinstance(self.box_content, TextContent):
            self.box_content.draw(self.surface, (0, 0))
        elif isinstance(self.box_content, ImageContent):
            self.box_content.draw(self.surface, (0, 0), (self.width, self.height))

        for box_location in self.child_boxes.values():
            child_box: Box = box_location["box"]
            child_box_location = box_location["location"]
            child_box_surface = child_box.draw()
            self.surface.blit(child_box_surface, child_box_location)

        if self.border_color:
            pygame.draw.rect(
                self.surface,
                self.border_color,
                (0, 0, self.width, self.height),
                2,
            )
        return self.surface

    def increase_relative_position(self, location):
        self.x += location[0]
        self.y += location[1]
        for box_location in self.child_boxes.values():
            child_box: Box = box_location["box"]
            child_box.increase_relative_position(location)

    def add_box(self, child_box: "Box", location):
        child_box.increase_relative_position(location)
        self.child_boxes[child_box.id] = {"box": child_box, "location": location}

    def is_collide(self, pos):
        for box_location in self.child_boxes.values():
            child_box: Box = box_location["box"]
            if child_box.is_collide(pos):
                return True
        print(self.surface.get_rect(topleft=(self.x, self.y)))
        if self.surface.get_rect(topleft=(self.x, self.y)).collidepoint(pos):
            self.bg_color = (255, 0, 0)
            return True


class BoxContent:
    def __init__(self) -> None:
        pass

    def draw(self):
        pass


class TextContent(BoxContent):
    def __init__(self, text) -> None:
        super().__init__()
        self.text = text

    def draw(self, surface: pygame.Surface, location):
        text_surface = font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, location)


class ImageContent(BoxContent):

    def __init__(self, img) -> None:
        super().__init__()
        self.img = img

    def draw(self, surface: pygame.Surface, location, scale):
        image_surface = pygame.transform.scale(self.img, scale)
        surface.blit(image_surface, location)


# b1 -> b2 -> b3

bg_color = (175, 175, 175)

b = Box(300, 125, bg_color, (0, 0, 0))

c_b1 = Box(25, 25, bg_color, (0, 0, 0))
header = Box(300, 25, bg_color, None)
header.add_box(c_b1, (275, 0))

right_bar = Box(50, 100, bg_color, None)

arrow_up_box = Box(50, 50, bg_color, (0, 0, 0))
arrow_up_content = ImageContent(pygame.image.load("data/sprites/arrow_up.png"))
arrow_up_box.box_content = arrow_up_content
arrow_down_box = Box(50, 50, bg_color, (0, 0, 0))
arrow_down_content = ImageContent(pygame.image.load("data/sprites/arrow_down.png"))
arrow_down_box.box_content = arrow_down_content

right_bar.add_box(arrow_up_box, (0, 0))
right_bar.add_box(arrow_down_box, (0, 50))


char_box = Box(250, 50, bg_color, None)

avt_box = Box(25, 25, bg_color, None)
char_box.add_box(avt_box, (0, 0))

level_box = Box(50, 25, bg_color, None)
char_box.add_box(level_box, (25, 0))

exp_box = Box(100, 25, bg_color, None)
char_box.add_box(exp_box, (75, 0))

power_box = Box(75, 25, bg_color, None)
char_box.add_box(power_box, (175, 0))

info_box = Box(150, 25, bg_color, None)
char_box.add_box(info_box, (0, 25))

hp_box = Box(100, 25, bg_color, None)
char_box.add_box(hp_box, (150, 25))

b.add_box(header, (0, 0))
b.add_box(right_bar, (250, 25))
b.add_box(char_box, (0, 25))
b.increase_relative_position((50, 50))

avt_content = ImageContent(pygame.image.load("data/sprites/character3.png"))
avt_box.box_content = avt_content

level_content = TextContent("11")
level_box.box_content = level_content

exp_content = TextContent("127/250")
exp_box.box_content = exp_content

power_content = TextContent("37")
power_box.box_content = power_content

hp_content = TextContent("16/303")
hp_box.box_content = hp_content

info_content = TextContent("128@Human")
info_box.box_content = info_content


# Initialize Pygame
pygame.init()


font = pygame.font.Font(None, 25)

# Screen settings
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Scrollable Health Status Window")

running = True
while running:
    screen.fill((200, 200, 200))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            b.is_collide(event.pos)

    box_surface = b.draw()
    screen.blit(box_surface, (50, 50))

    pygame.display.flip()
