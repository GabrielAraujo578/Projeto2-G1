describe('Ver meus horários', () => {
  it('faz login como aluno e acessa a aba de horários', () => {
    cy.visit('http://localhost:8000') 
    cy.contains('Login').click();
    cy.get('#id_email').type('chaves@email.com')     
    cy.get('#id_password').type('Aluno123') 
    cy.get('button.btn').click()
    cy.contains('Horário').click()
    cy.contains('Segunda') 
  })
})
