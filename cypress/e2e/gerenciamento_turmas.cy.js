describe('Gerenciamento de turmas', () => {
  beforeEach(() => {
    cy.visit('http://localhost:8000')
    cy.contains('Login').should('be.visible').click()
    cy.get('#id_email').should('be.visible').type('girafales@email.com')
    cy.get('#id_password').should('be.visible').type('Professor123')
    cy.get('button.btn').should('be.visible').click()
    cy.contains('Gerenciar Turmas').should('be.visible').click()
  })


  it('deve criar uma turma com sucesso', () => {
    cy.get('button.btn-criar').should('be.visible').click()
    cy.get('input.modal-input').should('be.visible').type('Turma testes testes')
    cy.get('select.modal-input').should('be.visible').select('Segunda-feira')
    cy.get('input[name="hora_inicio[]"]').should('be.visible').type('08:00')
    cy.get('input[name="hora_fim[]"]').should('be.visible').type('10:00')
    cy.get('textarea.modal-input').should('be.visible').type('Descrição turma testes')
    cy.contains('button', 'Criar Turma').should('be.visible').click()
    cy.contains('Turma testes testes').should('exist')
  })


  it('não deve criar turma sem nome', () => {
    cy.get('.turma-titulo').then($turmasAntes => {
      const qtdAntes = $turmasAntes.length


      cy.get('button.btn-criar').should('be.visible').click()
      cy.get('select.modal-input').should('be.visible').select('Terça-feira')
      cy.get('input[name="hora_inicio[]"]').should('be.visible').type('09:00')
      cy.get('input[name="hora_fim[]"]').should('be.visible').type('11:00')
      cy.get('textarea.modal-input').should('be.visible').type('Descrição sem nome')
      cy.contains('button', 'Criar Turma').should('be.visible').click()


      cy.wait(1000)
      cy.get('.turma-titulo').should('have.length', qtdAntes)
    })
  })


  it('não deve criar turma sem horário', () => {
    cy.get('.turma-titulo').then($turmasAntes => {
      const qtdAntes = $turmasAntes.length


      cy.get('button.btn-criar').should('be.visible').click()
      cy.get('input.modal-input').should('be.visible').type('Turma sem horário')
      cy.get('select.modal-input').should('be.visible').select('Quarta-feira')
      cy.get('textarea.modal-input').should('be.visible').type('Descrição sem horário')
      cy.contains('button', 'Criar Turma').should('be.visible').click()


      cy.wait(1000)
      cy.get('.turma-titulo').should('have.length', qtdAntes)
    })
  })


  it('deve cancelar criação de turma', () => {
    cy.get('.turma-titulo').then($turmasAntes => {
      const qtdAntes = $turmasAntes.length


      cy.get('button.btn-criar').should('be.visible').click()
      cy.get('input.modal-input').should('be.visible').type('Turma que será cancelada')
      cy.contains('button', 'Cancelar').should('be.visible').click()


      cy.wait(1000)
      cy.get('.turma-titulo').should('have.length', qtdAntes)
    })
  })


})
