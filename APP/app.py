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


@app.route('/grupo_matricula_selector', methods=['GET', 'POST'])
def grupoMatriculaSelector():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute('''select codHab, codCurso, nome from habilitacao''')
        habs = cur.fetchall()
        return render_template('grupo_matricula_selector.html', habilitacoes=habs)
    else:
        details = request.form
        codHab = details['select']
        return redirect("/horarios_grupo_matricula/{}".format(codHab))


@app.route('/horarios_grupo_matricula/<int:codHab>')
def horariosGrupoMatricula(codHab):
    cur = mysql.connection.cursor()

    # Seleciona informações da disciplina, turma e nome do
    # professor, de todas turmas de uma certa habilitação
    cur.execute('''select disciplina.codDisc, disciplina.nome, turma.codTurma,
                   turma.vagas, turma.horario, turma.numPredio, turma.numSala,
                   educador.nome from
                   turma
                   join entradacurriculo using (codDisc)
                   join disciplina using (codDisc)
                   join ministracao on (disciplina.codDisc = ministracao.codDisc and turma.codTurma=ministracao.codTurma)
                   join educador using (idEdu)
                   where codHab={}'''.format(codHab))
    turmas = cur.fetchall()

    cur.execute("select nome from habilitacao where codHab={}".format(codHab))
    habNome = cur.fetchall()
    
    return render_template('horarios_grupo_matricula.html', turmas=turmas, habNome=habNome)

@app.route('/departamento_selector', methods=['GET', 'POST'])
def departamentoSelector():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute('''select codDep, nome from departamento''')
        deps = cur.fetchall()
        return render_template('departamento_selector.html', departamentos=deps)
    else:
        details = request.form
        departamento = details['select']
        return redirect("/horarios_departamento/{}".format(departamento))


@app.route('/horarios_departamento/<int:codDep>')
def horariosDepartamento(codDep):
    cur = mysql.connection.cursor()

    # Seleciona informações da disciplina, turma e nome do
    # professor, de todas turmas de um certo departamento
    cur.execute('''select disciplina.codDisc, disciplina.nome, turma.codTurma,
                   turma.vagas, turma.horario, turma.numPredio, turma.numSala,
                   educador.nome from
                   turma
                   join entradacurriculo using (codDisc)
                   join disciplina using (codDisc)
                   join ministracao on (disciplina.codDisc = ministracao.codDisc and turma.codTurma=ministracao.codTurma)
                   join educador using (idEdu)
                   where codDep={}'''.format(codDep))
    turmas = cur.fetchall()

    cur.execute("select nome from departamento where codDep={}".format(codDep))
    depNome = cur.fetchall()

    return render_template('horarios_departamento.html', turmas=turmas, depNome=depNome)

if __name__ == '__main__':
    app.run()
