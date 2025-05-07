import os
import random
import time
from classes import PokemonJoueur, Objet
from utils import charger_statistiques, mettre_a_jour_statistiques, afficher_statistiques

def effacer_ecran():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def creer_objets():
    """Crée une liste d'objets utilisables"""
    objets = [
        Objet("Potion", "Restaure 30% des PV max", "soin", 30),
        Objet("Super Potion", "Restaure 50% des PV max", "soin", 50),
        Objet("Hyper Potion", "Restaure 70% des PV max", "soin", 70),
        Objet("Protéine", "Augmente la force de 20%", "force", 20),
        Objet("Fer", "Augmente la force de 30%", "force", 30)
    ]
    return objets

def choisir_objet(objets):
    """Permet au joueur de choisir un objet à utiliser"""
    print("\nChoisissez un objet à utiliser:")
    for i, objet in enumerate(objets, 1):
        print(f"{i}. {objet}")
    print(f"{len(objets) + 1}. Retour")
    
    choix = 0
    while choix < 1 or choix > len(objets) + 1:
        try:
            choix = int(input("Votre choix: "))
            if choix < 1 or choix > len(objets) + 1:
                print(f"Veuillez entrer un nombre entre 1 et {len(objets) + 1}")
        except ValueError:
            print("Veuillez entrer un nombre valide")
    
    if choix == len(objets) + 1:
        return None
    
    return objets[choix - 1]

def combat(pokemon_joueur, pokemon_adversaire, objets):
    """Gère un combat entre deux Pokémon"""
    tour = 1
    
    while pokemon_joueur.est_vivant() and pokemon_adversaire.est_vivant():
        effacer_ecran()
        print(f"\n=== Tour {tour} ===")
        print(f"\n{pokemon_joueur}")
        print(f"{pokemon_adversaire}\n")
        
        # Tour du joueur
        print("C'est votre tour!")
        print("1. Attaque normale")
        print("2. Attaque spéciale")
        print("3. Se soigner")
        print("4. Utiliser un objet")
        
        action = 0
        while action not in [1, 2, 3, 4]:
            try:
                action = int(input("Votre action (1-4): "))
                if action not in [1, 2, 3, 4]:
                    print("Action invalide. Veuillez choisir entre 1 et 4.")
            except ValueError:
                print("Veuillez entrer un nombre.")
        
        if action == 1:
            pokemon_joueur.attaquer(pokemon_adversaire)
        elif action == 2:
            pokemon_joueur.attaque_speciale(pokemon_adversaire)
        elif action == 3:
            pokemon_joueur.soigner()
        elif action == 4:
            objet = choisir_objet(objets)
            if objet:
                objet.utiliser(pokemon_joueur)
        
        # Vérifier si l'adversaire est K.O.
        if not pokemon_adversaire.est_vivant():
            print(f"\n{pokemon_adversaire.nom} est K.O.!")
            pokemon_joueur.gagner()
            mettre_a_jour_statistiques(True)
            input("\nAppuyez sur Entrée pour continuer...")
            return True
        
        # Tour de l'adversaire
        print("\nC'est le tour de l'adversaire!")
        time.sleep(1)  # Pause pour l'effet dramatique
        
        # L'IA choisit une action
        if pokemon_adversaire.pv < pokemon_adversaire.pv_max * 0.3 and random.random() < 0.7:
            # Si PV bas, 70% de chance de se soigner
            pokemon_adversaire.soigner()
        elif random.random() < 0.3:
            # 30% de chance d'utiliser l'attaque spéciale
            pokemon_adversaire.attaque_speciale(pokemon_joueur)
        else:
            # Sinon, attaque normale
            pokemon_adversaire.attaquer(pokemon_joueur)
        
        # Vérifier si le joueur est K.O.
        if not pokemon_joueur.est_vivant():
            print(f"\n{pokemon_joueur.nom} est K.O.!")
            pokemon_adversaire.gagner()
            mettre_a_jour_statistiques(False)
            input("\nAppuyez sur Entrée pour continuer...")
            return False
        
        tour += 1
        input("\nAppuyez sur Entrée pour continuer...")
    
    return pokemon_joueur.est_vivant()

def combat_joueur_vs_sauvage():
    """Mode de jeu: Joueur contre Pokémon sauvage"""
    effacer_ecran()
    print("\n=== Mode Joueur contre Pokémon sauvage ===")
    
    # Charger les statistiques pour déterminer le niveau du Pokémon sauvage
    statistiques = charger_statistiques()
    niveau_min = max(1, statistiques["niveau"] - 1)
    niveau_max = statistiques["niveau"] + 2
    
    # Créer le Pokémon du joueur
    pokemon_joueur = PokemonJoueur.creer_pokemon()
    
    # Générer un Pokémon sauvage
    pokemon_sauvage = PokemonJoueur.generer_pokemon_sauvage(niveau_min, niveau_max)
    
    print(f"\nUn {pokemon_sauvage.nom} sauvage apparaît!")
    time.sleep(1)
    
    # Créer les objets disponibles
    objets = creer_objets()
    
    # Lancer le combat
    return combat(pokemon_joueur, pokemon_sauvage, objets)

def combat_joueur_vs_joueur():
    """Mode de jeu: Joueur contre Joueur (local)"""
    effacer_ecran()
    print("\n=== Mode Joueur contre Joueur ===")
    
    print("\nJoueur 1, créez votre Pokémon:")
    pokemon_joueur1 = PokemonJoueur.creer_pokemon()
    
    print("\nJoueur 2, créez votre Pokémon:")
    pokemon_joueur2 = PokemonJoueur.creer_pokemon()
    
    # Créer les objets disponibles
    objets = creer_objets()
    
    # Lancer le combat
    return combat(pokemon_joueur1, pokemon_joueur2, objets)

def menu_principal():
    """Affiche le menu principal du jeu"""
    while True:
        effacer_ecran()
        print("\n=== POKÉMON BATTLE ===")
        print("1. Joueur contre Pokémon sauvage")
        print("2. Joueur contre Joueur (local)")
        print("3. Voir les statistiques du joueur")
        print("4. Quitter")
        
        choix = 0
        while choix not in [1, 2, 3, 4]:
            try:
                choix = int(input("Votre choix (1-4): "))
                if choix not in [1, 2, 3, 4]:
                    print("Choix invalide. Veuillez entrer 1, 2, 3 ou 4.")
            except ValueError:
                print("Veuillez entrer un nombre.")
        
        if choix == 1:
            combat_joueur_vs_sauvage()
        elif choix == 2:
            combat_joueur_vs_joueur()
        elif choix == 3:
            afficher_statistiques()
        elif choix == 4:
            print("\nMerci d'avoir joué! À bientôt!")
            break

if __name__ == "__main__":
    # Charger les statistiques au démarrage
    charger_statistiques()
    
    # Lancer le menu principal
    menu_principal()