# Documentation
## Remarques préalables

COMMENTER LA STRUCTURE DES DOCUMENTS
### Conventions
Dans ce travail les variables représentant des angles possèdent "angle" dans leur nom lorsqu'il s'agit de degrés et "rotation" s'il s'agit de radians.

## La classe simulation
La classe `simulation` constitue la coeur du simulateur. Cette classe a deux fonction principale: elle crée l'interface graphique dans lequel se déroule la simulation et elle regroupe les principaux éléments de celle-ci afin de rendre accessibles leur différentes méthodes.
``` {code-block} js
---
linenos: true
---
class simulation {
  constructor(
    width,
    height,
    id,
    mapLoad,
    mapCreate,
    background = 0xcccac0,
    mode = 0
  ) {
    this.robots = [];
    this.walls = [];
    this.marks = [];
    this.game = new Phaser.Game({
      width: width,
      height: height,
      backgroundColor: background,
      type: Phaser.WEBGL,
      canvas: document.getElementById(id),
      scene: [
        new Simul(
          this.robots,
          this.walls,
          this.marks,
          mapLoad,
          mapCreate
        ),
        new Over(this.robots, width, height),
      ],
      physics: {
        default: "matter",
        matter: {
          gravity: { y: 0, x: 0 },
          debug: 0,
        },
      },
      plugins: {
        scene: [
          {
            key: "PhaserRaycaster",
            plugin: PhaserRaycaster,
            mapping: "raycasterPlugin",
          },
        ],
      },
    });
  }
}

```
Ce code constitue l'intégralité de la classe simulation et il les deux but de la classe aisément indentifiable:
* La ligne 18 indique à Phaser d'utiliser WEBGL plutôt que canvas. Ce choix à été fait car même si WEBGL n'est pas supporté par tout les navigateurs, il est plus performant et tout de mêm très répandu.
* Les lignes 11, 12 et 13 créent des listes vides dans lesquelles s'ajouteront les différent éléments lorqu'ils seront créés. Ces listes permettent d'accéder et de modifier ces éléments simplement.
* Les lignes 14-46 initient l'interface Phaser en fonction des différents paramètres.

``` {admonition} Commentaire
---
class: note
---
Les lignes 20-29 créent les différentes scènes utilisées et leur donne certains paramètres essentiels. Il faut toutefois noter que seule la scène `Simul` démarre et que les autres seront lancées depuis celle-ci.

Les lignes 37-45 mettent en place un plugin qui servira à simuler les capteurs ultrason des robots:
* La ligne 41 assigne une clé de référence au plugin
* La ligne 42 indique le plugin
* La ligne 43 indique à Phaser la manière de mettre en place le plugin
```

## La scène principale

La premère scène lancée par Phaser est la scène `Simul`. Comme cette scène met en place l'environemment du robots il est donc logique que les autres scènes démarre après pour qu'elle puissent s'adapter aux éléments déjà en place.

### Le contructeur

``` {code-block} js
---
linenos: true
---
  constructor(robots, walls, marks, mapLoad, mapCreate) {
  super("simulation");
  this.mapLoad = mapLoad;
  this.mapCreate = mapCreate;
  this.robots = robots;
  this.walls = walls;
  this.marks = marks;
}
```

Le contructeur de la scène s'occupe simplement de recevoir et stocker les différents paramètres hérité de la classe `game`: `mapLoad` et `mapCreate` correspondent aux fonctions définie par l'utilisateur. `robots` `walls` et `marks` représentent les listes auquelles les différents éléments seront ajoutés.

### La fonction preload

La fonction preload charge les ressources nécéssaire pour les robots et les éventuelles images nécéssaire à l'utilisateur.

``` {code-block} js
---
linenos: true
---
preload() {
  this.load.json("liteShape", "assets/liteShape.json");
  this.load.json("plusShape", "assets/plusShape.json");

  this.load.spritesheet("liteBodyPic", "assets/liteBody.png", {
    frameWidth: 80,
    frameHeight: 80,
  });
  this.load.spritesheet("plusBodyPic", "assets/plusBody.png", {
    frameWidth: 100,
    frameHeight: 103,
  });

  this.mapLoad(this);
}
```

Le programme charge des documents JSON qui contiennent les informations quant à la forme des zone de collisions des robots aux lignes 2 et 3 ainsi que des sprites pour leur aspect visuel.
`mapLoad` est également exécutée et charge les fichiers nécessaire à l'utilisateur avec comme argument la scène principale de la simulation

### La fonction create

La fonction a deux fonction principales:
* exécuter la fonction `mapCreate` et donc mettre en place l'environnement des robots
* démarrer les autres scènes nécéssaire au programme

``` {code-block} js
---
linenos: true
---
create() {
  this.RaycasterDomain = [];

  this.mapCreate(this);
    
  this.scene.launch("overlay", [this.robots, this.cameras.main]);
}
```

Le permière ligne crée une liste qui sera complétée lorsque les éléments seront créés, cette liste sert à indiquer au plugin de raycasting quel éléments il doit considérer. La ligne 4 appelle la fonction `mapCreate` avec comme argument la scène principale de la simulation. La ligne 6 lance la scène nommée  `overlay`. Le second argument, `[this.robots, this.cameras.main]`, de la commande correspond à des données que la scène `simulation` passe à `overlay`

### La fonction update

Le seul usage de la fonction `update` est de constamment mettre à jour les robots. Ce sont les seuls éléments concernés car ces sont les seuls éléments à interagir avec d'autres. De plus, la plupart des composants du robots ne sont pas attaché à ce dernier: Phaser ne le pertmettant pas aisément et doivent donc être replacé relativement au robot à chaque actualisation de la simulation.

``` {code-block} js
---
linenos: true
---
update() {
  for (let i = 0; i < this.parent.robots.length; i++) {
    this.parent.robots[i].update();
  }
}
```

Les lignes 2 à 4 du code font une itération à travers la liste des robots et la ligne 3 actualise les différents robots.

## La scène overlay

La scène `overlay` a pour objectif la gestion de la caméra et des bouttons qui permet de la manipuler. La plupart de ces rôles sont pris en charge par la classe `CameraManager`. La création d'une scène dédiée à cet usage est toutefois essentielle car elle permet d'éviter d'avoir des interactions indésirables entre des éléments de l'interface et ceux de la simulation. La création d'une deuxième scène permet également d'éviter que l'interface se déplacer en même que la caméra puisque chaque scène possède sa propre caméra et que seule celle de la simulation est déplacée.

### Le constructeur

``` {code-block} js
constructor(robots, width, height) {
  super("overlay");
  this.robots = robots;
  this.height = height;
  this.width = width;
}
```

Le contructeur de la scène s'occupe simplement de recevoir et stocker les différents paramètres hérité de la classe. `height` et `width` permetteront à l'interface de se placer dans les bord de la fenêtre et `robots` d'accéder au robots pour créer les boutons qui gèrent la caméra en fonction des robots présents dans la simulation.
 
### La fonction init

``` {code-block} js
init(data) {
  this.robots = data[0];
  this.cameraMain = data[1];
}
```

La fonction `init` permet de recevoir des informations lorsque la scène est initialisée. Contrairement au constructeur qui est appelé lors de la création de la classe `Game` cette fonction est appélée lorsque la scène démarre alors que le constructeur est appélé lorsque la scène est créée avant que la simulation ait démarrée.

``` {code-block} js
scene: [
  new Simul(
    this.robots,
    this.walls,
    this.marks,
    mapLoad,
    mapCreate
  ),
  new Over(this.robots, width, height),
],
```

Par exemple dans ce code qui se trouve dans les paramètres de la classe `Game`, c'est le constructeur qui est appelé.

``` {code-block} js
this.scene.launch("overlay", [this.robots, this.cameras.main]);
```

Cette ligne sert à initialiser la scène `overlay` depuis un autre scène les arguments suivants la clé de la scène à initialiser sont transmis à la fonction `init`.
La fonction `init` est donc essentielle car est permet à la scène `overlay` de s'adapter au éléments présents dans la simulation. Ainsi dans ce cas, la fonction reçoit la scène principale et il lui sera donc possible d'en extraire les données nécessaires à la scène `overlay`

### La fonction preload

``` {code-block} js
preload() {
  this.load.image('echelle', 'assets/scale.png')
}
```

L'image `echelle` est un segment de 100 pixels qui représente 10 centimètres dans l'espace simulé.

```{image} ./figures/scale.png
:alt: scale
:width: 100px
:align: center
```

### La fonction create

``` {code-block} js
---
linenos: true
---
create() {
  this.echelle = this.add.image(70, this.height - 30, 'echelle')
  this.buttonsCam = []

  this.camera = new CameraManager(this, this.robots, this.cameraMain);
}
```

La fonction `create` met en place l'échelle à la ligne 2. Elle prépare également une liste vide nommée `buttonsCam` à la ligne suivante pour contenir les boutons de l'interface graphique. Finalement la ligne 5 créée une occurence de la classe `CameraManager` qui s'occupera de gérer la caméra de la scène principale.

### La fonction update

``` {code-block} js
---
linenos: true
---
update() {
  this.camera.update(this.robots, this);
}
```

La fonction `update` de la scène `overlay` sert simplement à actualiser la caméra, la fonction `CameraManager.update` est expliquée dans la section traitant de la classe `CameraManager`.

## Les éléments

### Les constructeurs

Les différents éléments poosèdent tous des constructeurs très similaires, c'est pourquoi ils seront tous traités ensembles.


``` {code-block} js
---
caption: constructeur de `wallRect`
---
constructor(scene, x, y, width, heigth, angle = 0) {
  this.position = { x: x, y: y };
  this.scale = { x: 1, y: 1 };
  this.angle = angle;
  this.body = scene.matter.add
    .gameObject(scene.add.rectangle(x, y, width, heigth, 0xff00000))
    .setStatic(true)
    .setAngle(angle);

  scene.walls.push(this);
  scene.RaycasterDomain.push(this.body);
}
```
---
``` {code-block} js
---
caption: constructeur de `wallCircle`
---
constructor(scene, x, y, radius) {
  this.position = { x: x, y: y };
  this.scale = { x: 1, y: 1 };
  this.angle = 0;
  this.body = scene.matter.add
    .gameObject(scene.add.circle(x, y, radius, 0xff0000),
    scene.matter.add.circle(x, y, radius))
    .setStatic(true)
    .setFriction(1);

  scene.walls.push(this);
  scene.RaycasterDomain.push(this.body);
}
```
---
``` {code-block} js
---
caption: constructeur de `markRect`
---
constructor(scene, x, y, width, height, angle = 0) {
  this.picture = "geom";
  this.position = { x: x, y: y };
  this.scale = { x: 1, y: 1 };
  this.angle = angle;
  this.body = scene.matter.add
    .gameObject(scene.add.rectangle(x, y, width, height, 0x000000))
    .setCollidesWith(0)
    .setAngle(angle);

  scene.marks.push(this);
}
```
---
``` {code-block} js
---
caption: constructeur de `markCircle`
---
constructor(scene, x, y, radius) {
  this.picture = "geom";
  this.position = { x: x, y: y };
  this.scale = { x: 1, y: 1 };
  this.angle = 0;
  this.body = scene.matter.add
    .gameObject(scene.add.circle(x, y, radius, 0x000000),
      scene.matter.add.circle(x, y, radius))
    .setCollidesWith(0);

  scene.marks.push(this);
}
```
---
``` {code-block} js
---
caption: constructeur de `Picture`
---
constructor(scene, key, x, y, scaleX = 1, scaleY = 1) {
  this.picture = key;
  this.position = { x: x, y: y };
  this.scale = { x: scaleX, y: scaleY };
  this.angle = 0;
  this.body = scene.matter.add
    .image(x, y, key)
    .setCollidesWith(0)
    .setAngle(0)
    .setScale(scaleX, scaleY);

  scene.marks.push(this);
}
```
---

Le constructeur des différentes classes ne remplit que deux objectifs: le premier est de créer un object Phaser rectangulaire statique en fonction des paramètres introduit par l'utilisateur, le second est de s'ajouter à la liste des murs afin d'être accessible facilement.  Additionnellement, les classes définissant des marques possèdent un attribut `picture` qui permet au capteurs infrarouges d'identifier si la marque qu'il survole est une image ou non. Si c'est une image `picture` représente également la clef de l'image source. Les éléments décrivant un mur ajoute également leur objet Phaser `body` à `scene.RaycasterDomain` car ce sont ces éléments qui seront détecté par les robots.

``` {admonition} Remarque
---
class: note
---
La liste des murs contenu dans la classe `simulation` ne peut pas être utilisée à la place de `RaycasterDomain` car elle contient des objets `wall` là où le plugin demande des élément Phaser, en l'occurence `wall.body`
```

### Les méthodes

``` {code-block} js
setPosition(x, y) {
  this.body.setPosition(x, y);
  this.position = { x: x, y: y };
}

setAngle(deg) {
  this.body.setAngle(deg);
  this.angle = angle;
}

setScale(x, y) {
  this.body.setScale(x, y);
  this.scale = { x: x, y: y };
}
```
Les méthodes des éléments sont de simple extensions de méthodes Phaser, pour cette raison un code parfaitement similaire est utilisé pour tous les éléments.

## Les composants des robots
### La classe motor
#### Le constructeur
##### Explications des paramètres
``` {code-block} js
constructor(
  scene,
  reference,
  robotRotation,
  x,
  y,
  width,
  height,
  point1,
  point2,
  powToSpeed
)
```
* `scene`: la scène à laquelle le robot est ajouté
* `reference`: l'objet Phaser auquel la roue doit être attachée
* `Botangle`: l'angle du robot lorsqu'il est chargé
* `x`: la coordonée en x de la roue par rapport à la position de `reference`
* `y`: la coordonée en y de la roue par rapport à la position de `reference`
* `width`: la largeur de la roue en pixel
* `height`: la hauteur de la roue en pixel
* `point1`: un objet Javascript ayant une clef x et un clef y, il représente un point d'attache pour la roue
* `point2`: un objet Javascript ayant une clef x et un clef y, il représente un point d'attache pour la roue
* `powToSpeed`: une fonction qui représente la croissance de la vitesse angulaire de la roue en fonction de la puissance

#### Explications des paramètres calculés

``` {code-block} js
---
linenos: true
---
constructor(
  scene,
  reference,
  robotRotation,
  x,
  y,
  width,
  height,
  point1,
  point2,
  powToSpeed
) {
  this.scene = scene;
  this.speed = 0;
  this.power = 0;
  this.dir = 0;
  this.radius = height / 20;

  if (powToSpeed === undefined) {
    this.powToSpeed = function (power) {
      return power;
    };
  } else {
    this.powToSpeed = powToSpeed;
  }

  this.deltaOrigin = Math.sqrt(x ** 2 + y ** 2);
  const deltaPoint1 = Math.sqrt(point1.x ** 2 + point1.y ** 2);
  const deltaPoint2 = Math.sqrt(point2.x ** 2 + point2.y ** 2);

  this.rotationOrigin = Math.atan2(y, x)

  this.rotationPoint1 =
    robotRotation + Math.atan2(point1.y, point1.x);
  this.rotationPoint2 =
    robotRotation + Math.atan2(point2.y, point2.x);
```

  

### Les capteurs infrarouges

### Les capteurs ultrasons

### Les leds

### Les i2c

### Les pins

## Les robots

## La caméra


[^src1]: R https://photonstorm.github.io/phaser3-docs/Phaser.Plugins.PluginManager.html (le 7 mars)