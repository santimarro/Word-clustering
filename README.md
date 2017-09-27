# Informe Clustering


## Introducción

En este informe se explicará los procesos realizados para clusterizar un corpus determinado en español.

El proceso se divide en varias etapas:
  - Preprocesamiento del corpus.
  - Parseo del mismo.
  - Creación de features.
  - Vectorizado de palabras.
  - Clusterizacion.
  
### Herramientas utilizadas
  - Para el parseo del corpus se utilizó la libreria _SpaCy_, la cual nos provee formas de preprocesar,
  tokenizar y analizar caracteristicas semánticas y sintácticas del mismo.
  
  - Para el vectorizado y clusterizado se utilizó la libreria Scikit Learn.

### Preprocesamiento del corpus
  Como corpus se utilizó el del diario la voz, el cual contiene 400000 lineas de texto de noticias. 
  Para su preprocesamiento, simplemente se extrajo los caracteres no relevantes para nuestro uso, como 
  por ejemplo _'%'_, _'#'_, _'&'_, etc. Se conservaron las letras y las distintas puntuaciones.
  
  Debido a que la libreria _SpaCy_ nos provee tokenización y detección de _stopwords_ automáticamente,
  no se lo implementó por separado.
  

### Parseo del corpus
  Para el parseo del corpus se utilizó la libreria _SpaCy_, donde primero se cargó el modelo de _español_
  y luego se le proveyó el corpus preprocesado.
  Esto nos provee un objeto tipo _Doc_, el cual posee todo el corpus tokenizado, junto a su información 
  sintáctica y semántica que el mismo puede proveer.
  A partir de esta información, se procedió a armar el diccionario de features de las palabras.
  
### Diccionario de features
  Para la creación del diccionario de features, tomando la información proveida por la libreria _SpaCy_
  se tuvieron en consideración distintas caracteristicas.
  Por cada token se utilizó:
    - Si el token está en minusculas.
    - Su pos tagging (Coarse grained tagging).
    - Su tag (Fine grained tagging)
    - El token anterior en la oración.
    - El pos tagging del token anterior.
    - El token siguiente en la oración.
    - El pos tagging del token siguiente.
    - Se implementaron triplas de dependencias con formato conll.

### Vectorizado de palabras
  Para el vectorizado de las palabras se utilizó _Dictvectorizer_ el cual nos genera la matriz
  de features necesaria para realizar el clusterizado. 
  Luego de generar la matriz, se procedió a reducir las dimensiones de la misma utilizando LSA.
  

### Clusterización

  El clusterizado se utilizó la versión del algoritmo _KMeans_ provisto por _Scikit Learn_, donde se utilizaron
  los siguientes parametros:
    - Cantidad de iteraciones: 
    - Cantidad de seeds:
    - Cantidad de clusters: Entre 25 y 100, dependiendo del experimento?.
  
  A partir de estos parametros, se ejecutó el algoritmo de _KMeans_ y se obtuvo los clusters a los cuales pertenece
  cada palabra.

    
    
    
    
    
    




  
 
  
  
