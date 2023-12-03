from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model
import pickle
import warnings

# Ignora todos os warnings durante a execução dos testes para facilitar a visibilidade do teste somente
warnings.simplefilter("ignore")

# Instanciando as classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "database/Breast_cancer_golden_dataset.csv"
colunas = ['rad', 'tex', 'per', 'area', 'smooth', 'target']

# Carregar dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Dividindo os dados em recursos (input) e rótulos (output).
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]

# Carregar o scaler salvo durante o treinamento
with open('ml_model/scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
    
# Aplicar a mesma transformação nos dados de teste
X_test_transformed = scaler.transform(X)

# Função para avaliar o desempenho do modelo SVC utilizando o arquivo correspondente.
def test_modelo_svc():
    # Importando modelo SVC
    svc_path = 'ml_model/breast_model.pkl'
    modelo_svc = Model.carrega_modelo(svc_path)
    
    # Obtendo as métricas do SVC
    acuracia_svc, recall_svc, precisao_svc, f1_svc = avaliador.avaliar(modelo_svc, X_test_transformed, Y)
    
    # Testando as métricas do SVC
    assert acuracia_svc >= 0.90
    assert recall_svc >= 0.90
    assert precisao_svc >= 0.80
    assert f1_svc >= 0.80
    
#execução por teste unitário
if __name__ == '__main__':
    import unittest

    class TestSeuScript(unittest.TestCase):
        def test_modelo_svc(self):
            test_modelo_svc()

    unittest.main()

