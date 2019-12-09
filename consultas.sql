-- Por instituto
CREATE VIEW TurmasDoINF
AS SELECT codDisc, codTurma, horario, codDep, Educador.nome as nomeProfessor, numPredio, numSala
FROM Ministracao JOIN Educador USING (idEdu)
	JOIN Turma USING (codTurma, codDisc)
    JOIN Disciplina USING (codDisc)
WHERE codDisc LIKE 'INF%';

-- Numero de disciplinas por departamento
SELECT codDep, COUNT(DISTINCT codDisc)
FROM Disciplina JOIN Departamento USING (codDep)
GROUP BY codDep;

-- Turmas que possuem pelo menos N (10) alunos
SELECT codDisc, codTurma
FROM Turma JOIN Matricula USING (codTurma, codDisc)
WHERE nota IS NULL
GROUP BY codTurma, codDisc
HAVING COUNT(numCartao) >= 10;

-- Numero de disciplinas por grupo de matrícula
SELECT codHab, codCurso, COUNT(DISTINCT codDisc)
FROM Habilitacao LEFT JOIN EntradaCurriculo USING (codHab, codCurso)
GROUP BY codHab, codCurso;

-- Bolsas com maior benefício
SELECT codBolsa
FROM Bolsa
WHERE beneficio = (SELECT MAX(beneficio)
					FROM Bolsa);

-- Alunos com maiores notas em uma disciplina específica
SELECT numCartao
FROM Aluno JOIN Matricula USING (numCartao)
WHERE codDisc = 'INF01154' AND nota = 
	(SELECT MIN(nota)
	FROM Matricula
    WHERE codDisc = 'INF01154');

-- Todas as disciplinas e suas turmas disponíveis para um determinado cartão
select disciplina.nome, disciplina.creditos, turma.codDisc,
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
                                                                         where numCartao=301212 and nota not in ("FF", "D", null)));

-- Disciplinas e turmas do Bill Gates que possuem horários nas terças
SELECT codDisc, codTurma
FROM TurmasDoINF
WHERE nomeProfessor = 'Bill Gates' AND horario LIKE '%Terças%';

-- Disciplinas e turmas do departamento de informática teórica
SELECT codDisc, codTurma
FROM TurmasDoINF
WHERE codDep = 704;

-- Bolsas de iniciação científica com o tema X (Métodos ágeis)
SELECT codBolsa
FROM BolsaIC
WHERE nome LIKE '%Métodos ágeis%';

-- Entradas de currículo e seus pré-requisitos por habilitacao
SELECT EntradaCurriculo.codCurso, EntradaCurriculo.codHab, EntradaCurriculo.codDisc, requisitoCreditos, codDiscRequisito
FROM EntradaCurriculo JOIN PreRequisito USING (codDisc)
ORDER BY EntradaCurriculo.codCurso, EntradaCurriculo.codHab;