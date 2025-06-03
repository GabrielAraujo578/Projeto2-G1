describe('Criar turma', () => {
  beforeEach(() => {
    cy.deletedatabase(); 
    cy.loginProfessor()
    cy.contains('Gerenciar Turmas').click()
  })

  it('deve criar uma turma com sucesso', () => {
    const nomeTurma = `Turma Teste ${Date.now()}`
    cy.criarTurma(nomeTurma, 'Segunda-feira', '08:00', '10:00', 'Descrição turma testes')
    cy.contains(nomeTurma).should('exist')
  })

  it('não deve criar turma sem nome', () => {
    cy.get('button.btn-criar').click()
    cy.get('select.modal-input').select('Terça-feira')
    cy.get('input[name="hora_inicio[]"]').type('09:00')
    cy.get('input[name="hora_fim[]"]').type('11:00')
    cy.get('textarea.modal-input').type('Descrição sem nome')
    cy.contains('button', 'Criar Turma').click()
    cy.get('input.modal-input').then($input => {
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
  })

  it('não deve criar turma sem horário', () => {
    const nomeTurma = `Turma Teste ${Date.now()}`
    cy.get('button.btn-criar').click()
    cy.get('input.modal-input').type(nomeTurma)
    cy.get('select.modal-input').select('Quarta-feira')
    cy.get('textarea.modal-input').type('Descrição sem horário')
    cy.contains('button', 'Criar Turma').click()
    cy.get('input[name="hora_inicio[]"]').then($input => {
      expect($input[0].validationMessage).to.eq('Preencha este campo.')
    })
  })

  it('deve cancelar criação de turma', () => {
    cy.get('.turma-titulo').then($turmasAntes => {
      const qtdAntes = $turmasAntes.length
      cy.get('button.btn-criar').click()
      cy.get('input.modal-input').type('Turma que será cancelada')
      cy.contains('button', 'Cancelar').click()
      cy.wait(1000)
      cy.get('.turma-titulo').should('have.length', qtdAntes)
    })
  })
})

