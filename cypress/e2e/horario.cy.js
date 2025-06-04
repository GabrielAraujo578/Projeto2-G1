describe('Visualização de horário após matrícula', () => {
  const nomeTurma = `Turma Horário ${Date.now()}`

  beforeEach(() => {
    cy.deletedatabase(); 
  });

  it('aluno se matricula e vê a turma no horário correto', () => {
    cy.loginProfessor()
    cy.contains('Gerenciar Turmas').click()
    cy.criarTurma(nomeTurma, 'Terça-feira', '08:00', '10:00', 'Turma para teste de horário')

    cy.get('@codigoTurma').then((codigoTurma) => {
      cy.loginAluno()
      cy.contains('Minhas Turmas').click()

      cy.get('button.btn-matricular').should('be.visible').click()
      cy.get('input[name="codigo"]').type(codigoTurma)
      cy.get('button.btn-acessar').contains('Matricular').click()

      cy.visit('http://localhost:8000/aluno/')
      cy.contains('Horário').click()

      cy.get('.horario-grid')
        .find('.aula-marcada')
        .contains(nomeTurma) 
        .should('exist')
    })
  })
})

