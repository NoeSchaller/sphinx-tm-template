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

```` {admonition} Commentaire
---
class: note
---
Les lignes 18-22
```
## Les robots

### Le robot lite

## La caméra