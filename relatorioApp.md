# Relatório da Aplicação
## Conexão com a base de dados
A aplicação foi desenvolvida em Python e HTML, com a biblioteca Flask de *back-end*, e o SGBD utilizado foi o MySQL.
A conexão com a base de dados é feita com a biblioteca *flask_mysqldb*.

Para conectar a aplicação à base de dados, alguns parâmetros são definidos no Flask, de acordo com a configuração de senha e nome da base de dados:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ufrgs'
```

E então, usa-se o objeto *app* para inicializar o `mysql`, e a partir do `mysql`, cria-se um cursor, para fazer uma transação:

```python
mysql = MySQL(app)
cur = mysql.connection.cursor()
```

## Envio e processo de consultas
Após criar um cursor, podemos executar operações *sql*:

```python
cur = mysql.connection.cursor()
        cur.execute('''select codHab, codCurso, nome from habilitacao''')
        habs = cur.fetchall()
```

Usando o objeto retornado por `fetchall()`, podemos enviar os resultados de uma consulta para um *Template*, que é uma página HTML com campos para serem preenchidos com a consulta:

```python
return render_template('grupo_matricula_selector.html', habilitacoes=habs)
```

## Envio e processo de atualizações
Para atualizar a base de dados, é necessário aplicar o comando `connect()`da classe `MySql` que, por sua vez, retorna uma outra classe que se refere a essa conexão com o banco de dados. Dessa forma, é possível aplicar *commit* nas transações executadas pelo cursor.

```python
con = mysql.connect()
```

Como o nosso sistema possui o intuito de que o aluno consiga inserir suas matrículas e se candidatar a bolsas, é necessário que ele possa definir, em se tratando de bolsas, qual bolsa ele quer se candidatar - levando em consideração que ele só pode estar cadastrado em uma bolsa.

```python
if request.method == "POST":
        details = request.form
        bolsa = details['codBolsa']
        
        cur = con.cursor()
        cur.execute('''update Aluno set codBolsa = {} where numCartao = {}'''.format(bolsa, cartao))
        con.commit()

        return redirect("/lista/{}".format(cartao))
```

Adquirindo os dados a partir da página HTML após o usuário apertar o botão, uma requisição será feita ao *back-end* e será possível inserir os dados a base de dados - garantindo as restrições pelo *back-end*, é claro.

## Estruturas e procedimentos usados

Em situações em que é necessário fazer uma consulta, a biblioteca Flask utiliza uma tupla de tuplas para indicar as linhas resultantes da consulta. Ademais, como visto anteriormente, informações adquiridas pelo *front-end* são manipuladas pelo *back-end* por meio de uma estrutura de dicionário - como exemplificado no trecho abaixo.

```python
details = request.form
cartao = details['cartao']
```

No geral, a manipulação dos dados são feitas com estruturas escolhidas pelo SGBD implicitamente, visando deixar essas operações invisíveis para o *front-end*.