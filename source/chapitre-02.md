# Mode d'emploi
## Mise en place
### La classe simulation
Tout comme Phaser, la simulation se repose principalement sur une seule et unique classe: la classe simulation. Lancer la simulation ne nécéssite ne nécéssite donc que d'appeler celle-ci avec les bon paramètres.
```{code-block} js
sim = new simulation(width, height, map)
```
- width et height servent à définir les dimensions souhaitées de l'interface graphique.
- map est chaîne de caractère, elle représente le chemin vers un document Json qui contient les intructions de mise en place de l'environnement du robot.

### Le document Json
Le document Json contient toute les informations nécéssaire à la simulation pour construire l'environnement virtuel, il peut donc contenir des commandes pour préparer:
- Des robots
- Des obstacles (murs)
- Des marquages au sol
```{code-block} json
---
caption: voici un exemple
linenos: true
---
{
    "bots": [
        "new botLight(this, 'bob', 400, 300)",
        "new botLight(this, 'nb2', 100, 300, 45)"
    ],
    "walls": [
        "new wallRect(this, 600, 0, 800, 200)"
    ],
    "marks": [
        "new markPic(this, 400, 100, 'test')",
        "new markPic(this, 200, 100, 'test2')",
        "new markRect(this, 0, 0, 100,100)"
    ]
}
```
## Contrôler les robots

### L'i2c

### Les pins
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  
.  

```{tip} Penser à clean des fois
``` 

```{code-block} js
---
linenos: true
caption: ceci est un test
---
for(let i = 0; i < 100; i++){
    console.log('voila')
};
```
---
% hmmmm...
>quote ?

```{figure} figures/turtle.png
---
width: 50%
align: left
---

```

Un petit tableau ?
```{warning}
le tableau est pour l'instant un échec
```
Par contre les ref: {ref}`uneref`