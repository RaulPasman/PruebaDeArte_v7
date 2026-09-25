# Diseño funcional

## Duelo
Cada duelo presenta dos obras sin información histórica. El usuario puede elegir A, B, Ambas o Ninguna. No existe botón de retroceso.

Los primeros 16 duelos son fijos. Los últimos 8 se seleccionan adaptativamente buscando contraste sobre ejes con menor evidencia y evitando repetir obras y artistas innecesariamente.

## Pausas
Cada cuatro duelos aparece una pausa editorial. Si corresponde, después de la pausa aparece una pregunta breve. El contenido contextual de la pausa se limita a una observación accesible sobre la obra.

## Scoring
Ocho ejes internos:
- Abstracto ↔ Figurativo
- Estructurado ↔ Espontáneo
- Sereno ↔ Expresivo
- Contenido ↔ Saturado
- Plano ↔ Material
- Cotidiano ↔ Imaginario
- Íntimo ↔ Dominante
- Transparente ↔ Conceptual

Elección directa: peso 1.00 / 1.05 / 1.10 por tramo del recorrido.
Ambas: peso 0.35.
Ninguna: no desplaza el centro del perfil; se usa principalmente para evitar recomendaciones demasiado parecidas a lo rechazado.
Preguntas: peso definido por pregunta.

La confianza de cada eje considera cantidad de evidencia y consistencia de las señales. Las barras visibles no muestran números.

## Perfil
Se calcula una distancia ponderada entre el vector del usuario y los 10 perfiles. El perfil P10, Explorador sin fronteras, es especial: se activa sólo cuando existe baja concentración, suficiente amplitud y diversidad de familias.

El resultado muestra un perfil principal y hasta tres matices cercanos. No se presentan etiquetas secundarias como diagnósticos.

## Selección y recomendaciones
Mi selección contiene obras ya vistas y representativas, con diversidad de familias y un umbral mínimo de compatibilidad.

Para seguir explorando combina compatibilidad y expansión moderada. Las obras muy parecidas a pares rechazados reciben una penalización.

## Ruta
La ruta contiene cinco pasos. Cuando es posible parte de un artista ya descubierto y muestra otras obras de ese artista; después abre el recorrido hacia obras nuevas. Termina con una pregunta abierta que se guarda como reflexión cualitativa.
