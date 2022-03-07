# Documentation
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
    this.game = new Phaser.Game({
      width: width,
      height: height,
      backgroundColor: background,
      type: Phaser.WEBGL,
      canvas: document.getElementById(id),
      scene: [
        new Simul(this, mapLoad, mapCreate, mode),
        new Setup(width, height),
        new Over(this, width, height),
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
* Les lignes 11 créent des listes vides dans lesquelles s'ajouteront les différent éléments lorqu'ils seront créés. Ces listes permettent d'accéder et de modifier ces éléments simplement.
* Les lignes 12-40 initient l'interface Phaser en fonction des différents paramètres.

``` {admonition} Commentaire
---
class: note
---
Les lignes 18-22 créent les différentes scènes utilisées et leur donne certains paramètres essentiels. Il faut toutefois noter que seule la scène `Simul` démarre et que les autres seront lancées depuis celle-ci.

Les lignes 30-38 mettent en place un plugin qui servira à simuler les capteurs ultrason des robots:
* La ligne 33 assigne une clé de référence au plugin
* La ligne 34 indique le plugin
* La ligne 35 indique à Phaser la manière de mettre en place le plugin
```

## La scène Simul
### Le contructeur

La premère scène lancée par Phaser est la scène `Simul`. Comme cette scène met en place l'environemment du robots il est donc logique que les autres scènes démarre après pour qu'elle puissent s'adapter aux éléments déjà en place.

``` {code-block} js
---
linenos: true
---
  constructor(that, mapLoad, mapCreate, mode) {
    super("simulation");
    this.mapLoad = mapLoad;
    this.mapCreate = mapCreate;
    this.parent = that;
    this.mode = mode;
  }
```

Le contructeur de la scène s'occupe simplement de recevoir et stocker les différents paramètres hérité de la classe `game`: `mapLoad` et `mapCreate` correspond aux fonctions définie par l'utilisateur, `that` représente la classe `game` elle même, `this.parent` sera surtout utilisé pour que les éléments de la simulation puissent s'ajouter aux différentes listes de la classe `simulation`.

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
``mapLoad`` est également exécutée et charge les fichiers nécessaire à l'utilisateur avec comme argument la scène principale de la simulation

### La fonction create

La fonction permet principalement de mettre en place 

## Les éléments

### Le robot lite

## La caméra


[^src1]: R https://photonstorm.github.io/phaser3-docs/Phaser.Plugins.PluginManager.html (le 7 mars)