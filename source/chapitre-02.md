# Mode d'emploi pour le professeur
## Mise en place

Tout les documents nécessaire à la mise en place de la simulation sont disponibles dans la branche `main` du dépot github dédié à ce travail[^git]. Pour pouvoir utiliser le simulateur, il suffit de télécharger tous les documents du dossier `TM_code` puis d'ajouter au code HTML de la page les fichiers `phaser.js`, `rayCasting.js` et `MaqueenSimulation.js` dans cet ordre. Il est également important de les ajouter à la fin du fichier HTML afin d'être sûr que l'élément `canvas` dans lequel la simulation est créée existe lorsque le script est exécuté. Il faut également être attentif à laisser le dossier `assets` dans le même document que `MaqueenSimulation.js`. Une fois ces étapes effectuées, il est possible d'initialiser la simulation.

### La classe simulation
Tout comme Phaser, la simulation repose principalement sur une seule et unique classe: la classe simulation. Lancer la simulation ne nécessite donc que d'appeler celle-ci avec les bons paramètres.
```{code-block} js
sim = new simulation(width, height, id, mapLoad, marCreate, background)
```
* `width` et `height`: définissent les dimensions de l'interface graphique.
* `id`: l'id d'un élement canvas dans le code HTML.
* `mapLoad`:  une fonction qui permet de charger des images.
* `mapCreate`: une fonction qui permet de mettre en place l'environnement.
* `background`: une couleur exprimée en hexadécimal qui définit l'aspect du fond de la simulation. Si rien n'est spécifié, le fond est beige.

### Les fonctions mapLoad et mapCreate
Les fonctions `mapLoad` et `mapCreate` sont les fonctions qui permettent de placer les différents éléments dans la simulation. Chaque fonction correspond à un état de la scène: `load` et `create`. Elles possèdent chacune un argument qui leur permet de recevoir la scène principale de la simulation afin qu'elles puissent interagir avec:

``` {code-block} js
function mapLoad(scene) {
}

function mapCreate(scene) {  
}
```

Les prochains paragraphes présentent les utilisations possibles de ces fonctions. Il est toutefois important de savoir que n'importe quelle instruction reconnue par Phaser peut y être exécutée.

#### la fonction mapLoad

 La fonction `mapLoad` a pour but de charger des images afin de les afficher avec la fonction `mapCreate`.

``` {code-block} js
---
linenos: true
---
function mapLoad(scene) {
  scene.load.image("key", "path");
  // voir chapitre 1: appeler un document
}
```

#### la fonction mapCreate

La fonction `mapCreate` permet d'ajouter les éléments initiaux à la simulation. Chaque élément est ajouté grâce à une classe spécifique:

``` {code block} js 
new wallRect(scene, x, y, width, height, angle);
```
Ce code ajoute un mur statique rectangulaire
* `scene` : la scène dans laquelle ajouter l'élément, il faut toujours mettre la scène principale 
* `x` : la coordonnée horizontale de l'élément
* `y` : la coordonnée verticale de l'élément
* `width` : la largeur du rectangle
* `height` : la hauteur du rectangle
* `angle` : l'angle de l'élément en degrés

---

``` {code block} js 
new wallCircle(scene, x, y, radius);
```
Ce code ajoute un mur statique circulaire
* `scene` : la scène dans laquelle ajouter l'élément, toujours la scène principale 
* `x` : la coordonnée horizontale de l'élément
* `y` : la coordonnée verticale de l'élément
* `radius` : le rayon du cercle

---

``` {code block} js 
new markRect(scene, x, y, width, height, angle);
```
Ce code ajoute une marque rectangulaire
* `scene` : la scène dans laquelle ajouter l'élément, toujours la scène principale 
* `x` : la coordonnée horizontale de l'élément
* `y` : la coordonnée verticale de l'élément
* `width` : la largeur du rectangle
* `height` : la hauteur du rectangle
* `angle` : l'angle de l'élément en degrés


---

``` {code block} js 
new markCircle(scene, x, y, radius);
```
Ce code ajoute une marque circulaire
* `scene` : la scène dans laquelle ajouter l'élément, toujours la scène principale 
* `x` : la coordonnée horizontale de l'élément
* `y` : la coordonnée verticale de l'élément
* `radius` : le rayon du cercle

---

``` {code-block} js
new Picture(scene, key, x, y, scaleX, scaleY)
```
Ce code ajoute une image dont les zones foncées sont détectées comme des marques
* `scene` : la scène dans laquelle ajouter l'élément, toujours la scène principale 
* `key` : la clé d'une image péalablement chargée dans la fonction `mapLoad`
* `x` : la coordonnée horizontale de l'élément
* `y` : la coordonnée verticale de l'élément
* `scaleX` : l'échelle horizontale de l'image
* `scaleY` : l'échelle verticale de l'image
---

``` {code-block} js
new maqueenPlus(scene, name, x, y, angle)
new maqueenLite(scene, name, x, y, angle)
```
Ce code ajoute un Maqueen Plus puis un Maqueen Lite
* `scene` : la scène dans laquelle ajouter l'élément, toujours la scène principale 
* `name` : une chaîne de caractères utilisée pour nommer le robot dans le menu de la caméra
* `x` : la coordonnée horizontale de l'élément
* `y` : la coordonnée verticale de l'élément
* `angle` : l'angle de l'élément en degrés



```{admonition} Note
---
class: note
---
Il faut noter que la caméra commence par défaut sur le premier robot ajouté.  
Dès lors, il est possible de choisir le point de vue de celle-ci à l'aide des boutons en haut à gauche (voir {ref}`image<img>`):
* Les +/- pour changer le zoom
* Les boutons gris en-dessous pour choisir quel robot est suivi par la caméra
* Le bouton "Free" laisse l'utilisateur déplacer la caméra lui-même à l'aide des flèches directionnelles
```
À partir de là, l'utilisateur peut user des robots créés comme il le souhaite à l'aide des commandes détaillées ci-dessous.

``` {code-block} js
---
linenos: true
caption: Par exemple
---
function mapLoad(scene) {
  scene.load.image("csud", "assets/Logo_csud.png");
}

function mapCreate(scene) {
  new Picture(scene, "csud", 400, 100);

  new wallRect(scene, 100, 200, 50, 200, 80);

  new wallCircle(scene, 500, 400, 50);

  new markRect(scene, 400, 500, 100, 100, 70);

  new markCircle(scene, 200, 500, 20);

  new maqueenPlus(scene, "N°1", 300, 300, 0);

  new maqueenLite(scene, "N°2", 450, 300, 70);
}

sim = new simulation(600, 600, "game", mapLoad, mapCreate);
```
Ce code affiche la simulation dans un élément HTML canvas dont l'id est `game`.

(img)=
```{image} ./figures/mapJs.png
:alt: map.js
:width: 600px
:align: center
```

## Contrôler les robots
Une fois que la simulation est créée, elle contient les listes `marks` `walls` et `robots`. Ces listes contiennent les éléments de la simulation classés selon leur type. Les élément sont triés dans leur liste en fonction de l'ordre de leur ajout à la simulation.
```{code-block} js
---
caption: Ainsi le premier robot ajouté peut être sélectionner ainsi
---
sim.robots[0]
```

```{admonition} Avertissement
---
class: warning
---
Dans cet exemple ainsi que tous les suivants, on suppose que la simulation est appelée `sim`.
```

### Le Maqueen Lite
#### L'i2c
L'i2c permet donc de contrôler les moteurs du robot. L'objet possède une seule fonction

```{code-block} js
sim.robot.i2c.write(adresse, [register, dir1, power1, dir2, power2])
```
* `adresse`: permet de choisir à quelle puce les données sont envoyées: les moteurs sont contrôlés par la puce `0x10`
* `register`: la référence de la commande à utiliser: 
  * `0x00`: qui permet de modifier l'état du moteur gauche avec `dir1` et `power1` et optionnellement du moteur droit avec `dir2` et `power2`.
  * `0x02`: ne prend que `dir1` et `power1` pour les appliquer au moteur droit
* `dir`: définit la direction du moteur, 0 pour le stopper, 1 pour aller vers l'avant et 2 pour reculer
* `power`: la vitesse de rotation des moteurs

```{admonition} Note
---
class: tip
---
Si l'on ne modifie le statut que d'un moteur, `dir2` et `power2` ne sont bien sûr pas nécessaires.
```

```{code-block} js
---
caption: Par exemple
---
sim.robots[0].i2c.write(0x10, [0x00, 1, 200, 2, 150])
```

```{admonition} Commentaire
---
class: note
---
Ce code fait avancer le moteur gauche à une puissance de 200 et reculer le moteur droit à une puissance de 150
```

#### Les pins
Les robots possèdent plusieurs pins qui prennent en charge la gestion des données qui ont un caractère binaire, chaque pin est associé à un capteur ou un actuateur.

| Pin | Capteur/Actuateur |
| :--- | :--- |
| `pin8` | led gauche |
| `pin12` | led droite |
| `pin13` | capteur infrarouge gauche|
| `pin14` | capteur infrarouge droit|


Chaque pin est doté de deux fonctions, l'une pour modifier son état et l'autre pour le lire.
* `read_digital()`: retourne un booléen qui représente l'état actuel de l'actuateur ou du capteur
* `write_digital(bool)`: prend en paramètre un booléen qui modifie l'état de l'actuateur (ou du capteur)  

```{code-block} js
---
caption: Voici un exemple
---
sim.robots[0].pin8.write_digital(true)
sim.robots[0].pin14.read_digital()
```

```{admonition} Commentaire
---
class: note
---
La première ligne allume la led gauche et la seconde retourne `true` si le capteur infrarouge droit se trouve au-dessus d'une marque ou d'une portion foncée d'une image.
```

(getDistance)=
#### La méthode `getDistance`

Comme il est très complexe de reproduire le fonctionnement du capteur ultrason de manière fidèle au robot original, il existe simplement une méthode qui retourne la distance en centimètres avec le mur le plus proche.

``` {code-block} js
sim.robot[0].getDistance()
```

### le Macqueen Plus

Toutes les fonctionnalités du Macqueen Plus sont contrôlables via l'i2c. Les fonctions `i2c.write` ajoutent des données au buffer[^glo] qui sont ensuite accessibles grâce à la méthode `i2c.read`. Le maqueen plus possède également une méthode `getDistance` qui permet d'utiliser le capteur ultrason.

#### La méthode `i2c.write`

``` {code-block} js
sim.robot[1].i2c.write(adresse, [register, byte1, byte2, ...])
```

* `adresse` : l'adresse de la puce (la seule puce existante est la puce `0x10`)
* `register`: La référence de la commande à utiliser (voir tableau ci-dessous)
* `byte`: un octet transmis à la puce

| Registre    | Effet    | Octet | Octet(s) ajouté au buffer |
| :--- | :--- | :--- | :--- |
| 0x00    | voir Maqueen lite | - | `dirL`, `powerL`, `dirR`, `powerR` |
  | 0x02 | voir Maqueen lite | - | `dirR`, `powerR` |
| 0x0b | change la couleur de la led rgb gauche et de la droite si 2 octet sont inserrés | Un nombre entre 1 et 8 (1 = rouge, 2 = vert, 3 = jaune, 4 = bleu, 5 = rose, 6 = cyan, 7 = blanc, 8 = éteint) | Aucun |
| 0x0c | change la couleur de la led rbg droite | voir `0x0b` | Aucun |
| 0x1d | Aucun | Aucun | Un octet dont l'état d'un bit représente l'état d'un capteur infrarouge (le sixième représente le capteur le plus à droite et le premier le plus à gauche) |

#### La méthode `i2c.read`

``` {code-block} js
sim.robot[1].i2c.read(adresse, nb)
```
* `adresse`: l'adresse de la puce
* `nb`: le nombre d'octets à lire

La méthode `i2c.read` permet d'accéder aux octets stockés dans le buffer

#### La méthode `getDistance`

Voir {ref}`le maqueen lite <getDistance>`

## Modifier la disposition des éléments

Une fois les éléments mis en place, il est possible d'en modifier certains paramètres:

| Méthode | Paramètre | Effet | Applicable à | Exemple |
| :--- | :--- | :--- | :--- | :--- |
| setPosition(x, y) | `x` et `y`: des coordonnées | Modifie l'emplacement de l'objet | Marques, murs, robots | `sim.robots[0].setPosition(200, 450)` |
| setAngle(deg) | `deg`: un angle en degrés | Modifie l'angle de l'objet | Marques, murs, robots | `sim.walls[1].setAngle(90)` |
|setScale(x, y)| `x` et`y`: l'échelle de l'objet par rapport à sa taille originale| Modifie la taille de l'objet | Marques, murs | `sim.marks[2].setScale(2, 3)` |



[^git]: https://github.com/NoeSchaller/TM_Noe
[^glo]: voir {ref}`glossaire<glo>`