#!/usr/bin/python

# Copyright 2025, Gurobi Optimization, Inc.


from gurobipy import *


"""
Min z = 7x_1 + 3x_2 + 4x_3
Sous contraintes:
 x_1 + 2x_2 + 3x_3 >= 8
3x_1 + x_2 +  x_3 >= 5

x_1, x_2, x_3 >= 0 x_i appartient à N où i = 1, .., 3
"""


nbcont=2 
nbvar=3

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[1 ,2, 3],
     [3, 1, 1]]

# Second membre
b = [8, 5]

# Coefficients de la fonction objectif
c = [7, 3, 4]

m = Model("mogplex")     
        
# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=GRB.INTEGER, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = LinExpr();
obj =0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,GRB.MINIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(quicksum(a[i][j]*x[j] for j in colonnes) >= b[i], "Contrainte%d" % i)

# Resolution
m.optimize()


print("")                
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)

   
