# Estado do Projeto de MySQL
## ESCLARECIMENTOS
- Todas entidades já foram modeladas, só falta revisar e testar
- Para pessoa-educador-aluno eu fiz 3 tabelas, uma pra cada
- tive que criar uma tabela só pra pro relacionamento entre aluno e turma (n:m), se chama LotacaoTurma
- tive que criar uma tabela só pro relacionamento pré requisitos, se chama PreRequisito
- supus que cada turma pode ter no maximo 2 professores (1 de aula e 1 de lab), pra não precisar criar uma tabela nova só pra isso
- Criei apenas uma tabela para bolsa de graduação, Iniciação Científica e Monitoria, se chama Bolsa

## DUVIDAS
- criar id para primary key do Departamento (tá com um varchar), EntradaCurriculo (tá com uma tripla) e PreRequisito (ta com uma quadrupla)? Criei ids pra curso e educador....
- como armazenar conta bancária? atualmente contaBanco, contaAgencia e contaNumero
- será que deveriamos juntar bolsa com aluno? agora a chave primaria da bolsa é o cartão de um aluno, pra ter certeza de que não vai ter mais de uma bolsa por aluno

## TODO (deixados para trás)
- Guardar o horário das turmas da maneira certa