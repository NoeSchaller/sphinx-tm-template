# Mode d'emploi
## Mise en place
### La classe simulation
Tout comme Phaser, la simulation se repose principalement sur une seule et unique classe: la classe simulation. Lancer la simulation ne nécéssite donc que d'appeler celle-ci avec les bon paramètres.
```{code-block} js
sim = new simulation(width, height, map, background)
```
* width et height servent à définir les dimensions de l'interface graphique.
* map est chaîne de caractère, elle représente le chemin vers un document Json qui contient les intructions de mise en place de l'environnement du robot.
* background est une couleur exprimée en hexadécimal qui définit l'aspect du fond de la simulation. Si rien n'est spécifé, le fond est beige.

### Le document Json
Le document Json contient toute les informations nécéssaire à la simulation pour construire l'environnement virtuel, il se divise en quatre partie qui représentent les différents élements utilisables:
* Des robots
* Des obstacles (des murs)
* Des marquages au sol
* Des images (qui sont également des marquages)  
Chaque objet a sa propre clé dans le fichier Json 
```{code-block} json
---
caption: voici un exemple de document "vide"
---
{
    "bots": [
    ],
    "walls": [
    ],
    "marks": [
    ],
    "pictures": [
    ]
}
```
Chaque type d'élements est donc représenté par une liste, pour y ajouter un objet il suffit d'utiliser dans la bonne liste la commande qui correspond à l'object choisi.

* new bot(id, x, y, angle): 
    * id: une chaîne de caratère qui définit le nom du robot qui apparaîtrera en haut à gauche pour séléctionner le robot que la caméra suit
    * x et y: la position du robot à son apparition
    * angle: (optionnel, 0° par défaut) la direction du robot en degrés dans le sens des aiguilles d'une montre, 0° indique le haut 
* new wallRect(x, y, width, heigth)
    * x et y: la position de l'obstacle
    * width: la largeur de l'obsacle
    * height: la hauteur de l'obstacle
* new markRect(x, y, width, heigth)
    * x et y: la position du marquage
    * width: la largeur du marquage
    * height: la hauteur du marquage
* new Picture(x, y, path)
    * x et y: la position de l'image
    * path: le chemin vers l'image

```{code-block} js
---
caption: Par exemple cette commmande avec ce document Json
---
sim = new simulation(600, 600, 'assets/map.json')
```

```{code-block} json
{
    "bots": [
        "new botLight('N°1', 300, 300, 70)"
    ],
    "walls": [
        "new wallRect(100, 200, 50, 200)"
    ],
    "marks": [
        "new markRect(400, 500, 100, 100)"
    ],
    "pictures": [
        "new Picture(400, 100, 'assets/Logo_csud.png')"
    ]
}
```
Donne ce résultat:  

```{image} figures/mapJson.png
```

```{admonition} Note
---
class: note
---
Il faut noter que la caméra commence par défaut à suivre le premier robot de la liste.  
Dès lors il est possible de choisir le point de vue de celle-ci à l'aide des boutons en haut à droite:
* Les +/- pour changer le zoom
* Les boutons gris en dessous pour choisir quel robot est suivit pas la caméra
* "Free" laisse l'utilisateur déplacer la caméra lui-même à l'aide des flèches directionnelle
```
À partir de là, l'utilisateur peut user des robots créés comme il le souhaite à l'aide des commandes détaillées ci-dessous.

## Contrôler les robots
Une fois que la simulation est créé, elle contient une liste nommée Light et dont les objets sont programmés pour contrôler les robots. Ainsi pour séléctionner un robot il faut aller le chercher dans cette liste.
```{code-block} js
sim.Light[0]
```

```{admonition} Avertissement
---
class: warning
---
Il est supposé que la simulation est appelée sim dans cet exemple et dans tout les suivants.
```
### L'i2c

### Les pins