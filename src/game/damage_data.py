
class SwordDamage:
    def __init__(self, damage, knockback):
        self.damage = damage
        self.knockback = knockback

class ArrowDamage:
    def __init__(self, damage, knockback):
        self.damage = damage
        self.knockback = knockback

class ExplosionDamage:
    def __init__(self, damage, origin, knockback_m):
        self.damage = damage
        self.origin = origin
        self.knockback_m = knockback_m