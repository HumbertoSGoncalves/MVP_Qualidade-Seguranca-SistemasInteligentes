import numpy as np
import pickle
import joblib
from sklearn.metrics._dist_metrics import ManhattanDistance32

class Model:
    
    def carrega_modelo(path):
        """Se o final for .pkl ou .joblib, carregamos de maneiras diferentes
        """
        
        if path.endswith('.pkl'):
            model = pickle.load(open(path, 'rb'))
        elif path.endswith('.joblib'):
            model = joblib.load(path)
        else:
            raise Exception('Arquivo de formato não suportado')
        return model
    
    def preditor(model, form):
        """Faz a previsão do diagnóstico de um paciente baseado no modelo previamente treinado
        """
        X_input = np.array([form.rad,
                            form.tex, 
                            form.per, 
                            form.area, 
                            form.smooth
                        ])
        # Reshape para que o modelo entenda que estamos passando corretamente
        diagnosis = model.predict(X_input.reshape(1, -1))
        return int(diagnosis[0])