import os
import json

def charger_statistiques():
    """Charge les statistiques du joueur depuis le fichier"""
    if not os.path.exists("statistiques.txt"):
        statistiques = {
            "niveau": 1,
            "victoires": 0,
            "defaites": 0,
            "combats_total": 0
        }
        sauvegarder_statistiques(statistiques)
        return statistiques
    
    try:
        with open("statistiques.txt", "r") as fichier:
            return json.load(fichier)
    except:
        # En cas d'erreur, créer des statistiques par défaut
        statistiques = {
            "niveau": 1,
            "victoires": 0,
            "defaites": 0,
            "combats_total": 0
        }
        sauvegarder_statistiques(statistiques)
        return statistiques

def sauvegarder_statistiques(statistiques):
    """Sauvegarde les statistiques du joueur dans le fichier"""
    with open("statistiques.txt", "w") as fichier:
        json.dump(statistiques, fichier, indent=4)

def mettre_a_jour_statistiques(victoire):
    """Met à jour les statistiques après un combat"""
    statistiques = charger_statistiques()
    
    statistiques["combats_total"] += 1
    
    if victoire:
        statistiques["victoires"] += 1
        # Augmenter le niveau tous les 3 victoires
        if statistiques["victoires"] % 3 == 0:
            statistiques["niveau"] += 1
            print(f"Félicitations! Vous avez atteint le niveau {statistiques['niveau']}!")
    else:
        statistiques["defaites"] += 1
    
    sauvegarder_statistiques(statistiques)
    return statistiques

def afficher_statistiques():
    """Affiche les statistiques du joueur"""
    statistiques = charger_statistiques()
    
    print("\n=== Statistiques du Joueur ===")
    print(f"Niveau: {statistiques['niveau']}")
    print(f"Victoires: {statistiques['victoires']}")
    print(f"Défaites: {statistiques['defaites']}")
    print(f"Total de combats: {statistiques['combats_total']}")
    
    if statistiques['combats_total'] > 0:
        ratio = (statistiques['victoires'] / statistiques['combats_total']) * 100
        print(f"Ratio de victoire: {ratio:.1f}%")
    
    input("\nAppuyez sur Entrée pour continuer...")