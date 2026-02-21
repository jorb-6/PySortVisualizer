import pygame

eventBindings = {}
keyBindings = [{},{},{}]

MonitorSize = (-1,-1)
Fullscreen = (-1,-2)

OnPress = 0
OnRelease = 1
OnChange = 2

def setup(scrsize: tuple[int, int]):
    # Just the normal pygame inits
    pygame.init()
    if scrsize == MonitorSize:
        info = pygame.display.Info()
        screen = pygame.display.set_mode((info.current_w, info.current_h))
    elif scrsize == Fullscreen:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(scrsize)
    clock = pygame.time.Clock()
    return screen, clock

def addEvent(event: str, function):
    eventBindings[getattr(pygame, event)] = function

def addKeyEvent(key: str, function, mode: int = 0):
    keyBindings[mode][getattr(pygame, 'K_' + key)] = (function)

def handleEvents():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            try:
                keyBindings[0][event.key]()
                keyBindings[2][event.key]()
            except KeyError:
                pass
        if event.type == pygame.KEYUP:
            try:
                keyBindings[1][event.key]()
                keyBindings[2][event.key]()
            except KeyError:
                pass
        try:
            eventBindings[event.type]()
        except KeyError:
            pass

def blit():
   pygame.display.flip()

def quit():
    pygame.quit()

colorNames = {
    # Pure / reference colors
    "Really Red": (255, 0, 0),
    "Really Green": (0, 255, 0),
    "Really Blue": (0, 0, 255),
    "White": (255, 255, 255),
    "Black": (0, 0, 0),

    # Greys
    "Light Grey": (200, 200, 200),
    "Grey": (128, 128, 128),
    "Dark Grey": (64, 64, 64),

    # Alternate spelling of gray
    "Light Gray": (200, 200, 200),
    "Gray": (128, 128, 128),
    "Dark Gray": (64, 64, 64),


    # Secondary colors
    "Yellow": (255, 255, 0),
    "Cyan": (0, 255, 255),
    "Magenta": (255, 0, 255),

    # Warm colors
    "Orange": (255, 165, 0),
    "Coral": (255, 127, 80),
    "Pink": (255, 105, 180),
    "Hot Pink": (255, 20, 147),
    "Red Brown": (165, 42, 42),

    # Cool colors
    "Sky Blue": (135, 206, 235),
    "Steel Blue": (70, 130, 180),
    "Navy Blue": (0, 0, 128),
    "Teal": (0, 128, 128),
    "Turquoise": (64, 224, 208),

    # Greens
    "Lime": (50, 205, 50),
    "Forest Green": (34, 139, 34),
    "Olive": (128, 128, 0),

    # Browns / earth tones
    "Brown": (139, 69, 19),
    "Saddle Brown": (139, 69, 19),
    "Tan": (210, 180, 140),

    # Purples
    "Purple": (128, 0, 128),
    "Indigo": (75, 0, 130),
    "Violet": (238, 130, 238),
}

def setColor(name: str, color: tuple[int, int, int]):
    colorNames[name] = color

class RGBA():
    r, g, b, a = (0, 0, 0, 1)

    def __init__(self, color: tuple[int, int, int] | str, opacity: int = 1):
        if type(color) == str:
            if color[0] == '#':
                color = str(color[1:])
                color = (
                    int(color[0:2], 16),
                    int(color[2:4], 16),
                    int(color[4:6], 16)
                )
            else:
                color = colorNames[str(color)]
        
        self.r = min(max(int(color[0]), 0), 255)
        self.g = min(max(int(color[1]), 0), 255)
        self.b = min(max(int(color[2]), 0), 255)
        self.a = min(max(opacity, 0), 1)
    
    def getTuple(self, A = False) -> tuple:
        return (self.r, self.g, self.b, self.a)
 
class rect:
    def __init__(self, pos: tuple[int,int], size: tuple[int,int], color: RGBA):
        self.pos = pos
        self.size = size
        self.color = color
    
    def draw(self, surface):
        if self.color.a == 1:
            pygame.draw.rect(surface, self.color.getTuple(), pygame.rect.Rect(self.pos, self.size))

class font:
    def __init__(self, font: str | None, size: int, sysfont: bool = True, bold: bool = False, italic: bool = False, underline: bool = False, strikethrough: bool = False):
        if sysfont:
            self.font = pygame.font.SysFont(font, size, bold, italic)
        else:
            self.font = pygame.font.Font(font, size)
            self.font.bold = bold
            self.font.italic = italic
        self.font.underline = underline
        self.font.strikethrough = strikethrough
    
    def get(self):
        return self.font

class text:
    def __init__(self, pos: tuple[int, int], color: RGBA, text: str, font: font):
        self.pos = pos
        self.color = color
        self.text = text
        self.font = font
    
    def draw(self, surface, antialias: bool = False):
        textSurface = self.font.get().render(self.text, antialias, self.color.getTuple())
        surface.blit(textSurface, self.pos)
    
    def getSize(self):
        return self.font.get().size(self.text)

class button:
    def __init__(self, pos: tuple[int,int], size: tuple[int,int], onClick, color: RGBA = RGBA('Black'), hoverColor: RGBA = RGBA('Grey')):
        self.rect = rect(pos, size, color)
        self.hover = False
        self.click = onClick
        self.color = color
        self.hoverColor = hoverColor
    
    def update(self):
        self.updateHoverState()
        self.updateClick()

    def updateHoverState(self):
        mx, my = pygame.mouse.get_pos()
        x = mx > self.rect.pos[0] and mx < self.rect.pos[0] + self.rect.size[0]
        y = my > self.rect.pos[1] and my < self.rect.pos[1] + self.rect.size[1]
        if x and y:
            self.hover = True
            self.rect.color = self.hoverColor
        else:
            self.hover = False
            self.rect.color = self.color
    
    def updateClick(self):
        if self.hover and pygame.mouse.get_pressed()[0]:
            self.click()

    def draw(self, surface):
        self.rect.draw(surface)

class textButton(button):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], onClick, text: text, color: RGBA = RGBA('Black'), hoverColor: RGBA = RGBA('Grey')):
        super().__init__(pos, size, color, onClick, hoverColor)
        self.text = text
    
    def draw(self, surface, antialias: bool = False):
        super().draw(surface)
        self.text.draw(surface, antialias)
