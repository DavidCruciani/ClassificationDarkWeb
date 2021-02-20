from os.path import isfile, join
from os import listdir
import allVariables

myDirectory = allVariables.pathToTrain

#fonction récursive permettant d'ecrire dans chaque fichier sa categorie
def fichier_rec(myDirectory):
    for f in listdir(myDirectory):
        chemin = join(myDirectory, f)
        if isfile(chemin):
            #on récupére le nom de la categorie en cours
            loc = myDirectory.split("\\")

            s = open(chemin,"a")
            s.write((" " + loc[-1]) * 50)
            s.close()
        else:
            #si le chemin n'est pas un fchier alors c'est un dossier et il faut recommencer en entrant dedans
            print(chemin)
            fichier_rec(chemin)

fichier_rec(myDirectory)