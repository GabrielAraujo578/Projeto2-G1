describe('Visualização de horário após matrícula', () => {
  const nomeTurma = `Turma Horário ${Date.now()}`

  it('aluno se matricula e vê a turma no horário correto', () => {
    cy.loginProfessor()
    cy.contains('Gerenciar Turmas').click()
    cy.criarTurma(nomeTurma, 'Quinta-feira', '15:00', '17:00', 'Turma para teste de horário')

    cy.get('@codigoTurma').then((codigoTurma) => {
      cy.loginAluno()
      cy.contains('Minhas Turmas').click()

      cy.get('i.fas.fa-plus').click()
      cy.get('input[name="codigo"]').type(codigoTurma)
      cy.contains('Matricular').click()

      cy.contains(nomeTurma).should('exist')

      cy.visit('http://127.0.0.1:8000/aluno/')
      cy.contains('Horários').click()

      cy.get('.horario-grid')
        .find('.aula-marcada')
        .contains(nomeTurma) 
        .should('exist')
    })
  })
})

