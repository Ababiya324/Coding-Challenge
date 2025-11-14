# Robbery Bob - Stealth Game

A stealth/puzzle game built with CMU Graphics and Python where you play as Bob, a master thief who must sneak through levels, avoid guards, collect loot, and escape!

## How to Play

### Installation
Make sure you have CMU Graphics installed:
```bash
pip install cmu-graphics
```

### Running the Game
```bash
python robbery_bob.py
```

## Controls
- **Arrow Keys**: Move Bob around
- **Space**: Toggle hiding mode (makes you invisible to guards but slows you down)
- **R**: Restart current level
- **M**: Return to menu (when game over or game won)

## Game Mechanics

### Objective
- Collect ALL the gold loot ($) in each level
- Avoid being detected by guards
- Reach the EXIT (green square) once all loot is collected

### Guards
- Guards patrol on fixed routes
- They have vision cones (yellow wedges) showing where they can see
- If a guard spots you, the detection meter fills up
- Get caught if the detection meter reaches 100%

### Hiding
- Press SPACE to hide in shadows
- While hiding, you move slower but guards cannot see you
- Use strategically to avoid detection

### Detection Meter
- Fills up when guards can see you
- Slowly decreases when you're out of sight
- Resets when you restart a level

## Levels

The game features 3 progressively challenging levels:

1. **Level 1**: Introduction - Learn the basics with 2 guards
2. **Level 2**: Maze - Navigate through a more complex layout with 3 guards
3. **Level 3**: The Vault - Most challenging level with 4 guards and tight spaces

## Features

- **Stealth Mechanics**: Vision cone system for guard detection
- **Patrol AI**: Guards follow patrol routes and turn to face movement direction
- **Hiding System**: Strategic gameplay element to avoid detection
- **Multiple Levels**: 3 distinct levels with increasing difficulty
- **Score System**: Collect loot to increase your score
- **Smooth Movement**: Responsive arrow key controls
- **Visual Feedback**: Detection meter, hiding indicator, and animated loot

## Game States

- **Menu**: Instructions and start screen
- **Playing**: Active gameplay
- **Caught**: Game over when detected
- **Level Complete**: Successfully collected all loot and reached exit
- **Game Won**: Completed all 3 levels

## Tips for Success

1. **Observe patrol patterns** before making your move
2. **Use hiding mode** when guards are looking your way
3. **Plan your route** to collect loot efficiently
4. **Stay behind guards** when possible - they can only see forward
5. **Take your time** - there's no time limit!
6. **Use walls** to break line of sight with guards

## Technical Details

- Built with CMU Graphics
- Object-oriented design with classes for Player, Guard, Loot, Wall, and Level
- Implements vision cone detection using angular calculations
- Collision detection for walls
- Smooth animation at 30 FPS

## Game Design

- **Player**: Navy circle with eye mask
- **Guards**: Red circles with vision cones and directional indicators
- **Loot**: Gold stars with dollar values
- **Walls**: Gray rectangles creating the level layout
- **Exit**: Green square indicating the level exit

Enjoy playing Robbery Bob!
