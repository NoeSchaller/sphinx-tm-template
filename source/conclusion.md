# Conclusion

L'objectif de ce travail était de créer un simulateur pour les robots Maqueen et de rendre sa mise en place la plus simple possible afin de pallier aux faiblesses du simulateur TigerJython.


Cet objectif est en grande partie remplit: le fait de développer le simulateur dans le navigateur le rend plus accessible et l'utilisation de fonctions pour créer l'environnement nécessaire au robot rend la mise en place relativement simple et efficace. Cependant, les éléments disponibles restent limités à des cercles des rectangles et des images détectables par les capteurs infrarouges. La possibilité d'ajouter des polygones plus complexes donnerait à l'utilisateur beaucoup plus de liberté.



De plus, le contrôle de la simulation est très restreint une fois celle-ci mise en place, bien que quelques méthodes aient été ajoutées pour augmenter les possiblités. D'autre part, l'ajout d'un élément ayant une fonction `callback` qui serait excécutée lorsqu'un robot touche sa zone de collision serait sans doute grandement bénéfique à la simulation. L'implémentation de méthodes applicables directement à la simulation seraient également bienvenue, elles pourraient par exemple permettre de la mettre en pause ou de la réinitialiser. Ces développements ne seraient pas trop complexes à intégrer, mais ils n'ont pas semblés prioritaires à ce stade du projet.


Pour terminer, il est intéressant de noter que l'utilisation de multiples classes pour créer les robots permet de modifier ceux-ci aisément, voir même d'en construire de nouveaux. Il est donc possible de s'écarter des robots Maqueen et de fabriquer des robots virtuels sur mesure si nécessaire.