# **************************************************************************
# INF7370-Hiver 2023
# Travail pratique 1
# ===========================================================================
# ===========================================================================
# GBEGAN HUGUES
# GBEH24279505
# ===========================================================================
# ===========================================================================

# ===========================================================================
# Le but de ce travail est de classifier les restaurants en 2 états (Fermeture définitive / Ouvert)
#
# Ce fichier consiste la troisième étape du travail -> entrainement des modèles de classification
# Dans ce fichier code, vous devez entrainer 5 modèles de classification sur les données préparées dans l'étape précédente.
# ===========================================================================

# ==========================================
# ======CHARGEMENT DES LIBRAIRIES===========
# ==========================================

# la librairie principale pour la gestion des données
import numpy as np
import pandas as pd
# la librairie pour normalizer les données par Z-Score
from sklearn.preprocessing import StandardScaler
# la librairie pour diviser les données en deux lots (entrainement et test)
from sklearn.model_selection import train_test_split
# la librairie pour entrainer les modèles de classification
from sklearn.metrics import confusion_matrix, f1_score, roc_auc_score
# la librairie pour tracer les graphiques et les courbes ROC et AUC
import matplotlib.pyplot as plt
import scikitplot as skplt

# la librairie pour selectionner les features les plus pertinentes
from sklearn.feature_selection import SelectKBest, mutual_info_classif



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Inclure ici toutes les autres librairies dont vous aurez besoin
# - Écrivez en commentaire le rôle de chaque librairie
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Votre code ici:


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# ==========================================
# ===============VARIABLES==================
# ==========================================

# l'emplacement des données sur le disque
# Note: Il faut placer le dossier "donnees"  contenant les 8 fichiers .csv dans le même endroit que les fichiers de code
data_path = "donnees/"

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Inclure ici toutes les autres variables globales dont vous aurez besoin
# - Écrivez en commentaire le rôle de chaque variable
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



def evaluate_models(clf, x_test, y_test):
    y_pred = clf.predict(x_test)
    # Matrice de confusion
    cm = confusion_matrix(y_test, y_pred)
    TN, FP, FN, TP = confusion_matrix(y_test, y_pred).ravel()
    # true positive rate
    TPR = TP/(TP+FN)
    # false positive rate
    FPR = FP/(FP+TN)
    # F-measure
    f1 = f1_score(y_test, y_pred, average='macro')
    # AUC
    roc = roc_auc_score(y_test, y_pred)

    return cm, TPR, FPR, f1, roc


# ==========================================
# ====CHARGEMENT DES DONNÉES EN MÉMOIRE=====
# ==========================================

# Charger en mémoire les features préparées dans la deuxième étape (pré-traités)
features = pd.read_csv(data_path + "features_finaux.csv")

# ==========================================
# INITIALIZATION DES DONNÉES ET DES ÉTIQUETTES
# ==========================================

# Initialisation des données et des étiquettes
x = features.copy() # "x" contient l'ensemble des données d'entrainement
y = x["ferme"]      # "y" contient les étiquettes des enregistrements dans "x"

# Elimination de la colonne classe (ferme) des features
x = x.drop('ferme', axis=1)

# Contient les noms des features
x_names = x.columns.to_list()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 1
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#  - Normaliser les données en utilisant Z-score (StandardScaler dans Scikit-learn)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
sc = StandardScaler()
x = sc.fit_transform(x)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 2
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Divisez les données en deux lots (entrainement et test)
# (indiquer dans votre rapport le pourcentage des données de test que vous avez utilisé)
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 3
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Entrainez 5 modèles de classification sur l'ensemble de données normalisées (avec tous les features)
#   1 - Arbre de decision
#   2 - Forêt d’arbres décisionnels (Random Forest)
#   3 - Classification bayésienne naïve
#   4 - Bagging
#   5 - AdaBoost
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 1 - Arbre de decision
from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier()
dtc.fit(x_train, y_train)

# 2 - Forêt d’arbres décisionnels (Random Forest)
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier()
rfc.fit(x_train, y_train)

# 3 - Classification bayésienne naïve
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(x_train, y_train)

# 4 - Bagging
from sklearn.ensemble import BaggingClassifier
bagging = BaggingClassifier()
bagging.fit(x_train, y_train)

# 5 - AdaBoost
from sklearn.ensemble import AdaBoostClassifier
adaboost = AdaBoostClassifier()
adaboost.fit(x_train, y_train)



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 4
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Afficher les resultats sur les données test de chaque algorithm entrainé avec tous les features
#   1- Le taux des vrais positifs (TP Rate) – de la classe Restaurants fermés définitivement.
#   2- Le taux des faux positifs (FP Rate) – de la classe Restaurants fermés définitivement.
#   3- F-measure de la classe Restaurants fermés définitivement.
#   4- La surface sous la courbe ROC (AUC).
#   5- La matrice de confusion.
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1 - Arbre de decision
cm_dtc, TPR_dtc, FPR_dtc, f1_dtc, roc_dtc = evaluate_models(dtc, x_test, y_test)
skplt.metrics.plot_roc(y_test, dtc.predict_proba(x_test))
skplt.metrics.plot_confusion_matrix(y_test, dtc.predict(x_test))
print("Arbre de decision ----- TP Rate, FP Rate, F-measure, AUC : ", TPR_dtc, FPR_dtc, f1_dtc, roc_dtc)

# 2 - Forêt d’arbres décisionnels (Random Forest)
cm_rf, TPR_rf, FPR_rf, f1_rf, roc_rf = evaluate_models(rfc, x_test, y_test)
skplt.metrics.plot_roc(y_test, rfc.predict_proba(x_test))
skplt.metrics.plot_confusion_matrix(y_test, rfc.predict(x_test))
print("Random Forest -----------TP Rate, FP Rate, F-measure, AUC: ", TPR_rf, FPR_rf, f1_rf, roc_rf)

# 3 - Classification bayésienne naïve  
cm_gnb, TPR_gnb, FPR_gnb, f1_gnb, roc_gnb = evaluate_models(gnb, x_test, y_test)
skplt.metrics.plot_roc(y_test, gnb.predict_proba(x_test))
skplt.metrics.plot_confusion_matrix(y_test, gnb.predict(x_test))
print("Classification bayésienne naïve----- TP Rate, FP Rate, F-measure, AUC: ", TPR_gnb, FPR_gnb, f1_gnb, roc_gnb)

# 4 - Bagging
cm_bagging, TPR_bagging, FPR_bagging, f1_bagging, roc_bagging = evaluate_models(bagging, x_test, y_test)
skplt.metrics.plot_roc(y_test, bagging.predict_proba(x_test))
skplt.metrics.plot_confusion_matrix(y_test, bagging.predict(x_test))
print("Bagging ----------- TP Rate, FP Rate, F-measure, AUC: ", TPR_bagging, FPR_bagging, f1_bagging, roc_bagging)

# 5 - AdaBoost
cm_adaboost, TPR_adaboost, FPR_adaboost, f1_adaboost, roc_adaboost = evaluate_models(adaboost, x_test, y_test)
skplt.metrics.plot_roc(y_test, adaboost.predict_proba(x_test))
skplt.metrics.plot_confusion_matrix(y_test, adaboost.predict(x_test))
print("AdaBoost ----------- TP Rate, FP Rate, F-measure, AUC: ", TPR_adaboost, FPR_adaboost, f1_adaboost, roc_adaboost)

print(' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 5
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Selectionnez les tops 10 features
#
# Vous devez identifier les 10 meilleurs features en utilisant la mesure du Gain d’information (Mutual Info dans scikit-learn).
# Afficher les 10 meilleurs features dans un tableau (par ordre croissant selon le score obtenu par le Gain d'information).
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# cols = mutual_info_classif(x_train, y_train, discrete_features=True)
# top_10_features = pd.DataFrame(cols, index=x_names, columns=['score'])
# t10_f = top_10_features.sort_values(by='score', ascending=False).head(10)
# print('t10_f', t10_f)
# plt.figure(figsize=(10, 5))
# plt.barh(t10_f.index.tolist(), t10_f['score'])
# plt.title('Top 10 features')

# x_train_reduced = x_train[:, cols.astype(int)]
# x_test_reduced = x_test[:, cols.astype(int)]


# deuxieme methode avec selectKbest
selector = SelectKBest(mutual_info_classif, k=10)
sel = selector.fit(x_train, y_train)
cols = selector.get_support(indices=True)
cols_with_name = pd.DataFrame(sel.scores_, index=x_names, columns=['score'])
kbest = cols_with_name.sort_values(by='score', ascending=False).head(10)
print('kbest', kbest)
plt.figure(figsize=(10, 5))
plt.barh(kbest.index.tolist(), kbest['score'])
plt.title('Top 10 features')

x_train_reduced = x_train[:, cols]
x_test_reduced = x_test[:, cols]

# plt.show()
# # On a pas les memes resultats avec les deux methodes

print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 6
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Entrainez 5 modèles de classification sur l'ensemble de données normalisées avec seulement les top 10 features selectionnés.
#   1 - Arbre de decision
#   2 - Forêt d’arbres décisionnels (Random Forest)
#   3 - Classification bayésienne naïve
#   4 - Bagging
#   5 - AdaBoost
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# 1 - Arbre de decision
from sklearn.tree import DecisionTreeClassifier
dtc_t10 = DecisionTreeClassifier()
dtc_t10.fit(x_train_reduced, y_train)

# 2 - Forêt d’arbres décisionnels (Random Forest)
from sklearn.ensemble import RandomForestClassifier
rfc_t10 = RandomForestClassifier()
rfc_t10.fit(x_train_reduced, y_train)

# 3 - Classification bayésienne naïve
from sklearn.naive_bayes import GaussianNB
gnb_t10 = GaussianNB()
gnb_t10.fit(x_train_reduced, y_train)

# 4 - Bagging
from sklearn.ensemble import BaggingClassifier
bagging_t10 = BaggingClassifier()
bagging_t10.fit(x_train_reduced, y_train)

# 5 - AdaBoost
from sklearn.ensemble import AdaBoostClassifier
adaboost_t10 = AdaBoostClassifier()
adaboost_t10.fit(x_train_reduced, y_train)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 7
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Afficher les resultats sur les données test de chaque algorithm entrainé avec les top 10 features
#   1- Le taux des vrais positifs (TP Rate) – de la classe Restaurants fermés définitivement.
#   2- Le taux des faux positifs (FP Rate) – de la classe Restaurants fermés définitivement.
#   3- F-measure de la classe Restaurants fermés définitivement.
#   4- La surface sous la courbe ROC (AUC).
#   5- La matrice de confusion.
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# 1 - Arbre de decision
cm_dtc, TPR_dtc, FPR_dtc, f1_dtc, roc_dtc = evaluate_models(dtc_t10, x_test_reduced, y_test)
skplt.metrics.plot_roc(y_test, dtc_t10.predict_proba(x_test_reduced))
skplt.metrics.plot_confusion_matrix(y_test, dtc_t10.predict(x_test_reduced))
plt.title('Top 10 Arbre de decision')
print("top_10_features Arbre de decision --------- TP Rate, FP Rate, F-measure, AUC: ", TPR_dtc, FPR_dtc, f1_dtc, roc_dtc)

# 2 - Forêt d’arbres décisionnels (Random Forest)
cm_rf, TPR_rf, FPR_rf, f1_rf, roc_rf = evaluate_models(rfc_t10, x_test_reduced, y_test)
skplt.metrics.plot_roc(y_test, rfc_t10.predict_proba(x_test_reduced))
skplt.metrics.plot_confusion_matrix(y_test, rfc_t10.predict(x_test_reduced))
plt.title('Top 10 Random Forest')
print("top_10_features Random Forest ----------- TP Rate, FP Rate, F-measure, AUC: ", TPR_rf, FPR_rf, f1_rf, roc_rf)

# 3 - Classification bayésienne naïve   
cm_gnb, TPR_gnb, FPR_gnb, f1_gnb, roc_gnb = evaluate_models(gnb_t10, x_test_reduced, y_test)
skplt.metrics.plot_roc(y_test, gnb_t10.predict_proba(x_test_reduced))
skplt.metrics.plot_confusion_matrix(y_test, gnb_t10.predict(x_test_reduced))
plt.title('Top 10 Classification bayésienne naïve')
print("top_10_features Classification bayésienne naïve----- TP Rate, FP Rate, F-measure, AUC: ", TPR_gnb, FPR_gnb, f1_gnb, roc_gnb)

# 4 - Bagging
cm_bagging, TPR_bagging, FPR_bagging, f1_bagging, roc_bagging = evaluate_models(bagging_t10, x_test_reduced, y_test)
skplt.metrics.plot_roc(y_test, bagging_t10.predict_proba(x_test_reduced))
skplt.metrics.plot_confusion_matrix(y_test, bagging_t10.predict(x_test_reduced))
plt.title('Top 10 Bagging')
print("top_10_features Bagging ----------- TP Rate, FP Rate, F-measure, AUC: ", TPR_bagging, FPR_bagging, f1_bagging, roc_bagging)

# 5 - AdaBoost
cm_adaboost, TPR_adaboost, FPR_adaboost, f1_adaboost, roc_adaboost = evaluate_models(adaboost_t10, x_test_reduced, y_test)
skplt.metrics.plot_roc(y_test, adaboost_t10.predict_proba(x_test_reduced))
skplt.metrics.plot_confusion_matrix(y_test, adaboost_t10.predict(x_test_reduced))
plt.title('Top 10 AdaBoost')
print("top_10_features AdaBoost -----------  TP Rate, FP Rate, F-measure, AUC: ", TPR_adaboost, FPR_adaboost, f1_adaboost, roc_adaboost)

plt.show()