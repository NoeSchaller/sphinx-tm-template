# Documentation
## Fonctionnement global

L'architecture du programme repose sur la classe simulation: une fois celle-ci initialisée, la scène `simulation` est lancée. Celle-ci lance la scène `overlay` et exécute la fonction `mapCreate` qui met en place les éléments.

```{image} ./figures/graf.png
:alt: schéma
:align: center
```

## La classe simulation
La classe `simulation` constitue le cœur du simulateur. Cette classe a deux fonctions principales: elle crée l'interface graphique dans lequel se déroule la simulation et elle regroupe les principaux éléments de celle-ci afin de rendre accessibles leur différentes méthodes.
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
        new Over(),
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
Ce code constitue l'intégralité de la classe simulation, les deux buts de la classe sont aisément identifiables:
* Les lignes 11, 12 et 13 créent des listes vides dans lesquelles s'ajouteront les différents éléments lorsqu'ils seront créés. Ces listes permettent d'accéder et de modifier ces éléments simplement.
* Les lignes 14-46 initient l'interface Phaser en fonction des différents paramètres.
* La ligne 18 indique à Phaser d'utiliser WebGL pour le rendu plutôt que Canvas. Ce choix à été fait car même si WebGL n'est pas supporté par tous les navigateurs, il est plus performant que Canvas et tout de même très répandu.


``` {admonition} Commentaire
---
class: note
---
Les lignes 20-29 créent les différentes scènes utilisées et leur donnent certains paramètres essentiels. Il faut toutefois noter que seule la scène `Simul` démarre et que les autres seront lancées depuis celle-ci.

Les lignes 37-45 mettent en place un plugin qui servira à simuler les capteurs ultrason des robots:
* La ligne 41 assigne une clé de référence au plugin
* La ligne 42 indique le plugin
* La ligne 43 indique à Phaser la manière de mettre en place le plugin
```

## La scène principale

La première scène lancée par Phaser est la scène `Simul`. Comme cette scène met en place l'environnement du robot, il est logique que les autres scènes démarrent après, pour qu'elle puissent s'adapter aux éléments déjà en place.

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

Le contructeur de la scène s'occupe simplement de recevoir et stocker les différents paramètres hérités de la classe `game`.


`mapLoad` et `mapCreate` correspondent aux fonctions définie par l'utilisateur.


`robots`, `walls` et `marks` représentent les listes auxquelles les différents éléments seront ajoutés.

### La fonction preload

La fonction preload charge les ressources nécessaires pour les robots et les éventuelles ressources utiles à l'utilisateur.

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

Le programme charge des documents JSON qui contiennent les informations quant à la forme des zones de collisions des robots aux lignes 2 et 3, ainsi que des sprites pour leur aspect visuel.
La fonction `mapLoad` est également exécutée et charge les fichiers utiles à l'utilisateur avec comme argument la scène principale de la simulation.

### La fonction create

La fonction a deux buts principaux:
* exécuter la fonction `mapCreate` et donc mettre en place l'environnement des robots
* démarrer la scène `overlay`

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

La permière ligne crée une liste qui sera complétée lorsque les éléments seront créés, cette liste sert à indiquer au plugin de raycasting[^glo] quels éléments il doit considérer (voir {ref}`le capteur ultrason<ultra>`). La ligne 4 appelle la fonction `mapCreate` avec comme argument la scène principale de la simulation. La ligne 6 lance la scène nommée  `overlay`. Le second argument, `[this.robots, this.cameras.main]`, de la commande correspond à des données que la scène `simulation` passe à `overlay`

### La fonction update

La seule utilité de la fonction `update` est de constamment mettre à jour les robots. Les autres éléments ne sont pas concernés car ils sont statiques.

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

Les lignes 2 à 4 du code parcourent la liste des robots et la ligne 3 actualise les différents robots.

## La scène overlay

La scène `overlay` a pour objectif la gestion de la caméra et des boutons qui permettent de la manipuler. La création d'une scène dédiée à cet usage est essentielle car elle permet d'éviter d'avoir des interactions indésirables entre les éléments de l'interface et ceux de la simulation. La création d'une deuxième scène permet également d'éviter à l'interface de se déplacer en même temps que la caméra, puisque chaque scène possède sa propre caméra et que seule celle de la simulation est déplacée.

### Le constructeur

``` {code-block} js
constructor() {
  super("overlay");
}
```
 
### La fonction `init`

``` {code-block} js
init(data) {
  this.robots = data[0];
  this.cameraMain = data[1];
}
```

La fonction `init` permet de recevoir des informations lorsque la scène est initialisée. Contrairement au constructeur qui est appelé lors de la création de la classe `Game` cette fonction est appellée lorsque la scène démarre.

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

Par exemple, dans ce code qui se trouve dans les paramètres de la classe `Game`, c'est le constructeur qui est appelé.

``` {code-block} js
this.scene.launch("overlay", [this.robots, this.cameras.main]);
```

Cette ligne sert à initialiser la scène `overlay` depuis une autre scène, le second argument est transmis à la fonction `init`.
La fonction `init` est donc essentielle car elle permet à la scène `overlay` de s'adapter aux éléments présents dans la simulation. Dans ce cas, la fonction reçoit la liste des robots et la caméra de la scène principale.

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
  this.buttons = [];
  this.echelle = this.add.image(70, this.height - 30, "echelle");

  this.add
    .text(10, 60, "-", {
      color: "#000",
      backgroundColor: "#fff",
      padding: 1,
      fontSize: 40,
    })
    .setInteractive()
    .on("pointerdown", () => {
      (this.camera.zoom /= 1.2), (this.echelle.scale /= 1.2);
    });

  this.add
    .text(10, 10, "+", {
      color: "#000",
      backgroundColor: "#fff",
      padding: 1,
      fontSize: 40,
    })
    .setInteractive()
    .on("pointerdown", () => {
      (this.camera.zoom *= 1.2), (this.echelle.scale *= 1.2);
    });

  this.buttons.push(
    this.add
      .text(10, 110, "Free", {
        color: "#000",
        backgroundColor: "#999",
        padding: 3,
      })
      .setInteractive()
      .on("pointerdown", () => {
        this.keyboardControl = true;
        this.cursor.setPosition(15 + this.buttons[0].width, 110);
        this.camera.stopFollow();
      })
  );

  for (let i = 0; i < this.robots.length; i++) {
    this.buttons.push(
      this.add
        .text(10, 140 + 30 * i, this.robots[i].name, {
          color: "#000",
          backgroundColor: "#999",
          padding: 3,
        })
        .setInteractive()
        .on("pointerdown", () => {
          this.keyboardControl = false;
          this.cursor.setPosition(
            15 + this.buttons[i + 1].width,
            140 + 30 * i
          );
          this.camera.startFollow(this.robots[i].body);
        })
    );
  }

  this.cursor = this.add.text(0, 0, "<=", { color: "#000", fontSize: 20 });

  if (this.robots.length !== 0) {
    this.keyboardControl = false;
    this.cursor.setPosition(15 + this.buttons[1].width, 140);
  } else {
    this.keyboardControl = true;
    this.cursor.setPosition(15 + this.buttons[0].width, 113);
  }
}
```

Les lignes 2-3 de la fonction `create` créent une liste vide pour contenir les boutons et une image qui servira d'échelle.


La fonction crée ensuite une série de boutons:
* Les deux premiers des lignes 5 à 27 servent à modifier le zoom de la caméra
* Le troisième aux lignes 29-42 sert à ajouter le bouton `Free` qui permettra de contrôler les déplacements de la caméra au clavier
* Les boutons suivants correspondent aux différents robots

La fonction met également le booléen `keyboardControl` en place et crée un curseur pour indiquer l'état de la caméra.

### La fonction update

``` {code-block} js
---
linenos: true
---
update() {
  if (this.keyboardControl) {
    const inputs = this.input.keyboard.addKeys({
      up: "up",
      down: "down",
      left: "left",
      right: "right",
    });

    if (inputs.up.isDown) {
      this.camera.scrollY -= 5;
    } else if (inputs.down.isDown) {
      this.camera.scrollY += 5;
    }

    if (inputs.left.isDown) {
      this.camera.scrollX -= 5;
    } else if (inputs.right.isDown) {
      this.camera.scrollX += 5;
    }
  }
}
```

La fonction `update` de la scène `overlay` sert simplement à utiliser les données du clavier lorsque cela est nécessaire.

## Les éléments
### Les constructeurs

Les différents éléments possèdent tous des constructeurs très similaires, c'est pourquoi ils seront tous traités ensemble.


``` {code-block} js
---
caption: constructeur de `wallRect`
---
constructor(scene, x, y, width, height, angle = 0) {
  this.position = { x: x, y: y };
  this.scale = { x: 1, y: 1 };
  this.angle = angle;
  this.body = scene.matter.add
    .gameObject(scene.add.rectangle(x, y, width, height, 0xff00000))
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
constructor(scene, key, x, y, angle = 0 scaleX = 1, scaleY = 1) {
  this.picture = key;
  this.position = { x: x, y: y };
  this.scale = { x: scaleX, y: scaleY };
  this.angle = angle;
  this.body = scene.matter.add
    .image(x, y, key)
    .setCollidesWith(0)
    .setScale(scaleX, scaleY);
    .setAngle(angle);

  scene.marks.push(this);
}
```
---

Les constructeurs des différentes classes ne remplissent que deux objectifs: le premier est de créer un objet Phaser rectangulaire statique en fonction des paramètres introduits par l'utilisateur, le second est de s'ajouter à la liste leur correspondant afin d'être accessible facilement.  Additionnellement, les classes définissant des marques possèdent un attribut `picture` qui permet au capteurs infrarouges d'identifier si la marque qu'il survole est une image ou non. Si c'est une image, `picture` représente alors la clef de l'image source (voir {ref}`les capteurs infrarouges<infra>`). Les éléments décrivant un mur ajoutent également leur objet Phaser `body` à `scene.RaycasterDomain` car ce sont ces éléments qui seront détectés par les capteurs infrarouges.

``` {admonition} Remarque
---
class: note
---
La liste des murs contenue dans la classe `simulation` ne peut pas être utilisée à la place de `RaycasterDomain` car elle contient des objets `wall` là où le plugin demande des éléments Phaser, en l'occurence `wall.body`
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
  this.body.setAngle(0)
  this.body.setScale(x, y);
  this.body.setAngle(this.angle);
  this.scale = { x: x, y: y };
}
```
Les méthodes des éléments sont de simple extensions de méthodes Phaser, pour cette raison un code parfaitement similaire est utilisé pour tous les éléments.


La fonction `setScale` nécessite que l'élément soit à un angle 0, sinon Phaser semble ne pas fonctionner correctement et, dans certains, cas la zone ne collision de correspond plus au visuel.

(composants)=
## Les composants des robots
### La classe motor
#### Le constructeur
##### Explication des paramètres
``` {code-block} js
constructor(
  scene,
  reference,
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
* `x`: la coordonée en x de la roue par rapport à la position de `reference`
* `y`: la coordonée en y de la roue par rapport à la position de `reference`
* `width`: la largeur de la roue en pixel
* `height`: la hauteur de la roue en pixel
* `point1`: un objet Javascript ayant une clef x et y, il représente un point sur reference pour y attacher la roue
* `point2`: un objet Javascript ayant une clef x et y, il représente un point sur reference pour y attacher la roue
* `powToSpeed`: une fonction qui représente la croissance de la vitesse angulaire de la roue en fonction de la puissance

#### Explications des paramètres calculés

``` {code-block} js
---
linenos: true
---
constructor(
  scene,
  reference,
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
  this.angle = 0;s.powToSpeed = powToSpeed;
  }

  this.deltaOrigin = Math.sqrt(x ** 2 + y ** 2);
  const deltaPoint1 = Math.sqrt(point1.x ** 2 + point1.y ** 2),
   deltaPoint2 = Math.sqrt(point2.x ** 2 + point2.y ** 2);

  this.rotationOrigin = Math.atan2(y, x)

  const rotationPoint1 = Math.atan2(point1.y, point1.x),
   rotationPoint2 = Math.atan2(point2.y, point2.x);
```

Les éléments `delta` représentent la distance, l'origine de `reference` et l'objet.


Les éléments `rotation` représentent les angles par rapport à l'horizontal.

#### L'élément `wheel`

``` {code-block} js
---
linenos: true
---
this.wheel = scene.matter.add
  .gameObject(
    scene.add.rectangle(
      reference.x +
        this.deltaOrigin *
          Math.cos(this.rotationOrigin + reference.rotation),
      reference.y +
        this.deltaOrigin *
          Math.sin(this.rotationOrigin + reference.rotation),
      width,
      height,
      0x808080
    ),
    scene.matter.add.rectangle(
      reference.x +
        this.deltaOrigin *
          Math.cos(this.rotationOrigin + reference.rotation),
      reference.y +
        this.deltaOrigin *
          Math.sin(this.rotationOrigin + reference.rotation),
      width,
      height
    )
  )
  .setRotation(reference.rotation)
  .setFrictionAir(3);

scene.matter.add.constraint(this.wheel, reference, undefined, 1, {
  pointA: {
    x: (height / 2) * Math.sin(-reference.rotation),
    y: (height / 2) * Math.cos(-reference.rotation),
  },
  pointB: {
    x: deltaPoint1 * Math.cos(rotationPoint1 + reference.rotation),
    y: deltaPoint1 * Math.sin(rotationPoint1 + reference.rotation),
  },
});

scene.matter.add.constraint(this.wheel, reference, undefined, 1, {
  pointA: {
    x: (height / 2) * Math.sin(-reference.rotation),
    y: (height / 2) * Math.cos(-reference.rotation),
  },
  pointB: {
    x: deltaPoint2 * Math.cos(rotationPoint2 + reference.rotation),
    y: deltaPoint2 * Math.sin(rotationPoint2 + reference.rotation),
  },
});

scene.matter.add.constraint(this.wheel, reference, undefined, 1, {
  pointA: {
    x: (height / 2) * Math.sin(reference.rotation),
    y: (-height / 2) * Math.cos(reference.rotation),
  },
  pointB: {
    x: deltaPoint1 * Math.cos(rotationPoint1 + reference.rotation),
    y: deltaPoint1 * Math.sin(rotationPoint1 + reference.rotation),
  },
});

scene.matter.add.constraint(this.wheel, reference, undefined, 1, {
  pointA: {
    x: (height / 2) * Math.sin(reference.rotation),
    y: (-height / 2) * Math.cos(reference.rotation),
  },
  pointB: {
    x: deltaPoint2 * Math.cos(rotationPoint2 + reference.rotation),
    y: deltaPoint2 * Math.sin(rotationPoint2 + reference.rotation),
  },
});
```

L'élément `wheel` est créé des lignes 1 à 22, puis est attaché à `reference` depuis `point1` et `point2` à l'aide de 4 éléments `constraint` afin de former une structure rigide.

```{image} ./figures/constraint.png
:alt: constraint
:width: 100px
:align: center
```
``` {code-block} js
---
caption: Les éléments Phaser `constraint` s'ajoutent ainsi:
---
scene.matter.add.contraint(bodyA, bodyB, length, stiffness, options)
```
* `bodyA`: le premier objet auquel attacher la contrainte
* `bodyB`: le second objet auquel attacher la contrainte
* `length`: la longueur de la contrainte
* `stiffness`: la rigidité de la contrainte
* `options`: des options diverses, voir documentation[^src2]

#### La méthode `setSpeed`

``` {code-block} js
---
linenos: true
---
setSpeed(dir, power) {
  if (power >= 0 && power <= 255) {
    this.dir = dir;
    this.power = power;
 let speed = this.powToSpeed(power) * this.radius  * (12 / 100);;

    if (speed < 0) {
      speed = 0;
    }

    if (dir == 0) {
        this.speed = 0;
      } else if (dir == 1) {
        this.speed = speed;
      } else if (dir == 2) {
        this.speed = -speed;
}
```

Cette méthode applique la fonction `powToSpeed` à `power` puis l'applique en accord avec `dir` si le résultat est plus grand que 0. Le facteur 12 / 100  permet de convertir la vitesse de centimètres en nombres utilisables par Phaser, il a été determiné de manière expérimentale.

#### La méthode `update`

``` {code-block} js
---
linenos: true
---
update() {
  const deltaX = this.wheel.x - this.wheel.body.positionPrev.x,
    deltaY = this.wheel.y - this.wheel.body.positionPrev.y,
    rotationSpeed =
      Math.round(
        (Math.sqrt(deltaX ** 2 + deltaY ** 2) / this.radius) *
          (100 / 12) *
          5.6 *
          100
      ) / 100;

  this.angle += Math.round((rotationSpeed / Math.PI) * 2 * 80);

  this.wheel.body.positionImpulse.x =
    (Math.cos(this.wheel.rotation - Math.PI / 2) * this.speed);

  this.wheel.body.positionImpulse.y =
    (Math.sin(this.wheel.rotation - Math.PI / 2) * this.speed);
}
```

La méthode `update` commence par calculer la vitesse de rotation du moteur. Les objects Phaser possèdent une propriété `speed` mais celle-ci ne semble pas être opérationnelle. En effet, elle augmente lorsque le robot bute contre un obstacle.


Ensuite, la méthode fait avancer la roue en fonction de la vitesse.

(infra)=
### Les capteurs infrarouges
#### Le constructeur

``` {code-block} js
---
linenos: true
---
constructor(scene, reference, x, y, radius = 2, StateBlack = true) {
  this.scene = scene;
  this.reference = reference;
  this.deltaOrigin = Math.sqrt(x ** 2 + y ** 2);
  this.rotationOrigin = Math.atan2(y, x);
  this.StateBlack = StateBlack;

  this.ir = scene.matter.add
    .gameObject(
      scene.add.circle(reference.x + x, reference.y + y, radius, 0xffffff),
      scene.matter.add.circle(reference.x + x, reference.y + y, 1)
    )
    .setCollidesWith(0)
    .setDepth(2);
}
```

#### La méthode `isMarked`

``` {code-block} js
---
linenos: true
---
isMarked() {
  for (let i = 0; i < this.scene.marks.length; i++) {
    if (this.scene.matter.overlap(this.ir, this.scene.marks[i].body)) {
      const mark = this.scene.marks[i];
      if (mark.picture == "geom") {
        return this.StateBlack;
      }

      const xAngle0 =
          Math.cos(-(mark.angle / 180) * Math.PI) *
            (this.ir.x - mark.position.x) -
          Math.sin(-(mark.angle / 180) * Math.PI) *
            (this.ir.y - mark.position.y),
        yAngle0 =
          Math.sin(-(mark.angle / 180) * Math.PI) *
            (this.ir.x - mark.position.x) +
          Math.cos(-(mark.angle / 180) * Math.PI) *
            (this.ir.y - mark.position.y);

      const color = this.scene.textures.getPixel(
        xAngle0 / mark.scale.x + mark.body.width / 2,
        yAngle0 / mark.scale.y + mark.body.height / 2,
        mark.picture
      );
      if (color !== null) {
        if (color.v < 0.3) {
          return this.StateBlack;
        }
      }
    }
  }
  return !this.StateBlack;
}
```

La méthode contrôle pour chaque marque de la liste `scene.marks` si elle se superpose avec le capteur infrarouge. Si c'est le cas elle obtient la propriété `picture` de la marque. Dans ce cas, si `picture` est égal à `geom` le programme retourne `StateBlack`, car `geom` représente les marques noires. Sinon, il obtient la couleur du pixel sur laquelle se trouve le capteur infrarouge.



Il peut arriver que le pixel recherché soit en dehors de l'image car la zone de collision du capteur est un cercle et que le pixel n'est mesuré qu'en son centre. Si c'est le cas, la couleur est égale `null` ce qui est interprété comme une absence de marque. Si la couleur n'est pas `null`, sa propriété `v` représente sa luminosité. Si cette dernière est inférieure à 0.3 qui est un coefficient choisit arbitrairement, la couleur est considérée comme noire.

#### La méthode `update`

``` {code-block} js
---
linenos: true
---
update() {
  this.ir.setPosition(
    this.reference.x +
      this.deltaOrigin *
        Math.cos(this.reference.rotation + this.rotationOrigin),
    this.reference.y +
      this.deltaOrigin *
        Math.sin(this.reference.rotation + this.rotationOrigin)
  );
   if (this.isMarked()) {
    this.ir.fillColor = 0xffffff;
  } else {
    this.ir.fillColor = 0x404040;
  }
}
```

`update` sert à la fois à replacer le capteur par rapport à la référence et à actualiser son apparence en fonction de son état.

(ultra)=
### Les capteurs ultrasons
#### Explication des paramètres

``` {code-block} js
constructor(scene, reference, x, y, angle = 0, range = 255, coneAngle = 60)
```
* `scene`: la scène à laquelle le robot est ajouté
* `reference`: l'objet Phaser auquel la roue doit être attachée
* `x`: la coordonnée horizontale du capteur par rapport à `reference`
* `y`: la coordonnée verticale du capteur par rapport à `reference`
* `angle`:  l'angle du capteur par rapport à `reference`
* `coneAngle`:  l'angle du cône de détection du capteur

#### Le constructeur

Pour mieux comprendre le fonctionnement du plugin utilisé pour simuler les capteurs ultrason, il est nécessaire de se référer à la documentation du plugin.[^ray]

``` {code-block} js
---
linenos: true
---
class ultrasonicD {
  constructor(scene, reference, x, y, angle = 0, range = 255, coneAngle = 60) {
    this.reference = reference;
    this.scene = scene;
    this.range = range;
    this.rotation = (angle / 180) * Math.PI;
    this.delta = Math.sqrt(x ** 2 + y ** 2);
    this.rotationOrigin = Math.atan2(y, x);

    this.raycaster = scene.raycasterPlugin.createRaycaster()
    this.rayCone = this.raycaster
      .createRay({
        origin: {
          x: reference.x + x,
          y: reference.y + y,
        },
        autoSlice: true,
        collisionRange: range * 10,
      })
      .setConeDeg(coneAngle)
      .setAngle(reference.rotation + Math.PI / 2 + this.rotation);

    this.rayCone.enablePhysics("matter");
  }
```

Le constructeur crée aux lignes 11-21 un élément `rayCone` à l'aide d'un plugin qui permet le rayCasting

``` {admonition} Commmentaire
---
class: note
---
Le terme `Math.PI / 2` à la ligne 21 est présent car l'angle 0 se trouve à droite pour le plugin alors que le robot est définit avec l'angle 0 vers le haut.
```

#### La méthode `getDistance()`

``` {code-block} js
---
linenos: true
---
getDistance() {
  let distances = [];
  this.raycaster.mapGameObjects(this.scene.RaycasterDomain);
  this.intersections = this.rayCone.castCone();
  for (let i = 0; i < this.intersections.length; i++) {
    distances.push(Math.round(Math.sqrt(
      (this.intersections[i].x - this.rayCone.origin.x) ** 2 +
      (this.intersections[i].y - this.rayCone.origin.y) ** 2
    )));
  }
  const min = Math.min(...distances);
  if (min < this.range * 10) {
    return Math.round(min / 10);
  } else {
    return this.range;
  }
}
```

Dans ce code `intersections` est une  liste de points d'intersections entre le capteur et les éléments de `RaycasterDomain`. La distance entre ces points et le capteur est calculée des lignes 5 à 10. Elle est ensuite ajoutée à `distances`. Seule la plus petite distance est retenue à la ligne 11.

#### La méthode `update`

``` {code-block} js
---
linenos: true
---
update() {
  this.rayCone
    .setOrigin(
      this.reference.x +
      this.delta * Math.cos(this.reference.rotation + this.rotationOrigin),
      this.reference.y +
      this.delta * Math.sin(this.reference.rotation + this.rotationOrigin)
    )
    .setAngle(this.reference.rotation - Math.PI / 2 + this.rotation);
}
```

Cette méthode sert à replacer le capteur par rapport au robot et d'ajuster son angle.

### Les leds
#### Le constructeur

``` {code-block} js
---
linenos: true
caption: Le contructeur de la classe `led`
---
constructor(scene, reference, x, y, radius = 4) {
  this.reference = reference;
  this.on = false;
  this.delta = Math.sqrt(x ** 2 + y ** 2);
  this.rotationOrigin = Math.atan2(y, x);

  this.led = scene.add
    .circle(reference.x + x, reference.y + y, radius, 0x500000)
    .setDepth(2);
}
```

``` {code-block} js
---
linenos : true
caption: Le constructeur de la classe `rgbLed`
---
constructor(scene, reference, x, y, radius = 5) {
  this.reference = reference;
  this.color = 0x808080;
  this.deltaOrigin = Math.sqrt(x ** 2 + y ** 2);
  this.rotationOrigin = Math.atan2(y, x)

  this.rgb = scene.add
    .circle(reference.x + x, reference.y + y, radius, 0x808080)
    .setDepth(2);
}
```

Les contructeurs des deux types de leds sont extrêmement similaires, la seule différence étant que les leds rgbs ont une propriété `color` et les autres une `on`.

#### Les méthodes

``` {code-block} js
---
linenos: true
caption: Les méthodes de la classe `led`
---
setOn(bool) {
  this.on = bool;
}

update() {
  this.led.setPosition(
    this.reference.x +
    this.delta * Math.cos(this.reference.rotation + this.rotationOrigin),
    this.reference.y +
    this.delta * Math.sin(this.reference.rotation + this.rotationOrigin)
  );

  if (this.on) {
    this.led.fillColor = 0xff0000;
  } else {
    this.led.fillColor = 0x500000;
  }
}
```

``` {code-block} js
---
linenos: true
caption: Les méthodes de la classe `rgbLed`
---
setColor(color) {
  this.color = color;
}

update() {
  this.rgb.setPosition(
    this.reference.x +
      this.deltaOrigin *
        Math.cos(this.reference.rotation + this.rotationOrigin),
    this.reference.y +
      this.deltaOrigin *
        Math.sin(this.reference.rotation + this.rotationOrigin)
  );

  this.rgb.fillColor = this.color;
}
```

Les méthodes `setOn` et `setColor` permettent de changer l'état de la led, soit avec un booléen, soit avec une couleur exprimée en hexadécimal. `update` met à jour la position et l'apparence de la led.

### Les pins

``` {code-block} js
---
linenos: true
---
class pin {
  constructor(component, read, write) {
    this.component = component;
    this.read = read;
    this.write = write;
  }

  read_digital() {
    return eval(`this.component.${this.read}()`);
  }

  write_digital(set) {
    eval(`this.component.${this.write}(${set})`);
  }
}
```

* `component`: l'élément auquel appliquer `read` et `write`
* `read`: une fonction applicable à `component`, ne prend pas d'argument
* `write`: une fonction applicable à `component`, prend un booléen comme argument

### L'élément `i2cLite`

``` {code-block} js
---
linenos: true
---
class i2cLite {
  constructor(robot) {
    this.robot = robot;
  }

  write(adresse, byte) {
    if (adresse == 0x10) {
      const register = byte[0];

      //gestion des moteur
      if (register == 0x00) {
        if (byte.length == 3) {
          const dirL = byte[1],
            pL = byte[2];
          this.robot.Lmotor.setSpeed(dirL, pL);
        } else if (byte.length >= 5) {
          const dirL = byte[1],
            pL = byte[2],
            dirR = byte[3],
            pR = byte[4];
          this.robot.Lmotor.setSpeed(dirL, pL);
          this.robot.Rmotor.setSpeed(dirR, pR);
        }
      } else if (register == 0x02) {
        const dirR = byte[1],
          pR = byte[2];
        this.robot.Rmotor.setSpeed(dirR, pR);
      }
    }
  }
}
```

Le constructeur reçoit le robot que l'i2c devra modifier.


La méthode `write` commence par vérifier que l'adresse corresponde à `0x10`, ensuite elle applique différentes méthodes en fonction de `register` et du nombre d'octets transmis.

### L'élément `i2cPlus`

``` {code-block} js
---
linenos: true
---
class i2cPlus {
  constructor(robot) {
    this.robot = robot;
    this.colors = [
      0xff0000, 0x00ff00, 0xffff00, 0x0000ff, 0xff00ff, 0x00ffff, 0xffffff,
      0x808080,
    ];
    this.buffer = [];
  }

  write(adresse, byte) {
    if (adresse == 0x10) {
      const register = byte[0];

      //gestion des moteur
      if (register == 0x00) {
        if (byte.length == 3) {
          const dirL = byte[1],
            pL = byte[2];
          this.robot.Lmotor.setSpeed(dirL, pL);
        } else if (byte.length >= 5) {
          const dirL = byte[1],
            pL = byte[2],
            dirR = byte[3],
            pR = byte[4];
          this.robot.Lmotor.setSpeed(dirL, pL);
          this.robot.Rmotor.setSpeed(dirR, pR);
        }
        this.buffer.push(
          this.robot.Rmotor.power,
          this.robot.Rmotor.dir,
          this.robot.Lmotor.power,
          this.robot.Lmotor.dir
        );
      } else if (register == 0x02) {
        const dirR = byte[1],
          pR = byte[2];
        this.robot.Rmotor.setSpeed(dirR, pR);

        this.buffer.push(this.robot.Rmotor.power, this.robot.Rmotor.dir);
      } else if (register == 0x04) {
        this.buffer.push(
          this.robot.Rmotor.angle % 256,
          (this.robot.Rmotor.angle >> 8) % 256,
          this.robot.Lmotor.angle % 256,
          (this.robot.Lmotor.angle >> 8) % 256
        );
      }

      //gestion des leds rgb
      else if (register == 0x0b) {
        if (byte.length >= 3) {
          const colorL = this.colors[byte[1] - 1],
            colorR = this.colors[byte[2] - 1];
          this.robot.LLed.setColor(colorL);
          this.robot.RLed.setColor(colorR);
        } else if (byte.length == 2) {
          const colorL = this.colors[byte[1] - 1];
          this.robot.LLed.setColor(colorL);
        }
      } else if (register == 0x0c) {
        if (byte.length >= 2) {
          const colorR = this.colors[byte[1] - 1];
          this.robot.RLed.setColor(colorR);
        }
      }

      // gestion des ir
      else if (register == 0x1d) {
        let byte = 0;
        if (this.robot.irL3.isMarked()) {
          byte += 32;
        }
        if (this.robot.irL2.isMarked()) {
          byte += 16;
        }
        if (this.robot.irL1.isMarked()) {
          byte += 8;
        }
        if (this.robot.irR1.isMarked()) {
          byte += 4;
        }
        if (this.robot.irR2.isMarked()) {
          byte += 2;
        }
        if (this.robot.irR3.isMarked()) {
          byte += 1;
        }

        this.buffer.push(byte);
      }
    }
  }

  read(adresse, nb) {
    if (adresse == 0x10) {
      let get = [];

      for (let i = 0; i < nb; i++) {
        get.push(this.buffer[this.buffer.length - i - 1]);
      }
      return get;
    }
  }
}
```

Le contructeur reçoit le robot à modifier, il prépare également un buffer[^glo2] vide et une liste de couleurs que peuvent prendre les leds rgbs.


La méthode `write` de la classe `i2cPlus` fonctionne de la même manière que `i2cLite`. Il y a toutefois plus de registres disponibles. De plus certains registres ajoutent des données au buffer afin qu'elles puissent être lues par la méthode `read`. Les éléments ainsi ajoutés sont ajoutés dans le sens inverse qu'ils seront lus puisque `i2c.read` lit les octets depuis la fin du buffer.

## Les robots

Le code des robots est relativement simple puisqu'il ne fait que mettre en place les différents {ref}`composants <composants>`

### Le constructeur

``` {code-block} js
---
linenos: true
caption: le constructeur du Maqueen Lite
---
constructor(scene, name, x, y, angle) {
  //mise  en place de variables
  this.name = name;
  this.type = "maqueenLite";
  this.angle = angle;
  this.position = { x: x, y: y };

  //mise en place de l'élément body
  this.body = scene.matter.add
    .sprite(x, y, "liteBodyPic", undefined, {
      shape: scene.cache.json.get("liteShape").body,
    })
    .setFrictionAir(0)
    .setAngle(angle);

  //mise en place des moteurs
  let speedGrowth = function (power) {
    return (
      -9e-9 * power ** 4 +
      7e-6 * power ** 3 -
      0.0021 * power ** 2 +
      0.3121 * power -
      1.2
    );
  };

  this.Lmotor = new motor(
    scene,
    this.body,
    -35,
    18,
    9,
    43,
    { x: -10, y: -4 },
    { x: -10, y: 40 },
    speedGrowth
  );

  this.Rmotor = new motor(
    scene,
    this.body,
    35,
    18,
    9,
    43,
    { x: 10, y: -4 },
    { x: 10, y: 40 },
    speedGrowth
  );

  //mise en place du capteur ultrason
  this.ultrasonic = new ultrasonicD(scene, this.body, 0, -35);

  //mise en place des capteurs infrarouges
  this.irL = new infra(scene, this.body, -7, -16, 2, false);

  this.irR = new infra(scene, this.body, 7, -16, 2, false);

  //mise en place des leds
  this.LLed = new led(scene, this.body, -18, -32);

  this.RLed = new led(scene, this.body, 18, -32);

  // mise en place des pins
  this.pin13 = new pin(this.irL, "isMarked"); //irLeft
  this.pin14 = new pin(this.irR, "isMarked"); // irRight
  this.pin8 = new pin(this.LLed, "getOn", "setOn"); //LLed
  this.pin12 = new pin(this.RLed, "getOn", "setOn"); // RLed
  this.pin1; // ultrason

  // mise en place de l'i2c
  this.i2c = new i2cLite(this);

  // ajout du robot à la liste des robots
  scene.robots.push(this);
}
```

``` {code-block} js
---
linenos: true
caption: le constructeur du Maqueen Plus
---
constructor(scene, name, x, y, angle) {
  //mise  en place de variables
  this.name = name;
  this.type = "maqueenPlus";
  this.angle = angle;
  this.position = { x: x, y: y };

  //mise en place de l'élément body
  this.body = scene.matter.add
    .sprite(x, y, "plusBodyPic", undefined, {
      shape: scene.cache.json.get("plusShape").body,
    })
    .setFrictionAir(0)
    .setAngle(angle);

  //mise en place des moteurs
  let speedGrowth = function (power) {
    return (
      -1e-8 * power ** 4 +
      1e-5 * power ** 3 -
      0.0032 * power ** 2 +
      0.4053 * power -
      2.8394
    );
  };
  this.Lmotor = new motor(
    scene,
    this.body,
    -45,
    27,
    9,
    43,
    { x: -10, y: 5 },
    { x: -10, y: 49 },
    speedGrowth
  );

  this.Rmotor = new motor(
    scene,
    this.body,
    45,
    27,
    9,
    43,
    { x: 10, y: 5 },
    { x: 10, y: 49 },
    speedGrowth
  );

  //mise en place du capteur ultrason
  this.ultrasonic = new ultrasonicD(scene, this.body, 0, -21);

  //mise en place des capteurs infrarouges
  this.irL1 = new infra(scene, this.body, -5, -31);

  this.irL2 = new infra(scene, this.body, -15, -31);

  this.irL3 = new infra(scene, this.body, -45, -11);

  this.irR1 = new infra(scene, this.body, 5, -31);

  this.irR2 = new infra(scene, this.body, 15, -31);

  this.irR3 = new infra(scene, this.body, 45, -11);

  //mise en place des leds rgb
  this.LLed = new rgbLed(scene, this.body, -20, -45);

  this.RLed = new rgbLed(scene, this.body, 20, -45);

  //mise en place de l'i2c
  this.i2c = new i2cPlus(this);

  // ajout du robot à la liste des robots
  scene.robots.push(this);
}
```

L'élement `body` est un sprite qui utilise l'image `liteBodyPic` comme apparence et dont la forme est stockée dans le document JSON qui possède la clé `liteShape`.


Les fonctions `speedGrowth` ont été trouvées par mesures.

### Les méthodes

``` {code-block} js
---
linenos: true
caption: les méthodes du Maqueen Lite
---
getDistance() {
  return this.ultrasonic.getDistance();
}

update() {
  this.Lmotor.update();
  this.Rmotor.update();
  this.ultrasonic.update();
  this.irL.update();
  this.irR.update();
  this.LLed.update();
  this.RLed.update();
  this.position = { x: this.body.x, y: this.body.y };
  this.angle = this.body.angle;
}

setPosition(x, y) {
  this.body.setPosition(x, y);
  this.Lmotor.wheel.setPosition(
    x +
      this.Lmotor.deltaOrigin *
        Math.cos(this.Lmotor.rotationOrigin + this.body.rotation),
    y +
      this.Lmotor.deltaOrigin *
        Math.sin(this.Lmotor.rotationOrigin + this.body.rotation)
  );
  this.Rmotor.wheel.setPosition(
    x +
      this.Rmotor.deltaOrigin *
        Math.cos(this.Rmotor.rotationOrigin + this.body.rotation),
    y +
      this.Rmotor.deltaOrigin *
        Math.sin(this.Rmotor.rotationOrigin + this.body.rotation)
  );
}

setAngle(deg) {
  this.body.setAngle(deg);

  this.Lmotor.wheel.setPosition(
    this.body.x +
      this.Lmotor.delta *
        Math.cos((deg / 180) * Math.PI + this.Lmotor.relAngle),
    this.body.y +
      this.Lmotor.delta *
        Math.sin((deg / 180) * Math.PI + this.Lmotor.relAngle)
  );
  this.Lmotor.wheel.setAngle(deg);

  this.Rmotor.wheel.setPosition(
    this.body.x +
      this.Rmotor.delta *
        Math.cos((deg / 180) * Math.PI + this.Rmotor.relAngle),
    this.body.y +
      this.Rmotor.delta *
        Math.sin((deg / 180) * Math.PI + this.Rmotor.relAngle)
  );
  this.Rmotor.wheel.setAngle(deg);
}
```

``` {code-block} js
---
linenos: true
caption: les méthodes du Maqueen Plus
---
getDistance(){
  return this.ultrasonic.getDistance();
}

update() {
  this.Lmotor.update();
  this.Rmotor.update();
  this.ultrasonic.update();
  this.irL1.update();
  this.irL2.update();
  this.irL3.update();
  this.irR1.update();
  this.irR2.update();
  this.irR3.update();
  this.LLed.update();
  this.RLed.update();
  this.position = { x: this.body.x, y: this.body.y };
  this.angle = this.body.angle;
}

setPosition(x, y) {
  this.body.setPosition(x, y);
  this.Lmotor.wheel.setPosition(
    x +
      this.Lmotor.deltaOrigin *
        Math.cos(this.Lmotor.rotationOrigin + this.body.rotation),
    y +
      this.Lmotor.deltaOrigin *
        Math.sin(this.Lmotor.rotationOrigin + this.body.rotation)
  );
  this.Rmotor.wheel.setPosition(
    x +
      this.Rmotor.deltaOrigin *
        Math.cos(this.Rmotor.rotationOrigin + this.body.rotation),
    y +
      this.Rmotor.deltaOrigin *
        Math.sin(this.Rmotor.rotationOrigin + this.body.rotation)
  );
}

  setAngle(deg) {
    this.body.setAngle(deg);

    this.Lmotor.wheel.setPosition(
      this.body.x +
        this.Lmotor.deltaOrigin *
          Math.cos((deg / 180) * Math.PI + this.Lmotor.rotationOrigin),
      this.body.y +
        this.Lmotor.deltaOrigin *
          Math.sin((deg / 180) * Math.PI + this.Lmotor.rotationOrigin)
    );
    this.Lmotor.wheel.setAngle(deg);

    this.Rmotor.wheel.setPosition(
      this.body.x +
        this.Rmotor.deltaOrigin *
          Math.cos((deg / 180) * Math.PI + this.Rmotor.rotationOrigin),
      this.body.y +
        this.Rmotor.deltaOrigin *
          Math.sin((deg / 180) * Math.PI + this.Rmotor.rotationOrigin)
    );
    this.Rmotor.wheel.setAngle(deg);
  }
}
```

Les méthodes `setPosition` et `setAngle` ne modifient les états que des éléments `body` et des deux moteurs. Les autres éléments se replacent eux-mêmes dans leur méthode `update`


[^src1]: PHOTON STORM "Class: PluginManager" Consulté le 07 mars 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Plugins.PluginManager.html>>
[^src2]: PHOTON STORM "Member of: Phaser.Physics.Matter.Factory" Consulté le 03 avril 2022 <<https://newdocs.phaser.io/docs/3.54.0/focus/Phaser.Physics.Matter.Factory-constraint>>
[^ray]: WISERIM "Phaser Raycaster" Consulté le 18 novembre 2021 <<https://github.com/wiserim/phaser-raycaster>>
[^glo]: voir {ref}`glossaire<glo>`
[^glo2]: voir {ref}`glossaire<glo>`