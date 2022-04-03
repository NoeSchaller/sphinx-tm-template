# Introduction

## Projet 
Ce travail de maturité vise à créer un simulation web du robot Maqueen. Il est ainsi construit de manière à répliquer aussi bien que possible la version physique du robot dans le but de servir d'outil complémentaire à celui-ci. En effet bien que le robot maqueen soit un bon outil pédagogique, il n'est par nature pas toujours adapté à un système scolaire gymnasial. Le robot, et plus particulièrement l'environnement qu'il nécessite (obstacles et marquages), peuvent être compliqués à mettre en place rapidement dans une salle de classe.  
Il existe toutefois déjà un simulateur du robot sur TigerJython mais celui-ci ne propose pas une mise en place de l'environement des plus aisée. De plus il peut être fastidieux de mettre en place TigerJython sur les appareils d'étudiants (particulièrement les mac).  
Afin de palier à ces problèmes ce travail est développé dans un navigateur pour de le rendre accessible et permettre aux étudiants de faire leurs devoisr sans avoir à installer TigerJython. De plus la manière de mettre en place l'environement est rendue aussi intuitive que possible

## Technologies utilisées

La simulation étant développée dans le navigateur, la quasi-totalité du programme est écrit en Javascript et contient bien sûr des ressources: principalement des images et des documents JSON.  
Afin de simplifier la gestion de l'interface graphique qui constitue le coeur du travail, le logiciel Phaser est utilisé. Il permet de simuler la plupart de la physique et fournit un grand nombre de méthodes extrêment utiles à ce genre de projet. De plus afin d'étendre la portée de Phaser sur la mesure de distances, un plugin permettant le Raycasting[^glo] est aussi utilisé.

## Prérequis

Tout d'abord, la mise en place de la simulation nécessite un serveur afin de pouvoir gérer toute les ressources utiles à son fonctionnement.  
Additionnelement, l'implémentation du travail à un site internet suppose des connaissances basique en Javascript et en HTML afin de pouvoir indiquer le lieu où lancer le travail sur la page et paramétrer la simulation correctement. La compréhension complète du travail implique toutefois une maîtrise un peu plus poussée du Javascript, la connaissance de notion telle que les objets et plus particulèrement des classes est indispensable. Une documentation des bases de Phaser est également incluse dans le travail car son fonctionnement et sa structure sont des eléments essentiels à ce projet.

[^glo]: voir {ref}`glossaire<glo>`