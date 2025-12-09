# Projet MOGPL


Ce projet implémente une solution complète pour :
- générer une grille d’obstacles respectant des contraintes structurelles via un
  programme linéaire (Gurobi) ;
- calculer le plus court chemin d’un robot orienté à l’aide d’un BFS adapté ;
- importer, sauvegarder et tester différentes grilles ;
- réaliser des expériences sur les performances de l’algorithme.


Architecture du projet :

```
MOGPL/
├── src/
│   ├── BFS.py
│   ├── BFSTest.py
│   ├── GenerateGrid.py
│   ├── ImportGraph.py
│   ├── SaveGraph.py
│   ├── SectionE.py
│   ├── Time.py
│   ├── test.ipynb
│   └── test.txt
├── requirements.txt
└── README.md
```

Brèves description des fichiers : 
- `BFS.py`: contient l'algorithme bfs et visualisation d'une chemin
- `BFSTest.py`: contient le menu pour tester des choses sur bfs, sauvegarder et charger un graph inclu
- `GenerateGrid.py`: contient les fonctions pour  generer un grid
- `ImportGraph.py`: contient les fonctions pour charger un graph
- `SaveGraph.py`: contient les fonctions pour save un graph
- `SectionE.py`: partie e) de sujet
- `Time.py`: contient les fonctions du temps
- `test.ipynb`: fichier jupyter notebook qui contient tout sauf la section e)

# Installer les dépendances Python
Assurez-vous d’être dans l’environnement virtuel de votre choix puis exécutez :

```bash
pip install -r requirements.txt
```


# Visualisation et experimentation : 

Vous pouvez acceder aux sections a)-d) depuis le fichier `BFSTest.py`. Pour le lancer, d'abord déplacez-vous dans le repertoire src:

```bash
cd src
```

Puis utilisez cette commande:

```bash
python BFSTest.py
```

ou

```bash
python3 BFSTest.py
```

Après avoir lancer, vous allez voir un menu. Il faut juste mettre le nombre indiqué pour la séléction puis appuyer sur `Enter`.

# Section e)

Pour la section e), vous devez utiliser le fichier `SectionE.py`. C'est nécessaire d'avoir la licence gurobi pour le lancer.

Pour lancer le fichier `SectionE.py`, executez cette commande:

```bash
python3 SectionE.py
```