from enum import Enum, StrEnum, auto
from character import *
from skill import *
from random import choice
from enemy_catalog import enemy_catalog
from hero_catalog import hero_catalog

class BattleState(StrEnum):
    IN_PROGRESS = "In Progress"
    VICTORY     = "Victory"
    DEFEAT      = "Defeat"

class PlayerAction(Enum):
    BASIC_ATTACK = auto()
    USE_SKILL = auto()

cycle_queue: list[Character] = []

# cycle_queue.append(hero_catalog['H001'].copy())
cycle_queue.append(hero_catalog['H002'].copy())
# cycle_queue.append(hero_catalog['H003'].copy())
cycle_queue.append(enemy_catalog['B0010'].copy())
# cycle_queue.append(enemy_catalog['E0001'].copy())
# cycle_queue.append(enemy_catalog['E0001'].copy())
# cycle_queue.append(enemy_catalog['E0001'].copy())
# cycle_queue.append(enemy_catalog['E0001'].copy())
# cycle_queue.append(enemy_catalog['E0002'].copy())

# cycle_queue[0].status.applyEffect(StatusEffect(StatusEffectType.ATK_BUFF, 5, 5))

for character in cycle_queue:
    print(character)
    print(character.status)
    print(character.skills)

current_state = BattleState.IN_PROGRESS

while current_state == BattleState.IN_PROGRESS:
    cycle_queue.sort(key=lambda character: character.getSpeedValue(), reverse=True)

    if [character for character in cycle_queue if character.type == CharacterType.ALLY] == []:
        print("No Character on Player Side")
        break

    if [character for character in cycle_queue if character.type == CharacterType.ENEMY] == []:
        print("No Character on Enemy Side")
        break

    for character in cycle_queue:
        character.status.updateEffects()
        character.status.clearCounterSkill()

        if character.status.is_alive != True:
            continue

        if character.type == CharacterType.ALLY:
            print(character)

            action = choice(list(PlayerAction))

            match action:
                case PlayerAction.BASIC_ATTACK:
                    target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)])
                    total_damage = int(character.getAttackValue() - 0.2 * target.getDefenseValue())
                    target.current_hp = max(0, target.current_hp - total_damage)
                    character.current_sp = min(character.max_sp, character.current_sp + 1) # SP recovery

                    print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) dealt {total_damage} damage to {target.name} ({target.current_hp}/{target.max_hp})")

                    if target.current_hp <= 0:
                        target.status.is_alive = False
                        print(f"{target.name} has been defeated")
                    
                    else:
                        if target.status.isCounterActive():
                            total_damage = int(target.status.counter_skill.calculate_power(target, character) - 0.2 * character.getDefenseValue())
                            character.current_hp = max(0, character.current_hp - total_damage)
                            # target.current_sp = min(target.max_sp, target.current_sp + 1)
                            
                            print(f"LV{target.level} {target.name} ({target.current_hp}/{target.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                            if character.current_hp <= 0:
                                character.status.is_alive = False
                                print(f"{character.name} has been defeated")
                                            
                case PlayerAction.USE_SKILL:
                    available_skills = [skill for skill in character.skills if (skill.sp_cost <= character.current_sp)]

                    if available_skills == []:
                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)])
                        total_damage = int(character.getAttackValue() - 0.2 * target.getDefenseValue())
                        target.current_hp = max(0, target.current_hp - total_damage)
                        character.current_sp = min(character.max_sp, character.current_sp + 1) # SP recovery

                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) dealt {total_damage} damage to {target.name} ({target.current_hp}/{target.max_hp})")

                        if target.current_hp <= 0:
                            target.status.is_alive = False
                            print(f"{target.name} has been defeated")

                        else:
                            if target.status.isCounterActive():
                                total_damage = int(target.status.counter_skill.calculate_power(target, character) - 0.2 * character.getDefenseValue())
                                character.current_hp = max(0, character.current_hp - total_damage)
                                # target.current_sp = min(target.max_sp, target.current_sp + 1)
                                
                                print(f"LV{target.level} {target.name} ({target.current_hp}/{target.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                                if character.current_hp <= 0:
                                    character.status.is_alive = False
                                    print(f"{character.name} has been defeated")
                            
                    else:
                        used_skill = choice(available_skills)
                        character.current_sp -= used_skill.sp_cost

                        match used_skill.type:
                            case SkillType.DAMAGE:
                                match used_skill.target:
                                    case SkillTarget.ENEMY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)])
                                        total_damage = int(used_skill.calculate_power(character, target) - 0.2 * target.getDefenseValue())
                                        target.current_hp = max(0, target.current_hp - total_damage)

                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) dealt {total_damage} damage using \"{used_skill.name}\" to LV{target.level} {target.name} ({target.current_hp}/{target.max_hp})")

                                        if target.current_hp <= 0:
                                            target.status.is_alive = False
                                            print(f"{target.name} has been defeated")

                                        else:
                                            if target.status.isCounterActive():
                                                total_damage = int(target.status.counter_skill.calculate_power(target, character) - 0.2 * character.getDefenseValue())
                                                character.current_hp = max(0, character.current_hp - total_damage)
                                                # target.current_sp = min(target.max_sp, target.current_sp + 1)
                                                
                                                print(f"LV{target.level} {target.name} ({target.current_hp}/{target.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                                                if character.current_hp <= 0:
                                                    character.status.is_alive = False
                                                    print(f"{character.name} has been defeated")
                                    
                                    case SkillTarget.ENEMY_ALL:
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) cast \"{used_skill.name}\" to all active enemies:")
                                        
                                        for enemy in [_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)]:
                                            total_damage = int(used_skill.calculate_power(character, enemy) - 0.2 * enemy.getDefenseValue())
                                            enemy.current_hp = max(0, enemy.current_hp - total_damage)

                                            print(f"LV{enemy.level} {enemy.name} lost HP by {total_damage}")

                                            if enemy.current_hp <= 0:
                                                enemy.status.is_alive = False
                                                print(f"{enemy.name} has been defeated")
                                            
                                            else:
                                                if enemy.status.isCounterActive():
                                                    total_damage = int(enemy.status.counter_skill.calculate_power(enemy, character) - 0.2 * character.getDefenseValue())
                                                    character.current_hp = max(0, character.current_hp - total_damage)
                                                    # target.current_sp = min(target.max_sp, target.current_sp + 1)
                                                    
                                                    print(f"LV{enemy.level} {enemy.name} ({enemy.current_hp}/{enemy.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                                                    if character.current_hp <= 0:
                                                        character.status.is_alive = False
                                                        print(f"{character.name} has been defeated")
                                    
                                    case _:
                                        pass # Error Function
                            
                            case SkillType.HEAL:
                                match used_skill.target:
                                    case SkillTarget.SELF:
                                        total_heal = used_skill.calculate_power(character, character)
                                        character.current_hp = min(character.max_hp, character.current_hp + total_heal)

                                        print(f"LV{character.level} {character.name} using \"{used_skill.name}\" on self, restoring HP by {total_heal}")

                                    case SkillTarget.ALLY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)])
                                        total_heal = used_skill.calculate_power(character, target)
                                        target.current_hp = min(target.max_hp, target.current_hp + total_heal)

                                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) using \"{used_skill.name}\" on {target.name}, restoring HP by {total_heal}")

                                    case SkillTarget.ALLY_ALL:
                                        print(f"LV{character.level} {character.name} casts \"{used_skill.name}\" to all active party members")

                                        for ally in [_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)]:
                                            total_heal = used_skill.calculate_power(character, ally)
                                            ally.current_hp = min(ally.max_hp, ally.current_hp + total_heal)
                                            print(f"Restoring LV{ally.level} {ally.name} HP by {total_heal}")

                                    case _:
                                        pass # Error Function

                            case SkillType.BUFF:
                                match used_skill.target:
                                    case SkillTarget.SELF:
                                        for effect in used_skill.effects:
                                            character.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) using \"{used_skill.name}\" on self")

                                    case SkillTarget.ALLY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)])
                                        
                                        for effect in used_skill.effects:
                                            target.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) cast \"{used_skill.name}\" on LV{target.level} {target.name}")

                                    case SkillTarget.ALLY_ALL:
                                        for ally in [_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)]:
                                            for effect in used_skill.effects:
                                                ally.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) cast \"{used_skill.name}\" on all active party members")

                                    case _:
                                        pass # Error Function

                            case SkillType.DEBUFF:
                                match used_skill.target:
                                    case SkillTarget.ENEMY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)])

                                        for effect in used_skill.effects:
                                            target.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) implied \"{used_skill.name}\" on LV{target.level} {target.name}")

                                    case SkillTarget.ENEMY_ALL:
                                        for enemy in [_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)]:
                                            for effect in used_skill.effects:
                                                enemy.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) implied \"{used_skill.name}\" on all active enemies")

                                    case _:
                                        pass # Error Function

                            case SkillType.COUNTER:
                                match used_skill.target:
                                    case SkillTarget.SELF:
                                        # Make counter status on
                                        character.status.setCounterSkill(used_skill)
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) set \"{used_skill.name}\" as counter skill")

                                    case _:
                                        pass # Error Function

        elif character.type == CharacterType.ENEMY:            
            action = choice(list(PlayerAction))

            match action:
                case PlayerAction.BASIC_ATTACK:
                    target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)])
                    total_damage = int(character.getAttackValue() - 0.2 * target.getDefenseValue())
                    target.current_hp = max(0, target.current_hp - total_damage)
                    character.current_sp = min(character.max_sp, character.current_sp + 1)

                    print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) dealt {total_damage} damage to LV{target.level} {target.name} ({target.current_hp}/{target.max_hp})")

                    if target.current_hp <= 0:
                        target.status.is_alive = False
                        print(f"{target.name} has been defeated")
                    
                    else:
                        if target.status.isCounterActive():
                            total_damage = int(target.status.counter_skill.calculate_power(target, character) - 0.2 * character.getDefenseValue())
                            character.current_hp = max(0, character.current_hp - total_damage)
                            # target.current_sp = min(target.max_sp, target.current_sp + 1)
                            
                            print(f"LV{target.level} {target.name} ({target.current_hp}/{target.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                            if character.current_hp <= 0:
                                character.status.is_alive = False
                                print(f"{character.name} has been defeated")

                case PlayerAction.USE_SKILL:
                    available_skill = [skill for skill in character.skills if (skill.sp_cost <= character.current_sp)]

                    if available_skill == []:
                        # Do the Basic Attack
                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)])
                        total_damage = int(character.getAttackValue() - 0.2 * target.getDefenseValue())
                        target.current_hp = max(0, target.current_hp - total_damage)
                        character.current_sp = min(character.max_sp, character.current_sp + 1)

                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) dealt {total_damage} damage to LV{target.level} {target.name} ({target.current_hp}/{target.max_hp})")

                        if target.current_hp <= 0:
                            target.status.is_alive = False
                            print(f"{target.name} has been defeated")

                        else:
                            if target.status.isCounterActive():
                                total_damage = int(target.status.counter_skill.calculate_power(target, character) - 0.2 * character.getDefenseValue())
                                character.current_hp = max(0, character.current_hp - total_damage)
                                # target.current_sp = min(target.max_sp, target.current_sp + 1)
                                
                                print(f"LV{target.level} {target.name} ({target.current_hp}/{target.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                                if character.current_hp <= 0:
                                    character.status.is_alive = False
                                    print(f"{character.name} has been defeated")
                    
                    else:
                        chosen_skill = choice(available_skill)
                        character.current_sp -= chosen_skill.sp_cost

                        match chosen_skill.type:
                            case SkillType.DAMAGE:
                                match chosen_skill.target:
                                    case SkillTarget.ENEMY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)])
                                        total_damage = int(chosen_skill.calculate_power(character, target) - 0.2 * target.getDefenseValue())
                                        target.current_hp = max(0, target.current_hp - total_damage)

                                        for effect in chosen_skill.effects:
                                            target.status.applyEffect(effect)
                                            # Suggestion: add chance of getting the effect. On this case, this is absolute

                                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) dealt {total_damage} damage using \"{chosen_skill.name}\" to LV{target.level} {target.name} ({target.current_hp}/{target.max_hp})")

                                        if target.current_hp <= 0:
                                            target.status.is_alive = False
                                            print(f"{target.name} has been defeated")
                                        
                                        else:
                                            if target.status.isCounterActive():
                                                total_damage = int(target.status.counter_skill.calculate_power(target, character) - 0.2 * character.getDefenseValue())
                                                character.current_hp = max(0, character.current_hp - total_damage)
                                                
                                                print(f"LV{target.level} {target.name} ({target.current_hp}/{target.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                                                if character.current_hp <= 0:
                                                    character.status.is_alive = False
                                                    print(f"{character.name} has been defeated")

                                    case SkillTarget.ENEMY_ALL:
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) cast \"{chosen_skill.name}\" to all party member:")

                                        for enemy in [_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)]:
                                            total_damage = int(chosen_skill.calculate_power(character, enemy) - 0.2 * enemy.getDefenseValue())
                                            enemy.current_hp = max(0, enemy.current_hp - total_damage)

                                            print(f"LV{enemy.level} {enemy.name} lost HP by {total_damage}")

                                            if enemy.current_hp <= 0:
                                                enemy.status.is_alive = False
                                                print(f"{enemy.name} has been defeated")
                                            else:
                                                # Could be better if the retaliatory attack started outside the for loop
                                                if enemy.status.isCounterActive():
                                                    total_damage = int(enemy.status.counter_skill.calculate_power(enemy, character) - 0.2 * character.getDefenseValue())
                                                    character.current_hp = max(0, character.current_hp - total_damage)
                                                    
                                                    print(f"LV{enemy.level} {enemy.name} ({enemy.current_hp}/{enemy.max_hp}) dealt {total_damage} damage to {character.name} ({character.current_hp}/{character.max_hp}) using retaliatory attack")

                                                    if character.current_hp <= 0:
                                                        character.status.is_alive = False
                                                        print(f"{character.name} has been defeated")

                                    case _:
                                        raise ValueError

                            case SkillType.HEAL:
                                match chosen_skill.target:
                                    case SkillTarget.SELF:
                                        total_heal = chosen_skill.calculate_power(character, character)
                                        character.current_hp = min(character.max_hp, character.current_hp + total_heal)

                                        print(f"LV{character.level} {character.name} using \"{chosen_skill.name}\" on self, restoring HP by {total_heal}")
                                    
                                    case SkillTarget.ALLY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)])
                                        total_heal = chosen_skill.calculate_power(character, target)
                                        target.current_hp = min(target.max_hp, target.current_hp + total_heal)

                                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) using \"{chosen_skill.name}\" on {target.name}, restoring HP by {total_heal}")

                                    case SkillTarget.ALLY_ALL:
                                        print(f"LV{character.level} {character.name} casts \"{chosen_skill.name}\" to all active allies (enemy)")

                                        for ally in [_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)]:
                                            total_heal = chosen_skill.calculate_power(character, ally)
                                            ally.current_hp = min(ally.max_hp, ally.current_hp + total_heal)
                                            print(f"Restoring LV{ally.level} {ally.name} HP by {total_heal}")

                                    case _:
                                        pass

                            case SkillType.BUFF:
                                match chosen_skill.target:
                                    case SkillTarget.SELF:
                                        for effect in chosen_skill.effects:
                                            character.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) using \"{chosen_skill.name}\" on self")

                                    case SkillTarget.ALLY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)])

                                        for effect in chosen_skill.effects:
                                            character.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} ({character.current_hp}/{character.max_hp}) using \"{chosen_skill.name}\" on LV{target.level} {target.name}")

                                    case SkillTarget.ALLY_ALL:
                                        for ally in [_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)]:
                                            for effect in chosen_skill.effects:
                                                ally.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) cast \"{used_skill.name}\" on all active allies (enemy)")

                                    case _:
                                        raise ValueError

                            case SkillType.DEBUFF:
                                match chosen_skill.target:
                                    case SkillTarget.ENEMY_SINGLE:
                                        target = choice([_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)])
                                        for effect in chosen_skill.effects:
                                            target.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) implied \"{chosen_skill.name}\" on LV{target.level} {target.name}")

                                    case SkillTarget.ENEMY_ALL:
                                        for enemy in [_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)]:
                                            for effect in chosen_skill.effects:
                                                enemy.status.applyEffect(effect)
                                        
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) implied \"{chosen_skill.name}\" on all active party members")

                            case SkillType.COUNTER:
                                # Make counter status on
                                match chosen_skill.target:
                                    case SkillTarget.SELF:
                                        character.status.setCounterSkill(chosen_skill)
                                        print(f"LV{character.level} {character.name} (HP {character.current_hp}/{character.max_hp}) set \"{chosen_skill.name}\" as counter skill")

                                    case _:
                                        raise ValueError
                            case _:
                                raise ValueError
            
        if not [_ for _ in cycle_queue if (_.type == CharacterType.ENEMY and _.status.is_alive == True)]:
            current_state = BattleState.VICTORY
            break

        if not [_ for _ in cycle_queue if (_.type == CharacterType.ALLY and _.status.is_alive == True)]:
            current_state = BattleState.DEFEAT
            break
        
        input()
    
if current_state == BattleState.VICTORY:
    print("Victory!")

    exp_gained = sum([character.exp_reward for character in cycle_queue if character.type == CharacterType.ENEMY])
    for _character in [character for character in cycle_queue if character.type == CharacterType.ALLY]:
        _character.gainExp(exp_gained)

elif current_state == BattleState.DEFEAT:
    print("Defeat!")