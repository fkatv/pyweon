<<<<<<< HEAD
# PyWeon, weones everywhere...

####  

**[alfa v0.0.2 - 10 Enero 2021]**

PyWeon es un módulo que traduce frases chilenas con weón y derivados, según la interpretación gramatical de sus palabras.

Dentro del directorio `/learn` se intenta enseñar a personas no-chilenas a usar y entender oraciones con uso de partículas de **weón** y sus variantes, explicando de forma fácil y a través de lenguaje linguístico formal  a las gramáticas que dan sentido a las oraciones que contengan la palabra weón.

La clase **Wn** de *pyWeon* puede ser usado para traducir las frases con partículas de weón y realiza **sentiment analysis** *(usando TextBlob)* a la traducción. Por ahora, el módulo no distingue más modismos chilenos.

## Requisitos

* Python 3.7+
* pip install **deep_translator**
* pip install **TextBlob**

## Modo de uso:

```
from pyWeon import Wn
wn = Wn()
L = "una frase con alguna weá aweoná"
T = wn.translate(L, lang="es")
print(T) # spanish translate

T2 = wn.translateAndAnalize(L)
print(T2) # english translate & sentiment analysis applied.
```
## Avances

- Version alpha v0.0.2
> - Reconoce varias frases con ciertas combinaciones de weón, weá, aweonao, aweoná, weás.
> - Integración de módulo de idioma y sentiment analysis

=======
# Pyweon, weon everywhere...
#### 
Pyweon es un esbozo que intenta enseñar a personas no chilenas a entender como se expresan los chilenos en la cotidianeidad, usando el modismo **weón** y sus variantes.

Se intentará explicar con lenguaje linguístico formal y computacional a las gramáticas que generan las oraciones que contengan la palabra weón.

Te enseñaré a leer definiciones formales que se programarán para poder ser empleados y exportados a tus apps.
>>>>>>> 73bd24e817a76fcb414754b1f299a98d76463685

De Chile pal mundo.

Fkatv.