(uneref)=
# Phaser
Phaser est un logiciel open source développé et maintenu par Photon Storm depuis 2013. Il permet de créer des interfaces graphiques 2D et de coder leur interactions avec l'utilisateur dans un environnement HTML5. Il est toutefois également possible de l'utiliser sur Android et iOS mais cela nécéssite que le code soit préalablement compilé. Le programme peut être utilisé à l'aide de Javascript et de Typescript. La version 3.0.0 est disponible depuis début 2018 et mon travail utilisé la version 3.55.2. Phaser dipose également d'un grand nombre de plugins mis à disposition par sa communauté.[^scr1][^scr2]
## La classe Game
La racine de Phaser est la classe Game, c'est cette classe qui va créer l'interface graphique selon les paramètres qui lui sont fournis puis l'actualiser.[^src3] La classe Game pouvant recevoir de nombreux paramètres, tous ceux-ci sont regroupés par l'utilisateur dans un unique dictionnaire qui sera le seul paramètre de Game.  
L'utilisation d'un dictionnaire à la place de plusieurs paramètres disctints à probablement pour but de rendre ce processus plus simple et intuitif. En effet dans un dictionnaire l'ordre des clés n'a pas d'importance (contrairement à l'utilisation multiples paramètres).  
Les différentes clés permettent de choisir principalement la manière dont l'interface sera implémenté à l'ensemble de la page ainsi que certaines configurations de base tel que le moteur physique ou les plugins utilisés. Toutes les clés disponibles  qu'il est possible d'utiliser sont documentées ici : <https://photonstorm.github.io/phaser3-docs/Phaser.Types.Core.html#.GameConfig>, 
```{code-block} js
---
caption: Par exemple
---
var config = {
    width: 500,
    height: 700,
    fps: 60,
    backgroundColor: 0x0000ff
    }

// Création d'un dictionnaire contenant les paramètres souhaité
// La création d'une variable dédiée à ce dictionnaire n'est pas obligatoire mais peut aider à rendre les paramètres plus lisibles

game = new Game(config)

// Ce code crée un interface de 500 pixels sur 700 qui tourne à 60 images par seconde et possède un fond bleu
// En plus d'éviter d'avoir à se préoccuper de l'ordre des clés du dictionnaire il est très aisé d'identifié l'effet de chaqu'une des données
```
Une fois cet objet Game créé, Phaser va créer les différentes scènes puis entrer dans un cycle afin d'actualiser la page en fonction des évenements se produisants.[^src3]
## Les scènes
Une scène est un ensemble d'objets et de cameras qui sont traité par Phaser, elle sont principalement utilisées
### Les objets
### Les caméras

## Les plugins
### Le raycasting




[^scr1]: PHOTON STORM "Welcome to Phaser 3" Consulté le 04 janvier 2022 <<https://phaser.io/phaser3>>
[^scr2]: PHOTON STORM "Phaser - HTML5 Game Framework" Consulté le 04 janvier 2022 <<https://github.com/photonstorm/phaser>>
[^src3]: PHOTON STORM "Class: Game" Consulté le 04 janvier 2022 <<https://photonstorm.github.io/phaser3-docs/Phaser.Game.html>>