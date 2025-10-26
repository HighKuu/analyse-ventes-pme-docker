import sqlite3
import csv

# Chemin vers la base de données
db_path = '/data/ventes.db'

# Connexion à SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("Connexion à SQLite réussie")

# Import des produits
print("Import des produits...")

with open('/app/produits.csv', 'r', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    produits_importes = 0

    for row in csv_reader:
        cursor.execute('''
            INSERT OR REPLACE INTO produits (id_produit, nom_produit, prix, stock)
            VALUES (?, ?, ?, ?)
        ''', (row['ID Référence produit'], row['Nom'], float(row['Prix']), int(row['Stock'])))
        produits_importes += 1

conn.commit()
print(f"{produits_importes} produits importés")

# Import des magasins
print("Import des magasins...")

with open('/app/magasins.csv', 'r', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    magasins_importes = 0

    for row in csv_reader:
        cursor.execute('''
            INSERT OR REPLACE INTO magasins (id_magasin, ville, nb_salaries)
            VALUES (?, ?, ?)
        ''', (int(row['ID Magasin']), row['Ville'], int(row['Nombre de salariés'])))
        magasins_importes += 1

conn.commit()
print(f"{magasins_importes} magasins importés")



# Importation des ventes
print("Import des ventes (avec vérification des doublons)...")

with open('/app/ventes.csv', 'r', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    ventes_importees = 0
    ventes_ignorees = 0

    for row in csv_reader:
        # Vérifie si la vente existe déjà
        cursor.execute('''
            SELECT COUNT(*) FROM ventes 
            WHERE date_vente = ? AND id_produit = ? AND id_magasin = ?
        ''', (row['Date'], row['ID Référence produit'], int(row['ID Magasin'])))

        existe = cursor.fetchone()[0]

        if existe == 0:
            # La vente n'existe pas, donc on l'insère
            cursor.execute('''
                INSERT INTO ventes (date_vente, id_produit, id_magasin, quantite)
                VALUES (?, ?, ?, ?)
            ''', (row['Date'], row['ID Référence produit'], int(row['ID Magasin']), int(row['Quantité'])))
            ventes_importees += 1
        else:
            # La vente existe déjà, on l'ignore
            ventes_ignorees += 1

conn.commit()
print(f"{ventes_importees} ventes importées")
print(f"{ventes_ignorees} ventes ignorées (déjà présentes)")



cursor.execute("SELECT COUNT(*) "
               "FROM ventes")
print(f"Total ventes en base : {cursor.fetchone()[0]}")
conn.close()

