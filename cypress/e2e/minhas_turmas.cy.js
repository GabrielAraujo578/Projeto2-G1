describe('aluno acessa turmas', () => {
  const nomeTurma = `Turma Completa ${Date.now()}`
  const tituloConteudo = `Conteúdo Aula ${Date.now()}`
  const descricaoConteudo = 'Descrição do conteúdo para teste completo.'

  it('professor cria turma, adiciona conteúdo e aluno se matricula', () => {
    cy.loginProfessor()
    cy.contains('Gerenciar Turmas').click()
    cy.criarTurma(nomeTurma, 'Segunda-feira', '14:00', '16:00', 'Turma criada para teste completo')

    cy.contains(nomeTurma).parent().within(() => {
      cy.get('a.btn-gerenciar').click()
      cy.get('div.turma-codigo').invoke('text').as('codigoTurma')
    })

    cy.adicionarConteudo(tituloConteudo, descricaoConteudo, 'cypress/fixtures/exemplo.pdf')

    cy.contains(tituloConteudo).should('exist')
    cy.contains(descricaoConteudo).should('exist')

    cy.loginAluno()
    cy.contains('Minhas Turmas').click()
    cy.get('@codigoTurma').then(codigo => {
      cy.get('i.fas.fa-plus').click()
      cy.get('input[name="codigo"]').type(codigo)
      cy.get('button.btn-acessar').contains('Matricular').click()
    })

    cy.contains(nomeTurma).should('exist')
    cy.contains(nomeTurma).parent().within(() => {
      cy.get('a.btn-acessar').click()
    })

    cy.contains(tituloConteudo).should('exist')
    cy.contains(descricaoConteudo).should('exist')
    cy.get('a').contains('Download').should('have.attr', 'href').and('include', 'exemplo.pdf')
  })

  it('não matricula com código errado e não mostra turma em Minhas Turmas', () => {
    cy.loginAluno()
    cy.contains('Minhas Turmas').click()

    cy.get('i.fas.fa-plus').click()
    cy.get('input[name="codigo"]').type('codigoErrado123')
    cy.get('button.btn-acessar').contains('Matricular').click()

    cy.contains(nomeTurma).should('not.exist')
  })

  it('abre modal de matrícula e clica em cancelar, não se matricula', () => {
    cy.loginAluno()
    cy.contains('Minhas Turmas').click()

    cy.get('i.fas.fa-plus').click()
    cy.get('@codigoTurma').then(codigo => {
      cy.get('input[name="codigo"]').type(codigo)

      cy.get('button.btn-acessar').contains('Cancelar').click()
    })

    cy.contains(nomeTurma).should('not.exist')
  })
})
