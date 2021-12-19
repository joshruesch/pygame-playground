import math
import pygame
from random import randint

# Controls:
# Spacebar -> Change background color
# Click -> Add a circle (if circle won't overlap another circle).
# Right Click -> Delete a circle (that your mouse is in).
# Left Arrow -> Move all circles to the left.
# Right Arrow -> Move all circles to the right.

(width, height) = (1000, 800)
GRAVITY_AMOUNT = 0.5
NUDGE_AMOUNT = 5

class Circle:
  def __init__(self, pos, radius, color):
    self.pos = pos
    self.radius = radius
    self.color = color


running = True

def main():
    global running, screen

    background = (255, 255, 255)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Circles")

    circles = []

    while running:
        # Make the entire screen background color (so that old circles don't render)
        screen.fill(background)
        ev = pygame.event.get()

        pos = getPos()
        for event in ev:
            # LEFT CLICK
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Add a new circle to the list if the new circle won't overlap another circle.
                potentialCircle = Circle(pos, getRandomSize(), getRandomColor())
                if (not doesCircleOverlapWithAnyCircle(potentialCircle, circles)):
                    circles.append(potentialCircle)

            # RIGHT CLICK
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
               deleteCircleIfMouseInside(pos, circles)

            # Spacebar
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                background = getRandomColor() 
            
            # Left Arrow
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                for circle in circles:
                    circle.pos = (circle.pos[0] - NUDGE_AMOUNT, circle.pos[1])
            # Right Arrow
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                for circle in circles:
                    circle.pos = (circle.pos[0] + NUDGE_AMOUNT, circle.pos[1])

            elif event.type == pygame.QUIT:
                running = False
  
        # Draw all the circles
        for circle in circles:
            pygame.draw.circle(screen, circle.color, circle.pos, circle.radius)

            # Move balls down by increasing Y (0,0) is the top of the screen
            circle.pos = (circle.pos[0], circle.pos[1] + GRAVITY_AMOUNT)

        # Tell the screen we're done putting stuff on it
        pygame.display.update()

# If distance from mouse to center of circle is <= radius it's inside
def deleteCircleIfMouseInside(pos, circles):
    i = 0
    length = len(circles)

    while i < length:
        circle = circles[i]
        if (math.sqrt((pos[0] - circle.pos[0])**2 + (pos[1] - circle.pos[1])**2)) <= (circle.radius):
            circles.pop(i)
            return 
        i = i + 1

    # random number 15 and 45 (made up)
def getRandomSize():
    return randint(15, 45)

# three numbers between 0 and 255
def getRandomColor():
    return (randint(0, 255),
            randint(0, 255), 
            randint(0, 255))

def getPos():
    pos = pygame.mouse.get_pos()
    return (pos)

# Use the distance formula. If the distance between the two center points is larger than the sum 
# of their radii, they would overlap
# https://courses.lumenlearning.com/cuny-hunter-collegealgebra/chapter/introduction-4/
def doesCircleOverlapWithAnyCircle(potentialCircle, circles):
    for circle in circles:
        if (math.sqrt((potentialCircle.pos[0] - circle.pos[0])**2 + (potentialCircle.pos[1] - circle.pos[1])**2)) <= (potentialCircle.radius + circle.radius):
            return True 
    return False


if __name__ == '__main__':
    main()
