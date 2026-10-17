import matplotlib.pyplot as plt
import os


# palette de couleurs orange (en hexa) pour avoir un rendu coherent sur tous les graphs
ORANGE_FONCE = "#8B3A1A"  # marron-orange pour les barres principales
ORANGE = "#E67E22"        # orange vif pour les barres secondaires
PECHE = "#F8B88B"         # peche clair pour les variations
ROUGE = "#C0392B"         # rouge profond pour les lignes de reference


def graphique_survie_sexe(df, dossier="output"):
    # on cree le dossier de sortie si il existe pas deja
    os.makedirs(dossier, exist_ok=True)

    # groupby par sexe + moyenne de la colonne survived = taux de survie en %
    taux = df.groupby("sex")["survived"].mean() * 100

    # une couleur differente pour chaque sexe
    couleurs = [ORANGE if s == "female" else ORANGE_FONCE for s in taux.index]

    # figsize = taille de la figure en pouces (largeur, hauteur)
    fig, ax = plt.subplots(figsize=(7, 5))
    barres = ax.bar(taux.index, taux.values, color=couleurs, width=0.5)

    # on rajoute le pourcentage au dessus de chaque barre pour la lisibilite
    for b in barres:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1,
                f"{b.get_height():.1f}%", ha="center", fontweight="bold")

    ax.set_title("Taux de survie par sexe", fontsize=13, fontweight="bold")
    ax.set_xlabel("Sexe")
    ax.set_ylabel("Taux de survie (%)")
    ax.set_ylim(0, 100)  # axe y de 0 a 100 pour pas que ca varie d'un graph a l'autre

    # ligne pointillee horizontale qui montre la moyenne globale, pour comparer
    ax.axhline(df["survived"].mean()*100, color=ROUGE, linestyle="--", label="Moyenne globale")
    ax.legend()
    fig.tight_layout()  # evite que les labels soient coupes

    # on sauvegarde en png et on ferme la figure pour liberer la memoire
    chemin = os.path.join(dossier, "survie_par_sexe.png")
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    return chemin


def graphique_survie_classe(df, dossier="output"):
    os.makedirs(dossier, exist_ok=True)

    # on force l'ordre First/Second/Third sinon pandas trie alphabetiquement
    ordre = ["First", "Second", "Third"]
    taux = df.groupby("class")["survived"].mean() * 100
    taux = taux.reindex(ordre)

    fig, ax = plt.subplots(figsize=(7, 5))
    barres = ax.bar(taux.index, taux.values, color=[ORANGE_FONCE, ORANGE, PECHE], width=0.5)

    # meme principe que pour le graph par sexe
    for b in barres:
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1,
                f"{b.get_height():.1f}%", ha="center", fontweight="bold")

    ax.set_title("Taux de survie par classe", fontsize=13, fontweight="bold")
    ax.set_xlabel("Classe")
    ax.set_ylabel("Taux de survie (%)")
    ax.set_ylim(0, 100)
    ax.axhline(df["survived"].mean()*100, color=ROUGE, linestyle="--", label="Moyenne globale")
    ax.legend()
    fig.tight_layout()

    chemin = os.path.join(dossier, "survie_par_classe.png")
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    return chemin


def histogramme_ages(df, dossier="output"):
    os.makedirs(dossier, exist_ok=True)

    # ici on cree 2 sous-graphs empiles : histogramme en haut, boite a moustaches en bas
    # height_ratios [4, 1.5] = l'histogramme prend ~3x plus de place que la boite
    # (on laisse un peu plus de hauteur pour la boite pour pouvoir afficher les valeurs Q1/Q3/mediane)
    # sharex=True = ils partagent le meme axe x (l'age) pour bien aligner
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 7.5),
                                    gridspec_kw={"height_ratios": [4, 1.5]},
                                    sharex=True)

    # Histogramme : montre combien de passagers tombent dans chaque tranche d'age
    # bins=30 = on decoupe l'axe en 30 barres
    ax1.hist(df["age"].dropna(), bins=30, color=ORANGE_FONCE, edgecolor="white")

    # 2 lignes verticales pour comparer mediane et moyenne sur le meme graph
    ax1.axvline(df["age"].median(), color=ROUGE, linestyle="--",
                label=f"Mediane : {df['age'].median():.1f} ans")
    ax1.axvline(df["age"].mean(), color=ORANGE, linestyle=":",
                label=f"Moyenne : {df['age'].mean():.1f} ans")
    ax1.set_title("Distribution des ages", fontsize=13, fontweight="bold")
    ax1.set_ylabel("Nombre de passagers")
    ax1.legend()

    # Boite a moustaches (boxplot) : autre facon de visualiser une distribution
    # - le rectangle = 50% des donnees centrales (entre Q1 et Q3, les quartiles)
    # - le trait au milieu de la boite = la mediane
    # - les "moustaches" = etendue des donnees normales (sans les extremes)
    # - les points qui depassent = valeurs aberrantes (outliers)
    # vert=False : la boite est horizontale (sinon par defaut elle est verticale)
    # patch_artist=True : permet de remplir la boite avec une couleur
    ages_clean = df["age"].dropna()
    q1 = ages_clean.quantile(0.25)
    med = ages_clean.median()
    q3 = ages_clean.quantile(0.75)

    ax2.boxplot(ages_clean, vert=False, patch_artist=True,
                boxprops=dict(facecolor=PECHE), medianprops=dict(color=ROUGE, linewidth=2))

    # on rajoute les valeurs au dessus de la boite pour aider a lire le graph
    ax2.text(q1, 1.45, f"Q1\n{q1:.0f} ans", ha="center", fontsize=8, color=ORANGE_FONCE)
    ax2.text(med, 1.45, f"Mediane\n{med:.0f} ans", ha="center", fontsize=8,
             color=ROUGE, fontweight="bold")
    ax2.text(q3, 1.45, f"Q3\n{q3:.0f} ans", ha="center", fontsize=8, color=ORANGE_FONCE)

    ax2.set_xlabel("Age")
    ax2.set_yticks([])  # on cache les graduations de l'axe y, inutiles ici
    ax2.set_ylim(0.5, 1.75)  # un peu plus haut pour laisser place aux annotations

    # petite note explicative en bas du graph pour ceux qui connaissent pas le boxplot
    fig.text(0.5, 0.01,
             "Boite a moustaches : la boite contient 50% des ages (Q1 a Q3), "
             "les moustaches = etendue normale, les points = valeurs aberrantes",
             ha="center", fontsize=8, style="italic", color="#666666")

    fig.tight_layout(rect=[0, 0.03, 1, 1])  # laisse un peu de place en bas pour la note
    chemin = os.path.join(dossier, "distribution_ages.png")
    fig.savefig(chemin, dpi=150)
    plt.close(fig)
    return chemin


def generer_graphiques(df, dossier="output"):
    print("Graphiques :")
    chemins = {
        "survie_sexe": graphique_survie_sexe(df, dossier),
        "survie_classe": graphique_survie_classe(df, dossier),
        "ages": histogramme_ages(df, dossier),
    }
    return chemins
