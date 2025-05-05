# Responsável apenas pela execução do servidor

from src.app import create_app

app = create_app()

# se o arquivo for o principal a ser rodado:
if __name__ == '__main__':
    app.run(debug=True)