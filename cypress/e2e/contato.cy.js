describe('Página institucional', () => {
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000')
    cy.contains('Sobre a Instituição').click()
  })


  it('1. deve permitir enviar o formulário com todos os campos preenchidos e exibir confirmação', () => {
    cy.get('#nome').type('João da Silva')
    cy.get('#email').type('joao@email.com')
    cy.get('#assunto').type('Dúvida sobre matrícula')
    cy.get('#mensagem').type('Gostaria de saber como realizar a matrícula no curso.')


    cy.contains('Enviar Mensagem').click()


    cy.url().should('include', '/confirmacao_email/')
    cy.contains('Mensagem Enviada!').should('be.visible')
  })


  it('2. deve exibir mensagem de erro ao tentar enviar sem preencher o nome', () => {
    cy.get('#email').type('joao@email.com')
    cy.get('#assunto').type('Dúvida sobre matrícula')
    cy.get('#mensagem').type('Gostaria de saber como realizar a matrícula no curso.')


    cy.contains('Enviar Mensagem').click()
    cy.get('#nome').then(($input) => {
      expect($input[0].checkValidity()).to.be.false
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
  })


  it('3. deve exibir mensagem de erro ao tentar enviar sem preencher o email', () => {
    cy.get('#nome').type('João da Silva')
    cy.get('#assunto').type('Dúvida sobre matrícula')
    cy.get('#mensagem').type('Gostaria de saber como realizar a matrícula no curso.')


    cy.contains('Enviar Mensagem').click()
    cy.get('#email').then(($input) => {
      expect($input[0].checkValidity()).to.be.false
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
  })


  it('4. deve exibir mensagem de erro ao tentar enviar sem preencher o assunto', () => {
    cy.get('#nome').type('João da Silva')
    cy.get('#email').type('joao@email.com')
    cy.get('#mensagem').type('Gostaria de saber como realizar a matrícula no curso.')


    cy.contains('Enviar Mensagem').click()
    cy.get('#assunto').then(($input) => {
      expect($input[0].checkValidity()).to.be.false
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
  })


  it('5. deve exibir mensagem de erro ao tentar enviar sem preencher a mensagem', () => {
    cy.get('#nome').type('João da Silva')
    cy.get('#email').type('joao@email.com')
    cy.get('#assunto').type('Dúvida sobre matrícula')


    cy.contains('Enviar Mensagem').click()
    cy.get('#mensagem').then(($input) => {
      expect($input[0].checkValidity()).to.be.false
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
  })
})


