describe('aluno acessa turmas', () => {
  const tituloConteudo = `Conteúdo Aula ${Date.now()}`
  const descricaoConteudo = 'Descrição do conteúdo para teste completo.'
  let nomeTurma = ''
  let codigoTurma = ''

  before(() => {
    cy.deletedatabase()
  })

  beforeEach(() => {
    nomeTurma = `Turma Completa ${Date.now()}`

    cy.loginProfessor()
    cy.contains('Gerenciar Turmas').click()
    cy.criarTurma(nomeTurma, 'Segunda-feira', '14:00', '16:00', 'Turma criada para teste completo')

    cy.contains(nomeTurma).closest('.turma-card').within(() => {
      cy.get('div.turma-codigo').invoke('text').then(codigo => {
        codigoTurma = codigo.replace('Código: ', '').trim()
      })
      cy.get('a.btn-gerenciar').click()
    })

    cy.url().should('include', '/turma/')
    cy.adicionarConteudo(tituloConteudo, descricaoConteudo, 'cypress/fixtures/exemplo.pdf')
  })

  it('professor adiciona conteúdo e aluno se matricula', () => {
    cy.contains(tituloConteudo).should('exist')
    cy.contains(descricaoConteudo).should('exist')

    cy.loginAluno()
    cy.contains('Minhas Turmas').click()
    cy.get('button.btn-matricular').should('be.visible').click()
    cy.get('input[name="codigo"]').type(codigoTurma)
    cy.get('button.btn-acessar').contains('Matricular').click()

    cy.url().should('include', '/aluno/')
    cy.contains('Minhas Turmas').click()

    cy.contains(nomeTurma).should('exist')
    cy.contains(nomeTurma).closest('.turma-card').within(() => {
      cy.get('a.btn-acessar').click()
    })

    cy.contains(tituloConteudo).should('exist')
    cy.contains(descricaoConteudo).should('exist')
    cy.get('a').contains('Download')
      .should('have.attr', 'href')
      .and('include', 'exemplo')
  })

  it('não matricula com código errado e não mostra turma em Minhas Turmas', () => {
    cy.loginAluno()
    cy.contains('Minhas Turmas').click()
    cy.get('button.btn-matricular').should('be.visible').click()
    cy.get('input[name="codigo"]').type('codigoErrado123')
    cy.get('button.btn-acessar').contains('Matricular').click()
    cy.contains(nomeTurma).should('not.exist')
  })

  it('abre modal de matrícula e clica em cancelar, não se matricula', () => {
    cy.loginAluno()
    cy.contains('Minhas Turmas').click()
    cy.get('button.btn-matricular').should('be.visible').click()
    cy.get('input[name="codigo"]').type(codigoTurma)
    cy.get('button.btn-acessar').contains('Cancelar').click()
    cy.contains(nomeTurma).should('not.exist')
  })
})
