import sqlite3

# chemin vers la base de donnée
db_path= '/data/ventes.db'

# connexion à la base de donnée sqlite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("Connexion à SQLite réussie")

# création de la table "produits"
cursor.execute('''
CREATE TABLE IF NOT EXISTS produits (
    id_produit TEXT PRIMARY KEY,
    nom_produit TEXT NOT NULL,
    prix REAL NOT NULL,
    stock INTEGER NOT NULL
)''')
print("Table produits créée")

# création de la table "magasins"
cursor.execute('''
CREATE TABLE IF NOT EXISTS magasins(
    id_magasin INTEGER PRIMARY KEY,
    ville TEXT NOT NULL,
    nb_salaries INTEGER NOT NULL
)''')
print("Table magasins créée")

# Création de la table "ventes"
# Création d'une nouvelle colonne "id_vente", pour plus de clarté
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventes (
    id_vente INTEGER PRIMARY KEY AUTOINCREMENT, 
    date_vente TEXT NOT NULL,
    id_produit TEXT NOT NULL,
    id_magasin INTEGER NOT NULL,
    quantite INTEGER NOT NULL,
    FOREIGN KEY (id_produit) REFERENCES produits(id_produit),
    FOREIGN KEY (id_magasin) REFERENCES magasins(id_magasin)
)''')
print("Table ventes créée")

# création de la nouvelle table "analyse" qui permettra de stocké les KPI
cursor.execute('''
CREATE TABLE IF NOT EXISTS analyses (
    id_analyse INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_kpi TEXT NOT NULL,
    date_calcul TEXT NOT NULL,
    resultat TEXT NOT NULL
)''')
conn.commit()

# Vérification
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables créées dans la base de données :")
for table in tables:
    print(f"  - {table[0]}")

# Fermeture de la connexion
conn.close()
print("Base de données créée avec succès !")

