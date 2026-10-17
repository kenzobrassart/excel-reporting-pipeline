import pandas as pd


# Partie 1 : chargement et exploration

def charger_donnees(chemin):
    df = pd.read_csv(chemin, sep=";")
    return df


def afficher_apercu(df):
    print("5 premieres lignes :")
    print(df.head())


def afficher_types(df):
    print("Types des variables :")
    print(df.dtypes)


def compter_passagers(df):
    total = len(df)
    print("Nombre total de passagers :", total)
    return total


def valeurs_manquantes(df):
    manquantes = df.isnull().sum()
    print("Valeurs manquantes par colonne :")
    print(manquantes[manquantes > 0])
    return manquantes


# Partie 2 : nettoyage

def nettoyer_donnees(df):
    df = df.copy()

    # age : 177 NaN, on remplace par la mediane (mieux que la moyenne car
    # moins sensible aux valeurs extremes)
    df["age"] = df["age"].fillna(df["age"].median())

    # embarked : seulement 2 NaN, on met le port le plus frequent
    df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])

    # deck : 688 NaN sur 891, colonne inutilisable, on la garde mais on l'utilise pas

    # taille de la famille = freres/soeurs/conjoint + parents/enfants
    df["FamilySize"] = df["sibsp"] + df["parch"]

    # variable indicatrice : 1 si le passager voyage seul, 0 sinon
    df["IsAlone"] = (df["FamilySize"] == 0).astype(int)

    # encodage du sexe avec un dico
    mapping_sex = {"male": 0, "female": 1}
    df["sex_num"] = df["sex"].map(mapping_sex)

    # categorisation de l'age
    tranches = [0, 18, 60, 120]
    labels = ["enfant", "adulte", "senior"]
    df["age_cat"] = pd.cut(df["age"], bins=tranches, labels=labels)
    df["age_cat"] = df["age_cat"].astype("category")

    return df
