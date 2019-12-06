-- Mostra as vagas disponíveis em uma turma específica
DELIMITER //
CREATE FUNCTION VAGAS_EM_TURMA(codT VARCHAR(2), codD CHAR(8))
RETURNS INT
BEGIN
	RETURN (SELECT vagas
	FROM Turma
	WHERE (codTurma, codDisc) = (codT, codD));
END 
//
DELIMITER ;

-- Verifica se um subhorario pertence a algum horario configurado sintaticamente de acordo com a descricao do atributo horario da tabela turma.
DELIMITER //
CREATE FUNCTION SUBHORARIO_PERTENCE_HORARIO(subhorario VARCHAR(19), horario VARCHAR(200))
RETURNS TINYINT(1)
BEGIN
	IF LOCATE(subhorario, horario) = 0 THEN
		RETURN 0;
	ELSE
		RETURN 1;
	END IF;
END
//
DELIMITER ;

-- Mostra as disciplinas e as propriedades das suas turmas de acordo com um departamento específico
DELIMITER //
CREATE PROCEDURE HORARIOS_POR_DEPARTAMENTO(IN dep SMALLINT)
BEGIN
	SELECT codDisc, codTurma, horario, Educador.nome as nomeProfessor, numPredio, numSala
	FROM Ministracao JOIN Educador USING (idEdu)
		JOIN Turma USING (codTurma, codDisc)
		JOIN Disciplina USING (codDisc)
	WHERE codDep = dep;
END
//
DELIMITER ;

-- Mostra as disciplinas e as propriedades das suas turmas de acordo com uma habilitação específica
DELIMITER //
CREATE PROCEDURE HORARIOS_POR_HABILITACAO(IN curso SMALLINT, IN hab SMALLINT)
BEGIN
	SELECT codDisc, codTurma, horario, Educador.nome as nomeProfessor, numPredio, numSala
	FROM Ministracao JOIN Educador USING (idEdu)
		JOIN Turma USING (codTurma, codDisc)
		JOIN Disciplina USING (codDisc)
        JOIN EntradaCurriculo USING (codDisc)
	WHERE codCurso = curso AND codHab = hab;
END
//
DELIMITER ;

-- Decrementa o número de vagas disponíveis em uma turma
DELIMITER //
CREATE PROCEDURE ATUALIZA_VAGAS_TURMA(IN codT VARCHAR(2), IN codD CHAR(8))
BEGIN
	UPDATE Turma
	SET vagas = vagas - 1
	WHERE codTurma = codT AND codDisc = codD AND vagas > 0;
END 
//
DELIMITER ;

-- Horário de uma turma específica
DELIMITER //
CREATE PROCEDURE HORARIOS_TURMA(IN codT VARCHAR(2), IN codD CHAR(8))
BEGIN
	SELECT horario
	FROM Turma
    WHERE codTurma = codT AND codDisc = codD; 
END
//
DELIMITER ;

-- Verifica se tem vaga na turma requerida e permite a inserção da matrícula em questão.
DELIMITER //
CREATE PROCEDURE INSERE_MATRICULA(IN cartao INT, IN codT VARCHAR(2), IN codD CHAR(8))
BEGIN
	IF VAGAS_EM_TURMA(codT, codD) < 0 THEN
		DELETE FROM Matricula
        WHERE numCartao = cartao AND codTurma = codT AND codDisc = codD;
        UPDATE Turma
        SET vagas = 0;
	ELSE
		CALL ATUALIZA_VAGAS_TURMA(codT, codD);
	END IF;
END 
//
DELIMITER ;

-- Apaga a matrícula caso ela não seja consistente com o número de vagas disponíveis.
DELIMITER //
CREATE TRIGGER TRIGGER_INSERE_MATRICULA
AFTER INSERT ON Matricula
FOR EACH ROW
BEGIN
	CALL INSERE_MATRICULA(NEW.numCartao, NEW.codTurma, NEW.codDisc);
END
//
DELIMITER ;