# Mode d'emploi
## Mise en place
### La classe simulation
Tout comme Phaser, la simulation se repose principalement sur une seule et unique classe: la classe simulation. Lancer la simulation ne nécéssite ne nécéssite donc que d'appeler celle-ci avec les bon paramètres.
```{code-block} js
sim = new simulation(width, height, map, background)
```
- width et height servent à définir les dimensions souhaitées de l'interface graphique.
- map est chaîne de caractère, elle représente le chemin vers un document Json qui contient les intructions de mise en place de l'environnement du robot.
- background est une couleur exprimée en hexadécimal qui définit l'aspect du fond de la simulation. Si rien n'est spécifé, le fond est beige.

### Le document Json
Le document Json contient toute les informations nécéssaire à la simulation pour construire l'environnement virtuel, il se divise en quatre partie qui représente les différents élements utilisables:
- Des robots
- Des obstacles (des murs)
- Des marquages au sol
- Des images (qui sont également des marquages)
Chaque object a sa
```{code-block} json
---
caption: voici un exemple
linenos: true
---
{
    "bots": [
        "new botLight('N°1', 400, 300, 45)"
    ],
    "walls": [
        "new wallRect(600, 0, 200, 200)"
    ],
    "marks": [
        "new markRect(0, 0, 100,100)"
    ],
    "pictures": [
        "new Picture(400, 100, 'assets/irTest.png')"
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