INSERT INTO Departamento
VALUES (
    471,
    'Departamento de Filosofia'
);
INSERT INTO Departamento
VALUES (
    704,
    'Departamento de Informática Aplicada'
);
INSERT INTO Departamento
VALUES (
    705,
    'Departamento de Informática Teórica'
);


INSERT INTO Curso
VALUES (
    305,
    'Ciência da Computação'
);
INSERT INTO Curso
VALUES (
    318,
    'Engenharia da Computação'
);
INSERT INTO Curso
VALUES (
    329,
    'Filosofia'
);


INSERT INTO Habilitacao
VALUES (
    36,
    305,
    'Bacharelado em Ciência da Computação',
    152,
    36,
    8
);
INSERT INTO Habilitacao
VALUES (
    41,
    329,
    'Bacharelado em Filosofia',
    84,
    54,
    14
);
INSERT INTO Habilitacao
VALUES (
    101,
    329,
    'Licenciatura em Filosofia',
    186,
    18,
    14
);

INSERT INTO Educador
VALUES (
    111111111,
    45678912345,
    'Immanuel Kant'
);
INSERT INTO Educador
VALUES (
    222222222,
    56789123456,
    'Bill Gates'
);
INSERT INTO Educador
VALUES (
    333333333,
    67891234567,
    'Alan Turin'
);



INSERT INTO Disciplina
VALUES (
    'HUM01060',
    'Lógica I - A',
    6,
    1,
    471
);
INSERT INTO Disciplina
VALUES (
    'HUM01085',
    'Ética I',
    6,
    0,
    471
);
INSERT INTO Disciplina
VALUES (
    'HUM01087',
    'Ética II',
    6,
    0,
    471
);
INSERT INTO Disciplina
VALUES (
    'INF01154',
    'Redes de Computadores N',
    6,
    1,
    704
);
INSERT INTO Disciplina
VALUES (
    'INF05501',
    'Teoria da Computação N',
    4,
    1,
    705
);


INSERT INTO Predio
VALUES (
    43324,
    -30.070384,
    -51.118759
);
INSERT INTO Predio
VALUES (
    43425,
    -30.068564,
    -51.120523
);
INSERT INTO Predio
VALUES (
    43424,
    -30.068622,
    -51.120236
);


INSERT INTO Sala
VALUES (
    107,
    43425
);
INSERT INTO Sala
VALUES (
    109,
    43425
);
INSERT INTO Sala
VALUES (
    202,
    43324
);


INSERT INTO Turma
VALUES (
    'Segundas 8:30-10:10\nQuartas 8:30-10:10',
    40,
    107,
    43425,
    'U',
    'INF05501'
);
INSERT INTO Turma
VALUES (
    'Terças 8:30-10:10\nQuintas 8:30-10:10',
    32,
    109,
    43425,
    'U',
    'INF01154'
);
INSERT INTO Turma
VALUES (
    'Terças 10:30-12:10\nTerças 13:30-15:10\nQuintas 8:30-10:10',
    47,
    202,
    43324,
    'A',
    'HUM01085'
);

INSERT INTO Ministracao
VALUES (
    333333333,
    'U',
    'INF05501',
    'Pratico'
);
INSERT INTO Ministracao
VALUES (
    222222222,
    'U',
    'INF01154',
    'Teorico'
);
INSERT INTO Ministracao
VALUES (
    111111111,
    'A',
    'HUM01085',
    'Teorico'
);


INSERT INTO Bolsa
VALUES (
    1,
    400,
    20,
    2,
    'ic',
    'Pesquisa em Teoria da Computação',
    704,
    null,
    null,
    333333333,
    1,
    984137431
);
INSERT INTO Bolsa
VALUES (
    2,
    null,
    30,
    3,
    'monitoria',
    null,
    471,
    'A',
    'HUM01085',
    111111111,
    null,
    null
);
INSERT INTO Bolsa
VALUES (
    3,
    2000,
    10,
    1,
    'ic',
    'Experimentos de Ética',
    471,
    null,
    null,
    111111111,
    2,
    347029382
);


INSERT INTO Aluno
VALUES (
    301212,
    12345678987,
    'Jorbesclebison Dragonslayer',
    101,
    329,
    3

);
INSERT INTO Aluno
VALUES (
    290103,
    23456789123,
    'Umdoistres de Oliveira Quatro',
    36,
    305,
    2
);
INSERT INTO Aluno
VALUES (
    279014,
    34567891234,
    'Rogerinho da Borracharia',
    36,
    305,
    1
);

INSERT INTO LotacaoTurma
VALUES (
    301212,
    'A',
    'HUM01085'
);
INSERT INTO LotacaoTurma
VALUES (
    290103,
    'U',
    'INF05501'
);
INSERT INTO LotacaoTurma
VALUES (
    279014,
    'U',
    'INF01154'
);


INSERT INTO EntradaCurriculo
VALUES (
    'HUM01085',
    101,
    329,
    null,
    'obrigatoria',
    3
);
INSERT INTO EntradaCurriculo
VALUES (
    'HUM01085',
    41,
    329,
    null,
    'obrigatoria',
    3
);
INSERT INTO EntradaCurriculo
VALUES (
    'INF01154',
    36,
    305,
    null,
    'obrigatoria',
    7
);


INSERT INTO PreRequisito
VALUES (
    'HUM01060',
    'HUM01085',
    41,
    329
);
INSERT INTO PreRequisito
VALUES (
    'HUM01085',
    'HUM01087',
    41,
    329
);
INSERT INTO PreRequisito
VALUES (
    'INF05501',
    'INF01154',
    36,
    305
);
