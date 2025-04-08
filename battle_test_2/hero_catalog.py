from character import Hero, StatusEffect, StatusEffectType
from skill import *

hero_catalog = {
    'H001': Hero("Patrice", 150, 20, 30, 35, 120, [
        Skill("Fireball", 5, SkillType.DAMAGE, SkillTarget.ENEMY_SINGLE, (lambda user, target: int(2.5 * user.getAttackValue() + 0.01 * (target.max_hp - target.current_hp))))
    ]), # Mage
    'H002': Hero("Brine", 200, 18, 35, 38, 110, [
        Skill("Strike!", 5, SkillType.DAMAGE, SkillTarget.ENEMY_SINGLE, (lambda user, target: int(3 * user.getAttackValue()))),
        Skill("Ripost", 5, SkillType.COUNTER, SkillTarget.SELF, (lambda user, target: int(1.5 * user.getAttackValue())))
    ], gauge_growth=1.55
    ), # Warrior
    'H003': Hero("Alicia", 180, 24, 18, 32, 110, [
        Skill("Haste", 4, SkillType.BUFF, SkillTarget.SELF, None, [StatusEffect(StatusEffectType.SPD_BUFF, 6, 3)]),
        Skill("Heal", 6, SkillType.HEAL, SkillTarget.ALLY_SINGLE, (lambda user, target: int(3 * user.getAttackValue() + 0.25 * target.max_hp))),
        Skill("Slow", 5, SkillType.DEBUFF, SkillTarget.ENEMY_SINGLE, None, [StatusEffect(StatusEffectType.SPD_NERF, 11, 3)])
    ], gauge_growth=1.48) # Healer
}