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
# Ce fichier consiste la deuxième étape du travail -> pré-traitement du dataset issu de la première tache.
# Dans ce fichier code vous devez  traiter l’ensemble de données préparées dans la  première étape afin de
# les rendre prêtes pour la consommation par les modèles d’apprentissage dans l'étape suivante.
# ===========================================================================

# ==========================================
# ======CHARGEMENT DES LIBRAIRIES===========
# ==========================================

# la librairie principale pour la gestion des données
import pandas as pd

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Inclure ici toutes les autres librairies dont vous aurez besoin
# - Écrivez en commentaire le rôle de chaque librairie
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# votre code ici:

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

# votre code ici:

# ==========================================
# ====CHARGEMENT DES DONNÉES EN MÉMOIRE=====
# ==========================================

# charger en mémoire les features préparées dans la première étape
features = pd.read_csv(data_path + "features.csv")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 1
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Remplacez les valeurs manquantes par de propres valeurs
#
# Vous devez identifier tous les features qui manquent de valeurs ou
# qui ont des valeurs erronées dans le fichier "features.csv" préparé dans la première etape,
# puis vous devez remplacez ces valeurs manquantes ou erronées par de propres valeurs.
# Les valeurs manquantes peuvent être remplacées par des 0, ou remplacées par la moyenne ou le mode.
# La méthode choisie doit dépendre de la nature de chaque feature.
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print('info', features.info())
# attributs avec des valeurs manquantes
'''
nb_restaurants_zone
ecart_type_etoiles
nb_avis_favorables
nb_avis_defavorables
ratio_avis_favorables
ratio_avis_defavorables
nb_avis_favorables_mention        
nb_avis_defavorables_mention      
nb_avis_favorables_elites         
nb_avis_defavorables_elites       
nb_conseils                       
nb_conseils_compliment           
nb_conseils_elites                
nb_checkin                        
moyenne_checkin                  
ecart_type_checkin
prix              
'''
# Remplacement des valeurs manquantes par 0
champs_remplacement_0 = ['nb_restaurants_zone', 'nb_avis_favorables', 'nb_avis_defavorables', 'ratio_avis_favorables', 'ratio_avis_defavorables', 'nb_avis_favorables_mention', 'nb_avis_defavorables_mention', 'nb_avis_favorables_elites', 'nb_avis_defavorables_elites', 'nb_conseils', 'nb_conseils_compliment', 'nb_conseils_elites', 'nb_checkin']
features[champs_remplacement_0] = features[champs_remplacement_0].fillna(value=0)

# Remplacement des valeurs manquantes par la moyenne
champs_remplacement_moyenne = ['ecart_type_etoiles', 'moyenne_checkin', 'ecart_type_checkin']
features[champs_remplacement_moyenne] = features[champs_remplacement_moyenne].fillna(value=features[champs_remplacement_moyenne].mean())

# Remplacement des valeurs manquantes des niveaux de prix par inconnu
features[['prix']] = features[['prix']].fillna(value='inconnu')

print(features.isnull().sum())


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#                      QUESTION 2
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# - Catégorisation des features: ville et zone
#
# Pour les deux attributs "ville" et "zone" avec des valeurs symboliques,
# il faut effectuer une transformation de ces symboles.
# Vous pouvez utiliser la fonction Categorical (de la librairie Pandas).
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
features.ville = pd.Categorical(features.ville)
features['ville'] = features.ville.cat.codes

features.zone = pd.Categorical(features.zone)
features['zone'] = features.zone.cat.codes

features.prix = pd.Categorical(features.prix)
features['prix'] = features.prix.cat.codes
# -----------------------------------------------------------
# Elimination de la colonne identifiante (ID): restaurant_id
print("------------------------")
print("Elimination de la colonne restaurant_id")
features = features.drop('restaurant_id', axis=1)
print("------------------------")

# -----------------------------------------------------------
# Sauvegarder l'ensemble de données pré-traitées dans un fichier csv afin d'être utilisées dans l'étape suivante
print('preprocessing file created .......')
features.to_csv("donnees/features_finaux.csv", index=False)
