import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comida = ctrl.Antecedent(np.arange(0, 9, 1), 'comida')
sedentario = ctrl.Antecedent(np.arange(0, 11, 1), 'sedentario') 
#Variaveis de saída (Consequent)
quilo = ctrl.Consequent(np.arange(0, 11, 1), 'quilo')

# automf -> Atribuição de categorias automaticamente
comida.automf(names=['pouco','razoavel','bastante'],)

sedentario['pouco'] = fuzz.trapmf(sedentario.universe, [0,0,4,6])
sedentario['medio'] = fuzz.trapmf(sedentario.universe, [4, 6, 8, 10])
sedentario['muito'] = fuzz.trapmf(sedentario.universe, [8,10,12,14])
sedentario.view()

# atribuicao trapezoidal
quilo['leve'] = fuzz.trapmf(quilo.universe, [0,0,4,6])
quilo['medio'] = fuzz.trapmf(quilo.universe, [4, 6, 8, 10])
quilo['pesado'] = fuzz.trapmf(quilo.universe, [8,10,12,14])
quilo.view()

#Visualizando as variáveis
comida.view()


#Criando as regras
regra_1 = ctrl.Rule(comida['pouco'] | (sedentario['medio'] & sedentario['pouco']), quilo['leve'])
regra_2 = ctrl.Rule(comida['razoavel'] | (sedentario['medio'] & sedentario['medio']), quilo['medio'])
regra_3 = ctrl.Rule(comida['bastante'] | (sedentario['medio'] & sedentario['muito']), quilo['pesado'])
controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3])


#Simulando
Calculoquilo = ctrl.ControlSystemSimulation(controlador)

valorComida = float(input('Comida: '))
valorSedentario = int(input('Sedentario: '))
Calculoquilo.input['comida'] = valorComida
Calculoquilo.input['sedentario'] = valorSedentario
Calculoquilo.compute()

valorquilo = Calculoquilo.output['quilo']

print("\nComida: %d \nSedentário: %d\nQuilo: %5.2f" %(
        valorComida,
        valorSedentario,
        valorquilo))


comida.view(sim=Calculoquilo)
sedentario.view(sim=Calculoquilo)
quilo.view(sim=Calculoquilo)

plt.show()