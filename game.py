# Zain Ghul (zrg7mdw)
# Amber Trinh (att8nms)
# CS Game Project

"""
CHECKPOINT COMMENTS
CP1: "Correct - Has a description of what game they want to do and how they want to meet the required
     and optional objectives - Students: Even if you are correct, please check if the TA left any feedback on your game;
     getting full credit for this checkpoint does not necessarily mean your game was approved."

CP2: "A few things: please remember to submit your images in the final submission, and the game does
     not seem to run. I noticed there is an implementation for movement, but other than that there is not much progress
     in the game, not even floor collision. Additionally, spritesheets are not gamebox objects. You have to use
     from_image to create objects from the sprite sheet you created. Come to office hours if you have any questions."

    *** Our game changed significantly from our checkpoints due to no longer wanting to use spritesheets as a feature.

GAME FINAL VERSION DESCRIPTION & FEATURES
Description: Multiplayer platform game with two players that move simultaneously to compete against each other to
             collect green gemstones around a cave map and earn points whilst avoiding floating white enemies who will
             deplete player health bar upon contact. Player wins by staying alive and collecting the most gems. Scores
             will be generated depending on the number of gems each player collects.

Required Features:  User Input - players click to start the game, operate character movement and jumping through
                    "A, S, D, W' keys for player 1 and the arrow keys for player 2, press 'R' to restart the game in the
                    game over screen or press 'space bar' to return to start up screen.

                    Start Screen - appears at the beginning of the game where title, names, ID's, instructions with
                    rules, and prompt to click to start game.

                    Game Over - appears once a player runs out of health or all 15 gems in the map have been collected
                    by the players. Game over screen will give players the option of pressing 'R' to restart
                    the game without returning to start up screen or 'space bar' to return to start up screen.

                    Small Enough Window - Camera is set to (800, 600).

                    Graphics/Images - obtained via internet and cited. Image files will be uploaded with game.

Optional Features: Restart from Game Over - players can hit 'R' in the game over screen to restart the game from the
                   beginning without re-running the program

                   Enemies - moving white, floating enemies on each level follow the player characters and deplete
                   player health to keep the player characters from scoring

                   Collectibles - characters can pick up green gems in the level, each player having a score counter.
                   15 gems exist within the map. Gems will vanish once players touch it and increase player score.
                   As gems disappear, a count of remaining gems in the map will be displayed at the top.

                   Health bar - each player has a health bar displayed in the upper corners that shorten as players hit
                   enemies. 0 health result in game over.

                   Two players simultaneously - two players are able to compete against each other within the game
                   simultaneously.
"""

import gamebox
import pygame
import random

# CAMERA SET UP
screen_width = 800
screen_height = 600
camera = gamebox.Camera(screen_width, screen_height)

# GLOBAL VARIABLES
p1 = None
p2 = None
floors = []
boundaries = []
p1_score = 0
p2_score = 0
p1_health = 100
p2_health = 100
p1_enemies = []
p2_enemies = []
gems = []
gem_count = 15
p1_game_over = None
p2_game_over = None
p1_game_over_shadow = None
p2_game_over_shadow = None
restart = None
restart_shadow = None
menu = None
menu_shadow = None
p1_win = None
p2_win = None
p1_win_shadow = None
p2_win_shadow = None
alive = True


def draw_map():
    """
    Draws scenery
    :return: nothing
    """
    game_map = gamebox.from_image(400, 300, "crystal.jpg")
    camera.draw(game_map)
    # crystal.jpg image, originally named "Amethyst geode cave" was created by artist 'mommottix' on deviantart.com.
    # url citation: https://www.deviantart.com/mommottix/art/Amethyst-geode-cave-860796874


def move_players(keys):
    """
    Sets player controls
    :param keys: keys pressed
    :return: nothing
    """
    global p1, p2

    # PLAYER 1
    # left and right movement controls
    if pygame.K_d in keys:  # move right
        p1.x += 5
    if pygame.K_a in keys:  # move left
        p1.x -= 5
    # gravity dynamics
    p1.yspeed += 1
    p1.y += p1.yspeed

    # PLAYER 2
    # left and right movement controls
    if pygame.K_RIGHT in keys:  # move right
        p2.x += 5
    if pygame.K_LEFT in keys:  # move left
        p2.x -= 5
    # gravity dynamics
    p2.yspeed += 1
    p2.y += p2.yspeed


def setup():
    """
    Sets game to initial states
    :return: nothing
    """
    global p1, p2, floors, p1_score, p2_score, p1_health, p2_health, p1_enemies, p2_enemies, gems, alive, boundaries, gem_count
    global p1_game_over, p2_game_over, p1_game_over_shadow, p2_game_over_shadow, restart, restart_shadow, p1_win, p2_win, p1_win_shadow, p2_win_shadow, menu, menu_shadow

    # CHARACTERS
    p1 = gamebox.from_color(100, 250, "pink", 20, 40)  # create character 1
    p1.yspeed = 0  # set initial speed of character 1

    p2 = gamebox.from_color(700, 250, "light blue", 20, 40)  # create character 2
    p2.yspeed = 0  # set initial speed of character 2

    # BOUNDARIES
    boundaries = [gamebox.from_color(-25, 600, "red", 50, 1200),
                  gamebox.from_color(825, 600, "red", 50, 1200),
                  gamebox.from_color(400, -25, "red", 800, 50),
                  gamebox.from_color(400, 625, "red", 800, 50)]

    # LEVELS
    # random integers for randomizing floors
    f1 = random.randint(125, 650)
    f1w2 = 800-f1-100

    f2 = random.randint(125, 650)
    f2w2 = 800-f2-100

    f3 = random.randint(125, 650)
    f3w2 = 800-f3-100

    floors = [gamebox.from_color(f1/2, 150, "light yellow", f1, 15),
              gamebox.from_color((800-f1w2/2), 150, "lavender", f1w2, 15),
              gamebox.from_color(f2/2, 300, "lavender", f2, 15),
              gamebox.from_color((800-f2w2/2), 300, "light yellow", f2w2, 15),
              gamebox.from_color(f3/2, 450, "light yellow", f3, 15),
              gamebox.from_color((800-f3w2/2), 450, "lavender", f3w2, 15),
              gamebox.from_color(400, 594, "lavender", 800, 15)]

    # ENEMIES
    p1_enemies = [gamebox.from_color(650, 100, "white", 40, 40),
                  gamebox.from_color(650, 225, "white", 40, 40),
                  gamebox.from_color(650, 375, "white", 40, 40),
                  gamebox.from_color(650, 520, "white", 40, 40)]
    p2_enemies = [gamebox.from_color(150, 100, "white", 40, 40),
                  gamebox.from_color(150, 225, "white", 40, 40),
                  gamebox.from_color(150, 375, "white", 40, 40),
                  gamebox.from_color(150, 520, "white", 40, 40)]

    for p1_enemy in p1_enemies:
        p1_enemy.xspeed = 0
        p1_enemy.yspeed = 0

    for p2_enemy in p2_enemies:
        p2_enemy.xspeed = 0
        p2_enemy.yspeed = 0

    # GEMS
    gems = [
        gamebox.from_color(random.randint(105, 695), 100, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 100, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 100, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 100, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 225, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 225, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 225, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 375, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 375, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 375, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 375, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 520, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 520, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 520, "light green", 12, 12),
        gamebox.from_color(random.randint(105, 695), 520, "light green", 12, 12)
    ]

    # INITIAL SCORE
    p1_score = 0
    p2_score = 0

    # INITIAL HEALTH
    # make health bar
    p1_health = 100
    p2_health = 100

    # INITIAL GEM COUNT
    gem_count = 15

    # GAME OVER SCREEN
    # game over
    p2_game_over = gamebox.from_text(400, 200, "- GAME OVER -", 120, "light blue")
    camera.draw(p2_game_over)
    p2_game_over_shadow = gamebox.from_text(405, 200, "- GAME OVER -", 120, "white")
    camera.draw(p2_game_over_shadow)

    p1_game_over = gamebox.from_text(400, 200, "- GAME OVER -", 120, "pink")
    camera.draw(p1_game_over)
    p1_game_over_shadow = gamebox.from_text(405, 200, "- GAME OVER -", 120, "white")
    camera.draw(p1_game_over_shadow)

    # restart
    restart = gamebox.from_text(400, 365, "PRESS 'R' TO RESTART OR", 35, "pink")
    camera.draw(restart)
    restart_shadow = gamebox.from_text(403, 365, "PRESS 'R' TO RESTART OR", 35, "white")
    camera.draw(restart_shadow)

    # winner
    p1_win_shadow = gamebox.from_text(400, 280, "PLAYER 1 WINS", 70, "pink")
    camera.draw(p1_win_shadow)
    p1_win = gamebox.from_text(405, 280, "PLAYER 1 WINS", 70, "white")
    camera.draw(p1_win)
    p2_win_shadow = gamebox.from_text(400, 280, "PLAYER 2 WINS", 70, "light blue")
    camera.draw(p2_win_shadow)
    p2_win = gamebox.from_text(405, 280, "PLAYER 2 WINS", 70, "white")
    camera.draw(p2_win)

    # menu
    menu_shadow = gamebox.from_text(400, 400, "'SPACE' TO RETURN TO MENU", 35, "light blue")
    camera.draw(menu_shadow)
    menu = gamebox.from_text(403, 400, "'SPACE' TO RETURN TO MENU", 35, "white")
    camera.draw(menu)

    alive = True


setup()


def tick(keys):
    global p1, p2, boundaries, floors, alive, p1_enemies, p2_enemies, gems, p1_score, p2_score, p1_health, p2_health, gem_count
    global p1_game_over, p2_game_over, p1_game_over_shadow, p2_game_over_shadow, restart, restart_shadow, p1_win, p2_win, p1_win_shadow, p2_win_shadow, menu, menu_shadow

    if alive:
        ##################### MAP #####################
        # draw the map
        draw_map()

        # set map boundaries
        for boundary in boundaries:
            camera.draw(boundary)
            if p1.touches(boundary) or p2.touches(boundary):
                p1.move_to_stop_overlapping(boundary)
                p2.move_to_stop_overlapping(boundary)

        ##################### PLAYERS #####################
        # set player controls
        move_players(keys)

        # draw players
        camera.draw(p1)
        camera.draw(p2)

        # player game dynamics
        for floor in floors:
            # draw floors
            camera.draw(floor)

            # check floor detection
            if p1.touches(floor) or p2.touches(floor):
                p1.move_to_stop_overlapping(floor)
                p2.move_to_stop_overlapping(floor)

            # jump mechanism with gravity
            if p1.bottom_touches(floor):
                p1.yspeed = 0
                if pygame.K_w in keys:
                    p1.yspeed = -20
            if p2.bottom_touches(floor):
                p2.yspeed = 0
                if pygame.K_UP in keys:
                    p2.yspeed = -20

        # jump mechanism with gravity off of enemies
        for p1_enemy in p1_enemies:
            if p1.bottom_touches(p1_enemy):
                p1.yspeed = 0
                if pygame.K_w in keys:
                    p1.yspeed = -20
            if p2.bottom_touches(p1_enemy):
                p2.yspeed = 0
                if pygame.K_UP in keys:
                    p2.yspeed = -20

        for p2_enemy in p2_enemies:
            if p1.bottom_touches(p2_enemy):
                p1.yspeed = 0
                if pygame.K_w in keys:
                    p1.yspeed = -20
            if p2.bottom_touches(p2_enemy):
                p2.yspeed = 0
                if pygame.K_UP in keys:
                    p2.yspeed = -20

        if p1.touches(p2) or p2.touches(p1):
            p1.move_to_stop_overlapping(p2)
            p2.move_to_stop_overlapping(p1)

        ###################### GEMS #####################
        for gem in gems:
            if p1.touches(gem):
                # update score and remove gem
                p1_score += 1
                gems.remove(gem)
            if p2.touches(gem):
                # update score and remove gem
                p2_score += 1
                gems.remove(gem)
            camera.draw(gem)

        total_score = int(p1_score) + int(p2_score)

        # gem counter
        gem_count = 15-int(total_score)
        gem_count_display = gamebox.from_text(400, 40, "GEMS REMAINING: " + str(gem_count), 30, "lavender", italic=True)
        camera.draw(gem_count_display)

        ##################### SCORE #####################
        # player 1 score
        p1_score_display = gamebox.from_text(40, 40, str(p1_score), 50, "pink")
        camera.draw(p1_score_display)

        # player 2 score
        p2_score_display = gamebox.from_text(760, 40, str(p2_score), 50, "light blue")
        camera.draw(p2_score_display)

        ###################### ENEMIES #####################
        # enemy dynamics for enemies chasing after p1
        for p1_enemy in p1_enemies:
            # draw enemies
            camera.draw(p1_enemy)

            # enemies chase p1 at varying speeds depending on level
            if p1.x < p1_enemy.x:
                if p1_enemy.y == 100:
                    p1_enemy.x -= 1
                if p1_enemy.y == 225:
                    p1_enemy.x -= 2
                if p1_enemy.y == 375:
                    p1_enemy.x -= 1
                if p1_enemy. y == 520:
                    p1_enemy.x -= 3
            if p1.x > p1_enemy.x:
                if p1_enemy.y == 100:
                    p1_enemy.x += 1
                if p1_enemy.y == 225:
                    p1_enemy.x += 2
                if p1_enemy.y == 375:
                    p1_enemy.x += 1
                if p1_enemy.y == 520:
                    p1_enemy.x += 3

            for boundary in boundaries:
                if p1_enemy.touches(boundary):
                    p1_enemy.move_to_stop_overlapping(boundary)

        # enemy dynamics for enemies chasing after p2
        for p2_enemy in p2_enemies:
            # draw enemies
            camera.draw(p2_enemy)

            # enemies chase p2 at varying speeds depending on level
            if p2.x < p2_enemy.x:
                if p2_enemy.y == 100:
                    p2_enemy.x -= 1
                if p2_enemy.y == 225:
                    p2_enemy.x -= 2
                if p2_enemy.y == 375:
                    p2_enemy.x -= 1
                if p2_enemy.y == 520:
                    p2_enemy.x -= 3
            if p2.x > p2_enemy.x:
                if p2_enemy.y == 100:
                    p2_enemy.x += 1
                if p2_enemy.y == 225:
                    p2_enemy.x += 2
                if p2_enemy.y == 375:
                    p2_enemy.x += 1
                if p2_enemy.y == 520:
                    p2_enemy.x += 3

            # enemy game dynamics
            for boundary in boundaries:
                if p2_enemy.touches(boundary):
                    p2_enemy.move_to_stop_overlapping(boundary)

        ###################### HEALTH #####################
        for p1_enemy in p1_enemies:
            if p1_enemy.touches(p1):
                p1.move_to_stop_overlapping(p1_enemy)
                p1_health -= 1  # deplete health if player 1 touch p1's enemies
            if p1_enemy.touches(p2):
                p2.move_to_stop_overlapping(p1_enemy)
                p2_health -= 1  # deplete health if player 2 touch p2's enemies
        for p2_enemy in p2_enemies:
            if p2_enemy.touches(p1):
                p1.move_to_stop_overlapping(p2_enemy)
                p1_health -= 1  # deplete health if player 1 touch p2's enemies
            if p2_enemy.touches(p2):
                p2.move_to_stop_overlapping(p2_enemy)
                p2_health -= 1  # deplete health if player 1 touch p2's enemies

        # create health bars
        p1_health_bar = gamebox.from_color(150, 40, "pink", p1_health, 25)
        p2_health_bar = gamebox.from_color(650, 40, "light blue", p2_health, 25)

        # draw health bars
        camera.draw(p1_health_bar)
        camera.draw(p2_health_bar)

        ###################### GAME OVER #####################
        # player 1 wins
        if (p2_health == 0) or (p1_score >= 8 and p1_health >= 0 and p2_health == 0) or ((total_score == 15) and p1_score >= 8) or p1_score == 15:
            draw_map()
            camera.draw(p2_game_over)
            camera.draw(p2_game_over_shadow)
            camera.draw(restart)
            camera.draw(restart_shadow)
            camera.draw(p1_win_shadow)
            camera.draw(p1_win)
            camera.draw(menu_shadow)
            camera.draw(menu)
            alive = False

        # player 2 wins
        if (p1_health == 0) or (p2_score >= 8 and p2_health >= 0 and p1_health == 0) or ((total_score == 15) and p2_score >= 8) or p2_score == 15:
            draw_map()
            camera.draw(p1_game_over)
            camera.draw(p1_game_over_shadow)
            camera.draw(restart)
            camera.draw(restart_shadow)
            camera.draw(p2_win_shadow)
            camera.draw(p2_win)
            camera.draw(menu_shadow)
            camera.draw(menu)
            alive = False

    else:
        if pygame.K_r in keys:
            alive = True
            setup()
        # return to start up menu
        elif pygame.K_SPACE in keys:
            gamebox.timer_loop(30, main_menu)

    camera.display()


def main_menu(keys):
    """
    Start screen with game name, student names and IDs, instructions
    :return: nothing
    """
    global alive
    alive = False
    # background
    draw_map()

    # game name
    title_shadows = []
    for i in range(0, 6):
        shadow_text = gamebox.from_text(400+i, 140+i, "GEO CATCH", 130, "white")
        title_shadows.append(shadow_text)

    for shadow in title_shadows:
        camera.draw(shadow)

    title_overlay = gamebox.from_text(400, 140, "GEO CATCH", 130, "pink")
    camera.draw(title_overlay)

    # student names
    names = gamebox.from_text(400, 205, "ZAIN GHUL (ZRG7MDW) & AMBER TRINH (ATT8NMS)", 25, "white", italic=True)
    camera.draw(names)

    # instructions
    instructions = [gamebox.from_text(400, 400, "Players (Pink P1 & Blue P2) compete to maneuver around the cave platforms and collect green gems",
                                      20, "white", italic=True),
                    gamebox.from_text(400, 420, "Avoid touching the floating white enemies or else player health bar will deplete",
                                      20, "white", italic=True),
                    gamebox.from_text(400, 440, "If a player dies, the other player automatically wins", 20,
                                      "white", italic=True),
                    gamebox.from_text(400, 460, "Player to stay alive and collect the most gems wins",
                                      20, "white", italic=True),
                    gamebox.from_text(400, 480, "Game ends once all 15 gems are collected or if a player runs out of health", 20,
                                      "white", italic=True),
                    gamebox.from_text(400, 510, "Controls (left, down, jump, right):", 22, "white", italic=True),
                    gamebox.from_text(400, 530, "P1: A, S, D, W", 22, "pink", italic=True),
                    gamebox.from_text(400, 550, "P2: Arrow keys", 22, "light blue", italic=True)
                    ]
    for line in instructions:
        camera.draw(line)

    # start
    button_shadows = []
    for i in range(0, 6):
        button_shadow = gamebox.from_color(400 + i, 300 + i, "white", 300, 50)
        button_shadows.append(button_shadow)
    for shadow in button_shadows:
        camera.draw(shadow)

    button_overlay = gamebox.from_color(400, 300, "pink", 300, 50)
    camera.draw(button_overlay)

    start = gamebox.from_text(400, 300, "- CLICK TO START -", 35, "white", bold=True)
    camera.draw(start)

    if camera.mouseclick:
        setup()
        alive = True
        gamebox.timer_loop(30, tick)
        not camera.mouseclick

    camera.display()


gamebox.timer_loop(30, main_menu)