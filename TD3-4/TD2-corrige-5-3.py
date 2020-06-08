# TD2-s6.py
# version, ccorrigée 10/12/2018

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote

import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd

import sqlite3

#
# Définition du nouveau handler
#
class RequestHandler(http.server.SimpleHTTPRequestHandler):

  # sous-répertoire racine des documents statiques
  static_dir = '/client'

  #
  # On surcharge la méthode qui traite les requêtes GET
  #
  def do_GET(self):

    # On récupère les étapes du chemin d'accès
    self.init_params()

    # le chemin d'accès commence par /time
    if self.path_info[0] == 'time':
      self.send_time()
   
     # le chemin d'accès commence par /regions
    elif self.path_info[0] == 'regions':
      self.send_regions()
      
    # le chemin d'accès commence par /ponctualite
    elif self.path_info[0] == 'ponctualite':
      self.send_ponctualite()
      
    # ou pas...
    else:
      self.send_static()

  #
  # On surcharge la méthode qui traite les requêtes HEAD
  #
  def do_HEAD(self):
    self.send_static()

  #
  # On envoie le document statique demandé
  #
  def send_static(self):

    # on modifie le chemin d'accès en insérant un répertoire préfixe
    self.path = self.static_dir + self.path

    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    if (self.command=='HEAD'):
        http.server.SimpleHTTPRequestHandler.do_HEAD(self)
    else:
        http.server.SimpleHTTPRequestHandler.do_GET(self)
  
  #     
  # on analyse la requête pour initialiser nos paramètres
  #
  def init_params(self):
    # analyse de l'adresse
    info = urlparse(self.path)
    self.path_info = [unquote(v) for v in info.path.split('/')[1:]]  # info.path.split('/')[1:]
    self.query_string = info.query
    self.params = parse_qs(info.query)

    # récupération du corps
    length = self.headers.get('Content-Length')
    ctype = self.headers.get('Content-Type')
    if length:
      self.body = str(self.rfile.read(int(length)),'utf-8')
      if ctype == 'application/x-www-form-urlencoded' : 
        self.params = parse_qs(self.body)
    else:
      self.body = ''
   
    # traces
    print('info_path =',self.path_info)
    print('body =',length,ctype,self.body)
    print('params =', self.params)
    
  #
  # On envoie un document avec l'heure
  #
  def send_time(self):
    
    # on récupère l'heure
    time = self.date_time_string()

    # on génère un document au format html
    body = '<!doctype html>' + \
           '<meta charset="utf-8">' + \
           '<title>l\'heure</title>' + \
           '<div>Voici l\'heure du serveur :</div>' + \
           '<pre>{}</pre>'.format(time)

    # pour prévenir qu'il s'agit d'une ressource au format html
    headers = [('Content-Type','text/html;charset=utf-8')]

    # on envoie
    self.send(body,headers)

  #
  # On génère et on renvoie un graphique de ponctualite (cf. TD1)
  #
  def send_regions(self):

    conn = sqlite3.connect('ter.sqlite')
    c = conn.cursor()
    
    # votre code ici
    c.execute("SELECT DISTINCT Région FROM 'regularite-mensuelle-ter'")
    r = c.fetchall()
    txt = 'Liste des {} régions :\n'.format(len(r))
    for a in r:
       txt = txt + '{}\n'.format(a[0])
    
    headers = [('Content-Type','text/plain;charset=utf-8')]
    self.send(txt,headers)

    
  #
  # On génère et on renvoie un graphique de ponctualite (cf. TD1)
  #
  def send_ponctualite(self):

    conn = sqlite3.connect('ter.sqlite')
    c = conn.cursor()
    
    if len(self.path_info) <= 1 or self.path_info[1] == '' :   # pas de paramètre => liste par défaut
        # Definition des régions et des couleurs de tracé
        regions = [("Rhône Alpes","blue"), ("Auvergne","green"), ("Auvergne-Rhône Alpes","cyan"), ('Bourgogne',"red"), 
                   ('Franche Comté','orange'), ('Bourgogne-Franche Comté','olive') ]
    else:
        # On teste que la région demandée existe bien
        c.execute("SELECT DISTINCT Région FROM 'regularite-mensuelle-ter'")
        reg = c.fetchall()
        if (self.path_info[1],) in reg:   # Rq: reg est une liste de tuples
          regions = [(self.path_info[1],"blue")]
        else:
            print ('Erreur nom')
            self.send_error(404)    # Région non trouvée -> erreur 404
            return None
    
    # configuration du tracé
    plt.figure(figsize=(18,6))
    plt.ylim(80,100)
    plt.grid(which='major', color='#888888', linestyle='-')
    plt.grid(which='minor',axis='x', color='#888888', linestyle=':')
    
    ax = plt.subplot(111)
    loc_major = pltd.YearLocator()
    loc_minor = pltd.MonthLocator()
    ax.xaxis.set_major_locator(loc_major)
    ax.xaxis.set_minor_locator(loc_minor)
    format_major = pltd.DateFormatter('%B %Y')
    ax.xaxis.set_major_formatter(format_major)
    ax.xaxis.set_tick_params(labelsize=10)
    
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
    plt.ylabel('% de régularité')
    plt.xlabel('Date')

    # génération des courbes dans un fichier PNG
    fichier = 'courbe_ponctualite.png'
    plt.savefig('client/{}'.format(fichier))

    html = '<img src="/{}?{}" alt="ponctualite {}" width="100%">'.format(fichier,self.date_time_string(),self.path)

    headers = [('Content-Type','text/html;charset=utf-8')]
    self.send(html,headers)

  #
  # On envoie les entêtes et le corps fourni
  #
  def send(self,body,headers=[]):

    # on encode la chaine de caractères à envoyer
    encoded = bytes(body, 'UTF-8')

    # on envoie la ligne de statut
    self.send_response(200)

    # on envoie les lignes d'entête et la ligne vide
    [self.send_header(*t) for t in headers]
    self.send_header('Content-Length',int(len(encoded)))
    self.end_headers()

    # on envoie le corps de la réponse
    self.wfile.write(encoded)

 
#
# Instanciation et lancement du serveur
#
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()

