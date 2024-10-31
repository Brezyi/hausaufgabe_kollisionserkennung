import os
import pygame
import random


class Settings:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")


class Moving:
    def __init__(self, image_file, x, y, speedx, speedy, scale_size):
        image_path = os.path.join(Settings.IMAGE_PATH, image_file)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_file}' not found at {Settings.IMAGE_PATH}")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_size = scale_size  
        self.image = pygame.transform.scale(self.image, scale_size)  
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speedx = speedx
        self.speedy = speedy

    def update(self):
        self.rect = self.rect.move(self.speedx, self.speedy)        
        if self.rect.left < 0 or self.rect.right > Settings.WINDOW_WIDTH:
            self.speedx *= -1
        if self.rect.top < 0 or self.rect.bottom > Settings.WINDOW_HEIGHT:
            self.speedy *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def grow(self, amount):
        new_width = self.image.get_width() + amount
        new_height = self.image.get_height() + amount
        self.image = pygame.transform.scale(self.image, (new_width, new_height))
        self.rect = self.image.get_rect(center=self.rect.center)  

    def respawn(self):
        """Neupositionierung des Balls an einer zufälligen Stelle."""
        x = random.randint(50, Settings.WINDOW_WIDTH - 100)  
        y = random.randint(50, Settings.WINDOW_HEIGHT - 100)
        self.rect.topleft = (x, y)

class Obstacle:
    def __init__(self, image_file, x, y, collision_type):
        image_path = os.path.join(Settings.IMAGE_PATH, image_file)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file '{image_file}' not found at {Settings.IMAGE_PATH}")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_type = collision_type  

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with(self, moving_object):
        if self.collision_type == 'rect':
            return moving_object.rect.colliderect(self.rect)


        elif self.collision_type == 'radius':
            obj_center = moving_object.rect.center
            obstacle_center = self.rect.center
            distance_squared = (obj_center[0] - obstacle_center[0]) ** 2 + (obj_center[1] - obstacle_center[1]) ** 2
            obj_radius = moving_object.rect.width / 2
            obs_radius = self.rect.width / 2
            return distance_squared < (obj_radius + obs_radius) ** 2  


  
def create_obstacles(num_obstacles):
    obstacle_configs = [
        ("bird01.png", 'radius'),
        ("car01.png", 'radius'),
        ("regenschirm01.png", 'rect'),
        ("Ballon.png", 'radius'),
        ("stone01.png", 'rect')
    ]

    obstacles = []
    positions = set()  

    while len(obstacles) < num_obstacles:
        image_file, collision_type = random.choice(obstacle_configs)
        x = random.randint(0, Settings.WINDOW_WIDTH - 50) 
        y = random.randint(0, Settings.WINDOW_HEIGHT - 50)  


        if (x, y) not in positions:
            positions.add((x, y))
            obstacles.append(Obstacle(image_file, x, y, collision_type))

    return obstacles

def main():
    pygame.init()
    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Object Game")
    clock = pygame.time.Clock()

    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background2.jpg")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))


    ball = Moving("ball.png", 100, 100, 3, 3, (50, 50))  


    obstacles = create_obstacles(6)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        ball.update()

   
        for obstacle in obstacles[:]:
            if obstacle.collides_with(ball):
                obstacles.remove(obstacle)  
                ball.grow(10) 
                ball.respawn()  
                break  

     
        screen.blit(background_image, (0, 0))
        for obstacle in obstacles:
            obstacle.draw(screen) 
        ball.draw(screen) 

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
