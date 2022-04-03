# Conclusion

L'objectif de ce travail était de créer un simulateur pour les robots Maqueen et de rendre sa mise en place la plus simple possible afin de palier aux faiblesses du simulation TigerJython.


Ce objectif est effectivement en grande partie remplit, le fait de développer le simulateur dans le navigateur le rend plus accessible et l'utilisation de fonctions pour créer l'environement nécessaire au robot rend la mise en place relativement simple et efficace. Cependant les éléments disponibles restent limités a des cercles des rectangles et des images détecables par les capteurs infrarouges. La possibilité d'ajouter des polygones plus complexes donnerait à l'utilisateur beaucoup plus de liberté.



De plus le contrôle de la simulation est très restraint en dehors de la mise en place malgré la mise en place de quelque méthodes. L'ajout d'une classe ayant une fonction `callback` qui serait excécutée lorsqu'un robot touche sa zone de collision accorderait serait sans doute grandement bénéfique à la simulation. L'implémentation de méthodes applicables directement à la simulation serait également bienvenue, elles pourraient par exemple permettre de la mettre en pause ou de la réinitialiser.


Pour terminer il est intéressant de noter que l'utilisation de multiples classes pour créer les robots permet de modifier ceux-ci aisément, voir même d'en construire de nouveau. Il serait donc possible de s'écarter des robots Maqueen et de fabriquer des robots virtuels sur mesure si nécessaire.