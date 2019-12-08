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


# TODO: checar notas
@app.route('/matricula/<int:cartao>', methods=['GET', 'POST'])
def matricula(cartao):
    if request.method == "GET":
        cur = mysql.connection.cursor()

        # Código de todas disciplinas que o aluno rodou ou nunca se matriculou
        cur.execute('''select codDisc from disciplina
                       where codDisc not in (select codDisc from matricula
                                             where numCartao={} and
                                                   (nota <> 'FF' and
                                                   nota <> 'D') or
                                                   nota is null)'''.format(cartao))
        codsAbertos = cur.fetchall()

        # Código de todas disciplinas que o aluno já fez e não rodou
        cur.execute('''select codDisc from matricula
                       where numCartao={} and
                             nota <> "FF" and
                             nota <> "D" and
                             nota is not null'''.format(cartao))
        feitas = cur.fetchall()

        # Códigos das disciplinas cujos requisitos foram satisfeitos
        codsElegiveis = []
        for codTuple in codsAbertos:
            cod = codTuple[0]
            cur.execute('''select codDiscRequisito from prerequisito
                           where codDisc="{}"'''.format(cod))
            requisitos = cur.fetchall()
            if set(requisitos).issubset(set(feitas)):
                codsElegiveis.append(cod)

        # Informações das turmas das disciplinas cujos requisitos forma satisfeitos e que tem vagas
        turmasElegiveis = []
        for cod in codsElegiveis:
            cur.execute('''select d.nome, d.creditos, t.codDisc,
                                  t.codTurma, t.horario, t.vagas,
                                  t.numPredio, t.numSala, e.nome from
                           disciplina d
                           join turma t using (codDisc)
                           join ministracao m on (m.codDisc = t.codDisc and m.codTurma = t.codTurma)
                           join educador e using (idEdu)
                           where t.codDisc="{}" and
                                 t.vagas > 0'''.format(cod))
            turmas = cur.fetchall()
            # Não é possível concatenar pois 'turmas' é tupla
            for turma in turmas:
                turmasElegiveis.append(turma)

        return render_template('matricula.html', turmas=turmasElegiveis)

    elif request.method == 'POST':
        turmas_list = request.form.getlist('turmas-list')
        cur = mysql.connection.cursor()

        for turma in turmas_list:
            codDisc = turma.split('/')[0]
            codTurma = turma.split('/')[1]
            horarioTurma = turma.split('/')[2]

            # Teste para ver se existe conflito de disciplina ou horário
            for outraTurma in turmas_list:
                outraCodDisc = outraTurma.split('/')[0]
                outraCodTurma = outraTurma.split('/')[1]

                if (outraCodDisc != codDisc or outraCodTurma != codTurma):
                    outroHorario = outraTurma.split('/')[2]

                    conflitaHorario = False
                    for horario in horarioTurma.split("\n"):
                        if horario in outroHorario:
                            conflitaHorario = True

                    if (outraCodDisc == codDisc and outraCodTurma != codTurma) or conflitaHorario:
                        return render_template('resultado_matricula.html',
                                            cartao=cartao,
                                            h1="Erro!",
                                            p="Dentre as turmas que você selecionou, há conflito de horários ou mais de uma turma para a mesma disciplina.")

            # Se não deu erro de conflitos entre turmas, realiza a matricula
            cur.execute('''insert into matricula
                           values('{}','{}','{}',null)'''.format(cartao, codTurma, codDisc))
            
            mysql.connection.commit()
        
        return render_template('resultado_matricula.html',
                               cartao=cartao,
                               h1="Sucesso!",
                               p="Sua matrícula foi realizada com sucesso.")


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
