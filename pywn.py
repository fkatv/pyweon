#
#    pyweon package
#    Fabián Catalán V. - github.com/fkatv
#    Chile, Enero 2022
#

class Wn:
    def __init__(self):
        self._wn = self.create_wn()
        self._aweon = 'aweon'

        self.conjugaciones = ['yo me ', 'tú te ', 'el se ', 'nosotros nos ', 'ellos se ', 'voh (te) ']
        self.presente_simple = ['o','as / ai' ,'a', 'amos', 'an', 'ai']
        self.conjugaciones_simplepass = ['yo me ', 'tú te ', 'el se ', 'nosotros nos ', 'ellos se ', 'voh (te)']
        self.pasado_simple = ['é','aste', 'ó', 'amos','aron','aste']
        self.preterito_simple = ['é', 'arás', 'ará','aremos', 'arán','ai']
        self.conjugaciones_simplepret = ['yo me ', 'tú te ', 'el se ', 'nosotros nos ', 'ellos se ', 'voh (te) ']

        self._PREP_LUGAR = self.PREP_LUGAR()
        self._PREP_CAUSALIDAD = self.PREP_CAUSA()
        
        self._ADVERBIO_PROXIMIDAD = ['aquí', 'acá']
        self._ADVERBIO_LEJANIA = ['allí', 'allá']
        self._ADVERBIO_INTERLOC = ['ahí']
        self._ADJET_DEM_PROXIM = ['este','esta', 'estos', 'estas']
        self._ADJET_DEM_LEJANIA = ['aquel', 'aquella','aquellos', 'aquellas']
        self._ADJET_DEM_INTERLOC = ['ese', 'esa', 'esos', 'esas']
        
        self._CONJ_SER = ['soy','eres', 'es', 'somos', 'son',
           'fui','fuiste','fue', 'fuimos','fueron',
            'jui','juiste','jue', 'juimos','jueron',
           'soi', 'eris','erih','erís','erai', 'eramos']
        
    def create_wn(self):
        _wn = ['wn', 'weon', 'weón', 'weona', 'aweonao', 'aweonah', 'wea', 'weá']
        hue = [x.replace('we','hue') for x in _wn[1:len(_wn)]]
        gue = [x.replace('we','gue') for x in _wn[1:len(_wn)]]
        return _wn + hue + gue

    def print_conjugar(self, conjugaciones, particula, tiempo):
        [print(conjugaciones[i] + particula + tiempo[i]) for i in range(len(tiempo))]

    def simplePresent(self, particula):
        presente_s = self.print_conjugar(self.conjugaciones, particula, self.presente_simple)
        return presente_s

    def simplePast(self, particula):
        pasado_s = self.print_conjugar(self.conjugaciones_simplepass, particula, self.pasado_simple)

    def simpleFuture(self, particula):
        pret_simpl = self.print_conjugar(self.conjugaciones_simplepret, particula, self.preterito_simple)
        
    def PREP_LUGAR(self):
        # https://www.spanish.cl/gramatica/preposiciones-de-lugar.htm
        PREP_LUGAR = ['al lado', 'alrededor', 'cerca', 'debajo', 'delante','dentro', 'detrás', 
                      'encima','enfrente', 'fuera','lejos']
        PREP_LUGAR = [x + ' de' for x in PREP_LUGAR]
        PREP_LUGAR = PREP_LUGAR + ['en', 'entre', 'sobre','junto a','frente a']
        return PREP_LUGAR
    
    def PREP_CAUSA(self):
        # https://www.ejemplode.com/12-clases_de_espanol/450-ejemplo_de_proposiciones_causales.html
        return ['por','porque', 'a causa de', 'puesto que','ya que','pues','debido a', 'toda vez que']
        
