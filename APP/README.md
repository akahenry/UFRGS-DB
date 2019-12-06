Aplicação que usa o banco de dados.

Para rodar, instale flask e flask_mysqldb usando o pip.

Em seguida, apenas rode app.py

A aplicação vai estar disponível no endereço http://127.0.0.1:5000/

Para carregar as mudanças feitas no app.py ao vivo, defina as seguintes variáveis de ambiente:

FLASK_APP={diretório APP}app.py
FLASK_ENV=development

E então, apenas execute 'flask run'.