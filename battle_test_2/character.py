from enum import Enum, StrEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skill import Skill

class CharacterType(StrEnum):
    ALLY  = "Ally"
    ENEMY = "COM"

class StatusEffectType(Enum):
    ATK_BUFF  = auto()
    DEF_BUFF  = auto()
    SPD_BUFF  = auto()
    ATK_NERF  = auto()
    DEF_NERF  = auto()
    SPD_NERF  = auto()
    GUARD_DEF = auto()

class StatusEffect:
    def __init__(self,
                 effect_type: StatusEffectType,
                 value: int,
                 duration: int):
        self.effect_type = effect_type
        self.value = value
        self.duration = duration
    
    def __repr__(self):
        return f"{self.effect_type.name}(Val: {self.value}, Dur: {self.duration})"

class CharacterStatus:
    def __init__(self):
        # self.attack_buff = 0
        # self.attack_nerf = 0
        # self.defense_buff = 0
        # self.guard_defense = 0
        # self.defense_nerf = 0
        # self.speed_buff = 0
        # self.speed_nerf = 0

        self.is_alive = True
        self.effects: list[StatusEffect] = []
        self.counter_skill: 'Skill' | None = None
    
    def isAlive(self):
        return self.is_alive
    
    def setCounterSkill(self, skill: 'Skill'):
        self.counter_skill = skill
    
    def clearCounterSkill(self):
        self.counter_skill = None
    
    def isCounterActive(self):
        return self.counter_skill is not None

    def applyEffect(self, effect: StatusEffect):
        self.effects.append(effect)
    
    def updateEffects(self):
        self.effects = [effect for effect in self.effects if effect.duration > 0]

        for effect in self.effects:
            effect.duration -= 1

    def getStatModifier(self, effect_type: StatusEffectType):
        return sum(effect.value for effect in self.effects if effect.effect_type == effect_type)

    def __repr__(self):
        return f"Effects: {self.effects}, isAlive={self.is_alive}"

class Character:
    def __init__(self, 
                 name: str,
                 type: CharacterType,
                 health_point: int,
                 skill_point: int|None,
                 base_attack: int,
                 base_defense: int,
                 base_speed: int = 100,
                 skills: list['Skill'] = [],
                 level: int = 1,
                 health_point_growth: float = 0.1,
                 skill_point_growth: float|None = 0.1,
                 attack_growth: float = 0.1,
                 defense_growth: float = 0.1
                 ) -> None:
        self.name = name
        self.type = type
        self.level = level
        self.base_hp = health_point
        self.max_hp = health_point
        self.current_hp = health_point
        self.base_sp = skill_point
        self.max_sp = skill_point
        self.current_sp = skill_point
        self.base_attack = base_attack
        self.attack = base_attack
        self.base_defense = base_defense
        self.defense = base_defense
        self.base_speed = base_speed
        self.speed = base_speed
        self.skills = skills

        # Growth Attribute
        self.hp_growth = health_point_growth
        self.sp_growth = skill_point_growth
        self.attack_growth = attack_growth
        self.defense_growth = defense_growth

        # In-Battle Attribute
        self.status = CharacterStatus()
    
    def getAttackValue(self):
        return self.attack + self.status.getStatModifier(StatusEffectType.ATK_BUFF) - self.status.getStatModifier(StatusEffectType.ATK_NERF)

    def getDefenseValue(self):
        return self.defense + self.status.getStatModifier(StatusEffectType.DEF_BUFF) - self.status.getStatModifier(StatusEffectType.DEF_NERF)

    def getSpeedValue(self):
        return self.speed + self.status.getStatModifier(StatusEffectType.SPD_BUFF) - self.status.getStatModifier(StatusEffectType.SPD_NERF)

    def __repr__(self):
        return f"<Level {self.level} {self.name}> ({self.type.name})" + (f"HP: {self.current_hp}/{self.max_hp}, SP: {self.current_sp}/{self.max_sp}" if self.type == CharacterType.ALLY else "")

class Hero(Character):
    def __init__(self, 
                 name, 
                 health_point, 
                 skill_point, 
                 base_attack, 
                 base_defense, 
                 base_speed = 100, 
                 skills = [],
                 equipment = [],
                 level = 1,
                 health_point_growth = 0.1,
                 skill_point_growth = 0.1,
                 attack_growth = 0.1, 
                 defense_growth = 0.1,
                 exp = 0,
                 gauge_growth = 1.5,
                 base_gauge = 150) -> None:
        super().__init__(name, CharacterType.ALLY, health_point, skill_point, base_attack, base_defense, base_speed, skills, level, health_point_growth, skill_point_growth, attack_growth, defense_growth)
        self.equipment = equipment          # Need to be improved
        
        self.current_exp = exp
        self.base_gauge = base_gauge
        self.current_gauge = base_gauge
        self.gauge_growth = gauge_growth
        
        # Updating level automatically
        self.gainExp(0)
    
    def copy(self):
        return Hero(
            self.name,
            self.base_hp,
            self.base_sp,
            self.base_attack,
            self.base_defense,
            self.base_speed,
            self.skills,
            self.equipment,
            self.level,
            self.hp_growth,
            self.sp_growth,
            self.attack_growth,
            self.defense_growth,
            self.current_exp,
            self.gauge_growth,
            self.base_gauge
        )

    def isLevelUpEligible(self) -> bool:
        return self.current_exp >= self.current_gauge

    def calculateGauge(self, current_level:int):
        return int(self.base_gauge * (current_level ** self.gauge_growth))

    def gainExp(self, exp):
        self.current_exp += exp
        while self.isLevelUpEligible():
            self.levelUp()
    
    def levelUp(self):
        self.level += 1
        self.current_gauge += self.calculateGauge(self.level)
        self.max_hp += int(self.base_hp * self.hp_growth)
        self.max_sp += int(self.base_sp * self.sp_growth)
        self.attack += int(self.base_attack * self.attack_growth)
        self.defense += int(self.base_defense * self.defense_growth)
        self.current_hp = self.max_hp
        self.current_sp = self.max_sp
        
        print(f"{self.name} leveled up to {self.level}! Exp: {self.current_exp}/{self.current_gauge}")

    def adjustStats(self):
        self.current_exp = self.current_exp if (self.level > 1) else sum([self.calculateGauge(i) for i in range(1, self.level)])
        self.current_gauge = sum([self.calculateGauge(i + 1) for i in range(self.level)])
        self.max_hp = self.level * int(self.base_hp * self.hp_growth)
        self.max_sp = self.level * int(self.base_sp * self.sp_growth)
        self.attack = self.level * int(self.base_attack * self.attack_growth)
        self.defense = self.level * int(self.base_defense * self.defense_growth)

    def __repr__(self):
        return super().__repr__()

class Enemy(Character):
    def __init__(self, 
                 name, 
                 health_point, 
                 base_attack, 
                 base_defense, 
                 base_speed = 100, 
                 exp_reward = 0, 
                 skills = [], 
                 level = 1,
                 skill_point = 0,  # Unused for simple system
                 health_point_growth = 0.1,
                 skill_point_growth: float | None = None,
                 attack_growth = 0.1, 
                 defense_growth = 0.1) -> None:
        super().__init__(name, CharacterType.ENEMY, health_point, skill_point, base_attack, base_defense, base_speed, skills, level, health_point_growth, skill_point_growth, attack_growth, defense_growth)
        self.exp_reward = exp_reward
    
    def copy(self):
        return Enemy(
            self.name,
            self.base_hp,
            self.base_attack,
            self.base_defense,
            self.base_speed,
            self.exp_reward,
            self.skills,
            self.level,
            self.base_sp,
            self.hp_growth,
            self.sp_growth,
            self.attack_growth,
            self.defense_growth
        )

    def __repr__(self):
        return super().__repr__()