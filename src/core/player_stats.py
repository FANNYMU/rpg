class PlayerStats:
    def __init__(self):
        self.max_health = 100
        self.health = self.max_health
        self.max_armor = 60
        self.armor = self.max_armor
        self.wood_count = 0
        
    def take_damage(self, damage):
        if self.armor > 0:
            armor_absorbed = min(damage * 0.5, self.armor)
            self.armor -= armor_absorbed
            remaining_damage = damage - armor_absorbed
        else:
            remaining_damage = damage
            
        self.health = max(0, self.health - remaining_damage)
        
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        
    def repair_armor(self, amount):
        self.armor = min(self.max_armor, self.armor + amount)
        
    def add_wood(self, amount):
        self.wood_count += amount
        
    def is_alive(self):
        return self.health > 0