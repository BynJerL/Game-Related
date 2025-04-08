from character import Enemy, StatusEffect, StatusEffectType
from skill import *

enemy_catalog = {
    'E0001' : Enemy("Skeleton", 50, 10, 10, exp_reward=100, skills=[
        Skill("Razor Cut", 0, SkillType.DAMAGE, SkillTarget.ENEMY_SINGLE, (lambda user, target: int(1.6 * user.getAttackValue() + min(100, 0.01 * (target.max_hp - target.current_hp)))))
    ]),
    'E0002' : Enemy("Skeleton Captain", 120, 15, 10, 110, skill_point=3, exp_reward=240, skills=[
        Skill("Razor Cut", 0, SkillType.DAMAGE, SkillTarget.ENEMY_SINGLE, (lambda user, target: int(1.6 * user.getAttackValue() + min(100, 0.01 * (target.max_hp - target.current_hp))))),
        Skill("Recharge", 3, SkillType.BUFF, SkillTarget.SELF, None, [
            StatusEffect(StatusEffectType.ATK_BUFF, 10, 3),
            StatusEffect(StatusEffectType.SPD_BUFF, 10, 3)
        ])
    ]),
    'B0010' : Enemy("Heorot-Rendezvoid", 800, 40, 60, 115, skill_point=6, exp_reward=3000, skills=[
        Skill("Headstriker", 0, SkillType.DAMAGE, SkillTarget.ENEMY_SINGLE, (lambda user, target: int(user.getAttackValue())), [StatusEffect(StatusEffectType.SPD_NERF, 10, 3)]),
        Skill("Hollow Cutter", 5, SkillType.DAMAGE, SkillTarget.ENEMY_SINGLE, (lambda user, target: int(1.6 * user.getAttackValue() + min(100, 0.01 * (target.max_hp - target.current_hp)))))
    ])
}