# Relatório da Aplicação
## Conexão com a base de dados
A aplicação foi desenvolvida em python e html, com a biblioteca Flask de backend, e o SGBD utilizado foi o MySQL.
A conexão com a base de dados é feita com a biblioteca flask_mysqldb.

Para conectar a aplicação à base de dados, alguns parâmetros são definidos no Flask, de acordo com a configuração de senha e nome da base de dados:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ufrgs'
```

E então, usa-se o objeto app para inicializar o `mysql`, e a partir do `mysql`, cria-se um cursor, para fazer uma transação:

```python
mysql = MySQL(app)
cur = mysql.connection.cursor()
```

## Envio e processo de consultas
Após criar um cursor, podemos executar um sql:

```python
cur = mysql.connection.cursor()
        cur.execute('''select codHab, codCurso, nome from habilitacao''')
        habs = cur.fetchall()
```

Usando o objeto retornado por `fetchall()`, podemos enviar os resultados de uma consulta para um Template, que é uma página html com campos para serem preenchidos com a consulta:

```python
return render_template('grupo_matricula_selector.html', habilitacoes=habs)
```

## Envio e processo de atualizações
c) detalhes de como prepara, envia
e processo o retorno de comandos de atualização. Descreva as estruturas de dados relevantes e aspectos
importantes dos procedimentos, ilustrando com porções de código. Não se esqueça de especificar a linguagem e
bibliotecas que usou. 