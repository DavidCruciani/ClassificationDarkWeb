# ClassificationDarkWeb

Le but de ce programme est d'améliorer la classification des sites récupérés sur le Darkweb dans des catégories.

Nous nous basons sur l'occurrence des mots afin d'augmenter la précision de notre classification.

(voir aussi https://github.com/DavidCruciani/AnalyseDarkWeb)

Pour l'apprentissage : 

## Prérequis :
<ul>
	<li>Python3;</li>
	<li>Scikit-learn</li>
</ul>

## Architecture :

### allVariables.py

Ce fichier permet de spécifier les chemins d'accès aux différents fichiers nécessaires.

### AugmenteDico.py

Dans ce fichier, une fonction permet après avoir enlevé les stop_words, de récupérer les mots avec les occurrences les plus fortes dans chaque fichier.
Les mots avec une fréquence supérieur à 9 sont ajoutés dans le tableau global des occurrences.
Une fois le tableau global complété, celui-ci est trié.
Enfin, le fichier des catégories est mis à jour avec les mots contenus dans le tableau global si leur occurrence est suffisante selon le seuil donné au début du fichier.

### AugmenteDicoAuto.py

Ce fichier permet de faire le même traitement que AugmenteDico.py en indiquant la borne supérieure en paramètre.
Si l'occurrence du mot clé est supérieure au paramètre, il sera ajouté au fichier de catégorie.

### cat.json

Ce fichier contient les catégories ainsi que les mots clés associés à ces catégories.

### Classification_test.py

Permet de tester l'apprentissage avec un set de données qui lui est donné et de copier les fichiers analysés dans leur catégorie de façon physique dans des répertoires.

### EcritureCat.py

Utile pour l'apprentissage lorsqu'un échantillon a été préalablement classé, permet d'écrire dans chaque fichier sa catégorie 50 fois afin que le fichier soit correctement classé lors de son traitement. Cela permet de récupérer les mots clés associés.

### ExecAuto.py

Permet une exécution automatique du programme : 
<ul>
	<li>AugmenteDicoAuto.py</li>
	<li>Classification_test.py</li>
	<li>NbMalClasse.py</li>
</ul>

### NbMalClasse.py

Cette fonction permet d'afficher le nombre de fichiers mal classés après l'exécution du traitement.

## Ordre de lancement : 

<ul>
	<li>Compléter le fichier allVariables.py</li>
	<li> Mode automatique :
		<ul>
		<li>ExecAuto.py</li>
		</ul></li>
	<li> Mode Manuel :
	<ul>
		<li>AugmenteDico.py</li>
		<li>Classification_test.py</li>
		<li>NbMalClasse.py</li>
	</ul>
	</li>
</ul>

