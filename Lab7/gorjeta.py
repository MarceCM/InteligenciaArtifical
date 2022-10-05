import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl

#Variaveis de Entrada (Antecedent)
comida = ctrl.Antecedent(np.arange(0, 9, 1), 'comida')
peso = ctrl.Antecedent(np.arange(0, 11, 1), 'peso')

#Variaveis de saída (Consequent)
quilo = ctrl.Consequent(np.arange(0, 31, 1), 'quilo')

# automf -> Atribuição de categorias automaticamente
comida.automf(names=['pouco','razoavel','bastante'],)
peso.automf(names=['leve','medio','pesado'])

# atribuicao gaussiana
quilo['minimo'] = fuzz.gaussmf(quilo.universe, 0,.1)
quilo['baixo'] = fuzz.gaussmf(quilo.universe, .1, 3)
quilo['medio'] = fuzz.gaussmf(quilo.universe, 15,5)
quilo['alto'] = fuzz.gaussmf(quilo.universe, 30,5)
quilo.view()

# atribuicao trapezoidal
quilo['minimo'] = fuzz.trapmf(quilo.universe, [0,.1,2,5])
quilo['baixo'] = fuzz.trapmf(quilo.universe, [.1, 3, 6, 10])
quilo['medio'] = fuzz.trapmf(quilo.universe, [15,20,25,30])
quilo['alto'] = fuzz.trapmf(quilo.universe, [30,35,40,45])
quilo.view()

#Visualizando as variáveis
comida.view()
peso.view()


#Criando as regras
regra_1 = ctrl.Rule(comida['pouco'] & peso['leve'], quilo['minimo'])
regra_2 = ctrl.Rule(comida['pouco'] & peso['medio'], quilo['medio'])
regra_3 = ctrl.Rule(peso['pesado'] & comida['bastante'], quilo['alto'])

controlador = ctrl.ControlSystem([regra_1, regra_2, regra_3])


#Simulando
Calculoquilo = ctrl.ControlSystemSimulation(controlador)

notaQualidade = int(input('Comida: '))
notaServico = int(input('Peso: '))
Calculoquilo.input['comida'] = notaQualidade
Calculoquilo.input['peso'] = notaServico
Calculoquilo.compute()

valorquilo = Calculoquilo.output['quilo']

print("\nComida %d \nPeso %d \nQuilo %5.2f" %(
        notaQualidade,
        notaServico,
        valorquilo))


comida.view(sim=Calculoquilo)
peso.view(sim=Calculoquilo)
quilo.view(sim=Calculoquilo)

plt.show()