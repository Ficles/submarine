import pygame
from math import *

class Radar:
    def __init__(self, size, speed, distance):
        self.size = size
        self.speed = speed
        self.distance = distance
        self.__clock__ = pygame.time.Clock()
        self.angle = 0
        self.points = []

    def tick(self, points):
        delta = self.__clock__.tick()
        distance = delta * (360 / (1000 * self.speed))
        prev_angle = self.angle
        self.angle = prev_angle + distance
        current_angle = self.angle
        if self.angle > 360:
            self.angle -= 360

        for point in self.points:
            point["age"] += distance
            if point["age"] >= 270:
                self.points.remove(point)

        for point in points:
            point_angle = degrees(atan2(point["pos"][1], point["pos"][0]))
            if point_angle < 0:
                point_angle += 360
            if prev_angle < point_angle <= current_angle:
                self.points.append({"pos": point["pos"], "colour": point["colour"], "age": 0})

    def draw(self):
        canvas = pygame.Surface((self.size+1, self.size+1), flags=pygame.SRCALPHA)

        pygame.draw.aacircle(canvas, (0,0,0), (self.size/2, self.size/2), self.size/2)
        pygame.draw.aacircle(canvas, (60, 60, 60), (self.size/2, self.size/2), self.size/6, 2)
        pygame.draw.aacircle(canvas, (60, 60, 60), (self.size/2, self.size/2), self.size/3, 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size/2, 0), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size/2 + self.size/2 * sqrt(0.5), self.size/2 - self.size/2 * sqrt(0.5)), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size, self.size/2), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size/2 + self.size/2 * sqrt(0.5), self.size/2 + self.size/2 * sqrt(0.5)), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size/2, self.size), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size/2 - self.size/2 * sqrt(0.5), self.size/2 + self.size/2 * sqrt(0.5)), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (0, self.size/2), 2)
        pygame.draw.aaline(canvas, (60, 60, 60), (self.size/2, self.size/2), (self.size/2 - self.size/2 * sqrt(0.5), self.size/2 - self.size/2 * sqrt(0.5)), 2)
        pygame.draw.aacircle(canvas, "white", (self.size/2, self.size/2), self.size/2, 3)

        x = cos(radians(self.angle)) * (self.size/2)
        y = sin(radians(self.angle)) * (self.size/2)
        x += self.size/2
        y += self.size/2
        pygame.draw.aaline(canvas, "green", (self.size/2, self.size/2), (x, y), 2)

        for point in self.points:
            x = (point["pos"][0]/self.distance) * (self.size/2) + self.size/2
            y = (point["pos"][1]/self.distance) * (self.size/2) + self.size/2
            colour = point["colour"]
            colour[3] = ((270-point["age"])/270)*255
            pygame.draw.circle(canvas, point["colour"], (x, y), self.size/50)

        return canvas

class TextBox:
    def __init__(self, text, font_size, width, height, colour, title=None, corner_radius=5, snap="left", margin=None, ver_snap="top", highlights=None):
        if not pygame.font.get_init():
            pygame.font.init()
        self.highlights = highlights
        self.text = text
        self.font_size = font_size
        self.width = width
        self.height = height
        self.snap = snap
        self.ver_snap = ver_snap
        self.title = title
        self.corner_radius = corner_radius
        match colour:
            case "dark":
                self.background_colour = (25,25,25)
                self.highlight_colour = (255,50,50)
                self.text_colour = (230,230,230)
                self.border_colour = (120,120,120)
                self.title_colour = (230,230,100)
            case "alert":
                self.background_colour = (35,35,35)
                self.highlight_colour = (255,255,0)
                self.text_colour = (255,200,200)
                self.border_colour = (255,0,0)
                self.title_colour = (255,0,0)
            case "tip":
                self.background_colour = (20,20,0)
                self.highlight_colour = (255,0,0)
                self.text_colour = (230,230,230)
                self.border_colour = (255,200,0)
                self.title_colour = (200,200,150)
            case "note":
                self.background_colour = (0,0,50)
                self.highlight_colour = (200,200,0)
                self.text_colour = (230,230,230)
                self.border_colour = (0,0,200)
                self.title_colour = (220,220,255)
            case "light":
                self.background_colour = (150, 150, 150)
                self.highlight_colour = (200, 200, 0)
                self.text_colour = (50, 50, 50)
                self.border_colour = (220, 220, 220)
                self.title_colour = (220, 220, 220)
            case _:
                self.background_colour = (25, 25, 25)
                self.highlight_colour = (255, 50, 50)
                self.text_colour = (230, 230, 230)
                self.border_colour = (120, 120, 120)
                self.title_colour = (230, 230, 100)
        self.font = pygame.font.SysFont("monospace", font_size, True)
        size = self.font.size("a")
        self.font_width = size[0]
        self.font_height = size[1]
        self.font.set_bold(True)
        if margin:
            self.margin = margin
        else:
            self.margin = self.font_width/2

    def draw(self):
        canvas = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)

        if self.title is None:
            rect = pygame.Rect()
            rect.left = self.corner_radius + 1
            rect.top = 1
            rect.width = self.width - (self.corner_radius+1)*2
            rect.height = self.height - 2
            pygame.draw.rect(canvas, self.background_colour, rect)
            rect.left = 1
            rect.top = self.corner_radius + 1
            rect.width = self.width - 2
            rect.height = self.height - (self.corner_radius+1)*2
            pygame.draw.rect(canvas, self.background_colour, rect)
        else:
            rect = pygame.Rect()
            rect.left = self.corner_radius + 1
            rect.top = self.font_height+(self.margin*2)+2
            rect.width = self.width - (self.corner_radius+1)*2
            rect.height = self.height - (self.font_height+(self.margin*2)+5)
            pygame.draw.rect(canvas, self.background_colour, rect)
            rect.left = 1
            rect.top = self.font_height+(self.margin*2)+2+self.corner_radius
            rect.width = self.width - 2
            rect.height = self.height - (self.font_height+(self.margin*2)+3 + self.corner_radius*2)
            pygame.draw.rect(canvas, self.background_colour, rect)
            rect.top = self.font_height+(self.margin*2)+4
            rect.width = self.corner_radius
            rect.height = self.corner_radius
            pygame.draw.rect(canvas, self.background_colour, rect)
            rect.top = self.corner_radius+1
            rect.left = 1
            rect.height = self.font_height + self.margin*2 - self.corner_radius
            rect.width = self.font.size(self.title)[0] + self.margin*2
            pygame.draw.rect(canvas, self.background_colour, rect)
            rect.top = 1
            rect.left = self.corner_radius+1
            rect.width = self.font.size(self.title)[0] + self.margin*2 - self.corner_radius*2 + 1
            rect.height = self.corner_radius
            pygame.draw.rect(canvas, self.background_colour, rect)

        pygame.draw.aaline(canvas, self.border_colour, (0.5, self.corner_radius+1), (0.5, self.height - self.corner_radius-2), 2)
        pygame.draw.aaline(canvas, self.border_colour, (self.corner_radius+1, self.height-2.5), (self.width - self.corner_radius-2, self.height-2.5), 2)

        circle = pygame.Surface(((self.corner_radius*2)+1, (self.corner_radius*2)+1), flags=pygame.SRCALPHA)
        pygame.draw.aacircle(circle, self.background_colour, (self.corner_radius+0.5, self.corner_radius+0.5), self.corner_radius-3)
        pygame.draw.aacircle(circle, self.border_colour, (self.corner_radius+0.5, self.corner_radius+0.5), self.corner_radius, 2)
        canvas.blit(circle, (0,0), (0,0,self.corner_radius+1,self.corner_radius+1))
        canvas.blit(circle, (0,self.height-self.corner_radius-1), (0,self.corner_radius,self.corner_radius+1, self.corner_radius+1))
        canvas.blit(circle, (self.width-self.corner_radius-1, self.height-self.corner_radius-1), (self.corner_radius, self.corner_radius, (self.corner_radius*2)+1, (self.corner_radius*2)+1))

        if self.title is None:
            pygame.draw.aaline(canvas, self.border_colour, (self.corner_radius+1, 0.5), (self.width-self.corner_radius-2, 0.5), 2)
            pygame.draw.aaline(canvas, self.border_colour, (self.width-2.5, self.corner_radius+1), (self.width-2.5, self.height-self.corner_radius-2), 2)
            canvas.blit(circle, (self.width-self.corner_radius-1, 0), (self.corner_radius, 0, (self.corner_radius*2)+1, self.corner_radius+1))
        else:
            pygame.draw.aaline(canvas, self.border_colour, (0, self.font_height+(self.margin*2)+1.5), (self.width-self.corner_radius-2, self.font_height+(self.margin*2)+1.5), 2)
            pygame.draw.aaline(canvas, self.border_colour, (self.width-2.5, self.font_height+(self.margin*2)+self.corner_radius+2), (self.width-2.5, self.height-self.corner_radius-2), 2)
            canvas.blit(circle, (self.width-self.corner_radius-1, self.font_height+(self.margin*2)+1), (self.corner_radius, 0, (self.corner_radius*2)+1, self.corner_radius+1))
            title_length = self.font.size(self.title)[0] + (self.margin+1)*2
            pygame.draw.aaline(canvas, self.border_colour, (self.corner_radius+1, 0.5), (title_length-self.corner_radius-1, 0.5), 2)
            pygame.draw.aaline(canvas, self.border_colour, (title_length-1.5, self.corner_radius+1), (title_length-1.5, self.font_height+(self.margin*2)+2), 2)
            canvas.blit(circle, (title_length-self.corner_radius, 0), (self.corner_radius, 0, (self.corner_radius*2)+1, self.corner_radius+1))

        lines = self.text.split("\n")
        fit = False
        while not fit:
            for line in range(0,len(lines)):
                while self.font.size(lines[line])[0] > self.width - self.margin*2 - 4:
                    split = lines[line].rsplit(" ", 1)
                    lines[line] = split[0]
                    if len(lines) <= line+1:
                        lines.append(" " + split[1])
                    else:
                        lines[line+1] = " " + split[1] + lines[line+1]

            fit = True
            for line in lines:
                if self.font.size(line)[0] > self.width - self.margin*2 - 4:
                    fit = False

        if self.title:
            canvas.blit(self.font.render(self.title, True, self.title_colour), (self.margin+1, self.margin+1))

        if self.title:
            box_height = self.height - (self.margin*2 + self.font_height)
            match self.ver_snap:
                case "top":
                    pos = self.margin + 2 + (self.margin*2 + self.font_height)
                case "bottom":
                    pos = box_height - self.margin - 2 - (len(lines) * self.font_height) + (self.margin*2 + self.font_height)
                case "center":
                    pos = box_height / 2 - (len(lines) * self.font_height) / 2 + (self.margin*2 + self.font_height)
                case _:
                    pos = self.margin + 2 + (self.margin*2 + self.font_height)
        else:
            match self.ver_snap:
                case "top":
                    pos = self.margin + 2
                case "bottom":
                    pos = self.height - self.margin - 2 - (len(lines) * self.font_height)
                case "center":
                    pos = self.height/2 - (len(lines) * self.font_height)/2
                case _:
                    pos = self.margin + 2

        for line in lines:
            width = self.font.size(line.strip())[0]
            match self.snap:
                case "left":
                    start = self.margin + 2
                case "right":
                    start = self.width - self.margin - 2 - width
                case "center":
                    start = self.width / 2 - width / 2
                case _:
                    start = self.margin + 2
            canvas.blit(self.font.render(line.strip(), True, self.text_colour), (start, pos))
            pos += self.font_height

        if self.title:
            box_height = self.height - (self.margin * 2 + self.font_height)
            match self.ver_snap:
                case "top":
                    pos = self.margin + 2 + (self.margin * 2 + self.font_height)
                case "bottom":
                    pos = box_height - self.margin - 2 - (len(lines) * self.font_height) + (
                                self.margin * 2 + self.font_height)
                case "center":
                    pos = box_height / 2 - (len(lines) * self.font_height) / 2 + (self.margin * 2 + self.font_height)
                case _:
                    pos = self.margin + 2 + (self.margin * 2 + self.font_height)
        else:
            match self.ver_snap:
                case "top":
                    pos = self.margin + 2
                case "bottom":
                    pos = self.height - self.margin - 2 - (len(lines) * self.font_height)
                case "center":
                    pos = self.height/2 - (len(lines) * self.font_height)/2
                case _:
                    pos = self.margin + 2

        if self.highlights:
            word_index = 0
            for line in lines:
                words = line.strip().split(" ")
                width = self.font.size(line.strip())[0]
                match self.snap:
                    case "left":
                        start = self.margin + 2
                    case "right":
                        start = self.width - self.margin - 2 - width
                    case "center":
                        start = self.width / 2 - width / 2
                    case _:
                        start = self.margin + 2
                for word in words:
                    if word_index in self.highlights:
                        rect = pygame.Rect()
                        rect.topleft = (start, pos)
                        rect.size = self.font.size(word.strip())
                        canvas.blit(self.font.render(word.strip(), True, self.highlight_colour), (start, pos))
                    start += self.font.size(word + " ")[0]
                    word_index += 1
                pos += self.font_height

        return canvas

class Gauge:
    def __init__(self, label, max_value, size, danger_zone, style, point_density):
        self.label = label
        self.style = style
        self.max = ceil(max_value / point_density) * point_density
        self.step = ceil(max_value / point_density)
        self.size = size
        self.danger_zone = danger_zone
        self.base_image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(self.base_image, (35, 35, 35), (0, 0, size, size), border_radius=10)
        pygame.draw.rect(self.base_image, (200, 200, 200), (0, 0, size, size), 2, 10)
        title_font = pygame.font.SysFont("monospace", floor(size/8), True)
        self.base_image.blit(title_font.render(label, True, (255,255,255)), ((size / 2) - (title_font.size(label)[0] / 2), size/12))
        if danger_zone > 0:
            pygame.draw.aacircle(self.base_image, (30, 0, 0), (size/5, size/3), (size/16))
            pygame.draw.aacircle(self.base_image, (70, 70, 70), (size/5, size / 3), (size / 16), 2)
        match style:
            case "dial":
                font = pygame.font.SysFont("monospace", floor(size / 12), False)
                text_size = font.size(str(self.max) + " ")
                rect = pygame.Rect(((size / 5) * 4) - (text_size[0] / 2), (size / 3) - (text_size[1] / 2), text_size[0], text_size[1])
                pygame.draw.rect(self.base_image, (70, 70, 70), rect, 2, 3)
                for num in range(0, 10):
                    text = str(num) * len(str(self.max))
                    text_size = font.size(text)
                    self.base_image.blit(font.render(text, True, (50, 50, 50)),(((size / 5) * 4) - (text_size[0] / 2), (size / 3) - (text_size[1] / 2)))
                self.draw_font = pygame.font.SysFont("monospace", floor(size/12), True)
                base_gauge = pygame.Surface((size/2+1, size/2+1), pygame.SRCALPHA)
                pygame.draw.aacircle(base_gauge, (100,100,100), (size/4, size/4), size/4)
                angle_step = 240/point_density
                angle = 150.0
                for step in range(0,point_density+1):
                    opp = sin(radians(angle))
                    adj = cos(radians(angle))
                    x1 = (size/4)+(adj*(size/4))
                    y1 = (size/4)+(opp*(size/4))
                    x2 = (size/4)+(adj*(((size/4)/10)*7))
                    y2 = (size/4)+(opp*(((size/4)/10)*7))
                    if (step / point_density) * self.max >= self.danger_zone:
                        pygame.draw.aaline(base_gauge, (255, 50, 50), (x2, y2), (x1, y1))
                    else:
                        pygame.draw.aaline(base_gauge, (250, 250, 250), (x2, y2), (x1, y1))
                    angle += angle_step
                self.base_image.blit(font.render("0", True, (255,255,255)), ((size/4)-(font.size(str(self.max))[0]/2), ((size/32)*25)))
                self.base_image.blit(font.render(str(self.max), True, (255, 255, 255)), (((size/4)*3), ((size/32)*25)))
                angle_step = 240 / (point_density*6)
                angle = 150.0
                for step in range(0, (point_density*6) + 1):
                    opp = sin(radians(angle))
                    adj = cos(radians(angle))
                    x1 = (size / 4) + (adj * (size / 4))
                    y1 = (size / 4) + (opp * (size / 4))
                    x2 = (size / 4) + (adj * (((size / 4) / 10) * 8))
                    y2 = (size / 4) + (opp * (((size / 4) / 10) * 8))
                    if (step/(point_density*6)) * self.max >= self.danger_zone:
                        pygame.draw.aaline(base_gauge, (200, 20, 20), (x2, y2), (x1, y1))
                    else:
                        pygame.draw.aaline(base_gauge, (250, 250, 250), (x2, y2), (x1, y1))
                    angle += angle_step
                pygame.draw.aacircle(base_gauge, (250, 250, 250), (size / 4, size / 4), size / 4, 2)
                self.base_image.blit(base_gauge, (self.size / 4, (self.size / 10) * 4))
            case "bar":
                font = pygame.font.SysFont("monospace", floor(size / 12), False)
                text_size = font.size(str(self.max) + " ")
                rect = pygame.Rect(((size / 5) * 4) - (text_size[0] / 2), (size / 3) - (text_size[1] / 2), text_size[0], text_size[1])
                pygame.draw.rect(self.base_image, (70, 70, 70), rect, 2, 3)
                for num in range(0, 10):
                    text = str(num) * len(str(self.max))
                    text_size = font.size(text)
                    self.base_image.blit(font.render(text, True, (50, 50, 50)),(((size / 5) * 4) - (text_size[0] / 2), (size / 3) - (text_size[1] / 2)))
                self.draw_font = pygame.font.SysFont("monospace", floor(size / 12), True)
                base_gauge = pygame.Surface(((size/6)*5, (size/10)*3), pygame.SRCALPHA)
                pygame.draw.rect(base_gauge, (70,70,70), (0,0,((size/6)*5), (size/10)*3), border_radius=4)
                #self.base_image.blit(base_gauge, (size/12, (size/12)*7))
                for step in range(0,point_density+1):
                    x = ((((size/6)*5)-9)/point_density)*step + 4
                    if (step / point_density * self.max) >= self.danger_zone:
                        pygame.draw.aaline(base_gauge, (255,40,40), (x, (((((size/10)*3)/4)*3)-1)), (x,((size/10)*3)-1))
                        pygame.draw.aaline(base_gauge, (255, 40, 40), (x, 0), (x, ((size/10)*3)/4))
                    else:
                        pygame.draw.aaline(base_gauge, (255,255,255), (x, (((((size/10)*3)/4)*3)-1)), (x,((size/10)*3)-1))
                        pygame.draw.aaline(base_gauge, (255, 255, 255), (x, 0), (x, ((size/10)*3)/4))
                for step in range(0,(point_density*4)+1):
                    x = ((((size/6)*5)-9)/(point_density*4))*step + 4
                    if (step / (point_density * 4) * self.max) >= self.danger_zone:
                        pygame.draw.aaline(base_gauge, (255,40,40), (x, (((((size/10)*3)/8)*7)-1)), (x,((size/10)*3)-1))
                        pygame.draw.aaline(base_gauge, (255, 40, 40), (x, 0), (x, ((size/10)*3)/8))
                    else:
                        pygame.draw.aaline(base_gauge, (255,255,255), (x, (((((size/10)*3)/8)*7)-1)), (x,((size/10)*3)-1))
                        pygame.draw.aaline(base_gauge, (255, 255, 255), (x, 0), (x, ((size/10)*3)/8))
                pygame.draw.rect(base_gauge, (220,220,220), (0,0,((size/6)*5), (size/10)*3), 2, 4)
                self.base_image.blit(base_gauge, (size/12, (size/12)*7))
                self.base_image.blit(font.render("0", True, (255,255,255)), ((size/12)+4, ((size/32)*17)-font.size("0")[1]/2))
                self.base_image.blit(font.render(str(self.max), True, (255, 255, 255)),(((size / 12)*11) - 4 - font.size(str(self.max))[0], ((size / 32) * 17) - font.size("0")[1] / 2))
            case "number":
                font = pygame.font.SysFont("monospace", floor(size / 6), False)
                text_size = font.size(str(self.max) + " ")
                rect = pygame.Rect(size/15, (size/5)*3, (size/15)*13,text_size[1])
                pygame.draw.rect(self.base_image, (70, 70, 70), rect, 2, 3)
                for num in range(0, 10):
                    text = str(num) * 8
                    text_size = font.size(text)
                    self.base_image.blit(font.render(text, True, (50, 50, 50)),((size/2)-(text_size[0]/2), (size/5)*3+1))
                self.draw_font = pygame.font.SysFont("monospace", floor(size / 6), True)


    def draw(self, value):
        canvas = pygame.Surface((self.size,self.size), pygame.SRCALPHA)
        canvas.blit(self.base_image)
        if value >= self.danger_zone > 0:
            pygame.draw.aacircle(canvas, (255, 0, 0), (self.size / 5, self.size / 3), (self.size / 16) - 2.5)
        match self.style:
            case "dial":
                value_text_base = str(round(value))
                if len(value_text_base) > len(str(self.max)):
                    value_text = ""
                    for i in range(0,len(str(self.max))):
                        value_text += value_text_base[(len(value_text_base)-(len(str(self.max)))) + i]
                        value_text = value_text.lstrip("0")
                else:
                    value_text = value_text_base
                text = self.draw_font.render(value_text, True, (255,0,0))
                pos = ((self.size/5)*4)+(self.draw_font.size(str(self.max))[0]/2), (self.size/3)-(self.draw_font.size(str(self.max))[1]/2)
                canvas.blit(text, (pos[0]-text.width, pos[1]))

                opp = sin(radians(150+(240*(value/self.max))))
                adj = cos(radians(150+(240*(value/self.max))))
                arm_x = adj*self.size/5
                arm_y = opp*self.size/5
                x = self.size/2
                y = (self.size/10*4)+self.size/4
                pygame.draw.aaline(canvas, (200,0,0), (x, y), (arm_x+x, arm_y+y), 2)
                pygame.draw.aacircle(canvas, (70,70,70), (x,y), self.size/20)
            case "bar":
                value_text_base = str(round(value))
                if len(value_text_base) > len(str(self.max)):
                    value_text = ""
                    for i in range(0,len(str(self.max))):
                        value_text += value_text_base[(len(value_text_base)-(len(str(self.max)))) + i]
                        value_text = value_text.lstrip("0")
                else:
                    value_text = value_text_base
                text = self.draw_font.render(value_text, True, (255,0,0))
                pos = ((self.size/5)*4)+(self.draw_font.size(str(self.max))[0]/2), (self.size/3)-(self.draw_font.size(str(self.max))[1]/2)
                canvas.blit(text, (pos[0]-text.width, pos[1]))

                if value > self.max:
                    line_value = self.max
                elif value < 0:
                    line_value = 0
                else:
                    line_value = value
                x = ((line_value/self.max)*((self.size/12)*9)) + (self.size/12) + 4
                pygame.draw.aaline(canvas, (200, 0, 0), (x, ((self.size/12)*7)+2), (x, (((self.size/12)*7)+((self.size/10)*3))-3), 2)

            case "number":
                value_text = str(value)
                text = self.draw_font.render(value_text, True, (255, 0, 0))
                pos = (((self.size/15)*14)-4, ((self.size/5)*3+1))
                canvas.blit(text, (pos[0] - text.width, pos[1]))

        return canvas


