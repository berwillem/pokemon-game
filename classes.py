from abc import ABC, abstractmethod
import random
from decorators import cooldown

class Pokemon(ABC):
    """Classe abstraite représentant un Pokémon"""
    
    def __init__(self, nom, type_pokemon, pv, force):
        self.nom = nom
        self.type = type_pokemon
        self.pv = pv
        self.pv_max = pv
        self.force = force
        self.current_turn = 0
    
    def attaquer(self, cible):
        """Méthode d'attaque de base"""
        # Vérifier les avantages de type
        multiplicateur = 1.0
        
        if (self.type == "Feu" and cible.type == "Plante") or \
           (self.type == "Eau" and cible.type == "Feu") or \
           (self.type == "Plante" and cible.type == "Eau"):
            multiplicateur = 1.5
            print(f"C'est super efficace! ({multiplicateur}x)")
        
        degats = int(self.force * multiplicateur)
        cible.pv = max(0, cible.pv - degats)
        
        print(f"{self.nom} attaque {cible.nom} et inflige {degats} points de dégâts!")
        if cible.pv == 0:
            print(f"{cible.nom} est K.O.!")
        else:
            print(f"Il reste {cible.pv}/{cible.pv_max} PV à {cible.nom}")
        
        self.current_turn += 1
        return degats
    
    @cooldown(turns=3)
    def soigner(self):
        """Méthode pour soigner le Pokémon"""
        if self.pv == self.pv_max:
            print(f"{self.nom} a déjà tous ses PV!")
            return 0
        
        soin = int(self.pv_max * 0.3)  # Soigne 30% des PV max
        self.pv = min(self.pv_max, self.pv + soin)
        
        print(f"{self.nom} se soigne de {soin} PV! ({self.pv}/{self.pv_max})")
        self.current_turn += 1
        return soin
    
    def gagner(self):
        """Méthode appelée quand le Pokémon gagne un combat"""
        print(f"{self.nom} a gagné le combat!")
        return True
    
    def afficher_statistiques(self):
        """Affiche les statistiques du Pokémon"""
        print(f"Statistiques de {self.nom}:")
        print(f"Type: {self.type}")
        print(f"PV: {self.pv}/{self.pv_max}")
        print(f"Force: {self.force}")
    
    def est_vivant(self):
        """Vérifie si le Pokémon est encore en vie"""
        return self.pv > 0
    
    @abstractmethod
    def attaque_speciale(self, cible):
        """Méthode abstraite pour l'attaque spéciale, à implémenter dans les sous-classes"""
        pass
    
    def __str__(self):
        """Représentation textuelle du Pokémon"""
        return f"{self.nom} ({self.type}) - PV: {self.pv}/{self.pv_max}, Force: {self.force}"


class PokemonFeu(Pokemon):
    """Classe représentant un Pokémon de type Feu"""
    
    def __init__(self, nom, pv, force):
        super().__init__(nom, "Feu", pv, force)
    
    @cooldown(turns=4)
    def attaque_speciale(self, cible):
        """Attaque spéciale: Lance-Flammes - Inflige des dégâts et a une chance de brûler"""
        print(f"{self.nom} utilise Lance-Flammes!")
        
        # Dégâts de base plus élevés que l'attaque normale
        multiplicateur = 1.8
        if cible.type == "Plante":
            multiplicateur = 2.2
            print("C'est super efficace!")
        elif cible.type == "Eau":
            multiplicateur = 1.0
            print("Ce n'est pas très efficace...")
        
        degats = int(self.force * multiplicateur)
        cible.pv = max(0, cible.pv - degats)
        
        # 30% de chance de brûler (réduction de force)
        if random.random() < 0.3 and cible.est_vivant():
            cible.force = int(cible.force * 0.8)
            print(f"{cible.nom} est brûlé! Sa force diminue à {cible.force}!")
        
        print(f"{self.nom} inflige {degats} points de dégâts à {cible.nom}!")
        if not cible.est_vivant():
            print(f"{cible.nom} est K.O.!")
        else:
            print(f"Il reste {cible.pv}/{cible.pv_max} PV à {cible.nom}")
        
        self.current_turn += 1
        return degats


class PokemonEau(Pokemon):
    """Classe représentant un Pokémon de type Eau"""
    
    def __init__(self, nom, pv, force):
        super().__init__(nom, "Eau", pv, force)
    
    @cooldown(turns=4)
    def attaque_speciale(self, cible):
        """Attaque spéciale: Hydrocanon - Inflige des dégâts et peut réduire la précision"""
        print(f"{self.nom} utilise Hydrocanon!")
        
        # Dégâts de base plus élevés que l'attaque normale
        multiplicateur = 1.8
        if cible.type == "Feu":
            multiplicateur = 2.2
            print("C'est super efficace!")
        elif cible.type == "Plante":
            multiplicateur = 1.0
            print("Ce n'est pas très efficace...")
        
        degats = int(self.force * multiplicateur)
        cible.pv = max(0, cible.pv - degats)
        
        # 25% de chance de réduire la précision (simulé par une réduction de force)
        if random.random() < 0.25 and cible.est_vivant():
            cible.force = int(cible.force * 0.9)
            print(f"{cible.nom} est trempé! Sa précision diminue (force réduite à {cible.force})!")
        
        print(f"{self.nom} inflige {degats} points de dégâts à {cible.nom}!")
        if not cible.est_vivant():
            print(f"{cible.nom} est K.O.!")
        else:
            print(f"Il reste {cible.pv}/{cible.pv_max} PV à {cible.nom}")
        
        self.current_turn += 1
        return degats


class PokemonPlante(Pokemon):
    """Classe représentant un Pokémon de type Plante"""
    
    def __init__(self, nom, pv, force):
        super().__init__(nom, "Plante", pv, force)
    
    @cooldown(turns=4)
    def attaque_speciale(self, cible):
        """Attaque spéciale: Tranch'Herbe - Inflige des dégâts et peut voler de l'énergie"""
        print(f"{self.nom} utilise Tranch'Herbe!")
        
        # Dégâts de base plus élevés que l'attaque normale
        multiplicateur = 1.8
        if cible.type == "Eau":
            multiplicateur = 2.2
            print("C'est super efficace!")
        elif cible.type == "Feu":
            multiplicateur = 1.0
            print("Ce n'est pas très efficace...")
        
        degats = int(self.force * multiplicateur)
        cible.pv = max(0, cible.pv - degats)
        
        # 40% de chance de voler de l'énergie (se soigner)
        if random.random() < 0.4:
            soin = int(degats * 0.3)
            self.pv = min(self.pv_max, self.pv + soin)
            print(f"{self.nom} absorbe l'énergie et récupère {soin} PV! ({self.pv}/{self.pv_max})")
        
        print(f"{self.nom} inflige {degats} points de dégâts à {cible.nom}!")
        if not cible.est_vivant():
            print(f"{cible.nom} est K.O.!")
        else:
            print(f"Il reste {cible.pv}/{cible.pv_max} PV à {cible.nom}")
        
        self.current_turn += 1
        return degats


class Objet:
    """Classe représentant un objet utilisable pendant le combat"""
    
    def __init__(self, nom, description, effet, valeur):
        self.nom = nom
        self.description = description
        self.effet = effet  # Type d'effet: "soin", "force", "defense"
        self.valeur = valeur  # Valeur de l'effet
    
    def utiliser(self, pokemon):
        """Utilise l'objet sur un Pokémon"""
        if self.effet == "soin":
            if pokemon.pv == pokemon.pv_max:
                print(f"{pokemon.nom} a déjà tous ses PV!")
                return False
            
            soin = int(pokemon.pv_max * (self.valeur / 100))
            pokemon.pv = min(pokemon.pv_max, pokemon.pv + soin)
            print(f"{pokemon.nom} utilise {self.nom} et récupère {soin} PV! ({pokemon.pv}/{pokemon.pv_max})")
            return True
            
        elif self.effet == "force":
            boost = int(pokemon.force * (self.valeur / 100))
            pokemon.force += boost
            print(f"{pokemon.nom} utilise {self.nom} et gagne {boost} points de force! (Force: {pokemon.force})")
            return True
            
        return False
    
    def __str__(self):
        """Représentation textuelle de l'objet"""
        return f"{self.nom}: {self.description}"


class PokemonJoueur:
    """Classe gérant la création de Pokémon pour le joueur et la génération de Pokémon sauvages"""
    
    @staticmethod
    def creer_pokemon():
        """Permet au joueur de créer un Pokémon personnalisé"""
        print("\n=== Création de votre Pokémon ===")
        
        nom = input("Entrez le nom de votre Pokémon: ")
        
        # Choix du type
        print("\nChoisissez le type de votre Pokémon:")
        print("1. Feu")
        print("2. Eau")
        print("3. Plante")
        
        choix_type = 0
        while choix_type not in [1, 2, 3]:
            try:
                choix_type = int(input("Votre choix (1-3): "))
                if choix_type not in [1, 2, 3]:
                    print("Choix invalide. Veuillez entrer 1, 2 ou 3.")
            except ValueError:
                print("Veuillez entrer un nombre.")
        
        # Valeurs de base pour les statistiques
        pv = random.randint(80, 120)
        force = random.randint(15, 25)
        
        # Création du Pokémon selon le type choisi
        if choix_type == 1:
            return PokemonFeu(nom, pv, force)
        elif choix_type == 2:
            return PokemonEau(nom, pv, force)
        else:
            return PokemonPlante(nom, pv, force)
    
    @staticmethod
    def generer_pokemon_sauvage(niveau_min=1, niveau_max=5):
        """Génère un Pokémon sauvage aléatoire"""
        # Noms possibles pour les Pokémon sauvages
        noms_feu = ["Salamèche", "Goupix", "Caninos", "Ponyta", "Magby"]
        noms_eau = ["Carapuce", "Stari", "Magicarpe", "Psykokwak", "Krabby"]
        noms_plante = ["Bulbizarre", "Germignon", "Mystherbe", "Paras", "Tropius"]
        
        # Choix aléatoire du type
        type_pokemon = random.choice(["Feu", "Eau", "Plante"])
        
        # Sélection d'un nom en fonction du type
        if type_pokemon == "Feu":
            nom = random.choice(noms_feu)
        elif type_pokemon == "Eau":
            nom = random.choice(noms_eau)
        else:
            nom = random.choice(noms_plante)
        
        # Calcul des statistiques en fonction du niveau
        niveau = random.randint(niveau_min, niveau_max)
        pv = 50 + (niveau * 10)
        force = 10 + (niveau * 3)
        
        # Création du Pokémon selon le type
        if type_pokemon == "Feu":
            return PokemonFeu(nom, pv, force)
        elif type_pokemon == "Eau":
            return PokemonEau(nom, pv, force)
        else:
            return PokemonPlante(nom, pv, force)