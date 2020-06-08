#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:34:39 2018

@author: sarahoterodelval
"""
import http.server
import socketserver
# définition du nouveau handler
class RequestHandler(http.server.SimpleHTTPRequestHandler): # sous-répertoire racine des documents statiques
    static_dir = '/client'
# on surcharge la méthode qui traite les requêtes GET
    def do_GET(self):
# on modifie le chemin d'accès en insérant un répertoire préfixe
        self.path = self.static_dir + self.path
# on traite la requête via la classe parent
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()