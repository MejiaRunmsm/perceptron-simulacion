import pygame
from sympy import *
import numpy as np
from decimal import Decimal, ROUND_UP
import math
import random

CC = (50,250) #centro de conjunto C
CD = (150,150) #centro de conjunto D
C = []
D = []

#---- Se Genera un conjunto de entrenamiento alrededor de los centros CA y CB
randDist = 50
for i in range(20):
  randDistX = random.random()*randDist*2 - randDist
  randDistY = random.random()*randDist*2 - randDist
  C.append((CC[0]+randDistX, CC[1]+randDistY))

for i in range(20):
  randDistX = random.random()*randDist*2 - randDist
  randDistY = random.random()*randDist*2 - randDist
  D.append((CD[0]+randDistX, CD[1]+randDistY))

A = [] # Conjunto total de puntos

for c in C:
    A.append((c, 1))

for d in D:
    A.append((d, -1))

minx = C[0][0]
maxx = C[0][0]
clistX = []
clistY = []
for c in C:
  clistX.append(c[0])
  clistY.append(c[1])
  if c[0] < minx:
    minx = c[0]
  if c[0] > maxx: 
    maxx = c[0]

dlistX = []
dlistY = []
for d in D:
  dlistX.append(d[0])
  dlistY.append(d[1])
  if d[0] < minx:
    minx = d[0]
  if d[0] > maxx: 
    maxx = d[0]

def sgn(a):
  if a >= 0:
    result = 1
  else:
    result =-1
  return result

def productPoint(a, b):
  return a[0]*b[0]+a[1]*b[1]

def Yde(normal, desplazamiento, x):
  y = -(normal[0]*x + desplazamiento)/normal[1]
  return y

#----------- Se inicializan los valores iniciales de la superficie de separacion
w = [0,0]
b  = 0
#----------- Se definen los valores del radio del radio del conjunto y la taza de aprendizaje
r = 0
for c in C:
  norm_of_d = math.sqrt(c[0]**2+c[1]**2)
  if r < norm_of_d:
    r = norm_of_d
for d in D:
  norm_of_d = math.sqrt(d[0]**2+d[1]**2)
  if r < norm_of_d:
    r = norm_of_d
mu = 0.5

#--------------------------------------

WIDTH, HEIGHT = 1000, 600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

WHITE = (255,255,255)
GREY = (200, 200, 200)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PURPLE = (255, 0, 255)

class Line_sep():
    def __init__(self, W, b):
        self.W = W
        self.b = b
        self.color = RED

    def set_W_b(self, W, B):
        self.W = W
        self.b = B

    def correct_line(self):
        self.color = PURPLE

    def draw(self, minx, maxx):
        #print( [ (minx, Yde(self.W, self.b, minx)), (maxx, Yde(self.W, self.b, maxx)) ] )
        #print([(minx + WIDTH/2 ,  HEIGHT/2 - Yde(self.W, self.b, minx) ), (maxx + WIDTH/2,  HEIGHT/2 - Yde(self.W, self.b, maxx))])
        pygame.draw.lines(WIN, self.color, closed=False, points=[(minx + WIDTH/2 ,  HEIGHT/2 - Yde(self.W, self.b, minx) ), (maxx + WIDTH/2,  HEIGHT/2 - Yde(self.W, self.b, maxx))], width=1 )

def draw_plano_cartesiano():
    posSquare = 0
    while(posSquare <= WIDTH or posSquare <= WIDTH):
        pygame.draw.lines(WIN, GREY, closed=False, points=[(0,posSquare), (WIDTH,posSquare)], width=1 )
        pygame.draw.lines(WIN, GREY, closed=False, points=[(posSquare,0), (posSquare,HEIGHT)], width=1 )
        posSquare += 100
    pygame.draw.lines(WIN, BLACK, closed=False, points=[(0,HEIGHT/2), (WIDTH,HEIGHT/2)], width=1 )
    pygame.draw.lines(WIN, BLACK, closed=False, points=[(WIDTH/2,0), (WIDTH/2,HEIGHT)], width=1 )
    

def draw_points():
    for i in range(20):
        pygame.draw.circle(WIN, GREEN, (C[i][0] + WIDTH/2, HEIGHT/2 - C[i][1]), 6)
        pygame.draw.circle(WIN, BLUE, (D[i][0] + WIDTH/2, HEIGHT/2 - D[i][1]), 6)



def draw_window():
    WIN.fill(WHITE)
    draw_plano_cartesiano()

    line_sep.draw( -500, 500)

    draw_points()


    pygame.display.update()


line_sep = Line_sep([0.1, 0.1], 0)

def main(): 
    count = 0
    clock = pygame.time.Clock()
    w = [1, 1]
    b = 0
    line_sep.set_W_b(w, b)

    count = 0
    i = 0

    unclassified = 0

    run = True
    while run:
        print( [ (minx, Yde(w, b, minx)), (maxx, Yde(w, b, maxx)), i , count] )

        clock.tick(20)
        draw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if sgn(productPoint(A[i][0],w) - b) != A[i][1]:
            w[0] = w[0] + mu*A[i][1]*A[i][0][0]
            w[1] = w[1] + mu*A[i][1]*A[i][0][1]
            #b = b - mu*A[i][1]*(r**2)
            line_sep.set_W_b(w, b)
            count+=1
            unclassified += 1


        i+=1
        if i == 40:
            if unclassified == 0:
                line_sep.correct_line()
            i = 0
            unclassified = 0

    pygame.quit()

if __name__ == "__main__":
    main()