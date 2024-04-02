# -*- coding: utf-8 -*-
"""Ab2_IA.ipynb
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Cria as variáveis linguísticas
'''
Antecedent: Variáveis de entrada (sintomas) no sistema fuzzy.
Consequent: Variável de saída (grau de pertinência do diagnóstico de diabetes).
'''

urina = ctrl.Antecedent(np.arange(0, 11, 1), 'urina')  # Urina excessivamente
obesidade = ctrl.Antecedent(np.arange(0, 11, 1), 'obesidade')  # Obesidade central (adicionando uma pequena tolerância)
formigamento = ctrl.Antecedent(np.arange(0, 11, 1), 'formigamento')  # Formingamento nos pés e nas mãos
visao = ctrl.Antecedent(np.arange(0, 11, 1), 'visao')  # Vista embaçada ou turva
diabetes = ctrl.Consequent(np.arange(0, 101, 1), 'diabetes')  # Grau de pertinência do diagnóstico de diabetes
tipo_diabetes = ctrl.Consequent(np.arange(0, 4, 1), 'tipo_diabetes')  # Tipo de diabetes


# Define as funções de pertinência (membership functions)
"""
trimf: Função de pertinência triangular.
Definimos as funções de pertinência para cada variável linguística (baixa, moderada, alta).
"""
urina['baixa'] = fuzz.trimf(urina.universe, [0, 0, 5])
urina['moderada'] = fuzz.trimf(urina.universe, [0, 5, 10])
urina['alta'] = fuzz.trimf(urina.universe, [5, 10, 10])

obesidade['baixa'] = fuzz.trimf(obesidade.universe, [0, 0, 5])  
obesidade['moderada'] = fuzz.trimf(obesidade.universe, [0, 5, 10]) 
obesidade['alta'] = fuzz.trimf(obesidade.universe, [5, 10, 10])

formigamento['baixa'] = fuzz.trimf(formigamento.universe, [0, 0, 5])
formigamento['moderada'] = fuzz.trimf(formigamento.universe, [0, 5, 10])
formigamento['alta'] = fuzz.trimf(formigamento.universe, [5, 10, 10])

visao['baixa'] = fuzz.trimf(visao.universe, [0, 0, 5])
visao['moderada'] = fuzz.trimf(visao.universe, [0, 5, 10])
visao['alta'] = fuzz.trimf(visao.universe, [5, 10, 10])

diabetes['baixa'] = fuzz.trimf(diabetes.universe, [0, 0, 100])
diabetes['moderada'] = fuzz.trimf(diabetes.universe, [0, 50, 100])
diabetes['alta'] = fuzz.trimf(diabetes.universe, [50, 100, 100])

tipo_diabetes['nao_diabetico'] = fuzz.trimf(tipo_diabetes.universe, [0, 0, 1])
tipo_diabetes['pre_diabetico'] = fuzz.trimf(tipo_diabetes.universe, [0, 1, 2])
tipo_diabetes['diabetico_tipo2'] = fuzz.trimf(tipo_diabetes.universe, [1, 2, 3])

# Regras fuzzy
'''
Definimos três regras fuzzy com base nos sintomas fornecidos.
'''
rule1 = ctrl.Rule(urina['alta'] & formigamento['alta'] |
                  obesidade['moderada'] & formigamento['alta'] |
                  urina['alta'] & obesidade['moderada'] & visao['moderada'] |
                  visao['moderada'] & obesidade['alta'] & formigamento['alta'] |
                  obesidade['alta'] | formigamento['alta'] |
                  visao['alta'], [diabetes['alta'],tipo_diabetes['diabetico_tipo2'] ])
rule2 = ctrl.Rule(urina['moderada'] & obesidade['moderada'] & formigamento['moderada'] & visao['moderada'], [diabetes['moderada'], tipo_diabetes['pre_diabetico']])
rule3 = ctrl.Rule(urina['baixa'] & obesidade['baixa'] & formigamento['baixa'] & visao['baixa'], [diabetes['baixa'], tipo_diabetes['nao_diabetico']])

# Criação do sistema de controle
diabetes_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# Simulação do sistema de controle
diabetes_sim = ctrl.ControlSystemSimulation(diabetes_ctrl)

# Entrada de exemplo
diabetes_sim.input['urina'] = 9
diabetes_sim.input['obesidade'] = 9
diabetes_sim.input['formigamento'] = 10
diabetes_sim.input['visao'] = 9

# Computa o resultado
diabetes_sim.compute()

tipo_mapeado = {
    0: 'nao_diabetico',
    1: 'pre_diabetico',
    2: 'diabetico_tipo2'
}

# Mostra o resultado
print("Grau de pertinência do diagnóstico de diabetes:", diabetes_sim.output['diabetes'])
print("Tipo de diabetes:", tipo_mapeado[int(diabetes_sim.output['tipo_diabetes'])])

'''
Pega o tipo de diabetes resultado 
'''
tipo_resultado = tipo_mapeado[int(diabetes_sim.output['tipo_diabetes'])]

# Tratamento para pré-diabético e diabético tipo 2
if tipo_resultado == 'pre_diabetico':
    print("Tratamento: Mudanças no estilo de vida, dieta saudável, exercício físico regular e monitoramento da glicose no sangue.")
elif tipo_resultado == 'diabetico_tipo2':
    print("Tratamento: Controle do açúcar no sangue através de dieta rigorosa, exercícios frequentes e medicamentos contínuos.")