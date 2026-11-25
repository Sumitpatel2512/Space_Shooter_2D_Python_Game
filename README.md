# 🚀 SPACE SHOOTER

### *Hold the line. Survive the waves. Defeat the boss.*

A fast-paced 2D arcade space shooter made with **Python + Pygame**.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00A86B?style=for-the-badge)
![Genre](https://img.shields.io/badge/Genre-Arcade%20Shooter-8A2BE2?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Playable-brightgreen?style=for-the-badge)

------------------------------------------------------------------------

## 🌌 The Mission

The galaxy is under attack. Enemy ships are entering from the right side
of the battlefield, and your spaceship is the last line of defense.

Move through the starfield, blast incoming enemies, collect upgrades,
and prepare for powerful boss encounters. The longer you survive, the
more intense the battle becomes.

## ✨ What Makes It Fun?

  -----------------------------------------------------------------------
  Feature                             What to expect
  ----------------------------------- -----------------------------------
  🌠 Living galaxy                    Scrolling stars, glowing nebulae,
                                      and moving planets

  🚀 Player ship                      Responsive movement and animated
                                      engine flames

  👾 Enemy formations                 Different enemy behaviors and
                                      attack styles

  💥 Combat effects                   Explosions, glowing bullets,
                                      particles, and screen shake

  🛡️ Power-ups                        Upgrade weapons, restore health,
                                      and activate shields

  👑 Boss battles                     Large boss ship, attack patterns,
                                      and a health bar

  📈 Increasing challenge             Enemy waves become harder as your
                                      score grows

  🏆 Score system                     Track your score, high score,
                                      health, lives, and weapon level
  -----------------------------------------------------------------------

## 🎮 Meet Your Enemies

  Enemy      Behavior                                              Points
  ---------- --------------------------------------------------- --------
  🔴 Red     Fast ship that moves toward your position                 10
  🟢 Green   Moves in a wave pattern, appearing in groups              25
  🔵 Blue    Hovers and fires bullets toward you                       40
  🟣 Boss    Heavy enemy with multiple attacks and high health      1,000

## ⚡ Collect Power-ups

  Power-up              Effect
  --------------------- ------------------------------------
  🔵 **W --- Weapon**   Upgrades your weapon up to Level 4
  🟢 **H --- Health**   Restores 40 health
  🟡 **S --- Shield**   Protects you for 6 seconds

**Tip:** Keep moving while shooting. A stationary spaceship is an easy
target!

## 🕹️ Controls

  Action                    Keyboard / Mouse
  ------------------------- -----------------------------------
  Move                      `W` `A` `S` `D` or Arrow Keys
  Shoot                     Hold `SPACE` or Left Mouse Button
  Pause / Resume            `P`
  Return to Menu            `ESC`
  Restart after Game Over   `R`
  Menu after Game Over      `M`
  Start Game                `ENTER`, `SPACE`, or Mouse Click

## 🧰 Built With

-   **Python** --- core programming and game logic
-   **Pygame** --- game window, rendering, input, sprites, and game loop
-   **Math** --- movement, angles, and animation calculations
-   **Random** --- enemy spawning, effects, and variation

## 🚀 Run It Locally

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

### 2. Open the project folder

``` bash
cd YOUR-REPOSITORY
```

### 3. Install Pygame

``` bash
python -m pip install pygame
```

### 4. Launch the game

``` bash
python main.py
```

That's it. Enter the battlefield and defend the galaxy!

## 🤖 Try Demo Mode

Want to see the action without controlling the ship? Run the built-in
demo mode:

``` bash
python main.py --demo
```

Run the demo for a limited number of frames:

``` bash
python main.py --demo --frames 600
```

Save a screenshot when the demo ends:

``` bash
python main.py --demo --frames 600 --shot screenshot.png
```

## 📁 Project Structure

``` text
SPACE-SHOOTER/
│
├── main.py       # Game code
└── README.md     # Project documentation
```

## 🧠 Behind the Game

The game uses a continuous Pygame loop to process input, update the
player and enemies, detect collisions, and draw each frame. Sprite
groups manage bullets, enemies, and power-ups, while particle effects
add visual feedback during combat.

The high score is kept during the current run of the program. It is not
written to a save file, so it resets after the game closes.

## 🗺️ Possible Future Upgrades

-   Persistent high-score saving
-   More enemy types and boss stages
-   New ships and weapon designs
-   Sound effects and background music
-   Additional levels and environments

## 🤝 Contributions

Suggestions and improvements are welcome. You can fork the repository,
make your changes, and open a pull request.

## 📜 License

No license has been specified yet. Add a `LICENSE` file if you want to
define how others may use, modify, and distribute this project.

------------------------------------------------------------------------

### ⭐ If you enjoyed the game, consider giving the repository a star!

**Made with Python 🐍 and Pygame 🎮**

*The galaxy is counting on you. Good luck, pilot!*
