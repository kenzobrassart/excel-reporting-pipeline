import pandas as pd


# Partie 3 : analyses statistiques

def taux_survie_global(df):
    taux = df["survived"].mean() * 100
    print("Taux de survie global :", round(taux, 1), "%")
    return round(taux, 2)


def taux_survie_par_sexe(df):
    taux = df.groupby("sex")["survived"].mean() * 100
    print("Taux de survie par sexe :")
    print(taux.round(1))
    return taux.round(2)


def taux_survie_par_classe(df):
    taux = df.groupby("class")["survived"].mean() * 100
    print("Taux de survie par classe :")
    print(taux.round(1))
    return taux.round(2)


def tableau_croise_survie(df):
    pivot = pd.pivot_table(
        df,
        values="survived",
        index="sex",
        columns="class",
        aggfunc="mean"
    ) * 100
    print("Tableau croise (taux de survie %) :")
    print(pivot.round(1))
    return pivot.round(2)


def age_moyen_survivants(df):
    # le prof demande de comparer l'age moyen, mais comme la distribution est
    # un peu asymetrique, on calcule aussi la mediane qui est plus robuste
    moy = df.groupby("survived")["age"].mean()
    med = df.groupby("survived")["age"].median()
    res = {
        "moyenne_non_survivants": round(moy[0], 1),
        "moyenne_survivants": round(moy[1], 1),
        "mediane_non_survivants": round(med[0], 1),
        "mediane_survivants": round(med[1], 1),
        # on garde aussi les anciennes cles pour pas casser le code excel
        "non_survivants": round(med[0], 1),
        "survivants": round(med[1], 1),
    }
    print("Age des passagers (survivants vs non-survivants) :")
    print(f"- moyenne : {res['moyenne_non_survivants']} ans (non survivants) "
          f"vs {res['moyenne_survivants']} ans (survivants)")
    print(f"- mediane : {res['mediane_non_survivants']} ans (non survivants) "
          f"vs {res['mediane_survivants']} ans (survivants)")
    return res


def lancer_analyses(df):
    resultats = {
        "taux_global": taux_survie_global(df),
        "taux_par_sexe": taux_survie_par_sexe(df),
        "taux_par_classe": taux_survie_par_classe(df),
        "tableau_croise": tableau_croise_survie(df),
        "age_median": age_moyen_survivants(df),
    }
    return resultats
