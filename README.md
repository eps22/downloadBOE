# downloadBOE
Python script based on selenium for downloading the BOE ('Boletín Oficial del Estado de España) publications based on a string and/or dates interval.

Arguments:

string=sys.argv[1] -> texto a buscar
field=sys.argv[2] -> en qué campo debe buscarse el texto ('titulo' o 'texto')
date1=sys.argv[3] -> fecha 1 -límite inferior-
date2=sys.argv[4] -> fecha 2 -límite superior-
dirtosave=sys.argv[5] -> directorio en el que guardar los resultados de la búsqueda

Ejemplo: Busca las publicaciones en las que aparece en el texto la palabra 'tropicales'.

python3 -W ignore downloadBOE.py 'tropicales' 'texto' '~/Downloads/boe'
