# Criando
    - instala o virtual env dentro da pasta
        -> pip install virtualenv
# Configurando
    - depois de já criado o ambiente roda o comando:
        -> virtualenv -p python3 venv
# Ativar o ambiente virtual
        -> . venv/bin/activate

# intalando o flask de novo
    - deve ser intalado dentro do ambiente da venv
        -> venv/bin/pip3 install flask

# exportando
    -  Exporta o que foi instalado no ambiente para um arquivo para que outros podesam codar, ver quando necessário e não instalar um por um manualmente
        -> venv/bin/pip3 freeze > requirements.txt
   
# importar
    - importar o que foi instalado no ambiente virtual de outra pessoa
        -> venv/bin/pip3 install -r requirements.txt

# USANDO MVC
    - vai salvar dentro do controller as paginas

# instalando o SQLAlchemy
    - utilizado para ser um meio termo da linguagem de SQL e de programação
        -> venv/bin/pip3 install flask-sqlalchemy

# criando as tabelas
    - No model cria as tabelas do banco de dados

# Usando formularios no flask
    - para submissão de formulário no flask instalar o WTF do flask
        -> venv/bin/pip3 install flask-wtf

# OBS
    Se der merda voltar na aula 04