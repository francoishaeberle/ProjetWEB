#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:34:39 2020

@author: Arthur
"""
import http.server
import socketserver
# définition du nouveau handler
class RequestHandler(http.server.SimpleHTTPRequestHandler): # sous-répertoire racine des documents statiques
    static_dir = '/client'
# on surcharge la méthode qui traite les requêtes GET
    def do_GET(self):
        if self.path[0:12] == "/TD3-s1.html":
            
        elif self.path_info[0] == 'toctoc'
        self.send_toctoc()
    
     def init_params(self):
         self.params = {}
         info = self.path.split('?',2)
         self.query_string = info[1] if len(info) > 1 else ''
         for c in self.query_string.split('&'):
             (k,v) = c.split('=',2) if '=' in c else ('',c)
             self.params[unquote(k)] = unquote(v)
    
    def send(self,body):
        self.send_response(200)
        self.end_headers()
        encoded = bytes(body, 'UTF-8')
        self.wfile.write(encoded)
        
        
# instanciation et lancement du serveur
httpd = socketserver.TCPServer(("", 8080), RequestHandler)
httpd.serve_forever()



form action = /toctoc
input name =
input prenom = 