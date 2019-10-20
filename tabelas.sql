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
    codHab smallint not null,
    codCurso smallint not null,
    nome varchar(80) not null,
    creditosObrigatorios int not null,
    creditosEletivos int not null,
    creditosComplementares int not null,
    FOREIGN KEY (codCurso) REFERENCES Curso (codCurso)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (codHab, codCurso)
);

CREATE TABLE Educador (
    idEdu int not null,
    CPF bigint not null unique,
    nome varchar(50) not null,
    PRIMARY KEY (idEdu)
);

CREATE TABLE Disciplina (
    codDisc char(8) not null,
    nome varchar(70) not null,
    creditos smallint not null,
    ativo boolean default 1 not null,
    codDep smallint not null,
    FOREIGN KEY (codDep) REFERENCES Departamento (codDep)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (codDisc)
);

CREATE TABLE Predio (
    numPredio int not null,
    latitude DECIMAL(6, 4) NOT NULL,
    longitude DECIMAL(7, 4) NOT NULL,
    UNIQUE (lagitude, longitude),
    PRIMARY KEY (numPredio)
);

CREATE TABLE Sala (
    numSala smallint not null,
    numPredio int not null,
    FOREIGN KEY (numPredio) REFERENCES Predio (numPredio)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (numSala, numPredio)
);

CREATE TABLE Turma (
    horario varchar not null,
    vagas smallint not null,
    numSala smallint,
    numPredio int,
    codTurma varchar(2) not null,
    codDisc char(8) not null,
    FOREIGN KEY (codDisc) REFERENCES Disciplina (codDisc)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (numSala, numPredio) REFERENCES Sala (numSala, numPredio)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    PRIMARY KEY (codTurma, codDisc)
);

CREATE TABLE Ministracao (
    idEdu int not null,
    codTurma varchar(2) not null,
    codDisc char(8) not null,
    papel char(7) not null,
    CHECK (papel in ('Pratico', 'Teorico')),
    FOREIGN KEY (idEdu) REFERENCES Educador (idEdu)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (codTurma, codDisc) REFERENCES Turma (codTurma, codDisc)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (idEdu, codTurma, codDisc)
);

CREATE TABLE Bolsa (
    codBolsa int not null,
    beneficio decimal(7,2),
    cargaHoraria int not null,
    creditos smallint not null,
    codDep smallint not null,
    eduResponsavel int not null,
    contaAgencia int,
    contaNumero int,
    CHECK (beneficio is null or (contaAgencia is not null and contaNumero is not null)),
    FOREIGN KEY (eduResponsavel) REFERENCES Educador (idEdu)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (codDep) REFERENCES Departamento (codDep)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (codBolsa)
);

CREATE TABLE BolsaMonitoria (
    codBolsa int not null,
    codTurma varchar(2) not null,
    codDisc char(8) not null,
    FOREIGN KEY (codBolsa) REFERENCES Bolsa (codBolsa)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (codTurma, codDisc) REFERENCES Turma (codTurma, codDisc)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE BolsaIC (
    codBolsa int not null,
    nome char(100) not null,
    FOREIGN KEY (codBolsa) REFERENCES Bolsa (codBolsa)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


CREATE TABLE Aluno (
    numCartao int not null,
    CPF bigint not null unique,
    nome varchar(50) not null,
    codHab smallint,
    codCurso smallint,
    codBolsa int unique,
    FOREIGN KEY (codBolsa) REFERENCES Bolsa (codBolsa)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    FOREIGN KEY (codHab, codCurso) REFERENCES Habilitacao (codHab, codCurso)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    PRIMARY KEY (numCartao)
);

-- Relacionamento Aluno-Turma
CREATE TABLE LotacaoTurma (
    numCartao int not null,
    codTurma varchar(2) not null,
    codDisc char(8) not null,
    FOREIGN KEY (codTurma, codDisc) REFERENCES Turma (codTurma, codDisc)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (numCartao) REFERENCES Aluno (numCartao)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (codTurma, codDisc, numCartao)
);

CREATE TABLE EntradaCurriculo (
    codDisc char(8) not null,
    codHab smallint not null,
    codCurso smallint not null,
    requisitoCreditos smallint,
    obrigatoriedade ENUM('obrigatoria', 'eletiva', 'opcional') not null,
    etapa smallint,
    CHECK ((obrigatoriedade in ('eletiva', 'opcional')) != (etapa is not null)), -- Se for obrigatoria, etapa não pode ser nulo
    FOREIGN KEY (codDisc) REFERENCES Disciplina (codDisc)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (codHab, codCurso) REFERENCES Habilitacao (codHab, codCurso)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (codDisc, codHab, codCurso)
);

-- Relacionamento Disciplina-EntradaCurriculo-Habilitacao
CREATE TABLE PreRequisito (
    codDiscRequisito char(8) not null,
    codDisc char(8) not null,
    codHab smallint not null,
    codCurso smallint not null,
    FOREIGN KEY (codDiscRequisito) REFERENCES Disciplina (codDisc)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (codHab, codCurso) REFERENCES Habilitacao (codHab, codCurso)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (codDisc, codHab, codCurso) REFERENCES EntradaCurriculo (codDisc, codHab, codCurso)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    PRIMARY KEY (codDiscRequisito, codDisc, codHab, codCurso)
);
