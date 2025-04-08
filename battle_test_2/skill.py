from enum import StrEnum, Enum, auto
from character import StatusEffect

class SkillType(StrEnum):
    DAMAGE  = "Damage"
    HEAL    = "Heal"
    BUFF    = "Buff"
    DEBUFF  = "Debuff"
    COUNTER = "Counter"

class SkillTarget(Enum):
    SELF            = auto()
    ALLY_SINGLE     = auto()
    ALLY_ALL        = auto()
    ENEMY_SINGLE    = auto()
    ENEMY_ALL       = auto()

class Skill:
    def __init__(self,
                 name: str,
                 sp_cost: int,
                 type: SkillType,
                 target: SkillTarget,
                 calculate_power: callable,
                 effects: list[StatusEffect] = []):
        self.name = name
        self.sp_cost = sp_cost
        self.type = type
        self.target = target
        self.calculate_power = calculate_power
        self.effects = effects
    
    def __repr__(self):
        return f"{self.name} -> {self.sp_cost} SP"