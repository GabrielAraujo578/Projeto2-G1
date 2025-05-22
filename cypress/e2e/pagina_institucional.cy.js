describe('Página institucional', () => {
  it('deve exibir as informações da instituição ao clicar no botão "Sobre a Instituição"', () => {
    cy.visit('http://localhost:8000')
    cy.contains('Sobre a Instituição').click();
    cy.contains('Sobre a Solidare').should('be.visible')
    cy.contains('Nossa Missão').should('be.visible')
    cy.contains('Nossa História').should('be.visible')
    cy.contains('Nossos Valores').should('be.visible')
  })
})
