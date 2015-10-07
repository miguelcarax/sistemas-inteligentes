# sistemas-inteligentes
Sistemas Inteligentes

·SAX en vez de DOM
·Nodo -> Identificador y Coordenadas(latitud, longitud)
·En un primer lugar tenemos que analizar primero las calles y luego los nodos.
·Las callas que me valen tienen una etiqueta "highway" con los valores {trunk(nacionales),                             Residential, pedastrian(peatonales)}.
·Grafo dirigido -> De nodo a nodo siempre habrá dos arcos.
·De una calle obtenemos los nodos que la componen.
·Arco -> Coste = Longitud(m) -> Cálculo mediante proyección de mercator.
·Realizar 2 pasadas:
    1. Para Realizar el grafo.
    2. Completar la información incompleta.
·Jugar con la persistencia. Una vez realizado el grafo salvaguardarlo para no tener que volver a construirlo.
·ID -> {(nodo, coste), (nodo, coste), ...}
·Las ID de los nodos están contenidos en una tabla has. Se crea un diccionario de ID.
