describe('Ver o calendário', () => {
  it('faz login como aluno e acessa a aba calenário', () => {
    cy.visit('http://localhost:8000') 
    cy.contains('Login').click();
    cy.get('#id_email').type('chaves@email.com')     
    cy.get('#id_password').type('Aluno123') 
    cy.get('button.btn').click()
    cy.contains('Calendário').click()
    const meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    const data = new Date()
    const mesAtual = meses[data.getMonth()]
    const anoAtual = data.getFullYear()
    cy.get('h2#monthYear').should('be.visible').and('contain', `${mesAtual} ${anoAtual}`) 
  })
})