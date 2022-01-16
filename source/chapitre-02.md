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
Une fois que la simulation est créé, elle contient une liste nommée Light et dont les objets sont programmés pour contrôler les robots. Ainsi pour séléctionner un robot il faut aller le chercher dans cette liste, les robots sont dans le même ordre dans cette liste que dans celle du document Json.
```{code-block} js
sim.Light[0]
```

```{admonition} Avertissement
---
class: warning
---
Il est supposé que la simulation est appelée sim dans cet exemple et dans tout les suivants.
```
Une fois le robot séléctionné il ne reste qu'à choisir un des composants simuler du robot, en effet à l'image du Maqueen, le robot simulé possède également des commandes basées sur des pins et de l'i2c.
### L'i2c
L'i2c permet donc de contrôler les moteurs du robot. L'objet possède une seule fonction

```{code-block} js
write(adresse, byte)
```
* adresse: permet de choisir à quelle puce les bytes sont envoyés: les moteurs sont contrôler par la puce 0x10
* byte: un objet Uint16Array(liste), la liste qu'il prend comme paramètre contient les bytes qui seront envoyés à la puce, les bytes prennent ce format:

```{code-block} js
Unit16Array([commande, dir1, puissance1, dir2, puissance2])
```

* commande: il y a deux valeure possible, 0x00 qui permet de modifier l'état du moteur gauche ou des deux et 0x02 qui ne modifie que le droit
* dir: définit la direction du moteur, 0 pour le stopper, 1 pour aller vers l'avant et 2 pour reculer
* puissance: la vitesse de rotation des moteurs

```{admonition} Note
---
class: info
---
Si l'on ne modifie le statut que d'un moteur dir2 et puissance2 ne sont bien sûr pas nécéssaire
```

```{code-block} js
---
caption: Par exemple
---
sim.Light[0].i2c.write(0x10, new Uint16Array[0x00, 1, 3, 2, 2])
```

```{admonition} Commentaire
---
class: note
---
Ce code fait donc avancer la roue gauche à une vitesse de 3 et reculer la roue droite à une vitesse de 2
```

### Les pins
Les robots possèdent plusieurs pins qui prennent en charge la gestion des données qui on un caractère binaire, les pins et les actuateurs/capteurs sont associé de la manière suivante: les leds sont gérées par le pin8 (la gauche) et le pin12 (la droite), de manière similaires les pin13 (gauche) et pin14 (droite) gèrent les capteurs infrarouges.  
Chaque pin est doté de deux fonction, l'une pour modifier son état et l'autre pour le lire.
* digital_read(): retourne un booléen qui représente l'état actuel de l'actuateur ou du capteur
* digital_write(bool): prend en paramètre un booléen qui modifie l'état de l'actuateur (ou du capteur)