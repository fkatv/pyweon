#
#    pyweon package
#    Fabián Catalán V. - github.com/fkatv
#    Chile, Enero 2022
#
import re 

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
        
        self.PRONOMBRES_DEMOSTRATIVOS = "éste | ese | aquel | ésta | esa | aquella | éstos | esos | aquellos | éstas | esas | aquellas | ésto | eso | aquéllo".split(' | ')
        
        self.articulos = 'el,un,al,del,los,unos,la,una,las,unas,les,los'.split(',')

        self._CONJ_SER = ['soy','eres', 'es', 'somos', 'son',
           'fui','fuiste','fue', 'fuimos','fueron',
            'jui','juiste','jue', 'juimos','jueron',
           'soi', 'eris','erih','erís','erai', 'eramos']

    def nand (self,s1,s2):
        return not(s1 and s2)
    
    def esPlural(self, frase, articulos, pronom, p):
        sa = sum(articulos)
        sb = sum(pronom)
        nand = self.nand(sa > 0, sb > 0)
        
        if (nand == False):
            return 'ERROR a y b'
        index_a = 0
        index_b = 0
        if (True in articulos):
            index_a = articulos.index(True)
        
        if (True in pronom):
            index_b = pronom.index(True)
            
        if (sa == sb ==0):
            test = p[-2:]
            if('webe' in p):
                return 'VERBO WEBEAR'
            if("as" in test or "es" in test):
                return 'PLURAL'
            else:
                return 'SINGLE'
        
        test = ''
        index = index_b
        if (index_a > index_b):
            index = index_a
            
        test = frase[index][-2:]
        if("as" in test or "os" in test):
            return 'PLURAL'
        else:
            return 'SINGLE'
    
    def create_wn(self):
        _wn = ['wn', 'weon', 'weón', 'weona', 'aweonao', 'aweonah', 'wea', 'weá']
        hue = [x.replace('we','hue') for x in _wn[1:len(_wn)]]
        gue = [x.replace('we','gue') for x in _wn[1:len(_wn)]]
        return _wn + hue + gue
    
    def lexicParser(self, L):
        #L = L.replace('ebia','ebe')
        L = L.replace('ahueon', 'aweon')
        L = L.replace('agueon', 'aweon')
        L = L.replace('wueo', 'weo')
        L = L.replace('wueó', 'weó')
        L = L.replace('hueo', 'weo')
        L = L.replace('hueó', 'weó')
        L = L.replace('gueo', 'weo')
        L = L.replace('gueó', 'weó')
        L = L.replace('huebo', 'weo')
        L = L.replace('huebó', 'weó')
        L = L.replace('guebo', 'weo')
        L = L.replace('guebó', 'weó')
        L = L.replace('huebe', 'webe')
        L = L.replace('guebe', 'webea')
        L = L.replace('huebe', 'webea')
        L = L.replace('webi', 'webe')
        L = L.replace('huebi', 'webe')
        L = L.replace('guebi', 'webe')
       
        return L
    
    def F_split(self, L, P):
        F = []
        for p in P:
            ip = L.index(p)
            Ftemp  = L[0:ip]
            F.append(Ftemp)
            L = L.replace(Ftemp+p, '')
        
        if (len(L) > 0):
            F.append(L)
        return F
    
    def rho(self, L):
        R = []
        particulas ="weon weón webe aweo weas weás wéas"
        
        for x in L:
            if (len(x)>=3):
                if(len(x) == 3):
                    if ('wea' in x):
                        R.append('wea')
                    if('weá' in x):
                        R.append('weá')
                else:
                    test_p = x[0:4]
                    if (test_p in particulas):
                        x = re.sub('[^a-záóíA-Z]+', '', x)
                        R.append(x)
        return R
    
    def Upsilon(self, F, P):
        upsilon = []
        for i in range(len(P)):
            f = F[i].split(' ')[::-1]
            p = P[i]
            a = self.getArticulos(f)
            b = self.getPronombres(f)
            #adj = self.esAdjetivo(f)
            #print(f,a,b)
            n = self.esPlural(f, a, b, p)
            g = 'neutro**'
            u = [sum(a),sum(b),g,n,p]
            upsilon.append(u)
            print(upsilon)
        
        return upsilon
    
    def getArticulos(self, f):
        return [ self.esArticulo(x.lower()) for x in f ]
    
    def getPronombres(self, f):
        return [ self.esPRONOMBRE_DEM(x.lower()) for x in f ]
        
    def esPRONOMBRE_DEM(self, p):
        return p in self.PRONOMBRES_DEMOSTRATIVOS
    
    def esArticulo(self, p):
        return p in self.articulos
    
    def comprobarLexico(self, a, b):
        r1 = True in a
        r2 = True in b
        return nand(r1,r2)

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
    
    def esAdjetivo(self, frase):
        L = frase.split(' ')
        for x in L:
            if (x.lower() in self._CONJ_SER):
                return True
        return False

    def desaweonizar(self, frase):
        frase = frase.replace('aweonao','horrible')
        frase = frase.replace('aweona','horrible')
        return frase
    
    def isArticuloDem(self, x, pwn):
        
        if (x not in self.articulos):
            return False

        if (x in 'la una'.split(' ') and pwn in "weona aweoná".split(' ')):
            return [1,0]
        if (x in 'las unas'.split(' ') and pwn in "weonas aweonás".split(' ')):
            return [1,1]
        if (x in 'la una'.split(' ') and pwn =="weá".split(' ')):
            return [2,0]
        if (x in 'las unas'.split(' ') and pwn == "weás".split(' ')):
            return [2,1]
        if (x in 'el un al del'.split(' ') and pwn in "weón aweonao".split(' ')):
            return [0,0]
        if (x in 'el un al del'.split(' ') and pwn in "wéa wéas".split(' ')):
            return [3,0]
        if (x in 'los unos'.split(' ') and pwn in "weones aweonaos".split(' ')):
            return [0,1]
        if (x in 'los unos'.split(' ') and pwn =="wéas"):
            return [3,1]
        if (x == 'les'):
            return 'FALTA ADJETIVO INTERMEDIO*'

        return False   
                                                                  
                                                                  
    def isPronomDemost(self, x, pwn):
        pron_dem = ['éste','ése','ésta','ésa','éstos','ésos','éstas','ésas','ésto','éso',
                'aquél','aquélla','aquéllos','aquéllas','aquéllo']

        if(x[0]=='e'):
            x = 'é' + x[1:]
        if(x[0:4]=='aque'):
            x = 'aqué' + x[4:]

        if (x not in pron_dem):
            return False

        if x in 'éste ése aquél'.split(' ') and pwn in 'weón aweonao'.split():
            return [0,0]
        if x in 'ésta ésa'.split(' ') and pwn in 'weona aweoná'.split():
            return [1,0]
        if x in 'éstos ésos aquéllos'.split(' ') and pwn in 'weones aweonaos'.split():
            return [0,1]
        if x in 'éstas ésas'.split(' ') and pwn in 'weonas aweonás'.split():
            return [1,1]
        if x in 'ésto éso aquéllo'.split(' ') and pwn in 'weón wéa aweonao'.split():
            return [3,0]
        if (x == 'aquélla') and pwn in 'weá'.split():
            return [2,0]
        if (x == 'aquéllas') and pwn in 'weás'.split():
            return [2,1]
        if (x == 'aquéllos') and pwn in 'wéas'.split():
            return [3,1]
        return False

    def reemplazar_particulas(self, kappa):
        reemplazo = []
        for i,frase_kappa in enumerate(kappa):
            if(len(frase_kappa)>1):
                if self.esAdjetivo(frase_kappa):
                    reemplazo.append('estúpido')
                else:
                    reemplazo.append('amigo')
            else:
                reemplazo.append('amiguito')
        return reemplazo
                                                                  
                                                                  
                                                                  
