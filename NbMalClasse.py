from os.path import isfile, join
from os import listdir
import allVariables

 
myDirectoryOk = allVariables.pathToProg + "/out"

def fonction_verification(myDirectoryOk):
    malClasse = 0
    for f in listdir(myDirectoryOk):
        chemin = join(myDirectoryOk, f)
        if isfile(chemin):
            #on récupére le nom de la categorie en cours
            loc = myDirectoryOk.split("\\")

            #on récupère la catégorie que devrait avoir le fichier (dans son nom)
            catFichier = chemin.split("-")

            if (loc[-1] != catFichier[-1].strip()):
                malClasse+=1

        else:
            #si le chemin n'est pas un fchier alors c'est un dossier et il faut recommencer en entrant dedans
            malClasse+= fonction_verification(chemin)
    return malClasse

print("NB de fichiers mal classés : " + str(fonction_verification(myDirectoryOk)))