# AI Breast Cancer Prediction

Este repositório contém o backend de uma aplicação para predição de câncer de mama. 

Desenvolvido como parte do MVP para o módulo "Qualidade de Software, Segurança e Sistemas Inteligentes" na pós-graduação em Engenharia de Software da PUC-Rio.

## Rotas das APIs existentes neste backend
_GET /_
Descrição: Redireciona para a página de documentação escolhida (Swagger, Redoc ou RapiDoc).

_GET /pacientes_
Descrição: Recupera todos os pacientes registrados na base de dados.

_POST /paciente_
Descrição: Adiciona um novo paciente e realiza a previsão do diagnóstico com um modelo de machine learning treinado.

_GET /paciente_
Descrição: Busca um paciente cadastrado na base pelo nome.

_DELETE /paciente_
Descrição: Deleta um paciente existente na base pelo nome.

---
## Como executar local

1. Clone este repositório para sua máquina, se ainda não o fez:
```
git clone https://github.com/seu-usuario/seu-repositorio.git
```

2. Atualizar todas as libs python listadas conforme o arquivo `requirements.txt`. Ou seja, execute, no ambiente escolhido, a instalação através do comando: 
```
pip install -r requirements.txt
```
3. Para executar a API: 
```
flask run --host 0.0.0.0 --port 5000
```

Recomendá-se utilizar o comando abaixo, quando em modo de desenvolvimento:
```
flask run --host 0.0.0.0 --port 5000 --reload
```
Desta forma o servidor é reinicia automaticamente após mudanças no código fonte.


4. Acesse o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador de preferência para verificar a API em execução.

Posteriormente, basta testar quaisquer rotas da API que desejar para testar o sistema. Cada rota tem sua devida descrição na documentação acessada.
