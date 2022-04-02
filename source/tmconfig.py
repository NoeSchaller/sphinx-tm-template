class TMConfig:

    title = u'Simulation Web du robot Maqueen'
    first_name = 'Noé'
    last_name = 'Schaller'
    author = f'{first_name} {last_name}'
    year = u'2022'
    month = u'Avril'
    seminary_title = u'Développement d’outils ou matériel d’enseignement de l’informatique'
    tutor = u"Cédric Donner"
    release = "version finale"
    repository_url = "https://github.com/NoeSchaller/TM_Noe"

    @classmethod
    def date(cls):
        return cls.month + " " + cls.year

tmconfig = TMConfig()