describe('Gerenciamento de conteúdo da turma', () => {
  const nomeTurma = `Turma Conteúdo Teste ${Date.now()}`

  beforeEach(() => {
    cy.loginProfessor()
    cy.contains('Gerenciar Turmas').click()
    cy.criarTurma(nomeTurma, 'Quinta-feira', '15:00', '17:00', 'Turma para teste de conteúdo')
    cy.contains(nomeTurma).parent().within(() => {
      cy.get('a.btn-gerenciar').click()
    })
  })

  it('deve adicionar conteúdo sem upload de arquivo', () => {
    cy.adicionarConteudo('Conteúdo sem arquivo', 'Descrição sem arquivo')
    cy.contains('Conteúdo sem arquivo').should('exist')
    cy.contains('Descrição sem arquivo').should('exist')
  })

  it('não deve adicionar conteúdo sem título', () => {
    cy.get('button.btn-adicionar').click()
    cy.get('textarea[name="descricao"]').type('Descrição sem título')
    cy.get('input[type="file"]').selectFile('cypress/fixtures/exemplo.pdf')
    cy.get('button[type="submit"]').contains('Adicionar').click()
    cy.get('input[name="titulo"]').then($input => {
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
    cy.get('div.modal').should('be.visible')
  })

  it('deve cancelar a adição de conteúdo', () => {
    cy.get('button.btn-adicionar').click()
    cy.get('input[name="titulo"]').type('Conteúdo que será cancelado')
    cy.get('textarea[name="descricao"]').type('Descrição cancelada')
    cy.contains('button', 'Cancelar').click()
    cy.get('div.modal').should('not.exist')
    cy.contains('Conteúdo que será cancelado').should('not.exist')
  })
})

