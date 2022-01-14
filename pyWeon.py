import re
from textblob import TextBlob
from deep_translator import GoogleTranslator

class Wn:
    def __init__(self): 
        self._pwn = ['webe', 'weón', 'weon', 'aweo', 'wéa','wéas', 'weá','weás']
        self.conjugaciones = ['yo me ', 'tú te ', 'el se ', 'nosotros nos ', 'ellos se ', 'voh (te) ']
        self.presente_simple = ['o','as / ai' ,'a', 'amos', 'an', 'ai']
        self.conjugaciones_simplepass = ['yo me ', 'tú te ', 'el se ', 'nosotros nos ', 'ellos se ', 'voh (te)']
        self.pasado_simple = ['é','aste', 'ó', 'amos','aron','aste']
        self.preterito_simple = ['é', 'arás', 'ará','aremos', 'arán','ai']
        self.conjugaciones_simplepret = ['yo me ', 'tú te ', 'el se ', 'nosotros nos ', 'ellos se ', 'voh (te) ']

        #self._PREP_LUGAR = self.PREP_LUGAR()
        ##self._PREP_CAUSALIDAD = self.PREP_CAUSA()

        self._ADVERBIO_PROXIMIDAD = ['aquí', 'acá']
        self._ADVERBIO_LEJANIA = ['allí', 'allá']
        self._ADVERBIO_INTERLOC = ['ahí']

        self.pron_dem = ['éste','ése','ésta','ésa','éstos','ésos','éstas','ésas','ésto','éso',
                'aquél','aquélla','aquéllos','aquéllas','aquéllo']

        self.articulos = 'el,un,al,del,los,unos,la,una,las,unas,les,los'.split(',')

        self._conjugacion_SER = ['ser','soy','eres', 'es', 'somos', 'son',
           'fui','fuiste','fue', 'fuimos','fueron',
            'jui','juiste','jue', 'juimos','jueron',
           'soi', 'eris','erih','erís','erai', 'eramos']


    def lexicParser(self, L):
        #L = L.replace('ebia','ebe')
        L = L.lower()
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

        _L = L.split(' ')
        for index, x in enumerate(_L):
            pal = self.borraPuntuacion(x)
            if pal == 'weon' or pal == "wéon":
                _L[index] = "weón"
            if pal == 'wea' or pal== "weas":
                s = 's' if len(pal) == 4 else ''
                _L[index] = "weá" + s  #asumimos weá sobre wéa si no hay tildes.
            if 'awéon' in pal or 'aweón' in pal :
                _L[index] = "aweon"
            if len(pal) > 3 and "nah" in pal or 'náh' in pal:
                _L[index] = _L[index].replace('nah', 'ná')
                _L[index] = _L[index].replace('náh', 'ná')
        L = " ".join(_L)
        print("[chileno] -> %s"%(L))
        return L

    def F_split(self, L, P):
        F = []
        for p in P:
            if (p in L):
                ip = L.index(p)
                Ftemp  = L[0:ip]
                F.append(Ftemp)
                L = L[ip+len(p):]
            else:
                F.append(L)

        if (len(L) > 0):
            F.append(L)
        return F

    def rho(self, L):
        R = []
        particulas = self._pwn

        for x in L.split(' '):
            x = self.borraPuntuacion(x)
            if (len(x)>=3):
                if(len(x) == 3 and x in particulas ):
                    R.append(x)
                else:
                    test_p = x[0:4]
                    if (test_p in particulas):
                        R.append(x)
        return R

    def borraPuntuacion(self, x):
        return re.sub('[^a-záóíA-Z0-9]+', '', x)

    def esFraseNula(self, f):
        for x in f:
            if (x != ''):
                return False
        return True

    def getOmega(self, U, P, d):
        O = []
        for i in range(d):
            y_translate = self.deschilenizar(U[i],P[i])
            O.append(y_translate)
        return O

    def articulate(self, F, Omega):
        trad = F[0]
        #|F|>|O|>1
        for i in range(len(Omega)):
            y = Omega[i]
            if (y!=None):
                trad = trad + y

            if (i+1 < len(Omega)):
                trad = trad + F[i + 1]
            if (i == len(Omega) - 1 and len(F)>len(Omega) and len(F) > 0):
                trad = trad + F[-1]

        return trad

    def translate(self, _lambda, lang = "es"):
        L = self.lexicParser(_lambda)
        K = L.split(".")
        trad = ""

        for kappa in K:
            Pk = self.rho(kappa)
            if (len(Pk) == 0):
                trad = trad + kappa
            else:
                Fk = self.F_split(kappa, Pk)
                Uk = self.getUpsilon(Fk,Pk)
                #print(Uk)
                Ok = self.getOmega(Uk, Pk, len(Pk))
                #print(Ok)
                Ck = self.articulate(Fk,Ok)
                #print(Ck)
                trad = trad + Ck.capitalize() + "."

        to_translate = trad
        translated = GoogleTranslator(source='auto', target=lang).translate(to_translate)
        return translated

    def translateAndAnalize(self, _lambda):
        text = self.translate(_lambda, 'en')
        a = self.getAnalysis(text)
        print(text, a)
        return [text, a]

    def getUpsilon(self, F, P):
        U = []
        for index, pwn in enumerate(P):
            f = F[index]
            u = self.Upsilon(f, pwn)
            #print(f,pwn , u)
            U.append(u)
        return U

    def Upsilon(self, F, pwn):
        upsilon = []
        f = F.split(' ')
        f = [self.borraPuntuacion(x) for x in f]
        f = f[::-1]

        a = self.primerArticulo(f)
        b = self.primerPronombre(f)
        c = self.primerSerConjugado(f)
        u = [0,0,0]
        v = [a,b,c]
        #print(v,f,pwn)
        if (c > -1):
            c_gn = self.isSerConjugado(f[c], pwn)
            if (c_gn != False and c_gn != None):
                u = [0,0,1] + c_gn

        if (a >-1  and  a > b):
            a_gn = self.isArticuloDem(a, f[a], pwn)
            if (a_gn != False):
                u = [1,0,0] + a_gn
        if (b >-1  and  b > a):
            b_gn = self.isPronomDemost(f[b], pwn)
            if (b_gn != False):
                u = [0,1,0] + b_gn

        if (-1< a < c):
            u = [1,0,0] + u[3:]
        if (-1< b < c):
            u = [0,1,0] + u[3:]

        if (u == [0,0,0] or self.esFraseNula(f)):
            #print('es frase NULA:',f,pwn)
            if (pwn == 'weás'):
                u = [0, 1, 0, 3, 1] #
            if (pwn == 'weá'):
                u = [0, 1, 0, 3, 0] # estúpido
            if (pwn in 'weón aweonao'.split(' ')):
                u =  [1, 0, 0, 2, 0] # estúpido
            if (pwn in 'weones aweonaos'.split(' ')):
                u =  [1, 0, 0, 2, 1] # estúpido
            if (pwn in 'weona aweoná'.split(' ')):
                u = [1, 0, 0, 3, 0] # estúpida
            if (pwn in 'weonas aweonás'.split(' ')):
                u = [1, 0, 0, 3, 1] # estúpido
        return u

    def primerPronombre(self, f):
        for i in range(len(f)):
            if (f[i] != ''):
                e = f[i]
                if (e[0] == 'e'):
                    e = 'é' + e[1:]
                if ( e in self.pron_dem):
                    return i
        return -1

    def primerArticulo(self, f):
        for i in range(len(f)):
            if (f[i] in self.articulos):
                return i
        return -1

    def primerSerConjugado(self, f):
        for i in range(len(f)):
            if (f[i] in self._conjugacion_SER):
                return i
        return -1


    def isArticuloDem(self, i, x, pwn):

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
            return [2,0]
        if (x in 'los unos'.split(' ') and pwn in "weones aweonaos".split(' ')):
            return [0,1]
        if (x in 'los unos'.split(' ') and pwn =="wéas"):
            return [2,1]
        if (x == 'les'):
            if (i == 0):
                return 'FALTA ADJETIVO INTERMEDIO*'
            else:
                if (pwn in 'weón aweonaos weones wéas'.split(' ')):
                    return [2, 1]
                if (pwn in 'weonas aweonás'.split(' ')):
                    return [3, 1]

        return False


    def isPronomDemost(self, x, pwn):

        if(x[0]=='e'):
            x = 'é' + x[1:]
        if(x[0:4]=='aque'):
            x = 'aqué' + x[4:]

        if (x not in self.pron_dem):
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
            return [2,0]
        if (x in 'ésa aquélla') and pwn in 'weá'.split():
            return [3,0]
        if (x == 'aquéllas') and pwn in 'weás'.split():
            return [3,1]
        if (x == 'aquéllos') and pwn in 'wéas'.split():
            return [2,1]
        return False


    def isSerConjugado(self, x, pwn):
        # como es verbo conjugado,, solo se queda con el género neutro del pwn
        if (x not in self._conjugacion_SER):
            return False
        if (pwn in ['weá']):
            return [3,0]
        if (pwn in ['weás']):
            return [3,1]
        if (pwn in ['weón', 'aweonao', 'wéa']):
            return [2,0]
        if (pwn in ['wéas']):
            return [2,1]
        if (pwn in ['weones', 'aweonaos']):
            return [2,1]
        if (pwn in ['weona, aweoná']):
            return[3,0]
        if (pwn in ['weonas, aweonás']):
            return[3,1]



    def deschilenizar(self, u,p):

        if ( p == "weá"):
            if (u == [1, 0, 0, 0, 0] ):
                return "#10000weá"
            if (u == [1, 0, 0, 0, 1] ):
                return "#10001weá"
            if (u == [1, 0, 0, 1, 0] ):
                return "#10010weá"
            if (u == [1, 0, 0, 1, 1] ):
                return "#10011weá"
            if (u == [1, 0, 0, 2, 0] ):
                return "asunto"
            if (u == [1, 0, 0, 2, 1] ):
                return "asuntos"
            if (u == [1, 0, 0, 3, 0] ):
                return "situación"
            if (u == [1, 0, 0, 3, 1] ):
                return "cosas*"

            if (u == [0, 1, 0, 0, 0] ):
                return "#01001weá"
            if (u == [0, 1, 0, 0, 1] ):
                return "#01010weá"
            if (u == [0, 1, 0, 1, 0] ):
                return "#01010weá"
            if (u == [0, 1, 0, 1, 1] ):
                return "#01011weá"
            if (u == [0, 1, 0, 2, 0] ):
                return "cosa"
            if (u == [0, 1, 0, 2, 1] ):
                return "cosas"
            if (u == [0, 1, 0, 3, 0] ):
                return "cosa"
            if (u == [0, 1, 0, 3, 1] ):
                return "cosas"


            if (u == [0, 0, 1, 2, 0] ):
                return "#00120weá"
            if (u == [0, 0, 1, 2, 1] ):
                return "#00121weá"
            if (u == [0, 0, 1, 3, 0] ):
                return "definición"
            if (u == [0, 0, 1, 3, 1] ):
                return "#00131weá"

        if ( p == "weás"):
            if (u == [1, 0, 0, 0, 0] ):
                return "#10000weás"
            if (u == [1, 0, 0, 0, 1] ):
                return "#10001weás"
            if (u == [1, 0, 0, 1, 0] ):
                return "#10010weás"
            if (u == [1, 0, 0, 1, 1] ):
                return "#10011weás"
            if (u == [1, 0, 0, 2, 0] ):
                return "tontera"
            if (u == [1, 0, 0, 2, 1] ):
                return "cizañerías"
            if (u == [1, 0, 0, 3, 0] ):
                return "tontería"
            if (u == [1, 0, 0, 3, 1] ):
                return "tonterías"

            if (u == [0, 1, 0, 0, 0] ):
                return "#01001weás"
            if (u == [0, 1, 0, 0, 1] ):
                return "#01010weás"
            if (u == [0, 1, 0, 1, 0] ):
                return "#01010weás"
            if (u == [0, 1, 0, 1, 1] ):
                return "#01011weás"
            if (u == [0, 1, 0, 2, 0] ):
                return "#01020weás"
            if (u == [0, 1, 0, 2, 1] ):
                return "#01021weás"
            if (u == [0, 1, 0, 3, 0] ):
                return "tontería"
            if (u == [0, 1, 0, 3, 1] ):
                return "boberías"


            if (u == [0, 0, 1, 2, 0] ):
                return "#00120weás"
            if (u == [0, 0, 1, 2, 1] ):
                return "#00121weás"
            if (u == [0, 0, 1, 3, 0] ):
                return "#00130weás"
            if (u == [0, 0, 1, 3, 1] ):
                return "#00131weás"


        if ( p == "wéas"):
            if (u == [1, 0, 0, 0, 0] ):
                return "#10000wéás"
            if (u == [1, 0, 0, 0, 1] ):
                return "#10001wéás"
            if (u == [1, 0, 0, 1, 0] ):
                return "#10010wéás"
            if (u == [1, 0, 0, 1, 1] ):
                return "#10011wéás"
            if (u == [1, 0, 0, 2, 0] ):
                return "tontera"
            if (u == [1, 0, 0, 2, 1] ):
                return "cizañerías"
            if (u == [1, 0, 0, 3, 0] ):
                return "#10030wéás"
            if (u == [1, 0, 0, 3, 1] ):
                return "#10031wéás"

            if (u == [0, 1, 0, 0, 0] ):
                return "#01001wéás"
            if (u == [0, 1, 0, 0, 1] ):
                return "#01010wéás"
            if (u == [0, 1, 0, 1, 0] ):
                return "#01010wéás"
            if (u == [0, 1, 0, 1, 1] ):
                return "#01011wéás"
            if (u == [0, 1, 0, 2, 0] ):
                return "#01020wéás"
            if (u == [0, 1, 0, 2, 1] ):
                return "#01021wéás"
            if (u == [0, 1, 0, 3, 0] ):
                return "#01030wéás"
            if (u == [0, 1, 0, 3, 1] ):
                return "#01031wéás"


            if (u == [0, 0, 1, 2, 0] ):
                return "#00120wéás"
            if (u == [0, 0, 1, 2, 1] ):
                return "#00121wéás"
            if (u == [0, 0, 1, 3, 0] ):
                return "#00130wéas"
            if (u == [0, 0, 1, 3, 1] ):
                return "#00131wéas"

        if ( p == "aweonao"):
            if (u == [1, 0, 0, 0, 0] ):
                return "imbécil"
            if (u == [1, 0, 0, 0, 1] ):
                return "imbéciles"
            if (u == [1, 0, 0, 1, 0] ):
                return "descerebrado"
            if (u == [1, 0, 0, 1, 1] ):
                return "malnacidos"
            if (u == [1, 0, 0, 2, 0] ):
                return ",subnormal"
            if (u == [1, 0, 0, 2, 1] ):
                return ",subnormales"
            if (u == [1, 0, 0, 3, 0] ):
                return "tontona"
            if (u == [1, 0, 0, 3, 1] ):
                return "destartalado!"

            if (u == [0, 1, 0, 0, 0] ):
                return "inútil"
            if (u == [0, 1, 0, 0, 1] ):
                return "sucio bueno para nada"
            if (u == [0, 1, 0, 1, 0] ):
                return "atorrante"
            if (u == [0, 1, 0, 1, 1] ):
                return "enfermo"
            if (u == [0, 1, 0, 2, 0] ):
                return "leso de mierda"
            if (u == [0, 1, 0, 2, 1] ):
                return "idiota"
            if (u == [0, 1, 0, 3, 0] ):
                return "avíspate!"
            if (u == [0, 1, 0, 3, 1] ):
                return "enfermo"

            if (u == [0, 0, 1, 2, 0] ):
                return "estúpido!"
            if (u == [0, 0, 1, 2, 1] ):
                return "estúpidos!"
            if (u == [0, 0, 1, 3, 0] ):
                return "!100130aweonao"
            if (u == [0, 0, 1, 3, 1] ):
                return "!00131aweonao"

        if ( p == "aweoná"):
            if (u == [1, 0, 0, 0, 0] ):
                return "zorra malparida"
            if (u == [1, 0, 0, 0, 1] ):
                return "malparida"
            if (u == [1, 0, 0, 1, 0] ):
                return "descerebrada"
            if (u == [1, 0, 0, 1, 1] ):
                return "descerebradas"
            if (u == [1, 0, 0, 2, 0] ):
                return "acéfala"
            if (u == [1, 0, 0, 2, 1] ):
                return "acéfalas"
            if (u == [1, 0, 0, 3, 0] ):
                return "tontona!"
            if (u == [1, 0, 0, 3, 1] ):
                return "destartalada!"

            if (u == [0, 1, 0, 0, 0] ):
                return "niña"
            if (u == [0, 1, 0, 0, 1] ):
                return "sucia bueno para nada"
            if (u == [0, 1, 0, 1, 0] ):
                return "loca"
            if (u == [0, 1, 0, 1, 1] ):
                return "enferma"
            if (u == [0, 1, 0, 2, 0] ):
                return "lesa de mierda"
            if (u == [0, 1, 0, 2, 1] ):
                return "lesa"
            if (u == [0, 1, 0, 3, 0] ):
                return "avíspate!"
            if (u == [0, 1, 0, 3, 1] ):
                return "enferma"

            if (u == [0, 0, 1, 2, 0] ):
                return "estúpida!"
            if (u == [0, 0, 1, 2, 1] ):
                return "estúpidas!"
            if (u == [0, 0, 1, 3, 0] ):
                return "!100130aweoná"
            if (u == [0, 0, 1, 3, 1] ):
                return "!00131aweoná"

        if ( p == "wéa"):
            if (u == [1, 0, 0, 0, 0] ):
                return "tonto"
            if (u == [1, 0, 0, 0, 1] ):
                return "tontos"
            if (u == [1, 0, 0, 1, 0] ):
                return "mamona"
            if (u == [1, 0, 0, 1, 1] ):
                return "raritas"
            if (u == [1, 0, 0, 2, 0] ):
                return "jetón"
            if (u == [1, 0, 0, 2, 1] ):
                return "fracasados"
            if (u == [1, 0, 0, 3, 0] ):
                return "#10030wéá"
            if (u == [1, 0, 0, 3, 1] ):
                return "#10031wéá"

            if (u == [0, 1, 0, 0, 0] ):
                return "#01001wéá"
            if (u == [0, 1, 0, 0, 1] ):
                return "#01010wéá"
            if (u == [0, 1, 0, 1, 0] ):
                return "#01010wéá"
            if (u == [0, 1, 0, 1, 1] ):
                return "#01011wéá"
            if (u == [0, 1, 0, 2, 0] ):
                return "#01020wéá"
            if (u == [0, 1, 0, 2, 1] ):
                return "#01021wéá"
            if (u == [0, 1, 0, 3, 0] ):
                return "#01030wéá"
            if (u == [0, 1, 0, 3, 1] ):
                return "#01031wéá"


            if (u == [0, 0, 1, 2, 0] ):
                return "#00120wéá"
            if (u == [0, 0, 1, 2, 1] ):
                return "#00121wéá"
            if (u == [0, 0, 1, 3, 0] ):
                return "#00130wéa"
            if (u == [0, 0, 1, 3, 1] ):
                return "#00131wéa"

        if ( p == "weón"):
            if (u == [1, 0, 0, 0, 0] ):
                return "bobo"
            if (u == [1, 0, 0, 0, 1] ):
                return "tarados"
            if (u == [1, 0, 0, 2, 0] ):
                return "tipejo"
            if (u == [1, 0, 0, 2, 1] ):
                return "imbéciles!"
            if (u == [0, 1, 0, 0, 0] ):
                return "zopenco"
            if (u == [0, 1, 0, 0, 1] ):
                return "malditos buenos para nada"
            if (u == [0, 1, 0, 2, 0] ):
                return "hijo de perra"
            if (u == [0, 1, 0, 2, 1] ):
                return "hijos de perra"
            if (u == [0, 0, 1, 2, 0] ):
                return "inútil"
            if (u == [0, 0, 1, 2, 1] ):
                return "inútiles"


            else:
                #weon sería solo una muletilla.
                return 'maldita sea!!'

        if ( p == "weona"):
            if (u == [1, 0, 0, 0, 0] ):
                return "amiga!"
            if (u == [1, 0, 0, 0, 1] ):
                return "amiga"
            if (u == [1, 0, 0, 1, 0] ):
                return "tipeja"
            if (u == [1, 0, 0, 1, 1] ):
                return "mujeres de mala muerte"
            if (u == [1, 0, 0, 2, 0] ):
                return "amiga"
            if (u == [1, 0, 0, 2, 1] ):
                return "amiga"
            if (u == [1, 0, 0, 3, 0] ):
                return "niña!"
            if (u == [1, 0, 0, 3, 1] ):
                return "lesas"

            if (u == [0, 1, 0, 0, 0] ):
                return "boba"
            if (u == [0, 1, 0, 0, 1] ):
                return "zorras"
            if (u == [0, 1, 0, 1, 0] ):
                return "trepadora"
            if (u == [0, 1, 0, 1, 1] ):
                return "culisueltas"
            if (u == [0, 1, 0, 2, 0] ):
                return "amiga!"
            if (u == [0, 1, 0, 2, 1] ):
                return "amiga?"
            if (u == [0, 1, 0, 3, 0] ):
                return "amiga#"
            if (u == [0, 1, 0, 3, 1] ):
                return "chiquilla"


            if (u == [0, 0, 1, 2, 0] ):
                return "estúpido"
            if (u == [0, 0, 1, 2, 1] ):
                return "estúpidos"
            if (u == [0, 0, 1, 3, 0] ):
                return "ridícula"
            if (u == [0, 0, 1, 3, 1] ):
                return "ridículas"

        if ( p == "weones"):
            if (u == [1, 0, 0, 0, 0] ):
                return "giles"
            if (u == [1, 0, 0, 0, 1] ):
                return "pelagatos"
            if (u == [1, 0, 0, 1, 0] ):
                return ", #10010wns"
            if (u == [1, 0, 0, 1, 1] ):
                return "#10011wns"
            if (u == [1, 0, 0, 2, 0] ):
                return "lerdos"
            if (u == [1, 0, 0, 2, 1] ):
                return "tipejos"
            if (u == [1, 0, 0, 3, 0] ):
                return "bastardos"
            if (u == [1, 0, 0, 3, 1] ):
                return "#10031wns"

            if (u == [0, 1, 0, 0, 0] ):
                return "#01000wns"
            if (u == [0, 1, 0, 0, 1] ):
                return "imbéciles"
            if (u == [0, 1, 0, 1, 0] ):
                return "inútiles"
            if (u == [0, 1, 0, 1, 1] ):
                return "#01011wns"
            if (u == [0, 1, 0, 2, 0] ):
                return "pendejos"
            if (u == [0, 1, 0, 2, 1] ):
                return "pendejos"
            if (u == [0, 1, 0, 3, 0] ):
                return "feos"
            if (u == [0, 1, 0, 3, 1] ):
                return "sucios"
            if (u == [0, 0, 1, 2, 0] ):
                return "estúpidos"
            if (u == [0, 0, 1, 2, 1] ):
                return "malolientes"


    # function to calculate subjectivity
    def getSubjectivity(self, phrase):
        return TextBlob(phrase).sentiment.subjectivity

    # function to calculate polarity
    def getPolarity(self, phrase):
        return TextBlob(phrase).sentiment.polarity

    # function to analyze the polarity
    def getAnalysis(self, text="", score=0):
        if (len(text) > 0):
            score = self.getPolarity(text)
        s = "%2.2f%% "%(abs(100*score))
        if score < 0:
            return s + 'Negative'
        elif score == 0:
            return 'Neutral'
        else:
            return 'Positive'

    def getSentimentAnalysis(self, text):
        sc = self.getSubjectivity(text)
        p  = self.getPolarity(text)
        a = self.getAnalysis('', p)
        return [sc, p, a]
