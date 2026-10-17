import os
import sys
import subprocess
from data_processing import (charger_donnees, afficher_apercu, afficher_types,
                              compter_passagers, valeurs_manquantes, nettoyer_donnees)
from analysis import lancer_analyses
from visualization import generer_graphiques
from excel_export import generer_rapport_excel


CHEMIN_CSV = os.path.join("data", "titanic.csv")
DOSSIER_OUTPUT = "output"
CHEMIN_RAPPORT = os.path.join(DOSSIER_OUTPUT, "rapport_titanic.xlsx")


def ouvrir_fichier(chemin):
    # ouvre le fichier excel avec l'appli par defaut (Windows, macOS ou Linux)
    try:
        if sys.platform.startswith("win"):
            os.startfile(chemin)
        elif sys.platform == "darwin":
            subprocess.run(["open", chemin], check=False)
        else:
            subprocess.run(["xdg-open", chemin], check=False)
    except OSError:
        pass  # pas d'appli disponible : le fichier reste dans le dossier output


def main():
    print("Projet Titanic")
    print("--------------")

    # Partie 1 : chargement
    print("\nPartie 1 : chargement")
    df_brut = charger_donnees(CHEMIN_CSV)
    afficher_apercu(df_brut)
    afficher_types(df_brut)
    compter_passagers(df_brut)
    valeurs_manquantes(df_brut)

    # Partie 2 : nettoyage
    print("\nPartie 2 : nettoyage")
    df = nettoyer_donnees(df_brut)
    print("Colonnes ajoutees : FamilySize, IsAlone, sex_num, age_cat")

    # Partie 3 : analyses
    print("\nPartie 3 : analyses")
    resultats = lancer_analyses(df)

    # Partie 4 : graphiques
    print("\nPartie 4 : graphiques")
    chemins = generer_graphiques(df, DOSSIER_OUTPUT)

    # Partie 5 : excel
    print("\nPartie 5 : excel")
    generer_rapport_excel(df, resultats, chemins, CHEMIN_RAPPORT)

    print("\nFini. Rapport :", CHEMIN_RAPPORT)

    # ouvre le fichier excel automatiquement avec l'appli par defaut
    ouvrir_fichier(CHEMIN_RAPPORT)


if __name__ == "__main__":
    main()
