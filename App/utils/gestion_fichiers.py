import json

def charger_projets(nom_fichier):
    try:
        with open(nom_fichier, 'r') as f:
            data = json.load(f)
            return data  # Retourne l'objet complet avec "projets" et "utilisateurs"
    except FileNotFoundError:
        return {"projets": [], "utilisateurs": []}  # Retourne un objet par défaut

def sauvegarder_projets(data, nom_fichier):
    with open(nom_fichier, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
