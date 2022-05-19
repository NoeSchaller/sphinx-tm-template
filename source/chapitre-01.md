# Présentation de Phaser
Phaser est un logiciel open source développé et maintenu par Photon Storm depuis 2013. Il permet de créer des interfaces graphiques 2D (principalement des jeux) et de coder leurs interactions avec l'utilisateur dans un environnement HTML5. Il est toutefois également possible de l'utiliser sur Android et IOS mais cela nécessite que le code soit préalablement compilé. Le programme peut être utilisé à l'aide de Javascript et de Typescript. La version 3.0.0 est disponible depuis début 2018 et mon travail utilise la version 3.55.2. Phaser dipose également d'un grand nombre de plugins mis à disposition par sa communauté. [^src1][^src2]

## La classe Game
Le coeur de Phaser est la classe `Game`. Il s'agit de la classe qui va créer l'interface graphique selon les paramètres qui lui sont fournis puis l'actualiser.[^src3] La classe `Game` pouvant recevoir de nombreux paramètres, tous ceux-ci sont regroupés par l'utilisateur dans un unique objet qui sera le seul paramètre de Game. L'utilisation d'un objet à la place de plusieurs paramètres distincts a pour but de rendre ce processus plus simple et intuitif. En effet, dans un objet, l'ordre des clés n'a pas d'importance (contrairement à l'utilisation de multiples paramètres). Les différentes clés permettent de choisir principalement la manière dont l'interface sera ajoutée à l'ensemble de la page, ainsi que certaines configurations de base telles que le moteur physique ou les plugins utilisés. Toutes les clés disponibles  qu'il est possible d'utiliser sont documentées par Phaser[^src4].

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
Ce code crée une interface de 500 pixels sur 700 qui tourne à 60 images par seconde et possède un fond bleu.  

Lignes 1-6:
* La création d'une variable dédiée à cet objet n'est pas obligatoire mais peut aider à rendre les paramètres plus lisibles.
  
Ligne 8:
* En plus d'éviter d'avoir à se préoccuper de l'ordre des clés, un objet permet aussi d'identifier plus aisément l'effet de chacune des données.
```




Une fois cet objet `Game` créé, Phaser va mettre en place les différentes scènes puis entrer dans un cycle afin d'actualiser la page en fonction des événements se produisant.

### Les moteurs physiques
Phaser possède deux moteurs physiques distincts: Arcade et Matter.
Arcade est utilisé par défaut. Il est plus léger que Matter mais moins puissant.


Arcade ne permettant que des zones de collisions rectangulaires, il est plus appropié pour ce travail d'utiliser Matter. Ainsi, le reste de l'introduction à Phaser se concentrera sur ce dernier. L'utilisation des deux moteurs n'est cependant pas très différente et il est possible d'appliquer des procédés très semblables avec Arcade.

```{code-block} js
---
linenos: true
caption: Il est possible de changer de moteur ainsi
---
var config = {
    physics: {
        default: 'matter',
        matter: {
            debug: 0
        }
    }
};
```
```{admonition} Note
---
class: tip
---
Il est également possible de modifier des paramètres physiques basiques de cette manière et d'activer le système de debogage comme le montre l'exemple.
```

## Les scènes
Une scène est un groupe d'objets et de caméras qui sont traités ensemble par Phaser. Une scène se définit à partir d'au moins quatre méthodes: `constructor`, `preload`, `create` et `update`: 
1. La fonction `preload` charge les ressources spécifiées dans la mémoire vive de l'ordinateur afin que le reste du programme soit aussi fluide que possible.
2. La fonction `create` met en place les objets et variables nécessaires à la scène qui lui correspond.
3. La fonction `update` est exécutée en boucle afin d'actualiser la scène.
```{admonition} Note
---
class: tip
---
Le constructeur est principalement utile pour donner une clé à la scène afin de pouvoir s'y référer plus tard.


Les fonctions `preload` et `create` de toutes les scènes sont exécutées avant le début du cycle d'actualisation de Phaser.
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
    scene: [new Scene1()],
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
Ce code crée un jeu avec une scène vide. Il est également possible d'en ajouter plusieurs. `super()` sert à donner une clé de référence à la scène.
On peut dès lors faire référence à la scène de la manière suivante: `game.scene.keys.scene1`
```
```{admonition} Avertissement
---
class: warning
---
La majeure partie du code sera dès maintenant sous-entendue afin de pouvoir rester concis et mettre en évidence l'essentiel.  
* Les fonctions `preload`, `create` et `update` ne seront mentionnées que si elles contiennent du code.  
* Les élements `class Scene1 extends Phaser.Scene`, `game = new Phaser.Game(config)`, le constructeur et la variable `config` ne seront pas répétés, car ils ne subissent généralement pas de changements majeurs.
```
Chaque scène est traitée de manière complètement indépendante par Phaser. Elles sont donc utilisées pour représenter divers états ainsi que différents niveaux de profondeur de notre simulateur. Par exemple, mon travail utilise deux scènes superposées lors de la simulation : une sert de monde simulé et une autre sert pour les boutons qui gèrent la caméra. De cette manière, les boutons ne génèrent pas de collisions avec les robots ou les murs. De plus, comme chaque scène a sa propre caméra, l'interface qui permet de gérer le point de vue reste en place même lorsque le robot se déplace [^src5]. La gestion des scènes se fait dans les scènes elles-mêmes.
 
Phaser lance systématiquement la première scène de la liste lorsqu'il démarre. Depuis là, Phaser met à diposition des commandes qui permettent de gérer les scènes qui sont actives ou non, celles qui s'actualisent et, si plusieurs sont actives à la fois, la manière dont elles se superposent. (voir documentation[^src6])

## Les objets
Les objets de Phaser sont les seuls élements en dehors de l'arrière-fond qui apparaissent à l'écran et c'est avec eux que l'utilisateur peut interagir. Ils ont donc des formes et des utilisations extrêmement variées et il est donc essentiel d'en maîtriser l'usage.
```{code-block} js
---
linenos: true
caption: Création d'un objet
---
    create() {
        const x = 300,
            y = 300,
            width = 100,
            height = 100,
            color = 0x00ff00;

        this.add.rectangle(x, y, width, height, color)
    };
```
```{admonition} Commentaire
---
class: note
---
Ce code place un carré vert de 100 pixels de côté aux coordonnées `(300;300)` L'origine est par défaut au coin en haut à gauche.


Dans cet exemple, c'est un rectangle qui est ajouté, mais Phaser met à diposition beaucoup d'autres formes qui sont détaillées dans la  documentation[^src7][^src8]. Chaque type d'objet a donc des paramètres qui lui sont propres. Il est bien sûr possible d'ajouter des objets depuis d'autres fonctions que `create`.
```
### Les objets visuels et physiques

Il est important de savoir que l'objet qui vient d'être ajouté n'est pas un objet physique et n'est donc pas pris en compte par Matter. En effet, il existe des différences entre les objets que Phaser affiche à l'écran et ceux  que Matter traite: certains peuvent apparaître visuellement mais ne pas créer de collisions, l'inverse est également vrai. Pour ajouter un objet au moteur physique, il suffit d'ajouter "matter" à la commande, comme suit:

```{code-block} js
this.matter.add.rectangle(x, y, width, height)
```

Il n'est pas nécessaire d'y ajouter une couleur, car cet objet est uniquement traité par Matter mais n'apparait pas à l'écran sauf si le mode de débogage est actif. Pour avoir un objet visuel qui possède une boîte de collision, il faut utiliser la fonction suivante:

```{code-block} js
this.matter.add.gameObject(visual, hitbox)
```

Cette fonction prend un ou deux paramètres:
* `visual`: l'aspect visuel de la forme à ajouter.
* `hitbox`: la boîte de collision. Si aucun paramètre n'est donné, un rectangle qui contient la forme est ajouté.
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
Ce code ajoute un cercle rouge d'un rayon de 50 pixels au point de coordonnées `(300;300)`. La ligne 9 est importante dans le cas d'un cercle, car sans elle la zone de collision de l'objet `cercle` serait  un carré de 100 pixels de côté qui contiendrait le cercle rouge. Cependant elle n'a aucune influence sur l'apparence de l'objet. 
```
### Appeler un document

Certains objets comme les images et les sprites sont basés sur des documents externes au code. Il est donc nécessaire de charger ces documents dans la mémoire pour pouvoir les utiliser plus tard. Pour ce faire, on utilise, généralement dans la fonction `preload`, la commande `this.load` suivie du type de document à charger.

```{code-block} js
---
caption: Par exemple
---
this.load.image(key, path)
```

Cette commande utilise les paramètres suivants:  
* `key`: Une chaîne de caractères désignant la clé dont on souhaite se servir pour faire référence à l'image plus tard.
* `path`: Une chaîne de caractères indiquant le chemin de l'image choisie dans le système de fichiers.

```{code-block} js
---
linenos: true
---
preload(){
    this.load.image("picture", "assets/picture.png")
};

create(){
    this.add.image(x, y, "picture")
};
```
Ce procédé n'est pas réservé aux images mais est nécessaire dès que le programme utilise un document externe au code.

### Les méthodes

Une fois un objet créé, il est souvent utile d'en modifier les attributs. Pour ce faire, deux manières de procéder coexistent:
* Utiliser une méthode mise à disposition par Phaser qui ira changer l'attribut souhaité.
* Accéder directement à cet attribut et le modifier soi-même.  

```{code-block} js 
---
caption: Par exemple
linenos: true
---
create(){
    this.Rectangle = this.add.rectangle(100, 100, 50, 50, 0x0000ff)
    this.Rectangle.setX(500)
    this.Rectangle.x = 500
};
```

Dans ce code, les lignes 3 et 4 ont le même effet: changer la coordonnée x du rectangle en 500.  
Même s'il est toujours possible d'utiliser les deux manières, il existe cependant certaines situations dans lesquelles la seconde méthode est plus agréable. La différence reste toutefois légère mais peut être plus marquée dans un code plus complexe.


Les différents attributs et méthodes sont documentés par Phaser[^src9].



[^src1]: PHOTON STORM "Welcome to Phaser 3" Consulté le 04 janvier 2022 <<https://phaser.io/phaser3>>
[^src2]: PHOTON STORM "Phaser - HTML5 Game Framework" Consulté le 04 janvier 2022 <<https://github.com/photonstorm/phaser>>
[^src3]: PHOTON STORM "Class: Game" Consulté le 05 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Game.html>>
[^src4]: PHOTON STORM "Phaser.Types. Core: GameConfig" Consulté le 05 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Types.Core.html#.GameConfig>>
[^src5]: PHOTON STORM "How Scenes Work" Consulté le 7 janvier 2022 <<https://phaser.io/phaser3/contributing/part5>>
[^src6]: PHTON STORM "Class: SceneManager" Consulté le 7 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Scenes.SceneManager.html>>
[^src7]: PHOTON STORM "Namespace: GameObjects" Consulté le 7 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.html>>
[^src8]: PHOTON STORM "Namespace: Geom" Consulté le 10 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Geom.html>>
[^src9]: PHOTON STORM "Namespace: Components"  Consulté le 10 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.GameObjects.Components.html>>