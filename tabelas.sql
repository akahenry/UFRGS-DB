CREATE TABLE Departamento (
    codDep smallint not null,
    nome varchar(70) not null,
    PRIMARY KEY (codDep)
);

CREATE TABLE Curso (
    codCurso smallint not null,
    nome varchar(50) not null,
    PRIMARY KEY (codCurso)
);

CREATE TABLE Habilitacao (
    idHab smallint not null,
    codCurso smallint not null,
    nome varchar(50) not null,
    creditosObrigatorios int not null,
    creditosEletivos int not null,
    creditosComplementares int not null,
    FOREIGN KEY (codCurso) REFERENCES Curso (codCurso),
    PRIMARY KEY (idHab, codCurso)
);

CREATE TABLE Pessoa (
    CPF int not null,
    nome varchar(50) not null,
    PRIMARY KEY (CPF)
);

CREATE TABLE Educador (
    idEdu  int not null,
    PRIMARY KEY (idEdu)
);



CREATE TABLE Disciplina (
    codDisc char(8) not null,
    nome varchar(70) not null,
    creditos smallint not null,
    dataInicio int(5) not null,
    dataTermino int(5),
    codDep smallint not null,
    FOREIGN KEY (codDep) REFERENCES Departamento (codDep),
    PRIMARY KEY (codDisc)
);


CREATE TABLE Predio (
    numPredio int not null,
    PRIMARY KEY (numPredio)
);

CREATE TABLE Sala (
    numSala smallint not null,
    numPredio int not null,
    FOREIGN KEY (numPredio) REFERENCES Predio (numPredio),
    PRIMARY KEY (numSala, numPredio)
);

CREATE TABLE Turma (
    horario datetime not null,
    numSala smallint not null,
    numPredio int not null,
    codTurma varchar(2) not null,
    codDisc char(8) not null,
    idEdu int not null,
    idEdu2 int,
    FOREIGN KEY (idEdu) REFERENCES Educador (idEdu),
    FOREIGN KEY (idEdu2) REFERENCES Educador (idEdu),
    FOREIGN KEY (codDisc) REFERENCES Disciplina (codDisc),
    FOREIGN KEY (numSala, numPredio) REFERENCES Sala (numSala, numPredio),
    PRIMARY KEY (codTurma, codDisc)
);

CREATE TABLE Bolsa (
    codBolsa int not null,
    beneficio decimal(7,2),
    cargaHoraria int not null,
    creditos smallint not null,
    tipo ENUM('ic', 'monitoria') not null,
    nome varchar(50),
    codDep smallint not null,
    turmaMonitoriaCod varchar(2),
    turmaMonitoriaDisc char(8),
    eduResponsavel int not null,
    contaBanco int,
    contaAgencia int,
    contaNumero int,
    FOREIGN KEY (eduResponsavel) REFERENCES Educador (idEdu),
    FOREIGN KEY (turmaMonitoriaCod, turmaMonitoriaDisc) REFERENCES Turma (codTurma, codDisc),
    CHECK (tipo='ic' != (turmaMonitoriaCod is not null and turmaMonitoriaDisc is not null)), -- Se for monitoria, precisa ter turma
    FOREIGN KEY (codDep) REFERENCES Departamento (codDep),
    PRIMARY KEY (codBolsa)
);

CREATE TABLE Aluno (
    numCartao int not null,
    idHab smallint not null,
    codCurso smallint not null,
    codBolsa int unique,
    FOREIGN KEY (codBolsa) REFERENCES Bolsa (codBolsa),
    FOREIGN KEY (idHab, codCurso) REFERENCES Habilitacao (idHab, codCurso),
    PRIMARY KEY (numCartao)
);

-- Relacionamento Aluno-Turma
CREATE TABLE LotacaoTurma (
    numCartao int not null,
    codTurma varchar(2) not null,
    codDisc char(8) not null,
    FOREIGN KEY (codTurma, codDisc) REFERENCES Turma (codTurma, codDisc),
    FOREIGN KEY (numCartao) REFERENCES Aluno (numCartao),
    PRIMARY KEY (codTurma, codDisc, numCartao)
);

CREATE TABLE EntradaCurriculo (
    codDisc char(8) not null,
    idHab smallint not null,
    codCurso smallint not null,
    requisitoCreditos smallint,
    obrigatoriedade ENUM('orbigatoria', 'eletiva', 'opcional') not null,
    etapa smallint,
    CHECK ((obrigatoriedade in ('eletiva', 'opcional')) != (etapa is not null)), -- Se for obrigatoria, etapa não pode ser nulo
    FOREIGN KEY (codDisc) REFERENCES Disciplina (codDisc),
    FOREIGN KEY (idHab, codCurso) REFERENCES Habilitacao (idHab, codCurso),
    PRIMARY KEY (codDisc, idHab, codCurso)
);

CREATE TABLE PreRequisito (
    codDiscRequisito char(8) not null,
    codDisc char(8) not null,
    idHab smallint not null,
    codCurso smallint not null,
    FOREIGN KEY (codDiscRequisito) REFERENCES Disciplina (codDisc),
    FOREIGN KEY (codDisc, idHab, codCurso) REFERENCES EntradaCurriculo (codDisc, idHab, codCurso),
    PRIMARY KEY (codDiscRequisito, codDisc, idHab, codCurso)
);