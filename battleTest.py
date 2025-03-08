from enum import StrEnum
from random import choice

class CharacterType(StrEnum):
    PROTAGONIST  = "Ally"
    OPPONENT     = "COM"

class BattleState(StrEnum):
    IN_PROGRESS = "In Progress"
    VICTORY     = "Victory"
    DEFEAT      = "Defeat"

class Character:
    def __init__(self, name: str, character_type: CharacterType, hp: int, sp: int, atk: int, defense: int):
        self.name = name
        self.character_type = character_type
        self.hp = hp
        self.sp = sp
        self.atk = atk
        self.defense = defense
        self.temp_defense = 0
    
character_list = [
    Character("Alicia", CharacterType.PROTAGONIST, 150, 20, 15, 10),
    Character("Brine", CharacterType.OPPONENT, 200, 10, 20, 5)
]

battle_state = BattleState.IN_PROGRESS

while battle_state == BattleState.IN_PROGRESS:
    for character in character_list:
        print(f"{character.name} ({character.character_type.value}) - HP: {character.hp}, SP: {character.sp}, ATK: {character.atk}, DEF: {character.defense}")

        match character.character_type:
            case CharacterType.PROTAGONIST:
                print("Actions:")
                print("1 <- Attack")
                print("2 <- Defend")
                print("3 <- Use Skill")

                action = int(input("Select an action: "))

                if action == 1:
                    print("Choose target to attack.")

                    # Make a list of opponents to choose from
                    for i, opponent in enumerate(character_list):
                        if opponent.character_type == CharacterType.OPPONENT:
                            print(f"{i + 1} <- {opponent.name} - HP: {opponent.hp}, SP: {opponent.sp}, ATK: {opponent.atk}, DEF: {opponent.defense}")
                    
                    # Select a target
                    target = character_list[int(input("Select a target: ")) - 1]
                    print(f"You chose to attack {target.name}.")

                    damage = int(character.atk - 0.2 * (target.defense + target.temp_defense)) # Simple damage calculation
                    target.hp -= damage # Apply damage to target
                    target.temp_defense = 0 # Reset temporary defense

                    print(f"{target.name} took {damage} damage.")

                    # Check if target is defeated
                    if target.hp <= 0:
                        target.hp = 0
                        print(f"{target.name} has been defeated.")


                    # Scan for remaining opponents
                    remaining_opponents = [opponent for opponent in character_list if opponent.character_type == CharacterType.OPPONENT and opponent.hp > 0]
                    if not remaining_opponents:
                        print("All opponents have been defeated.")
                        battle_state = BattleState.VICTORY
                        break

                elif action == 2:
                    print("You chose to defend.")
                    character.temp_defense = int(2 * character.defense) # Temporary defense boost

                elif action == 3:
                    print("You chose to use a skill.")
                
                print()
                
            case CharacterType.OPPONENT:
                if character.hp <= 0:
                    continue # Skip turn if character is K.O.

                actions = ["Attack", "Defend"]
                action = choice(actions)

                match action:
                    case "Attack":
                        target = choice([character for character in character_list if character.character_type == CharacterType.PROTAGONIST])
                        print(f"{character.name} chose to attack {target.name}.")

                        damage = int(character.atk - 0.2 * (target.defense + target.temp_defense))
                        target.hp -= damage
                        target.temp_defense = 0

                        print(f"{target.name} took {damage} damage.")

                        # Check if target is defeated
                        if target.hp <= 0:
                            target.hp = 0
                            print(f"{target.name} has been defeated.")

                        # Scan for remaining protagonists
                        remaining_protagonists = [protagonist for protagonist in character_list if protagonist.character_type == CharacterType.PROTAGONIST and protagonist.hp > 0]
                        if not remaining_protagonists:
                            print("All protagonists have been defeated.")
                            battle_state = BattleState.DEFEAT
                            break

                    case "Defend":
                        print(f"{character.name} chose to defend.")
                        character.temp_defense = int(2 * character.defense) # Temporary defense boost

            case _:
                print("This character is not recognized.")

if battle_state == BattleState.VICTORY:
    print("Victory!")
elif battle_state == BattleState.DEFEAT:
    print("Defeat.")