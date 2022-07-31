import numpy
from sklearn.neural_network import MLPClassifier
from sklearn import metrics

def display(T):
    print(' '+T[0]+' '+'|'+' '+T[1]+' '+'|'+' '+T[2]+' ')
    print('-----------')
    print(' '+T[3]+' '+'|'+' '+T[4]+' '+'|'+' '+T[5]+' ')    
    print('-----------')
    print(' '+T[6]+' '+'|'+' '+T[7]+' '+'|'+' '+T[8]+' ')

def tablero_esta_lleno(T):
    if T.count(' ') > 0:
        return False
    else:
        return True

def espacio_esta_libre(T,pos):
    if T[pos] == ' ':
        return True
    else:
        return False

def es_ganador(T, s):
    return ((T[0]==s and T[1]==s and T[2]==s) or
            (T[3]==s and T[4]==s and T[5]==s) or
            (T[6]==s and T[7]==s and T[8]==s) or
            (T[0]==s and T[3]==s and T[6]==s) or
            (T[1]==s and T[4]==s and T[7]==s) or
            (T[2]==s and T[5]==s and T[8]==s) or
            (T[0]==s and T[4]==s and T[8]==s) or
            (T[2]==s and T[4]==s and T[6]==s))

def juega_x(T): 
    buscar = True
    while buscar and not tablero_esta_lleno(T):
        pos = numpy.random.randint(9)
        if espacio_esta_libre(T,pos):
            buscar = False
            T[pos] = 'X'
    # while buscar and not tablero_esta_lleno(T):
    #     seleccion = input('Seleccionar una posicion para una X (1-9) : ')
    #     try:
    #         pos = int(seleccion) - 1
    #         if pos >= 0 and pos <= 8 :
    #             if espacio_esta_libre(T,pos):
    #                 buscar = False
    #                 T[pos] = 'X'
    #             else:
    #                 print('La posición esta ocupada')
    #         else:
    #             print('Indicar una posición válida')
    #     except:
    #         print('Debe ingresar un número')
    return T


def juega_o(T):
    buscar = True
    while buscar and not tablero_esta_lleno(T):
        pos = numpy.random.randint(9)
        if espacio_esta_libre(T,pos):
            buscar = False
            T[pos] = 'O'
    return T

def jugar(T):
    # print("\nComienza un nuevo Juego...\n")
    juego = []
    while not tablero_esta_lleno(T):
        if not es_ganador(T,'O'):
            T = juega_x(T)
            tablero_actual = T[:]
            juego.append(tablero_actual)
            if es_ganador(T,'X'):
                break
        if not es_ganador(T,'X'):
            T = juega_o(T)
            tablero_actual = T[:]
            juego.append(tablero_actual)
            if es_ganador(T,'O'):
                break

    if es_ganador(T,'X'):
        juego.append('X')
        return(juego)
    elif es_ganador(T,'O'):
        juego.append('O')
        return(juego)
    else:
        juego.append('E')
        return(juego)

#inicio del juego
log = []
for i in range(2000):
    T0 = [' ' for pos in range(9)]
    log.append(jugar(T0))

#print(log)

# Recogiendo Datos
movimientos = []
resultados = []
for n in range(len(log)):
    for m in range(1, len(log[n]) - 1, 2):
        movimientos.append(log[n][m])
        resultados.append(log[n][len(log[n])-1])

# print(len(movimientos))
# print(len(resultados))

#acondicionamos los datos
for n in range(len(movimientos)):
    for m in range(len(movimientos[n])):
        if movimientos[n][m] == 'X': movimientos[n][m] = 1
        if movimientos[n][m] == 'O': movimientos[n][m] = -1
        if movimientos[n][m] == ' ': movimientos[n][m] = 0

for n in range(len(resultados)):
    if resultados[n] == 'X': resultados[n] = 1
    if resultados[n] == 'O': resultados[n] = -1
    if resultados[n] == 'E': resultados[n] = 0

# print(len(movimientos))
# print((resultados))
 
red = MLPClassifier(activation='tanh',
                    hidden_layer_sizes=(64,),
                    max_iter=10,
                    learning_rate_init=.1)

#entrenamos la red
n = 5000
red.fit(movimientos[:n], resultados[:n])

#verificamos las predicciones con los datos restantes
esperados = resultados[n:]
prediccion = red.predict(movimientos[n:])

# mostramos resultados
print(metrics.classification_report(esperados, prediccion))


def juega_o2(T):
    buscar = True
    while buscar and not tablero_esta_lleno(T):
        # buscamos en forma inteligente
        print('buscando el mejor movimiento...')
        for pos1 in range(9):
            if espacio_esta_libre(T,pos1) and prediccion(T,pos1)=='O':
                buscar = False
                T[pos1] = 'O'
                print('selecciona la posición ',pos1)
                break 
        #sino encuentra una buena opcion, elige en forma aleatoria
        pos = numpy.random.randint(9)
        if espacio_esta_libre(T,pos) and buscar:
            buscar = False
            T[pos] = 'O'
            print('jugando en forma aleatoria')
    return T

def prediccion(T,pos):
    Tn = T[:]
    Tn[pos] = 'O'
    for i in range(len(Tn)):
        if Tn[i] == 'X': Tn[i] = 1
        if Tn[i] == 'O': Tn[i] = -1
        if Tn[i] == ' ': Tn[i] = 0
    p = red.predict([Tn])
    print(Tn,p)
    if p == [1] : return 'X'
    if p == [-1] : return 'O'
    if p == [0] : return 'E'


def jugar2(T):
    print("\nComienza un nuevo Juego...\n")
    juego = []
    while not tablero_esta_lleno(T):
        if not es_ganador(T,'O'):
            T = juega_x(T)
            tablero_actual = T[:]
            # juego.append(tablero_actual)
            if es_ganador(T,'X'):
                break
        if not es_ganador(T,'X'):
            T = juega_o2(T)
            tablero_actual = T[:]
            # juego.append(tablero_actual)
            if es_ganador(T,'O'):
                break

    if es_ganador(T,'X'):
        juego.append('X')
        return(juego)
    elif es_ganador(T,'O'):
        juego.append('O')
        return(juego)
    else:
        juego.append('E')
        return(juego)



# inicio del juego con la red ya entrenada
log = []
for i in range(100):
    T0 = [' ' for pos in range(9)]
    log.append(jugar2(T0))

print(log)

print('Gana X ', log.count(['X']))
print('Gana O ', log.count(['O']))
print('Empate ', log.count(['E']))