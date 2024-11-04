# Configuração ambiente

-   Instalar pyenv:
    
    > https://github.com/pyenv/pyenv

-   Instalar Python (v 3.10.11)

    > pyenv install 3.10.11
    > pyenv global 3.10.11

# Ambiente local de desenvolvimento

No diretório src

-   Criar ambiente

    > python -m venv .env

-   Ativar ambiente

    > ps1
    > .\.env\Scripts\activate

    > linux
    > source .env/bin/activate

-   Instalar dependências
    > pip install -r requirements.txt


# Ambiente docker

-   Criar ambiente

    > docker-compose up --build

-   Limpando ambiente
    > docker-compose down --volumes --rmi all