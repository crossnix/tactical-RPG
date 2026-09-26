import random


class Character:
    def __init__(self, name, char_class, hp, attack, defense, movement, symbol):
        self.name = name
        self.char_class = char_class
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.movement = movement
        self.symbol = symbol
        self.x = 0
        self.y = 0
        self.alive = True

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def show_stats(self):
        print(f"\n{name_line(self.name)}")
        print(f"Class: {self.char_class}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Movement: {self.movement}")
        print(f"Position: ({self.x}, {self.y})")


def name_line(name):
    return f"--- {name} ---"


players = [
    Character("Marth", "Lord", 30, 10, 5, 3, "M"),
    Character("Shamir", "Archer", 22, 9, 3, 4, "S"),
    Character("Edelgard", "Knight", 35, 8, 8, 2, "E"),
    Character("Lysithea", "Mage", 20, 12, 2, 3, "L")
]

enemies = [
    Character("Raider", "Fighter", 18, 7, 2, 3, "r"),
    Character("Bandit", "Fighter", 22, 8, 3, 3, "b"),
    Character("Archer", "Archer", 16, 7, 2, 4, "a")
]


WIDTH = 8
HEIGHT = 8

players[0].x, players[0].y = 0, 3
players[1].x, players[1].y = 1, 2
players[2].x, players[2].y = 0, 4
players[3].x, players[3].y = 1, 4

enemies[0].x, enemies[0].y = 6, 2
enemies[1].x, enemies[1].y = 7, 4
enemies[2].x, enemies[2].y = 6, 5


def draw_board():
    print("\n")
    print("    0 1 2 3 4 5 6 7")
    print("   -----------------")

    for y in range(HEIGHT):
        row = f"{y} | "

        for x in range(WIDTH):
            symbol = "."

            for player in players:
                if player.alive and player.x == x and player.y == y:
                    symbol = player.symbol

            for enemy in enemies:
                if enemy.alive and enemy.x == x and enemy.y == y:
                    symbol = enemy.symbol

            row += symbol + " "

        print(row)

    print("\nPlayers: M=Marth S=Shamir E=Edelgard L=Lysithea")
    print("Enemies: r=Raider b=Bandit a=Archer")

def distance(unit1, unit2):
    return abs(unit1.x - unit2.x) + abs(unit1.y - unit2.y)


def position_occupied(x, y):
    for player in players:
        if player.alive and player.x == x and player.y == y:
            return True

    for enemy in enemies:
        if enemy.alive and enemy.x == x and enemy.y == y:
            return True

    return False


def get_player(symbol):
    for player in players:
        if player.symbol.lower() == symbol.lower():
            return player

    return None


def get_enemy(symbol):
    for enemy in enemies:
        if enemy.symbol.lower() == symbol.lower():
            return enemy

    return None




def show_all_players():
    print("\n===== YOUR UNITS =====")

    for player in players:
        if player.alive:
            print(
                f"{player.symbol} - {player.name} "
                f"({player.char_class}) "
                f"HP: {player.hp}/{player.max_hp} "
                f"ATK: {player.attack} "
                f"DEF: {player.defense}"
            )
        else:
            print(f"{player.symbol} - {player.name} - DEFEATED")

def show_enemies():
    print("\n===== ENEMIES =====")

    for enemy in enemies:
        if enemy.alive:
            print(
                f"{enemy.symbol} - {enemy.name} "
                f"({enemy.char_class}) "
                f"HP: {enemy.hp}/{enemy.max_hp}"
            )

def move_player(player):
    print(f"\nMoving {player.name}")
    print("Enter direction:")
    print("w = up")
    print("s = down")
    print("a = left")
    print("d = right")
    print("q = cancel")

    moves = 0

    while moves < player.movement:

        draw_board()

        print(f"\n{player.name}")
        print(f"Movement remaining: {player.movement - moves}")

        direction = input("Move: ").lower()

        if direction == "q":
            break

        new_x = player.x
        new_y = player.y

        if direction == "w":
            new_y -= 1

        elif direction == "s":
            new_y += 1

        elif direction == "a":
            new_x -= 1

        elif direction == "d":
            new_x += 1

        else:
            print("Invalid movement.")
            continue

        if new_x < 0 or new_x >= WIDTH:
            print("You cannot move outside the map.")
            continue

        if new_y < 0 or new_y >= HEIGHT:
            print("You cannot move outside the map.")
            continue

        if position_occupied(new_x, new_y):
            print("That space is occupied.")
            continue

        player.x = new_x
        player.y = new_y
        moves += 1

def attack_enemy(player):
    possible_targets = []

    for enemy in enemies:
        if enemy.alive:
            if distance(player, enemy) <= 1:
                possible_targets.append(enemy)

    if not possible_targets:

        if player.char_class == "Archer":
            for enemy in enemies:
                if enemy.alive and distance(player, enemy) <= 3:
                    possible_targets.append(enemy)

        elif player.char_class == "Mage":
            for enemy in enemies:
                if enemy.alive and distance(player, enemy) <= 2:
                    possible_targets.append(enemy)

    if not possible_targets:
        print("No enemies are in range.")
        return

    print("\nEnemies in range:")

    for enemy in possible_targets:
        print(
            f"{enemy.symbol} - {enemy.name} "
            f"HP: {enemy.hp}/{enemy.max_hp}"
        )

    choice = input("Choose enemy: ").lower()

    target = None

    for enemy in possible_targets:
        if enemy.symbol.lower() == choice:
            target = enemy

    if target is None:
        print("Invalid target.")
        return
 
    damage = max(1, player.attack - target.defense)

    damage += random.randint(0, 2)

    print(
        f"\n{player.name} attacks {target.name} "
        f"for {damage} damage!"
    )

    target.take_damage(damage)

    if not target.alive:
        print(f"{target.name} was defeated!")


def enemy_turn():
    print("\n====================")
    print("     ENEMY TURN")
    print("====================")

    for enemy in enemies:

        if not enemy.alive:
            continue

        living_players = [
            player for player in players
            if player.alive
        ]

        if not living_players:
            return

        target = min(
            living_players,
            key=lambda player: distance(enemy, player)
        )

        if distance(enemy, target) <= 1:

            damage = max(
                1,
                enemy.attack - target.defense
            )

            damage += random.randint(0, 2)

            print(
                f"{enemy.name} attacks "
                f"{target.name} for {damage} damage!"
            )

            target.take_damage(damage)

            if not target.alive:
                print(f"{target.name} was defeated!")

        else:

            old_x = enemy.x
            old_y = enemy.y

            if target.x > enemy.x:
                new_x = enemy.x + 1
            elif target.x < enemy.x:
                new_x = enemy.x - 1
            else:
                new_x = enemy.x

            if target.y > enemy.y:
                new_y = enemy.y + 1
            elif target.y < enemy.y:
                new_y = enemy.y - 1
            else:
                new_y = enemy.y

            if (
                0 <= new_x < WIDTH
                and 0 <= new_y < HEIGHT
                and not position_occupied(new_x, new_y)
            ):
                enemy.x = new_x
                enemy.y = new_y

            print(
                f"{enemy.name} moved "
                f"from ({old_x},{old_y}) "
                f"to ({enemy.x},{enemy.y})"
            )

def check_victory():

    for enemy in enemies:
        if enemy.alive:
            return False

    return True


def check_defeat():

    for player in players:
        if player.alive:
            return False

    return True


def player_turn():

    print("\n====================")
    print("     PLAYER TURN")
    print("====================")

    for player in players:

        if not player.alive:
            continue

        has_acted = False

        while not has_acted:

            draw_board()

            print(f"\n{player.name}'s turn")
            print(
                f"HP: {player.hp}/{player.max_hp}"
            )

            print("\n1. Move")
            print("2. Attack")
            print("3. Stats")
            print("4. Skip")

            choice = input("Choose: ")

            if choice == "1":
                move_player(player)
                has_acted = True

            elif choice == "2":
                attack_enemy(player)
                has_acted = True

            elif choice == "3":
                player.show_stats()
                input("\nPress Enter to continue...")

            elif choice == "4":
                has_acted = True

            else:
                print("Invalid choice.")

def game():

    print("===================================")
    print("       Fire Emblem At Home")
    print("===================================")

    print("\nA small enemy force has invaded the kingdom.")
    print("Defeat all enemies to win!")
    print("\nPress Enter to begin.")

    input()

    turn = 1

    while True:

        print("\n")
        print("###################################")
        print(f"             TURN {turn}")
        print("###################################")

        player_turn()

        if check_victory():

            draw_board()

            print("\n===================================")
            print("           VICTORY!")
            print("===================================")
            print("All enemies have been defeated!")

            break

        enemy_turn()

        if check_defeat():

            draw_board()

            print("\n===================================")
            print("            DEFEAT")
            print("===================================")
            print("All of your characters were defeated.")

            break

        turn += 1

    print("\nGame Over!")


if __name__ == "__main__":
    game()