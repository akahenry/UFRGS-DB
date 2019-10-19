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
    FOREIGN KEY (codCurso) REFERENCES Curso,
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

CREATE TABLE Aluno (
    numCartao int not null,
    idHab smallint not null,
    codCurso smallint not null,
    FOREIGN KEY (idHab, codCurso) REFERENCES Habilitacao,
    PRIMARY KEY (numCartao)
);



CREATE TABLE Departamento (
    nome varchar(70) not null,
    PRIMARY KEY (nome)
);

CREATE TABLE Disciplina (
    cod char(8) not null,
    nome varchar(70) not null,
    creditos smallint not null,
    dataInicio int(5) not null,
    dataTermino int(5),
    dep varchar(70) not null,
    FOREIGN KEY (dep) REFERENCES Departamento,
    PRIMARY KEY (cod)
);


CREATE TABLE Predio (
    numPredio int not null,
    PRIMARY KEY (numPredio)
);

CREATE TABLE Sala (
    numSala smallint not null,
    numPredio int not null,
    PRIMARY KEY (numSala, numPredio)
);

CREATE TABLE Turma (
    horario datetime not null,
    numSala smallint not null,
    numPredio int not null,
    cod varchar(2) not null,
    disc char(8) not null,
    idEdu int not null,
    idEdu2 int,
    FOREIGN KEY (idEdu) REFERENCES Educador,
    FOREIGN KEY (idEdu2) REFERENCES Educador,
    FOREIGN KEY (disc) REFERENCES Disciplina,
    FOREIGN KEY (numSala, numPredio) REFERENCES Sala,
    PRIMARY KEY (cod, disc)
);

-- Relacionamento Aluno-Turma
CREATE TABLE LotacaoTurma (
    numCartao int not null,
    cod varchar(2) not null,
    disc char(8) not null,
    FOREIGN KEY (cod, disc) REFERENCES Turma,
    FOREIGN KEY (numCartao) REFERENCES Aluno
);

CREATE TABLE Bolsa (
    numCartao int not null,
    beneficio decimal(7,2),
    cargaHoraria int not null,
    creditos smallint not null,
    tipo ENUM('ic', 'monitoria') not null,
    nome varchar(50),
    dep varchar(70) not null,
    turmaMonitoriaCod varchar(2),
    turmaMonitoriaDisc char(8),
    eduResponsavel int not null,
    contaBanco int,
    contaAgencia int,
    contaNumero int,
    FOREIGN KEY (eduResponsavel) REFERENCES Educador,
    FOREIGN KEY (turmaMonitoriaCod, turmaMonitoriaDisc) REFERENCES Turma,
    CHECK (tipo='ic' != (turmaMonitoriaCod is not null and turmaMonitoriaDisc is not null)), -- Se for monitoria, precisa ter turma
    FOREIGN KEY (dep) REFERENCES Departamento,
    PRIMARY KEY (numCartao)
);

CREATE TABLE EntradaCurriculo (
    codDisc char(8) not null,
    idHab smallint not null,
    codCurso smallint not null,
    requisitoCreditos smallint,
    obrigatoriedade ENUM('orbigatoria', 'eletiva', 'opcional') not null,
    etapa smallint,
    CHECK ((obrigatoriedade in ('eletiva', 'opcional')) != (etapa is not null)), -- Se for obrigatoria, etapa não pode ser nulo
    FOREIGN KEY (codDisc) REFERENCES Disciplina,
    FOREIGN KEY (idHab, codCurso) REFERENCES Habilitacao,
    PRIMARY KEY (codDisc, idHab, codCurso)
);

CREATE TABLE PreRequisito (
    codDiscRequisito char(8) not null,
    codDisc char(8) not null,
    idHab smallint not null,
    codCurso smallint not null,
    FOREIGN KEY (codDiscRequisito) REFERENCES Disciplina,
    FOREIGN KEY (codDisc, idHab, codCurso) REFERENCES EntradaCurriculo,
    PRIMARY KEY (codDiscRequisito, codDisc, idHab, codCurso)
);