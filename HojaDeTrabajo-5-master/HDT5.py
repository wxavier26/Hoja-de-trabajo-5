#Autores: Xavier Cifuentes - 13316
#         Pablo de Leon - 13227
#Fecha: 31/08/16


import random
import simpy
import math

intervalo= 5#Cantidad de Intervalos
random.seed(42)

def proceso(env, nombre, time, cpu, memoria, nIns, nWait, intervalo, posicion):
     global tiempototal #Tiempo total de este proceso
     global tiempolista #Lista de tiempos totales
     numram = nIns #Cantidad de ram 
     time = random.expovariate(1.0 / intervalo) #Tiempo variable
     yield  env.timeout(time) 
     memoria.get(numram) #Obtener cantidad de memoria ram a partir de la cantidad de instrucciones del proceso
     t1= env.now #Guardar tiempo 1
     print('%s Generando:  %7.4f' % (nombre,  t1))
     with cpu.request() as req2:
         yield req2
         while (nIns > 0):
             t2= env.now #Guardar tiempo 2
             print('%s starting to CPU at %7.4f' % (nombre, t2))
             if (nIns >= 3): 
                 nIns = nIns -3 #Disminuir las instrucciones en 3 si la cantidad de instrucciones totaltes en el proceso es mayora a 3
                 yield env.timeout(1) #Agregar 1 unidad de tiempo por las 3 insutrucciones que se realizaron
                 if (nWait == 1):
                     env.timeout(random.randint(1, 10)) #Si hay espera, entonces es un tiempo variable de espera
             else:
                 print('%s waitin at %7.4f' % (nombre, env.now))
                 nIns = 0 #Si la cantidad de instrucciones es mayor a 3 entonces salir del proceso
     t2 = env.now #Guardar el segundo tiemop
     tiempoProm= t2 - t1 #Ver el tiempo promedio
     tiempolista.append(tiempoProm) #Enlistar el tiempo promedio del proceso
     tiempototal=tiempototal+tiempoProm #Agregar el tiempo promedio al tiempo total
     print('%s terminar at %7.4f' % (nombre, t2))
     print( 'Su tiempo del proceso es: %7.4f ' % (tiempoProm))
     memoria.put(numram)
      
     
     

tiempototal=0
total=0
tiempolista=[]
numprocesos= 200 #CANTIDAD DE PROCESOS
env = simpy.Environment()               
memoria= simpy.Container(env, init = 100, capacity= 200)
cpu = simpy.Resource(env, capacity = 2)

# crear los procesos
for i in range(numprocesos):
    numIns = 10
    nIns = random.randint(1,10)
    nWait= random.randint(0,1)
    env.process(proceso(env, 'Proceso %d' % i,i, cpu, memoria, nIns, nWait, intervalo, i))
    
#Correr el ambiente
env.run()
tiempototal=tiempototal/numprocesos
print('su tiempo final es: %7.4f ' % (tiempototal))
#Desviacion estandar
def desviacion_standar(lists, media):
     global total
     for i in range(0,len(lists)):
          value = lists[i]
          value = value - media
          value = value**2
          total = total + value
          total = total/float(len(lists))
          return math.sqrt(total)
#Desplegar desviacion estandar     
total = desviacion_standar(tiempolista, tiempototal)
print('su desviacion estandar es: %7.4f ' % (total))
