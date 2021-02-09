from sklearn.feature_extraction.text import CountVectorizer
from os import listdir
from os.path import isfile, join
import re
import json
import operator
import allVariables

#Valeur minimal pour qu un mot rentre dans le dictionnaire global
PETIT=10
MOYEN=40
GRAND=70

###################################################################################
#https://kavita-ganesan.com/how-to-use-countvectorizer/#.YCE9MOhKiUl

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
 
def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """return n-gram counts in descending order of counts"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]
 
    results=[]
    
    # word index, count i
    for idx, count in sorted_items:
        
        # get the ngram name
        n_gram=feature_names[idx]
        
        # collect as a list of tuples
        results.append((n_gram,count))
 
    return results

###################################################################################

documents = []
globListcat = {}
LaCateg = allVariables.pathToCat
myDirectory = allVariables.pathToFile

pattern = re.compile('^([0-9]+)')

MotMax = GRAND

#on créé le tableau global pour stocker tous les mots retenus
with open(LaCateg, 'r') as json_file:

    dataCateg = json.load(json_file)

    for key in dataCateg.keys():
        globListcat[key] = []
    globListcat["Other"] = []

#fonction récursive permettant de parcourir l'ensemble des dossiers
def fichier_rec(myDirectory):

    for f in listdir(myDirectory):
        chemin = join(myDirectory, f)
        if isfile(chemin):
            with open(chemin, 'rb') as file:
                content = ''
                for line in file:
                    word = str(line).split(" ")
                    for m in word:
                        if not( pattern.match(str(m)) ):
                            content += str(m)+" "
            documents = [content]
    

            cv = CountVectorizer(stop_words="english")
            count_vector=cv.fit_transform(documents)

            #sort the counts of first book title by descending order of counts
            sorted_items=sort_coo(count_vector[0].tocoo())

            #Get feature names (words/n-grams). It is sorted by position in sparse matrix
            feature_names=cv.get_feature_names()
            n_grams=extract_topn_from_vector(feature_names,sorted_items,20)

            listCat = {}

            #on défini la valeur des différentes catégories pour le document courant
            with open(LaCateg, 'r') as json_file:
                dataCateg = json.load(json_file)

                for key in dataCateg.keys():
                    listCat[key] = 0

                for key in dataCateg.keys():
                    for i in n_grams:
                        if i[0] in dataCateg[key]:
                            listCat[key] += i[1]
                    

            #on défini la cétgorie qui a l'a plus grande occurence 
            #print("listCat: ", listCat)
            cpt = 0
            catMax = ""
            for j in listCat:
                if cpt < listCat[j]:
                    cpt = listCat[j]
                    catMax = j

            if catMax == "":
                catMax="Other"

            limitadd = 9

            #on range les mots les plus fréquents du document
            if catMax != "":
                for i in n_grams:
                    l = True
                    if len(globListcat[catMax]) > 0 :
                        j=0
                        for c in globListcat[catMax]:
                            if i[0] == c[0]:

                                x = list(c)
                                x[1]+=i[1] 
                                t=tuple(x)

                                globListcat[catMax][j]=t

                                l = False
                            j+=1
                        if l:
                            if i[1] > limitadd:
                                globListcat[catMax].append(i)
                    else:
                        if i[1] > limitadd:
                            globListcat[catMax].append(i)

        else:
            print(chemin)
            fichier_rec(chemin)

fichier_rec(myDirectory)

#on trie le tableau gloabl par les occurences
for k in globListcat.keys():
    if len(globListcat[k])>0:
        sorted_tuples = sorted(globListcat[k], key=operator.itemgetter(1))
        
        sorted_tuples=sorted_tuples[::-1]
        
        globListcat[k] = sorted_tuples


#Ajout des nouveaux mot dans le json

cat={}

with open(LaCateg, 'r') as json_file:
    cat = json.load(json_file)
    for key in cat.keys():
        tmp = cat[key]
        for mot in globListcat[key]:
            if mot[1] > MotMax:
                if mot[0] not in tmp:
                    tmp.append(mot[0])
    

with open(LaCateg, 'w') as json_file:
    json.dump(cat,json_file, indent=4)