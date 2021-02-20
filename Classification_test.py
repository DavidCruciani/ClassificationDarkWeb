#sudo apt install python3-sklearn
from sklearn.feature_extraction.text import CountVectorizer
from os import listdir, mkdir
from os.path import isfile, join, exists
from shutil import copyfile
from ntpath import basename
import re
import json
import allVariables


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

LaCateg = allVariables.pathToCat
myDirectory = allVariables.pathToTest
monRep = allVariables.pathToProg + "/out"

pattern = re.compile('^([0-9]+)|[0-9]+')

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

            with open(LaCateg) as json_file:
                if not exists(monRep):
                    mkdir(monRep)

                dataCateg = json.load(json_file)

                for key in dataCateg.keys():
                    if not exists(monRep + "/" + key):
                        mkdir(monRep + "/" + key)
                    
                    if not exists(monRep + "/Other"):
                        mkdir(monRep + "/Other")

                    listCat[key] = 0

                for key in dataCateg.keys():
                    for i in n_grams:
                        if i[0] in dataCateg[key]:
                            listCat[key] += i[1]

            cpt = 0
            k = ""
            for j in listCat:
                if cpt < listCat[j]:
                    cpt = listCat[j]
                    k = j

            if k == "":
                k="Other"
            
            """with open(allVariables.pathToProg + "/class.txt", "a") as clas:
                clas.write("fichier: " + str(chemin.split("\\")[-1]) + "\n")
                clas.write("listCat: " + str(listCat) + "\n")
                clas.write("mot: " + str(n_grams) + "\n")
                clas.write(k + "\n\n")"""

            copyfile(chemin, monRep + "/" + k + "/" + basename(chemin) + "-" + myDirectory.split("\\")[-1])
        else:
            print(chemin)
            fichier_rec(chemin)

fichier_rec(myDirectory)
