#RSF KOBOL EXPANDER 2 - VCO dataset

Los parámetros variables que proporciona el VCO pueden generar un gran número de señales, lo que dificulta realizar un muestreo continuo. Por ello se muestreo la salida de los dos vcos realizando la discretización de diversas configuraciones de los parámetros de `frecuencia` y `forma de onda` (sin considerar el parámetro volumen el cual su valor fue máximo (10) en todo momento).

Una de las dificultades en la captación de muestras es la variabilidad que ofrecen los controles del módulo VCO, aumentando considerablemente la complejidad para definir con exactitud los valores de cada parámetro. Por este motivo se hizo uso de la fuente de alimentación PROMAX FAC-363B para controlar el modulo mediante una señal de voltage de contro (CV) que se destino exclusivamente al parámetro de la frecuencia, utilizando la entrada de tensión VCO Frequency.

Los muestreos tienen una duración de 2s aproximadamente, estableciendo una forma de onda y modificando los valores de la frecuencia en incrementos de 0.5V (en todo momento con la configuración del control manual de frecuencia en su valor mínimo, 10Hz).

Este proceso se realizo para todas las formas de onda definidas en la imagen `metadata/waveforms.png`.

Asi hay disponibles 21 muestras de frecuencias por forma de onda. En total son 273 archivos en formato wav (21 frecuencias x 11 formas de onda) para cada VCO, es decir 546 archivos en total.

Estas muestras se almacenan en dos carpetas vco1 y vco2 que a su vez contienen subcarpetas para cada forma de onda.

###Nomenclatura
La nomenclatura definida para las muestras grabadas es la siguiente,

*vco[NumVCO]_Vin_waveform.wav*

donde,

* **NumVCO**: VCO muestreado, puede ser 1 o 2.
* **Vin**: voltaje introducido en la entrada de la frecuencia del Kobol.
* **waveform**: Forma de onda de la señal generada (pulse, sawtooth, sawtooth-square, square, square-pulse, triangular, triangular-sawtooth).
