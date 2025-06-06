describe('Chat entre aluno e professor', () => {
  const mensagemAluno = 'Olá, professor!'
  const respostaProfessor = 'Olá, aluno! Mensagem recebida.'


  it('deve permitir troca de mensagens entre aluno e professor', () => {
    cy.loginAluno()
    cy.get('button[onclick*="/chat/aluno/"]').click()
    cy.url().should('include', '/chat/aluno/')
    cy.get('input[name="mensagem"]').type(mensagemAluno)
    cy.get('button[type="submit"]').click()
    cy.contains(mensagemAluno).should('be.visible')


    cy.loginProfessor()
    cy.get('button[onclick*="/chat/professor/"]').click()
    cy.url().should('include', '/chat/professor/')
    cy.get('a.aluno-link').first().click()
    cy.url().should('match', /\/chat\/professor\/\d+\//)
    cy.contains(mensagemAluno).should('be.visible')
    cy.get('input[name="mensagem"]').type(respostaProfessor)
    cy.get('button[type="submit"]').click()
    cy.contains(respostaProfessor).should('be.visible')


    cy.loginAluno()
    cy.get('button[onclick*="/chat/aluno/"]').click()
    cy.url().should('include', '/chat/aluno/')
    cy.contains(respostaProfessor).should('be.visible')
  })
})

