class TMConfig:

    title = u'Simulation Web du robot MacQueen'
    first_name = 'Noé'
    last_name = 'Schaller'
    author = f'{first_name} {last_name}'
    year = u'2022'
    month = u'Janvier'
    seminary_title = u'Développement d’outils ou matériel d’enseignement de l’informatique'
    tutor = u"Cédric Donner"
    release = "Version intermédiaire"
    repository_url = "https://github.com/NoeSchaller/TM_Noe"

    @classmethod
    def date(cls):
        return cls.month + " " + cls.year

tmconfig = TMConfig()