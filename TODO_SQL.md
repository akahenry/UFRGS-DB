# Estado do Projeto de MySQL
## ENTIDADES MODELADOS ATÉ AGORA:
- Pessoa
- Educador
- Aluno
- Turma
- Prédio
- Sala
- Bolsa de graduação
- Iniciação Científica
- Monitoria
- Disciplina
- Departamento

## ESCLARECIMENTOS
- Atualmente, em dois sites que testei, não funciona esse código (um outro funciona (??))
- Para pessoa-educador-aluno eu fiz 3 tabelas, uma pra cada
- tive que criar uma tabela só pra pro relacionamento entre aluno e turma (n:m), se chama lotacaoTurma
- supus que cada turma pode ter no maximo 2 professores (1 de aula e 1 de lab), pra não precisar criar uma tabela nova só pra isso
- Criei apenas uma tabela para bolsa de graduação, Iniciação Científica e Monitoria

## DUVIDAS
- primary key do departamento fica como o seu nome (varchar) mesmo?
- deixar Bolsa em uma única tabela?
- como armazenar conta bancária? atualmente contaBanco, contaAgencia e contaNumero
- será que deveriamos juntar bolsa com aluno? agora um aluno poderia ter mais de uma bolsa, mas caso seja 1:1 é considerável...

## TODO (deixados para trás)
- Guardar o horário das turmas da maneira certa