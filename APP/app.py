from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ufrgs'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        cartao = details['cartao']
        # cur = mysql.connection.cursor()
        # cur.execute(
        #     "INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        # mysql.connection.commit()
        # cur.close()
        return redirect("/lista/{}".format(cartao))
    else:
        return render_template('index.html')


@app.route('/lista/<int:cartao>')
def lista(cartao):
    return render_template('lista.html', cartao=cartao)


@app.route('/matricula/<int:cartao>')
def matricula(cartao):
    cur = mysql.connection.cursor()
    cur.execute('''select disciplina.nome, disciplina.creditos, turma.codDisc,
                          turma.codTurma, turma.horario, turma.vagas,
                          turma.numPredio, turma.numSala, educador.nome from
                   disciplina
                   left join turma using (codDisc)
                   left join ministracao on (ministracao.codTurma=turma.codTurma and ministracao.codDisc=turma.codDisc)
                   left join educador using (idEdu)
                   left join matricula m on (turma.codDisc=m.codDisc)
                   where turma.codDisc not in (select codDisc from
                                               matricula
                                               where numCartao={})
                   and not exists (select codDiscRequisito from
		                           prerequisito
                                   where codDisc=m.codDisc
                                         and codDiscRequisito not in (select codDisc from matricula
                                                                      where numCartao={}))'''.format(cartao,cartao))
    rv = cur.fetchall()
    return render_template('matricula.html', turmas=rv)


@app.route('/bolsas')
def bolsas():
    cur = mysql.connection.cursor()

    cur.execute('''select bolsa.codBolsa, bolsa.creditos, bolsa.cargaHoraria,
                          bolsa.beneficio, bolsaic.nome, educador.nome from
                   bolsaic
                   join bolsa using (codBolsa)
                   join educador on (bolsa.eduResponsavel = educador.idEdu)
                   where codBolsa not in (select codBolsa from aluno
                                          where codBolsa is not null)''')
    ic = cur.fetchall()

    cur.execute('''select bolsa.codBolsa, disciplina.nome, bolsamonitoria.codTurma,
                          bolsa.creditos, bolsa.cargaHoraria, bolsa.beneficio,
                          educador.nome from
                   bolsamonitoria
                   join bolsa using (codBolsa)
                   join educador on (bolsa.eduResponsavel = educador.idEdu)
                   join disciplina using (codDisc)
                   where codBolsa not in (select codBolsa from aluno
                                          where codBolsa is not null)''')
    monitorias = cur.fetchall()

    return render_template('bolsas.html', bolsasic=ic, bolsasmonitoria=monitorias)

if __name__ == '__main__':
    app.run()
