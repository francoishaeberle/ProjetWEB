# -*- coding: utf-8 -*-
# corrige de la question 4 du TD1

import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd
import sqlite3

# ouverture d'une connexion avec la base de données
conn = sqlite3.connect('ter.sqlite')
c = conn.cursor()

# Definition des régions et des couleurs de tracé
regions = [("Rhône Alpes","blue"), ("Auvergne","green"), ("Auvergne-Rhône Alpes","cyan"), ('Bourgogne',"red"), 
           ('Franche Comté','orange'), ('Bourgogne-Franche Comté','olive') ]

# configuration du tracé
fig1 = plt.figure(figsize=(18,6))
ax = fig1.add_subplot(111)
ax.set_ylim(bottom=80,top=100)
ax.grid(which='major', color='#888888', linestyle='-')
ax.grid(which='minor',axis='x', color='#888888', linestyle=':')
ax.xaxis.set_major_locator(pltd.YearLocator())
ax.xaxis.set_minor_locator(pltd.MonthLocator())
ax.xaxis.set_major_formatter(pltd.DateFormatter('%B %Y'))
ax.xaxis.set_tick_params(labelsize=10)
ax.xaxis.set_label_text("Date")
ax.yaxis.set_label_text("% de régularité")

# boucle sur les régions
for l in (regions) :
    c.execute("SELECT * FROM 'regularite-mensuelle-ter' WHERE Région=? ORDER BY Date",l[:1])  # ou (l[0],)
    r = c.fetchall()
    # recupération de la date (colonne 2) et transformation dans le format de pyplot
    x = [pltd.date2num(dt.date(int(a[1][:4]),int(a[1][5:]),1)) for a in r if not a[7] == '']
    # récupération de la régularité (colonne 8)
    y = [float(a[7]) for a in r if not a[7] == '']
    # tracé de la courbe
    plt.plot_date(x,y,linewidth=1, linestyle='-', marker='o', color=l[1], label=l[0])
    
# légendes
plt.legend(loc='lower left')
plt.title('Régularité des TER (en %)',fontsize=16)

# affichage des courbes
plt.show()

# fermeture de la base de données
conn.close()
