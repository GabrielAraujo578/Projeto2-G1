// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
// Login genérico
// login do professor
Cypress.Commands.add('loginProfessor', () => {
  cy.visit('http://localhost:8000')
  cy.contains('Login').click()
  cy.get('#id_email').type('jirafales@email.com')
  cy.get('#id_password').type('Professor123')
  cy.get('button.btn').click()
})

// login do aluno
Cypress.Commands.add('loginAluno', () => {
  cy.visit('http://localhost:8000')
  cy.contains('Login').click()
  cy.get('#id_email').type('chaves@email.com')
  cy.get('#id_password').type('Aluno123')
  cy.get('button.btn').click()
})

// criar turma (retorna nome e código da turma)
Cypress.Commands.add('criarTurma', (nomeTurma, dia='Segunda-feira', horaInicio='14:00', horaFim='16:00', descricao='Descrição') => {
  cy.contains('Gerenciar Turmas').click()
  cy.get('button.btn-criar').click()
  cy.get('input.modal-input').type(nomeTurma)
  cy.get('select.modal-input').select(dia)
  cy.get('input[name="hora_inicio[]"]').type(horaInicio)
  cy.get('input[name="hora_fim[]"]').type(horaFim)
  cy.get('textarea.modal-input').type(descricao)
  cy.contains('button', 'Criar Turma').click()
  cy.contains(nomeTurma).parent().within(() => {
    cy.get('div.turma-codigo').invoke('text').then(text => {
      const codigo = text.replace('Código: ', '').trim()
      cy.wrap(codigo).as('codigoTurma')
    })
  })
})

// adicionar conteúdo na turma atual
Cypress.Commands.add('adicionarConteudo', (titulo, descricao, arquivo = null) => {
  cy.get('button.btn-adicionar').click()
  cy.get('input[name="titulo"]').type(titulo)
  cy.get('textarea[name="descricao"]').type(descricao)
  if (arquivo) {
    cy.get('input[type="file"]').selectFile(arquivo)
  }
  cy.get('button[type="submit"]').contains('Adicionar').click()
})

Cypress.Commands.add('deletedatabase', () => {
  cy.exec('set DJANGO_SETTINGS_MODULE=solidare.settings_test && python delete_database.py', {
    failOnNonZeroExit: false
  });
});


