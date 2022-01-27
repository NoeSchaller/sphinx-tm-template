# Introduction

## Projet 
Ce travail de maturité vise à créer un simulation web du robot Maqueen, et est ainsi construit de manière à répliquer aussi bien que possible la version physique du robot afin de servir d'outil complétmentaire à celui-ci. En effet bien que le robot maqueen soit un bon outil pédagogique, il n'est par nature pas toujours adapté à un système scolaire gymnasial. Le robot et plus particulièrement l'environnement qu'il nécessite (obstacles et marquages) peuvent être compliqué à mettre en place rapidement dans une salle de classe.  
Il existe toutefois déjà un simulateur du robot sur TigerJython mais celui-ci ne propose pas une mise en place de l'environement des plus simple. De plus il peut être fastidieux de mettre en place TigerJython sur les appareils d'étudiants (particulièrement les mac).  
Afin de palier à ces problèmes ce travail este donc développé dans le navigateur afin de le rendre accessible et permettre aux étudiants de faire leurs devoir sans avoir à installer TigerJython, de plus la manière de mettre en place l'environement est rendue aussi intuitive que possible

## Technologies utilisées

La simulation étant développer sur le navigateur, la quasi-totalité du programme est écrit en Javascript et contient bien sûr des assets: principalement des images et des documents Json.  
Afin de simplifier la gestion de l'interface graphique qui constitue le coeur du travail,vle logiciel Phaser est utilisé. Il permet de simuler la plupart de la physique et fournit un grand nombres de méthode extrêment utiles à ce genre de projet. De plus afin d'étendre la portée de Phaser sur le gestion de collision et le mesure de distance, un plugin permettant le Raycasting est aussi utilisé.

## Prérequis

Tout d'abord le mise en place de la simulation nécessite bien sûr un serveur afin de pouvoir gérer toute les ressources utiles à son fonctionnement.  
Additionnelement l'implémentation du travail à un site internet suppose des connaissances basique en Javascript et en HTML afin de pouvoir indiquer le lieu où lancer le travail sur la page et paramètrer la simulation correctement. La compréhension complète du travail implique toutefois une maîtrise un peu plus poussée du Javascript, la connaissance de notion tel que les objects et plus particulèrement des classes est indispensable. Une documentation des bases de Phaser est également incluse dans le travail car son fonctionnement et sa structure sont des eléments essentiels à projet.