# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 11:11:03 2021

@author: nadee
"""

import flask
from flask.globals import session
from flask.helpers import url_for
from flask import Flask, render_template, Response,send_file
import cv2
from app import app
from flask import render_template
from flask import request 
from flask import redirect, url_for , globals
from datetime import timedelta
import sqlite3
import random
import json
import re
from email_validator import validate_email, EmailNotValidError

app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=3)



@app.route('/connexion', methods = ['POST', 'GET'])
def postConnexion():
    #1ère connexion
    if request.method == 'POST' and 'Se connecter' in request.form:
        login = request.form['login']
        password = request.form['password']
        session['user'] = login
    else:

    #Retour à la page précédente donc le même utilisateur
        login = session['user']
         #On récupère le mot de passe de l'utilisateur avec le login de l'utilisateur connecté    
        with sqlite3.connect("projet_api.db") as con:
            cur = con.cursor()
            cur.execute("SELECT password from auth WHERE login=?;", [str(login)])
            con.commit()
            rows = cur.fetchall();
            if rows:
                print(rows)
                password= rows[0][0]

         
    #On récupère les données de l'utilisateur avec le login saisi    
    with sqlite3.connect("projet_api.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * from auth WHERE login=?;", [str(login)])
        con.commit()
        rows = cur.fetchall();
        datauser={"id": rows[0][0], "login": rows[0][1], "password":rows[0][2], "statut":rows[0][3]}
        #datauser={"id":rows[0][0], "age": rows[0][1], "sexe":rows[0][2], "anemie":rows[0][3], "creatphospho":rows[0][4], "diabete":rows[0][5], "fraction_ejection":rows[0][6], "hypertension":rows[0][7],"plaquettes":rows[0][8],"serum_creatinine":rows[0][9], "serum_sodium":rows[0][10],"fumeur":rows[0][11],"temps":rows[0][12], "deces":rows[0][13], "login":rows[0][14], "password":rows[0][15], "statut":rows[0][16]}
        
        print(rows)
        id= int(rows[0][0])
        print(id)
        #S'il existe, on récupère les données dans un dictionnaire
        if id:
            
            #Si le statut de l'utilisateur connecté est un patient
            if datauser['statut']=='patient':
                print("Patient")
                with sqlite3.connect("projet_api.db") as con:
                    cur = con.cursor()
                    cur.execute("SELECT * from Patient WHERE identifier=?;", [id])
                    con.commit()
                    rows = cur.fetchall();
                
                if rows:
                    #user={"id":id, "nom" : rows[0][1], "prenom":rows[0][2], "date": rows[0][3], "mail":rows[0][4],"tel":rows[0][5]};
                    user={"id":id, "nom" : rows[0][1], "mail":rows[0][2], "gender": rows[0][3], "date":rows[0][4],"address":rows[0][5],"generalPracticioner":rows[0][6], "tel":rows[0][7]};
                    
                    #Le bouton submit du fichier action.html permettra de se déconnecter
                    a={"type":"Deconnexion"}
                    
    
                        #Si le mot de passe saisi correspond bien à celui enregistré dans la base de données
                    if datauser['password']== password:
                            
                        with sqlite3.connect("projet_api.db") as con:
                            cur = con.cursor()
                            cur.execute("SELECT * from medecins;")
                            con.commit()
                            dataSet=cur.fetchall()
                            fields=cur.description
                                    
                            #On récupère sous forme de liste les données de l'ensemble des médecins disponibles
                            if dataSet:
                                i=0
                                j=0
                                result={}
                                resultSet={}
                                for data in dataSet:
                                    i=0
                                    for field in fields:
                                            if i<data.__len__():
                                                    result[field[0]]=str(data[i])
                                                    i+=1
                                    resultSet[j] = result.copy()
                                    j+=1
                                #On envoie en paramètre cette liste pour pouvoir l'afficher dans le fichier patient.html
                    
                                #return render_template('accueil.html')
                                return render_template('patient.html', title='Bienvenue', utilisateur=user, datauser=datauser,medecins=resultSet,action=a)
           
                    
                 #L'utilisateur est l'admin   
            elif datauser['statut']=='admin':
                #Si le mot de passe saisi correspond bien à celui enregistré dans la base de données
                if datauser['password']== password:
                    
                    #On récupère la liste des utilisateurs 
                    with sqlite3.connect("projet_api.db") as con:
                        cur = con.cursor()
                        cur.execute("SELECT * from data_patients WHERE statut!='admin';")
                        con.commit()
                        dataSet=cur.fetchall()
                        fields=cur.description
                        print(dataSet)
                        #On récupère sous forme de liste les données de l'ensemble des patients
                        if dataSet:
                            i=0
                            j=0
                            result={}
                            resultSet={}
                            for data in dataSet:
                                i=0
                                for field in fields:
                                        if i<data.__len__():
                                                result[field[0]]=str(data[i])
                                                i+=1
                                resultSet[j] = result.copy()
                                j+=1
                            #On envoie en paramètre cette liste pour pouvoir l'afficher dans le fichier admin.html
                            return render_template('admin.html', title='Bienvenue', datauser=datauser, patients=resultSet)
    
                    con.close()     
                
            #L'utilisateur est un medecin                    
            else:
                #Si le mot de passe saisi correspond bien à celui enregistré dans la base de données
                if datauser['password']== password:
                    with sqlite3.connect("projet_api.db") as con:
                        cur = con.cursor()
                        cur.execute("SELECT * from Practitioner WHERE identifier=?;", [id])
                        con.commit()
                        rows = cur.fetchall();
                    
                    if rows:
                        user={"id":id, "nom" : rows[0][1], "mail":rows[0][2], "gender": rows[0][3], "date":rows[0][4],"address":rows[0][5], "tel":rows[0][6]};
                        
                        #Le bouton submit du fichier action.html permettra de se déconnecter
                        a={"type":"Deconnexion"}
    
                        
                        #On récupère la liste de patients 
                        with sqlite3.connect("projet_api.db") as con:
                            cur = con.cursor()
                            cur.execute("SELECT * from data_patients WHERE statut='patient';")
                            con.commit()
                            dataSet=cur.fetchall()
                            fields=cur.description
                            
                            #On récupère sous forme de liste les données de l'ensemble des patients
                            if dataSet:
                                i=0
                                j=0
                                result={}
                                resultSet={}
                                for data in dataSet:
                                    i=0
                                    for field in fields:
                                            if i<data.__len__():
                                                    result[field[0]]=str(data[i])
                                                    i+=1
                                    resultSet[j] = result.copy()
                                    j+=1
                                #On envoie en paramètre cette liste pour pouvoir l'afficher dans le fichier medecin.html
                                return render_template('medecin.html', title='Bienvenue', utilisateur=user, datauser=datauser, patients=resultSet)
        
                        con.close()   
        else:
            #Sinon message d'erreur
            return render_template('erreur.html', title='Erreur')

@app.route('/preinscription', methods = ['POST', 'GET'])
def preInscription():
    if "Ajouter un patient" in request.form:
        return render_template('register.html', title='Inscription')

@app.route('/inscription', methods = ['POST','GET'])
def postInscription():
    error=''
    if request.method == 'POST':
        login = request.form['login']
        #password = request.form['password']
        #confirm = request.form['confirm']
        mail= request.form['mail']
        password="0000"
        nom= request.form['nom']
        prenom= request.form['prenom']
        date= request.form['date']
        tel= request.form['tel']
        id=  random.randint(16,100)
        a={"type":"Deconnexion"}
        session["user"]=login
        if not re.match(r'[^@]+@[^@]+\.[^@]+', mail):
            error = 'L`adresse mail est invalide !'
        else:
            error = 'valide!'
        with sqlite3.connect("projet_api.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO data_patients(id,login,password,statut) VALUES (?,?,?,'patient')", (id,login,password))
            con.commit()
            print("Inscription réalisée avec succès dans data_patients")

            cur.execute("INSERT INTO users(id,nom,prenom,date,mail,tel) VALUES (?,?,?,?,?,?)", (id,nom,prenom,date,mail,tel))
            con.commit()
            print("Inscription réalisée avec succès dans patients")
        con.close()    
        return render_template('register.html', title='Ajouter un patient', error=error)
            
        """try:
            email = validate_email(mail).email
        except EmailNotValidError as e:
            print(str(e))
            print(mail)
            print("L'adresse mail est valide.")"""
        #if confirm!= "" and confirm == password:
        
        '''else:
            return render_template('erreurinscription.html', title='Ajouter un patient', error=error)'''


        
""" user={"id":id, "nom" : nom, "prenom":prenom, "date": date, "mail":mail,"tel":tel};
 fname="Patients/"+str(id)+".json"
 with open(fname, 'w') as f:
     json.dump(user, f, indent=4)
 return render_template('patient.html', title='Bienvenue',utilisateur=user,action=a)
 #else:
     #return render_template('erreurinscription.html', title='Erreur')
 """

@app.route('/details', methods = ['POST', 'GET'])
def details():
    #Selon l'id récupéré dans le formulaire, on affiche les détails du patient correspondant
    for i in range(0,100):
        if str(i) in request.form:
            with sqlite3.connect("projet_api.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from data_patients WHERE id=?;", [str(i)])
                con.commit()
                rows = cur.fetchall();
                user={"id":rows[0][0], "age": rows[0][1], "sexe":rows[0][2], "anemie":rows[0][3], "creatphospho":rows[0][4], "diabete":rows[0][5], "fraction_ejection":rows[0][6], "hypertension":rows[0][7],"plaquettes":rows[0][8],"serum_creatinine":rows[0][9], "serum_sodium":rows[0][10],"fumeur":rows[0][11],"temps":rows[0][12], "deces":rows[0][13], "login":rows[0][14], "password":rows[0][15], "statut":rows[0][16]}
                
                #Le bouton submit du fichier action.html permettra de retourner à la page précédene
                a={"type":"Retourner"}
            return render_template('action.html', title='Bienvenue', utilisateur=user, action=a)

    if request.method == 'POST':
        
        
        #Si l'utilisateur a appuyer sur le bouton rechercher            
        if 'recherche' in request.form:     
            #On récupère l'identifiant saisi
            id= request.form['recherche']
            with sqlite3.connect("projet_api.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from data_patients WHERE id=? and statut='patient';", [id])
                con.commit()
                rows = cur.fetchall();
                
                #S'il y a un résultat correspondant à cet id dans la base
                if rows:
                    a={"type":"Retourner"}
                    user={"id":rows[0][0], "age": rows[0][1], "sexe":rows[0][2], "anemie":rows[0][3], "creatphospho":rows[0][4], "diabete":rows[0][5], "fraction_ejection":rows[0][6], "hypertension":rows[0][7],"plaquettes":rows[0][8],"serum_creatinine":rows[0][9], "serum_sodium":rows[0][10],"fumeur":rows[0][11],"temps":rows[0][12], "deces":rows[0][13], "login":rows[0][14], "password":rows[0][15], "statut":rows[0][16]}
                    return render_template('action.html', title='Bienvenue', utilisateur=user, action=a)
                    con.close()
                #L'identifiant n'existe pas donc message d'erreur
                else:
                    return render_template('erreur2.html', title='Erreur')
            
        
                
@app.route('/info', methods = ['POST', 'GET'])
def info():
      if request.method == 'POST':
    
        if 'Mon espace' in request.form:
            #On récupère les informations actuelles
            nom= request.form['nom']
            address= request.form['address']
            date= request.form['date']
            mail= request.form['mail']
            tel= request.form['tel']   
            id= request.form["id"]
            user={"id":id, "nom" : nom, "address":address, "date": date, "mail":mail,"tel":tel};
            a={"type":"Retourner"}
            return render_template('info.html', title='Mes informations', utilisateur=user, action=a)
    

@app.route('/modifier', methods = ['POST', 'GET'])
def modifierinfo():

  if request.method == 'POST':
        
        
        #Si l'utilisateur a appuyer sur le bouton modifier            
        if 'Modifier' in request.form:     
            #On récupère les informations modifiées
            nom= request.form['nom']
            mail= request.form['mail']

            address= request.form['address']
            date= request.form['date']
            tel= request.form['tel']   
            id= request.form["id"]
            ident=int(id)
            print(ident)
            
            a={"type":"Retourner"}

            with sqlite3.connect("projet_api.db") as con:
                cur = con.cursor()
                sql = "UPDATE users SET name = ?, telecom = ?, birthDate = ?, address = ?, num = ?  WHERE identifier = ?"
                value=(nom,mail,date,address,tel,ident)
                cur.execute(sql,value)
                con.commit()
                rows = cur.fetchall();
                print(rows)
                
                print("Table modifiée avec succès")
                
                user={"id":ident, "nom" : nom, "address":address, "date": date, "mail":mail,"tel":tel}
                print(user)
                return render_template('info.html', title='Bienvenue', utilisateur=user, action=a)
                con.close()

                #L'identifiant n'existe pas donc message d'erreur
        else:
            return render_template('erreur2.html', title='Erreur')

@app.route('/chatbot', methods = ['POST', 'GET'])
def chatbot():
    return render_template('contact.html', title='Erreur')


@app.route('/contact', methods = ['POST', 'GET'])
def contact():
    return render_template('indexchat.html', title='Contact')

@app.route('/recherche', methods = ['POST', 'GET'])
def recherche():
    
    if request.method == 'POST':

        nom= request.form['nom']
        mail= request.form['mail']
        address= request.form['address']
        date= request.form['date']
        tel= request.form['tel']   
        id= request.form["id"]
        ident=int(id)
        mot= request.form["mot"]
        user={"id":ident, "nom" : nom, "address":address, "date": date, "mail":mail,"tel":tel}

        if mot=="":    
            with sqlite3.connect("projet_api.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from medecins")
                con.commit()
                rows = cur.fetchall();
                
                print(rows)
                print(len(rows))
                
                if rows:
                    a={"type":"Retourner"}
                    return render_template('post_recherche.html', title='Bienvenue', medecins=rows, utilisateur=user, action=a)
                    con.close()
                
        else:
            with sqlite3.connect("projet_api.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * from medecins WHERE nom=? or specialite=?;", [mot, mot])
                con.commit()
                rows = cur.fetchall();
                
                print(rows)
                print(len(rows))
                
                #S'il y a un résultat correspondant à cet id dans la base
                if rows:
                    a={"type":"Retourner"}
                    return render_template('post_recherche.html', title='Bienvenue', medecins=rows, utilisateur=user, action=a)
                    con.close()
                else:
                    return render_template('erreurrecherche.html', title='Erreur Recherche')

@app.route('/rdv', methods = ['POST','GET'])
def rdv():
    if request.method == 'POST':
        id=int(request.form['id'])
        print(id)
        a={"type":"Retourner"}
        return render_template('rdv.html', title='Bienvenue', action=a)
    
    


@app.route('/deconnexion', methods = ['POST','GET'])
def logout():
    if request.method == 'POST':
        
        #On récupère l'action saisi dans le formulaire: soit se deconnecter soit retourner à la page précédente
        action=request.form['action']
        
        #Si deconnexion
        if action=="Deconnexion":
            #On efface les données enregistrés dans la session et donc el login de l'utilisateur
            session.clear()
            if 'user' in session:
                 session.pop("user", None)
            #On retourne à la page d'auhentification
            return redirect(url_for("index"))
        else:
            #On retourne à la page précédente soit la liste de patients du médecin
            return redirect(url_for("postConnexion"))
            

@app.route('/',methods = ['POST', 'GET'])
def index():
    if request.method == 'POST' or 'GET':
        #Page d'authentification
        return render_template('index.html', title='Teledoc')

