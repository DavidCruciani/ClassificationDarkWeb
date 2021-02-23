from os import system, remove
from shutil import rmtree, copyfile
import subprocess
import allVariables

MotMax = 10
i = 1
with open(allVariables.pathToProg + "/sortie.txt", "a") as sortie:
    while MotMax < 60:
        copyfile(allVariables.pathToProg + "/cat.json", allVariables.pathToProg + "/cat - Copie.json")
        
        sortie.write(str(i) + ". " + str(MotMax) + ": ")

        print(str(i) + ": AugmenteDicoAuto")

        request = "python " + allVariables.pathToProg + "/AugmenteDicoAuto.py " + str(MotMax)
        p = subprocess.Popen(request, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        #sortie.write(str(output))
        print("Classification_test")

        request = "python " + allVariables.pathToProg + "/Classification_test.py"
        p = subprocess.Popen(request, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        #sortie.write(str(output))
        print("NbMalClasse")

        request = "python " + allVariables.pathToProg + "/NbMalClasse.py"
        p = subprocess.Popen(request, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        sortie.write(str(output) + "\n")
        print()

        remove(allVariables.pathToProg + "/cat - Copie.json")
        rmtree(allVariables.pathToProg + "/out")

        MotMax += 10
        i += 1