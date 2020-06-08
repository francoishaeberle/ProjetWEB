#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 11:27:00 2018

@author: sarahoterodelval
"""

import http.server
import socketserver
# définition du nouveau handler
class RequestHandler(http.server.SimpleHTTPRequestHandler): # sous-répertoire racine des documents statiques
    static_dir = '/client'
# on surcharge la méthode qui traite les requêtes GET
    def do_GET(self):
        # on vérifie si le chemin commence par /service
        if self.path[0:5] == "/time":
            # on traite l'affichage de l'heure
            self.send_time()
        else:
            # on traite la requête vers un document statique
            # on modifie le chemin d'accès en insérant un répertoire préfixe
            self.path = self.static_dir + self.path
            # on traite la requête via la classe parent
            http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def send_time(self):        
        #Recup L'heure
        response = '<!DOCTYPE html><title>hello</title>' + \
        '<meta charset="utf-8"><p>Voici l\'heure du serveur {}</p>' \
        .format(self.date_time_string())
        self.send(response)
        
    
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
        
# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()


