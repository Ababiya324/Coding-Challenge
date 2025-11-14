"""
Robbery Bob - A stealth game using CMU Graphics
Navigate Bob through levels, avoid guards, and collect loot!
Controls: Arrow keys to move, Space to hide, R to restart
"""

from cmu_graphics import *
import math

# Game Constants
GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_SIZE = 20
GUARD_SIZE = 20
LOOT_SIZE = 15
WALL_COLOR = 'dimGray'
FLOOR_COLOR = 'lightGray'

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = PLAYER_SIZE
        self.speed = 3
        self.color = 'navy'
        self.hiding = False
        self.detected = False

    def move(self, dx, dy, walls):
        newX = self.x + dx
        newY = self.y + dy

        # Check collision with walls
        if not self.collidesWithWalls(newX, newY, walls):
            self.x = newX
            self.y = newY

    def collidesWithWalls(self, x, y, walls):
        for wall in walls:
            if (x + self.size/2 > wall.x and
                x - self.size/2 < wall.x + wall.width and
                y + self.size/2 > wall.y and
                y - self.size/2 < wall.y + wall.height):
                return True
        return False

    def draw(self):
        # Draw player as a thief character
        if self.hiding:
            fill = 'darkSlateGray'
            opacity = 50
        else:
            fill = self.color
            opacity = 100

        # Body
        drawCircle(self.x, self.y, self.size/2, fill=fill, opacity=opacity)

        # Mask (eyes)
        if not self.hiding:
            drawCircle(self.x - 5, self.y - 3, 2, fill='white')
            drawCircle(self.x + 5, self.y - 3, 2, fill='white')
            drawCircle(self.x - 5, self.y - 3, 1, fill='black')
            drawCircle(self.x + 5, self.y - 3, 1, fill='black')

class Guard:
    def __init__(self, x, y, patrolPoints):
        self.x = x
        self.y = y
        self.size = GUARD_SIZE
        self.speed = 1.5
        self.color = 'darkRed'
        self.patrolPoints = patrolPoints
        self.currentTarget = 0
        self.direction = 0  # Angle in degrees
        self.visionRange = 100
        self.visionAngle = 60
        self.detectionTimer = 0

    def update(self):
        # Move towards current patrol point
        if len(self.patrolPoints) > 0:
            targetX, targetY = self.patrolPoints[self.currentTarget]

            # Calculate direction
            dx = targetX - self.x
            dy = targetY - self.y
            distance = math.sqrt(dx**2 + dy**2)

            if distance < 5:
                # Reached patrol point, move to next
                self.currentTarget = (self.currentTarget + 1) % len(self.patrolPoints)
            else:
                # Move towards target
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
                # Update direction
                self.direction = math.degrees(math.atan2(dy, dx))

    def canSeePlayer(self, player):
        if player.hiding:
            return False

        # Calculate distance to player
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > self.visionRange:
            return False

        # Calculate angle to player
        angleToPlayer = math.degrees(math.atan2(dy, dx))
        angleDiff = abs(angleToPlayer - self.direction)

        # Normalize angle difference to 0-180
        if angleDiff > 180:
            angleDiff = 360 - angleDiff

        return angleDiff < self.visionAngle / 2

    def draw(self):
        # Draw vision cone
        drawWedge(self.x, self.y, self.visionRange * 2, self.visionRange * 2,
                  self.direction - self.visionAngle/2, self.visionAngle,
                  fill='yellow', opacity=20)

        # Draw guard body
        drawCircle(self.x, self.y, self.size/2, fill=self.color)

        # Draw guard face direction
        endX = self.x + math.cos(math.radians(self.direction)) * self.size/2
        endY = self.y + math.sin(math.radians(self.direction)) * self.size/2
        drawLine(self.x, self.y, endX, endY, fill='white', lineWidth=2)

class Loot:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.size = LOOT_SIZE
        self.value = value
        self.collected = False
        self.sparkle = 0

    def draw(self):
        if not self.collected:
            # Animated sparkle effect
            self.sparkle = (self.sparkle + 1) % 60
            opacity = 50 + abs(math.sin(self.sparkle / 10)) * 50

            # Draw diamond shape
            drawStar(self.x, self.y, self.size, 4, fill='gold',
                    opacity=opacity, rotateAngle=45)
            drawLabel(f'${self.value}', self.x, self.y,
                     size=10, fill='darkGoldenrod', bold=True)

class Wall:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        drawRect(self.x, self.y, self.width, self.height,
                fill=WALL_COLOR, border='black', borderWidth=2)

class Level:
    def __init__(self, levelNum):
        self.levelNum = levelNum
        self.walls = []
        self.guards = []
        self.loot = []
        self.exitZone = None
        self.createLevel()

    def createLevel(self):
        if self.levelNum == 1:
            self.createLevel1()
        elif self.levelNum == 2:
            self.createLevel2()
        elif self.levelNum == 3:
            self.createLevel3()

    def createLevel1(self):
        # Border walls
        self.walls = [
            Wall(0, 0, GAME_WIDTH, 20),  # Top
            Wall(0, GAME_HEIGHT - 20, GAME_WIDTH, 20),  # Bottom
            Wall(0, 0, 20, GAME_HEIGHT),  # Left
            Wall(GAME_WIDTH - 20, 0, 20, GAME_HEIGHT),  # Right
        ]

        # Interior walls
        self.walls.extend([
            Wall(200, 100, 20, 200),
            Wall(400, 300, 20, 200),
            Wall(500, 100, 200, 20),
        ])

        # Guards
        self.guards = [
            Guard(300, 200, [(300, 200), (300, 400), (500, 400), (500, 200)]),
            Guard(600, 300, [(600, 300), (700, 300), (700, 450), (600, 450)]),
        ]

        # Loot
        self.loot = [
            Loot(150, 150, 100),
            Loot(450, 150, 150),
            Loot(650, 200, 200),
            Loot(300, 500, 250),
        ]

        # Exit zone
        self.exitZone = (700, 500, 60, 60)

    def createLevel2(self):
        # Border walls
        self.walls = [
            Wall(0, 0, GAME_WIDTH, 20),
            Wall(0, GAME_HEIGHT - 20, GAME_WIDTH, 20),
            Wall(0, 0, 20, GAME_HEIGHT),
            Wall(GAME_WIDTH - 20, 0, 20, GAME_HEIGHT),
        ]

        # Create a maze-like structure
        self.walls.extend([
            Wall(100, 100, 20, 300),
            Wall(200, 200, 20, 300),
            Wall(300, 100, 20, 200),
            Wall(400, 200, 20, 300),
            Wall(500, 100, 20, 300),
            Wall(150, 150, 150, 20),
            Wall(350, 350, 150, 20),
        ])

        # More guards
        self.guards = [
            Guard(250, 150, [(250, 150), (450, 150), (450, 250), (250, 250)]),
            Guard(150, 400, [(150, 400), (350, 400)]),
            Guard(550, 300, [(550, 300), (550, 500), (650, 500), (650, 300)]),
        ]

        # More loot
        self.loot = [
            Loot(50, 50, 100),
            Loot(250, 100, 150),
            Loot(450, 450, 200),
            Loot(600, 150, 250),
            Loot(350, 300, 300),
        ]

        self.exitZone = (720, 520, 60, 60)

    def createLevel3(self):
        # Border walls
        self.walls = [
            Wall(0, 0, GAME_WIDTH, 20),
            Wall(0, GAME_HEIGHT - 20, GAME_WIDTH, 20),
            Wall(0, 0, 20, GAME_HEIGHT),
            Wall(GAME_WIDTH - 20, 0, 20, GAME_HEIGHT),
        ]

        # Complex room structure
        self.walls.extend([
            Wall(150, 80, 200, 20),
            Wall(450, 80, 200, 20),
            Wall(150, 250, 500, 20),
            Wall(300, 400, 300, 20),
            Wall(250, 100, 20, 150),
            Wall(550, 100, 20, 150),
        ])

        # Many guards
        self.guards = [
            Guard(200, 150, [(200, 150), (500, 150)]),
            Guard(400, 350, [(400, 350), (400, 500), (600, 500), (600, 350)]),
            Guard(650, 200, [(650, 200), (700, 200), (700, 400), (650, 400)]),
            Guard(100, 450, [(100, 450), (250, 450)]),
        ]

        # Lots of loot
        self.loot = [
            Loot(50, 50, 100),
            Loot(400, 50, 200),
            Loot(700, 50, 300),
            Loot(200, 200, 150),
            Loot(500, 200, 250),
            Loot(500, 450, 400),
            Loot(150, 550, 350),
        ]

        self.exitZone = (50, 520, 60, 60)

def onAppStart(app):
    app.gameState = 'menu'  # menu, playing, caught, levelComplete, gameWon
    app.currentLevel = 1
    app.totalScore = 0
    app.detectionMeter = 0
    resetLevel(app)

def resetLevel(app):
    app.level = Level(app.currentLevel)
    app.player = Player(50, 50)
    app.levelScore = 0
    app.detectionMeter = 0
    app.gameMessage = ''

def onKeyPress(app, key):
    if app.gameState == 'menu':
        if key == 'space':
            app.gameState = 'playing'

    elif app.gameState == 'playing':
        if key == 'space':
            app.player.hiding = not app.player.hiding
        elif key == 'r':
            resetLevel(app)

    elif app.gameState == 'caught':
        if key == 'r':
            resetLevel(app)
            app.gameState = 'playing'
        elif key == 'm':
            app.gameState = 'menu'
            app.currentLevel = 1
            app.totalScore = 0
            resetLevel(app)

    elif app.gameState == 'levelComplete':
        if key == 'space':
            app.totalScore += app.levelScore
            app.currentLevel += 1
            if app.currentLevel > 3:
                app.gameState = 'gameWon'
            else:
                resetLevel(app)
                app.gameState = 'playing'

    elif app.gameState == 'gameWon':
        if key == 'm':
            app.gameState = 'menu'
            app.currentLevel = 1
            app.totalScore = 0
            resetLevel(app)

def onKeyHold(app, keys):
    if app.gameState == 'playing':
        dx, dy = 0, 0
        moveSpeed = app.player.speed if not app.player.hiding else app.player.speed * 0.5

        if 'left' in keys:
            dx -= moveSpeed
        if 'right' in keys:
            dx += moveSpeed
        if 'up' in keys:
            dy -= moveSpeed
        if 'down' in keys:
            dy += moveSpeed

        app.player.move(dx, dy, app.level.walls)

def onStep(app):
    if app.gameState == 'playing':
        # Update guards
        for guard in app.level.guards:
            guard.update()

            # Check if guard sees player
            if guard.canSeePlayer(app.player):
                app.detectionMeter += 2
                if app.detectionMeter >= 100:
                    app.gameState = 'caught'
                    app.gameMessage = 'You were caught!'
            else:
                app.detectionMeter = max(0, app.detectionMeter - 1)

        # Check loot collection
        for loot in app.level.loot:
            if not loot.collected:
                distance = math.sqrt((app.player.x - loot.x)**2 +
                                   (app.player.y - loot.y)**2)
                if distance < app.player.size/2 + loot.size:
                    loot.collected = True
                    app.levelScore += loot.value

        # Check exit zone
        if app.level.exitZone:
            ex, ey, ew, eh = app.level.exitZone
            if (app.player.x > ex and app.player.x < ex + ew and
                app.player.y > ey and app.player.y < ey + eh):
                # Check if all loot collected
                allCollected = all(loot.collected for loot in app.level.loot)
                if allCollected:
                    app.gameState = 'levelComplete'
                    app.gameMessage = f'Level {app.currentLevel} Complete!'

def redrawAll(app):
    if app.gameState == 'menu':
        drawMenu(app)
    elif app.gameState == 'playing':
        drawGame(app)
    elif app.gameState == 'caught':
        drawGame(app)
        drawGameOver(app)
    elif app.gameState == 'levelComplete':
        drawGame(app)
        drawLevelComplete(app)
    elif app.gameState == 'gameWon':
        drawGameWon(app)

def drawMenu(app):
    drawRect(0, 0, GAME_WIDTH, GAME_HEIGHT, fill='black')

    drawLabel('ROBBERY BOB', GAME_WIDTH/2, 150,
             size=60, fill='gold', bold=True, font='monospace')

    drawLabel('A Stealth Adventure', GAME_WIDTH/2, 220,
             size=20, fill='white', font='monospace')

    drawLabel('HOW TO PLAY:', GAME_WIDTH/2, 300,
             size=24, fill='lightBlue', bold=True)

    instructions = [
        'Use ARROW KEYS to move Bob',
        'Press SPACE to hide (slower movement, invisible to guards)',
        'Collect all the GOLD loot ($)',
        'Avoid the GUARDS and their vision cones',
        'Reach the EXIT (green square) to complete the level',
        'Press R to restart level',
    ]

    y = 340
    for instruction in instructions:
        drawLabel(instruction, GAME_WIDTH/2, y, size=14, fill='white')
        y += 25

    drawLabel('Press SPACE to Start', GAME_WIDTH/2, 520,
             size=22, fill='lime', bold=True)

def drawGame(app):
    # Draw floor
    drawRect(0, 0, GAME_WIDTH, GAME_HEIGHT, fill=FLOOR_COLOR)

    # Draw grid pattern on floor
    for i in range(0, GAME_WIDTH, 40):
        drawLine(i, 0, i, GAME_HEIGHT, fill='gray', opacity=20)
    for i in range(0, GAME_HEIGHT, 40):
        drawLine(0, i, GAME_WIDTH, i, fill='gray', opacity=20)

    # Draw exit zone
    if app.level.exitZone:
        ex, ey, ew, eh = app.level.exitZone
        drawRect(ex, ey, ew, eh, fill='limeGreen', opacity=60)
        drawLabel('EXIT', ex + ew/2, ey + eh/2,
                 size=16, fill='darkGreen', bold=True)

    # Draw walls
    for wall in app.level.walls:
        wall.draw()

    # Draw loot
    for loot in app.level.loot:
        loot.draw()

    # Draw guards (with vision cones)
    for guard in app.level.guards:
        guard.draw()

    # Draw player
    app.player.draw()

    # Draw UI
    drawUI(app)

def drawUI(app):
    # Background panel
    drawRect(0, 0, GAME_WIDTH, 50, fill='black', opacity=70)

    # Level info
    drawLabel(f'Level: {app.currentLevel}', 80, 15,
             size=16, fill='white', bold=True, align='left')

    # Score
    totalLoot = sum(loot.value for loot in app.level.loot)
    drawLabel(f'Score: ${app.levelScore}/{totalLoot}', 80, 35,
             size=14, fill='gold', bold=True, align='left')

    # Detection meter
    drawLabel('Detection:', 300, 25, size=14, fill='white', align='left')
    drawRect(380, 15, 200, 20, fill='darkGray', border='white')
    if app.detectionMeter > 0:
        meterColor = 'yellow' if app.detectionMeter < 50 else 'orange' if app.detectionMeter < 75 else 'red'
        drawRect(380, 15, app.detectionMeter * 2, 20, fill=meterColor)

    # Hiding indicator
    if app.player.hiding:
        drawLabel('HIDING', 650, 25, size=16, fill='cyan', bold=True)

    # Controls reminder
    drawLabel('SPACE: Hide | R: Restart', GAME_WIDTH - 20, 25,
             size=11, fill='lightGray', align='right')

def drawGameOver(app):
    drawRect(GAME_WIDTH/2 - 200, GAME_HEIGHT/2 - 100, 400, 200,
            fill='black', opacity=90, border='red', borderWidth=3)

    drawLabel('CAUGHT!', GAME_WIDTH/2, GAME_HEIGHT/2 - 50,
             size=40, fill='red', bold=True)

    drawLabel(f'Score: ${app.levelScore}', GAME_WIDTH/2, GAME_HEIGHT/2,
             size=20, fill='white')

    drawLabel('Press R to Retry', GAME_WIDTH/2, GAME_HEIGHT/2 + 40,
             size=18, fill='yellow')

    drawLabel('Press M for Menu', GAME_WIDTH/2, GAME_HEIGHT/2 + 70,
             size=18, fill='lightBlue')

def drawLevelComplete(app):
    drawRect(GAME_WIDTH/2 - 200, GAME_HEIGHT/2 - 100, 400, 200,
            fill='black', opacity=90, border='gold', borderWidth=3)

    drawLabel(f'Level {app.currentLevel} Complete!', GAME_WIDTH/2, GAME_HEIGHT/2 - 50,
             size=32, fill='gold', bold=True)

    drawLabel(f'Loot Collected: ${app.levelScore}', GAME_WIDTH/2, GAME_HEIGHT/2,
             size=20, fill='white')

    nextLevel = app.currentLevel + 1
    if nextLevel <= 3:
        drawLabel(f'Press SPACE for Level {nextLevel}', GAME_WIDTH/2, GAME_HEIGHT/2 + 50,
                 size=18, fill='lime', bold=True)
    else:
        drawLabel('Press SPACE to Continue', GAME_WIDTH/2, GAME_HEIGHT/2 + 50,
                 size=18, fill='lime', bold=True)

def drawGameWon(app):
    drawRect(0, 0, GAME_WIDTH, GAME_HEIGHT, fill='black')

    drawLabel('CONGRATULATIONS!', GAME_WIDTH/2, 150,
             size=50, fill='gold', bold=True)

    drawLabel('You completed all levels!', GAME_WIDTH/2, 220,
             size=24, fill='white')

    drawLabel(f'Total Score: ${app.totalScore}', GAME_WIDTH/2, 300,
             size=32, fill='gold', bold=True)

    drawLabel('You are the master thief!', GAME_WIDTH/2, 380,
             size=20, fill='lightBlue')

    drawLabel('Press M to return to Menu', GAME_WIDTH/2, 500,
             size=18, fill='lime')

def main():
    runApp(width=GAME_WIDTH, height=GAME_HEIGHT)

if __name__ == '__main__':
    main()
