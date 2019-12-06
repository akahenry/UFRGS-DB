DELIMITER //
CREATE PROCEDURE HORARIOSPORDEPARTAMENTO
(IN dep SMALLINT)
BEGIN
	SELECT codDisc, codTurma, horario, Educador.nome as nomeProfessor, numPredio, numSala
	FROM Ministracao JOIN Educador USING (idEdu)
		JOIN Turma USING (codTurma, codDisc)
		JOIN Disciplina USING (codDisc)
	WHERE codDep = dep;
END
//
DELIMITER ;
CALL HORARIOSPORDEPARTAMENTO(704);