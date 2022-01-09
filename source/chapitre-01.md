(uneref)=
# Phaser
Phaser est un logiciel open source développé et maintenu par Photon Storm depuis 2013. Il permet de créer des interfaces graphiques 2D (pricipalement des jeux) et de coder leur interactions avec l'utilisateur dans un environnement HTML5. Il est toutefois également possible de l'utiliser sur Android et iOS mais cela nécéssite que le code soit préalablement compilé. Le programme peut être utilisé à l'aide de Javascript et de Typescript. La version 3.0.0 est disponible depuis début 2018 et mon travail utilisé la version 3.55.2. Phaser dipose également d'un grand nombre de plugins mis à disposition par sa communauté.[^scr1][^scr2]

## La classe Game
La racine de Phaser est la classe Game, c'est cette classe qui va créer l'interface graphique selon les paramètres qui lui sont fournis puis l'actualiser.[^src3] La classe Game pouvant recevoir de nombreux paramètres, tous ceux-ci sont regroupés par l'utilisateur dans un unique dictionnaire qui sera le seul paramètre de Game.  
L'utilisation d'un dictionnaire à la place de plusieurs paramètres disctints à probablement pour but de rendre ce processus plus simple et intuitif. En effet dans un dictionnaire l'ordre des clés n'a pas d'importance (contrairement à l'utilisation multiples paramètres).  
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

game = new Game(config)
```
```{admonition} Commentaire
---
class: info
---
Ce code crée un interface de 500 pixels sur 700 qui tourne à 60 images par seconde et possède un fond bleu  

**Lignes 1-6:**
- La création d'une variable dédiée à ce dictionnaire n'est pas obligatoire mais peut aider à rendre les paramètres plus lisibles
  
**Ligne 8:**
- Ce code crée un interface de 500 pixels sur 700 qui tourne à 60 images par seconde et possède un fond bleu
- En plus d'éviter d'avoir à se préoccuper de l'ordre des clés, un dictionnaire reand aussi plus aisé d'identifié l'effet de chaqu'une des données
```




Une fois cet objet Game créé, Phaser va créer les différentes scènes puis entrer dans un cycle afin d'actualiser la page en fonction des évenements se produisants.[^src3]

## Les scènes
Une scène est un groupe d'objets et de cameras qui sont traité ensemble par Phaser. Une scène se définit à partir d'au moins 4 function: constructor, preload, create et update. Lorsqu'une scene est lancée par Phaser procède ainsi:   
1. La function preload charge les assets spécifiés dans la mémoire vive de l'ordinateur afin que le reste du programme soit aussi fluide que possible
2. La fonction create met en place les objets et variables nécéssaires à cette scènes
3. La fonction update est exécutée en boucle afin d'actualisé la scène.
```{admonition} Note
---
class: tip
---
Le contructeur est pricipalement utile pour donner un nom (key dans le programme) à la scène afin de pouvoir s'y référer plus tard.
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
    scene: [Scene1]
    };

game = new Game(config)
```
```{admonition} Commentaire
---
class: info
---
Ce code crée un jeu avec une scène vide  
Super() sert à donner une clé de référence à la scène
À présent on peut référer la scène de cette manière: game.scene.keys.scene1
```
Chaque scène est traité de manière complètement indépendante par Phaser, elles sont donc utilisées pour représenter divers états ainsi que différents niveaux de profondeurs de notre simulateur. Par exemple mon travail utilise deux scènes superposées lors de la simulation: une sert de monde simulés et une autre pour les boutons tel que ceux qui gèrent la caméra. De cette manière les boutons ne générent pas de collision avec les robots ou les murs, de plus comme chaque scène à sa propre caméra l'interface qui permet de gérer le point de vue reste en place même lorsque le robots se déplace.[^src4]  
La gestion des scènes se fait dans les scènes même, Phaser va systématiquement lancer la première scène de la liste. Depuis là Phaser met à diposition des commander qui permettent de gérer les scènes qui sont actives ou non, celles qui s'actualisent et si plusieurs sont actives à la fois, la manière dont elles se superposent. (documentation ici: <https://photonstorm.github.io/phaser3-docs/Phaser.Scenes.SceneManager.html>)

### Les objets
Les objets 
### Les caméras

## Les plugins
### Le raycasting




[^scr1]: PHOTON STORM "Welcome to Phaser 3" Consulté le 04 janvier 2022 <<https://phaser.io/phaser3>>
[^scr2]: PHOTON STORM "Phaser - HTML5 Game Framework" Consulté le 04 janvier 2022 <<https://github.com/photonstorm/phaser>>
[^src3]: PHOTON STORM "Class: Game" Consulté le 05 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Game.html>>
[^src4]: PHOTON STROM "How Scenes Work" Consulté le 7 janvier 2022 <<https://phaser.io/phaser3/contributing/part5>>