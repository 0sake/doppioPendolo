import numpy as np
from scipy.integrate import solve_ivp
import pygame
import sys

# Parametri del doppio pendolo
m1 = 1.0  # massa del primo pendolo (kg)
m2 = 1.0  # massa del secondo pendolo (kg)
l1 = 1.0  # lunghezza della prima asta (m)
l2 = 1.0  # lunghezza della seconda asta (m)
g = -9.81  # accelerazione gravitazionale (m/s^2)

def equations(t, y):
    theta1, omega1, theta2, omega2 = y
    
    # Derivate prime
    dtheta1 = omega1
    dtheta2 = omega2
    
    # Calcolo delle derivate seconde
    delta = theta2 - theta1
    den1 = (m1 + m2) * l1 - m2 * l1 * np.cos(delta) * np.cos(delta)
    den2 = (l2 / l1) * den1
    
    domega1 = ((m2 * l1 * omega1 * omega1 * np.sin(delta) * np.cos(delta) +
                m2 * g * np.sin(theta2) * np.cos(delta) +
                m2 * l2 * omega2 * omega2 * np.sin(delta) -
                (m1 + m2) * g * np.sin(theta1)) / den1)
    
    domega2 = ((-m2 * l2 * omega2 * omega2 * np.sin(delta) * np.cos(delta) +
                (m1 + m2) * g * np.sin(theta1) * np.cos(delta) -
                (m1 + m2) * l1 * omega1 * omega1 * np.sin(delta) -
                (m1 + m2) * g * np.sin(theta2)) / den2)
    
    return [dtheta1, domega1, dtheta2, domega2]

# Condizioni iniziali
theta1_0 = np.pi/4    # angolo iniziale del primo pendolo (rad)
omega1_0 = 0.0        # velocità angolare iniziale del primo pendolo (rad/s)
theta2_0 = np.pi/4    # angolo iniziale del secondo pendolo (rad)
omega2_0 = 0.0        # velocità angolare iniziale del secondo pendolo (rad/s)

y0 = [theta1_0, omega1_0, theta2_0, omega2_0]

# Intervalo di tempo per l'integrazione
t_span = (0, 20)  # da 0 a 20 secondi
t_eval = np.linspace(t_span[0], t_span[1], 5000)  # punti di valutazione

# Risolvere il sistema di equazioni differenziali
sol = solve_ivp(equations, t_span, y0, t_eval=t_eval, method='RK45')

# Estrazione dei risultati
theta1 = sol.y[0]
theta2 = sol.y[2]

# Calcolo delle coordinate (x, y) delle masse
x1 = l1 * np.sin(theta1)
y1 = -l1 * np.cos(theta1)
x2 = x1 + l2 * np.sin(theta2)
y2 = y1 - l2 * np.cos(theta2)

# Setup di Pygame
pygame.init()

# Parametri della finestra
width, height = 1000, 1000
origin = (width // 2, height // 2)

# Colori
background_color = (255, 255, 255)
pendulum_color = (0, 0, 0)
trajectory_color = (0, 0, 255)

# Creazione della finestra
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Doppio Pendolo con Traiettoria')

# Funzione per scalare le coordinate
def scale_coords(x, y):
    return (int(origin[0] + x * 200), int(origin[1] + y * 200))

# Lista per memorizzare la traiettoria
trajectory = []

# Funzione per disegnare il doppio pendolo
def draw_pendulum(x1, y1, x2, y2):
    screen.fill(background_color)
    pygame.draw.line(screen, pendulum_color, origin, scale_coords(x1, y1), 2)
    pygame.draw.line(screen, pendulum_color, scale_coords(x1, y1), scale_coords(x2, y2), 2)
    pygame.draw.circle(screen, pendulum_color, scale_coords(x1, y1), 10)
    pygame.draw.circle(screen, pendulum_color, scale_coords(x2, y2), 10)
    
    # Disegna la traiettoria
    if len(trajectory) > 1:
        pygame.draw.lines(screen, trajectory_color, False, trajectory, 1)
    
    pygame.display.flip()

# ANimazione
clock = pygame.time.Clock()
running = True
frame = 0
num_frames = len(t_eval)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if frame < num_frames:
        x1_frame, y1_frame, x2_frame, y2_frame = x1[frame], y1[frame], x2[frame], y2[frame]
        draw_pendulum(x1_frame, y1_frame, x2_frame, y2_frame)
        
        # Aggiungi il punto corrente alla traiettoria
        trajectory.append(scale_coords(x2_frame, y2_frame))
        
        frame += 1
    else:
        frame = 0

    clock.tick(30)  # 60 FPS

pygame.quit()
sys.exit()
