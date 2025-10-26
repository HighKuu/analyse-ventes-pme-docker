import sqlite3
from datetime import datetime

db_path = '/data/ventes.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print("Connexion à SQLite réussie")

# Date actuelle pour les analyses
date_calcul = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# 1. CHIFFRE D'AFFAIRES TOTAL
print("Calcul du chiffre d'affaires total")

cursor.execute('''
    SELECT SUM(v.quantite * p.prix) as ca_total
    FROM ventes v
    JOIN produits p ON v.id_produit = p.id_produit
''')

ca_total = cursor.fetchone()[0]
print(f" Résultat : {ca_total} €")

# Stocker dans la table analyses
cursor.execute('''
    INSERT INTO analyses (nom_kpi, date_calcul, resultat)
    VALUES (?, ?, ?)
''', ('CA_total', date_calcul, str(ca_total)))


# 2. VENTES PAR PRODUIT
print("Calcul des ventes par produit")

cursor.execute('''
    SELECT p.nom_produit, SUM(v.quantite) as total_quantite
    FROM ventes v
    JOIN produits p ON v.id_produit = p.id_produit
    GROUP BY p.id_produit, p.nom_produit
    ORDER BY total_quantite DESC
''')

ventes_produits = cursor.fetchall()
print(" Résultats :")
for produit, quantite in ventes_produits:
    print(f"   - {produit} : {quantite} unités")

    # Stocker chaque produit dans analyses
    cursor.execute('''
        INSERT INTO analyses (nom_kpi, date_calcul, resultat)
        VALUES (?, ?, ?)
    ''', (f'ventes_{produit}', date_calcul, str(quantite)))


# 3. VENTES PAR RÉGION (VILLE)
print("Calcul des ventes par région (ville)...")

cursor.execute('''
    SELECT m.ville, SUM(v.quantite) as total_quantite
    FROM ventes v
    JOIN magasins m ON v.id_magasin = m.id_magasin
    GROUP BY m.ville
    ORDER BY total_quantite DESC
''')

ventes_regions = cursor.fetchall()
print("   Résultats :")
for ville, quantite in ventes_regions:
    print(f"- {ville} : {quantite} unités")

    # Stocker chaque région dans analyses
    cursor.execute('''
        INSERT INTO analyses (nom_kpi, date_calcul, resultat)
        VALUES (?, ?, ?)
    ''', (f'ventes_{ville}', date_calcul, str(quantite)))

# Validation
conn.commit()

# Vérification finale
cursor.execute("SELECT COUNT(*) FROM analyses")
print(f"{cursor.fetchone()[0]} KPI stockés dans la table analyses")

# Fermeture
conn.close()
print("Analyses terminées avec succès !")


