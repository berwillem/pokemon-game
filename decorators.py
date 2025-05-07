import functools
import time

def cooldown(turns=3):
    """
    Décorateur qui empêche l'utilisation d'une méthode pendant un certain nombre de tours.
    """
    def decorator(func):
        cooldowns = {}
        
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # Identifiant unique pour chaque instance et méthode
            instance_id = id(self)
            
            # Vérifier si la méthode est en cooldown
            current_turn = getattr(self, 'current_turn', 0)
            if instance_id in cooldowns and current_turn - cooldowns[instance_id] < turns:
                remaining = turns - (current_turn - cooldowns[instance_id])
                print(f"Cette action est en cooldown pour encore {remaining} tour(s)!")
                return None
            
            # Exécuter la méthode et mettre à jour le cooldown
            result = func(self, *args, **kwargs)
            cooldowns[instance_id] = current_turn
            return result
            
        return wrapper
    return decorator