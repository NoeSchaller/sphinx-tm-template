(uneref)=
# Présentation de Phaser
Phaser est un logiciel open source développé et maintenu par Photon Storm depuis 2013. Il permet de créer des interfaces graphiques 2D (principalement des jeux) et de coder leurs interactions avec l'utilisateur dans un environnement HTML5. Il est toutefois également possible de l'utiliser sur Android et iOS mais cela nécessite que le code soit préalablement compilé. Le programme peut être utilisé à l'aide de Javascript et de Typescript. La version 3.0.0 est disponible depuis début 2018 et mon travail utilise la version 3.55.2. Phaser dipose également d'un grand nombre de plugins mis à disposition par sa communauté.[^scr1][^scr2]

## La classe Game
La racine de Phaser est la classe Game, c'est cette classe qui va créer l'interface graphique selon les paramètres qui lui sont fournis puis l'actualiser.[^src3] La classe Game pouvant recevoir de nombreux paramètres, tous ceux-ci sont regroupés par l'utilisateur dans un unique dictionnaire qui sera le seul paramètre de Game.  
L'utilisation d'un dictionnaire à la place de plusieurs paramètres distincts a probablement pour but de rendre ce processus plus simple et intuitif. En effet dans un dictionnaire, l'ordre des clés n'a pas d'importance (contrairement à l'utilisation de multiples paramètres).  
Les différentes clés permettent de choisir principalement la manière dont l'interface sera implémenté à l'ensemble de la page ainsi que certaines configurations de base tel que le moteur physique ou les plugins utilisés. Toutes les clés disponibles  qu'il est possible d'utiliser sont documentées ici : <https://photonstorm.github.io/phaser3-docs/Phaser.Types.Core.html#.GameConfig>.

```{code-block} js
---
linenos: true
caption: Par exemple
---
var config = {
    width: 500,
    height: 700,
    fps: 60,
    backgroundColor: 0x0000ff
    }

game = new Phaser.Game(config)
```
```{admonition} Commentaire
---
class: info
---
Ce code crée un interface de 500 pixels sur 700 qui tourne à 60 images par seconde et possède un fond bleu.  

Lignes 1-6:
- La création d'une variable dédiée à ce dictionnaire n'est pas obligatoire mais peut aider à rendre les paramètres plus lisibles.
  
Ligne 8:
- Ce code crée un interface de 500 pixels sur 700 qui tourne à 60 images par seconde et possède un fond bleu.
- En plus d'éviter d'avoir à se préoccuper de l'ordre des clés, un dictionnaire permet aussi d'identifier plus aisément l'effet de chacune des données.
```




Une fois cet objet Game créé, Phaser va mettre en place les différentes scènes puis entrer dans un cycle afin d'actualiser la page en fonction des événements se produisant.[^src3]

### Les moteurs physiques
Phaser possède deux moteurs physique distincts: Arcade et Matter.
Arcade est utilisé par défaut, il est plus léger que matter mais est également moins puissant. 
```{code-block} js
---
linenos: true
caption: Il est possible de changer de moteur ainsi
---
var config = {
    physics: {
        default: 'matter',
        matter: {
            debug: 1
        }
    }
    };
```
```{admonition} Note
---
class: tip
---
Il est également possible de modifier des paramètres physique basique de cette manière et d'activer le sysème de debug comme fait dans l'exemple.
```
Arcade ne permettant que des zones de collisions rectangulaires, il est plus appropié pour mon travail d'utiliser Matter. Ainsi le reste de l'introduction à Phaser se concentrera dessus. L'utilisation des deux moteurs n'est cependant pas très différentes et il est possible d'appliquer des procédés très semblables avec Arcade.

## Les scènes
Une scène est un groupe d'objets et de caméras qui sont traités ensemble par Phaser. Une scène se définit à partir d'au moins 4 fonctions: "constructor", "preload", "create" et "update". Lorsqu'une scène est lancée par Phaser, il procède ainsi:   
1. La fonction "preload" charge les ressources spécifiées dans la mémoire vive de l'ordinateur afin que le reste du programme soit aussi fluide que possible.
2. La fonction "create" met en place les objets et variables nécessaires à la scène qui lui correspond.
3. La fonction "update" est exécutée en boucle afin d'actualiser la scène.
```{admonition} Note
---
class: tip
---
Le constructeur est pricipalement utile pour donner un nom ("key" dans le programme) à la scène afin de pouvoir s'y référer plus tard.
```
```{code-block} js
---
linenos: true
caption: Par exemple
---
class Scene1 extends Phaser.Scene {

    constructor() {
        super('scene1')
    };

    preload() {
    };

    create() {
    };

    update() {
    };
};


var config = {
    scene: [Scene1],
    physics: {
        default: 'matter',
        matter: {
            debug: 1
        }
    }
};

game = new Phaser.Game(config)
```
```{admonition} Commentaire
---
class: info
---
Ce code crée un jeu avec une scène vide.  
Super() sert à donner une clé de référence à la scène.
On peut dès lors référer la scène de cette manière: game.scene.keys.scene1
```
```{admonition} Avertissement
---
class: warning
---
La plupart du code sera dès maintenant sous-entendu afin de pouvoir rester concis et mettre en évidence l'essentiel.  
- Les fonctions "preload", "create" et "update", ne seront mentionnée seulement si elle contiennent du code.  
- Les élements "class Scene1 extends Phaser.Scene", "game = new Phaser.Game(config)", le constructeur et la variable "config" ne seront pas répétés car ils ne subisse généralement pas de chagement majeur.
```
Chaque scène est traitée de manière complètement indépendante par Phaser, elles sont donc utilisées pour représenter divers états ainsi que différents niveaux de profondeurs de notre simulateur. Par exemple mon travail utilise deux scènes superposées lors de la simulation : une sert de monde simulé et une autre pour les boutons tel que ceux qui gèrent la caméra. De cette manière les boutons ne génèrent pas de collision avec les robots ou les murs, de plus comme chaque scène a sa propre caméra l'interface qui permet de gérer le point de vue reste en place même lorsque le robots se déplace.[^src4]  
La gestion des scènes se fait dans les scènes même, Phaser va systématiquement lancer la première scène de la liste. Depuis là Phaser met à diposition des commandes qui permettent de gérer les scènes qui sont actives ou non, celles qui s'actualisent et si plusieurs sont actives à la fois, la manière dont elles se superposent. (documentation ici: <https://photonstorm.github.io/phaser3-docs/Phaser.Scenes.SceneManager.html>)

## Les objets
Les objets de Phaser sont les seuls élements (en dehors du background) qui apparaissent à l'écran et ce sont avec eux que l'utilisateur peut interagir. Il ont donc des formes et des utilisations extrêmement variées et il est donc essentiel d'en maîtriser l'usage.
```{code-block} js
---
linenos: true
caption: Création d'un objet
---
    create() {
        var x = 300,
            y = 300,
            width = 100,
            height = 100,
            color = 0x00ff00

        this.add.rectangle(x, y, width, height, color)
    };
```
```{admonition} Commentaire
---
class: note
---
Ce code code place un carré vert de 100 pixels de côté aux coordonnées {300;300} (L'origine est par défaut au coin en haut à gauche).  
Dans cet exemple c'est un rectangle qui est ajouté mais Phaser met à diposition beaucoup d'autre forme qui sont listées ici: <https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.html> et <https://photonstorm.github.io/phaser3-docs/Phaser.Geom.html>, chaque type d'objet à donc ses paramètres qui lui sont propres.  
Il est bien sûr possible d'ajouter des objets depuis d'autre fonction que "create", aucun outil n'est exclusif à l'un des trois états.
```
### Les objets visuels et physiques

Il est toutefois important de noter que l'objet que qui vient d'être ajouté n'est pas un objet physique et n'est donc pas pris en compte par Matter. En effet il existe des différences entre les objets que Phaser affiche à l'écran et ceux  que Matter traite: certains peuvent être apparaitre visuellement mais ne pas créer de collsions, l'inverse est également vrai.  
Pour l'ajouter au moteur physique il suffit de d'ajouter "matter" dans la commande comme suit:

```{code-block} js
this.matter.add.rectangle(x, y, width, height)
```

Il n'est pas nécéssaire d'y ajouter une couleur car cet objet est uniquement traiter par Matter mais n'apparait pas à l'écran (sauf si le mode debug est actif).  
Pour avoir un objet visuel qui possède une boîte de collision, il faut utiliser la fonction suivante:

```{code-block} js
this.matter.add.gameObject()
```

Cette fonction prend un ou deux paramètres:
- Le premier est l'aspect visuel de la forme à ajouter.
- Le second est la boîte de collision, si aucun paramètre n'est donné un rectangle qui contient la forme est ajouter.
```{code-block} js
---
linenos: true
caption: Exemple
---
create(){
    var x = 300,
        y = 300,
        radius = 50,
        color = 0xff0000

    var cercle = this.matter.add.gameObject(
        this.add.circle(x, y, radius, color),
        this.matter.add.circle(x, y, radius)
    )
};
```
```{admonition} Commentaire
---
class: note
---
Ce code ajoute donc un cercle rouge d'un rayon de 50 pixels en {300,300}.  
La ligne 9 est importante dans le cas d'un cercle, sans elle la zone de collision de l'objet "*cercle*" serait  un carré de 100 pixels de coté qui contiendrait le cercle rouge, cependant elle n'a aucune influence sur le rendu visuel tant qu'il n'y a pas de collisions. 
```
### Appeler un document

Certains objets comme les images et les sprites sont basés sur des documents externe au code, il est donc nécessaire de charger ces document dans la mémoire pour pouvoir les utiliser plus tard. Pour ce faire on utilise, généralement dans la fonction "preload", la commande "this.load" suivi du type de document à charger. Par exemple, pour une image:

```{code-block} js
this.load.image()
```

En utilisant les paramètres suivant:  
- Une chaîne de caractère désignant la clé dont l'on souhaite se servir pour faire référence à l'image plus tard.
- Une chaîne de caractères indiquant le chemin de l'image choisie.

```{code-block} js
---
linenos: true
---
preload(){
    this.load.image('picture', 'assets/picture.png')
};

create(){
    this.add.image(x, y, 'picture')
};
```
Une fois de plus ce procédé n'est pas résérvé aux images mais est nécéssaire dès que le programme nécéssite un document externe au code.

### Les méthodes

## Les plugins
### Le raycasting




[^scr1]: PHOTON STORM "Welcome to Phaser 3" Consulté le 04 janvier 2022 <<https://phaser.io/phaser3>>
[^scr2]: PHOTON STORM "Phaser - HTML5 Game Framework" Consulté le 04 janvier 2022 <<https://github.com/photonstorm/phaser>>
[^src3]: PHOTON STORM "Class: Game" Consulté le 05 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Game.html>>
[^src4]: PHOTON STROM "How Scenes Work" Consulté le 7 janvier 2022 <<https://phaser.io/phaser3/contributing/part5>>