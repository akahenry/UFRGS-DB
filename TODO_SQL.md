# Estado do Projeto de MySQL
## ESCLARECIMENTOS
- Todas entidades já foram modeladas, só falta revisar e testar
- Para pessoa-educador-aluno eu fiz 3 tabelas, uma pra cada
- tive que criar uma tabela só pra pro relacionamento entre aluno e turma (n:m), se chama LotacaoTurma
- tive que criar uma tabela só pro relacionamento pré requisitos, se chama PreRequisito
- supus que cada turma pode ter no maximo 2 professores (1 de aula e 1 de lab), pra não precisar criar uma tabela nova só pra isso
- Criei apenas uma tabela para bolsa de graduação, Iniciação Científica e Monitoria, se chama Bolsa
- Para o relacionamento bolsa-aluno, fizemos uma referencia a bolsa no aluno com uma chave estrangeira e única
- só pode uma turma por bolsa de monitoria...
- tem mais de um grupo de matrícula por habilitação (grrr)
- horario das turmas é varchar

## DUVIDAS
- criar id para primary key do LotacaoTurma (tá com uma tripla), EntradaCurriculo (tá com uma tripla) e PreRequisito (tá com uma quadrupla)? Criei ids pra departamento, curso e educador....

## ON UPDATES E ON DELETES PERIGOSOS/ESTRANHOS
- DELETE educador -> bolsa CASCADE
- DELETE educador -> turma SET NULL
- DELETE sala -> turma SET NULL

## TODO (deixados para trás)
- checar todos os not null
- Setar valores default