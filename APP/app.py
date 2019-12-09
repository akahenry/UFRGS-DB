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


@app.route('/bolsas/<int:cartao>', methods=['GET', 'POST'])
def bolsas(cartao):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        if request.form.get('submit_button') == "Inscrever-se para IC":
            codBolsa = request.form.get('codBolsaIC')
        else:
            codBolsa = request.form.get('codBolsaMON')
        print(codBolsa)
        if codBolsa != None:
            cur.execute('''update aluno set codBolsa = {} where numCartao = {}'''.format(codBolsa, cartao))
            mysql.connection.commit()
            return render_template('resultado_bolsa.html', cartao = cartao, h1="Sucesso!", p="Sua inscrição na bolsa foi realizada com sucesso.")
        else:
            return render_template('resultado_bolsa.html', cartao = cartao, h1="Erro!", p="Sua inscrição não foi efetuada pois você não selecionou uma bolsa.")
    else:
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

@app.route('/consultas', methods=['GET', 'POST'])
def consultas():
    if request.method == "POST":
        if request.form.get('submit_button') == 'Turmas que possuem pelo menos N alunos':
            N = request.form.get('N')
            if N != "":
                try:
                    int(N)
                    return redirect('c2/{}'.format(N))
                except:
                    pass
        elif request.form.get('submit_button') == 'Alunos com maiores notas em uma disciplina específica':
            disciplina = request.form.get('disciplina')
            if disciplina != "":
                return redirect('c5/{}'.format(disciplina))
        else:
            departamento = request.form.get('departamento')
            if departamento != "":
                try:
                    int(departamento)
                    return redirect('c8/{}'.format(departamento))
                except:
                    pass
    return render_template('consultas.html')


@app.route('/c1')
def c1():
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codDep, COUNT(DISTINCT codDisc)
                    FROM Disciplina JOIN Departamento USING (codDep)
                    GROUP BY codDep''')
    table = cur.fetchall()

    return render_template('c1.html', table = table)

@app.route('/c2/<int:N>')
def c2(N):
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codDisc, codTurma
                    FROM Turma JOIN Matricula USING (codTurma, codDisc)
                    WHERE nota IS NULL
                    GROUP BY codTurma, codDisc
                    HAVING COUNT(numCartao) >= {}'''.format(N))
    table = cur.fetchall()

    return render_template('c2.html', table = table)

@app.route('/c3')
def c3():
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codHab, codCurso, COUNT(DISTINCT codDisc)
                    FROM Habilitacao LEFT JOIN EntradaCurriculo USING (codHab, codCurso)
                    GROUP BY codHab, codCurso''')
    table = cur.fetchall()

    return render_template('c3.html', table = table)

@app.route('/c4')
def c4():
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codBolsa
                    FROM Bolsa
                    WHERE beneficio = ( SELECT MAX(beneficio)
					                    FROM Bolsa)''')
    table = cur.fetchall()

    return render_template('c4.html', table = table)
@app.route('/c5/<string:disciplina>')
def c5(disciplina):
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT numCartao
                    FROM Aluno JOIN Matricula USING (numCartao)
                    WHERE codDisc = '{}' AND nota = 
                        (SELECT MIN(nota)
                        FROM Matricula
                        WHERE codDisc = '{}')'''.format(disciplina, disciplina))
    table = cur.fetchall()

    return render_template('c5.html', table = table)

@app.route('/c6')
def c6():
    cur = mysql.connection.cursor()

    cur.execute(''' select disciplina.nome, disciplina.creditos, turma.codDisc,
                            turma.codTurma, turma.horario, turma.vagas,
                            turma.numPredio, turma.numSala, educador.nome from
                    disciplina
                    left join turma using (codDisc)
                    left join ministracao on (ministracao.codTurma=turma.codTurma and ministracao.codDisc=turma.codDisc)
                    left join educador using (idEdu)
                    left join matricula m on (turma.codDisc=m.codDisc)
                    where turma.codDisc not in (select codDisc from
                                                matricula
                                                where numCartao=301212)
                    and not exists (select codDiscRequisito from
                                    prerequisito
                                    where codDisc=m.codDisc
                                            and codDiscRequisito not in (select codDisc from matricula
                                                                         where numCartao=301212 and nota not in ("FF", "D", null)))''')
    table = cur.fetchall()

    return render_template('c6.html', table = table)

@app.route('/c7')
def c7():
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codDisc, codTurma
                    FROM TurmasDoINF
                    WHERE nomeProfessor = 'Bill Gates' AND horario LIKE '%Terças%' ''')
    table = cur.fetchall()

    return render_template('c7.html', table = table)

@app.route('/c8/<int:departamento>')
def c8(departamento):
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codDisc, codTurma
                    FROM Turma JOIN Disciplina USING (codDisc)
                    WHERE codDep = {} '''.format(departamento))
    table = cur.fetchall()

    return render_template('c8.html', table = table)

@app.route('/c9')
def c9():
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT codBolsa
                    FROM BolsaIC
                    WHERE nome LIKE '%Métodos ágeis%' ''')
    table = cur.fetchall()

    return render_template('c9.html', table = table)

@app.route('/c10')
def c10():
    cur = mysql.connection.cursor()

    cur.execute(''' SELECT EntradaCurriculo.codCurso, EntradaCurriculo.codHab, EntradaCurriculo.codDisc, requisitoCreditos, codDiscRequisito
                    FROM EntradaCurriculo JOIN PreRequisito USING (codDisc)
                    ORDER BY EntradaCurriculo.codCurso, EntradaCurriculo.codHab''')
    table = cur.fetchall()

    return render_template('c10.html', table = table)

if __name__ == '__main__':
    app.run()
