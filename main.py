import pygame
from classes import ui

radar = ui.Radar(200, 2.5, 50)

points = []

points.append({"pos": [24, 8], "colour": [255, 0, 255, 255]})
points.append({"pos": [38, -4], "colour": [0, 0, 255, 255]})
points.append({"pos": [-21, -20], "colour": [0, 255, 0, 255]})
points.append({"pos": [-40, 5], "colour": [255, 255, 0, 255]})


screen = pygame.display.set_mode((0, 0), flags=pygame.FULLSCREEN)
clock = pygame.Clock()
running = True

textBoxes = []
textBoxes.append(ui.TextBox("This is a text box", 20, 400, 120, "dark", title="Dark Box", highlights=[3]))
textBoxes.append(ui.TextBox("This is an ALERT!!!", 20, 400, 120, "alert", title="Alert Box", highlights=[3]))
textBoxes.append(ui.TextBox("This is a useful tip", 20, 400, 120, "tip", title="Tip Box", highlights=[4]))
textBoxes.append(ui.TextBox("This is making a note", 20, 400, 120, "note", title="Note Box", highlights=[4]))
textBoxes.append(ui.TextBox("This is a racist", 20, 400, 120, "light", title="Light Box", highlights=[3]))
textBoxes.append(ui.TextBox("This has no colour", 20, 400, 120, "", title="Default Box", highlights=[3]))

gauge = ui.Gauge("Depth", 200, 120, 150, "dial", 5)
gauge2 = ui.Gauge("Temperature", 100, 120, 70, "bar", 5)
gauge3 = ui.Gauge("Balance", 1, 120, 0, "number", 1)

clock.tick()
value = 0
value2 = 20
value3 = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    radar.tick(points)
    screen.fill("black")
    dest = 20
    for textBox in textBoxes:
        screen.blit(textBox.draw(), (20, dest))
        dest += 130
    screen.blit(radar.draw(), (500, 20))
    delta = clock.tick()
    value += delta/15
    value2 += delta/20
    if value >= 300:
        value = 0
    if value2 >= 120:
        value2 = 20
    value3 += delta
    screen.blit(gauge.draw(value), (500, 300))
    screen.blit(gauge2.draw(value2), (500, 450))
    screen.blit(gauge3.draw(value3), (500,600))

    pygame.display.flip()