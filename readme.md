# Sistema de leitura

Um sistema simples usando a framework flask (python), é um sistema simples, onde há o cadastramento de usuario e livros.

# Banco de dados:

Para o banco de dados eu usei o mysql workbench (o banco estara disponibilizado aqui).

# Uso:

- Usuario : os usuarios poderao fazer o cadastro, dando um nickname e email (no qual vão percorrer no banco, para ver se há dupicidade, se tiver, dará um flash (alert)), e uma senha (na qual sera criptografada com bcrypt), e tera a opção de sair, para troca de conta. Na aba 'lista de usuario' você poderá  escolher a opção editar perfil, podendo mudar o email, nickname e senha, e  tera a opção de exclusão de perfil.

- Livros : seguindo o padrão do crud, podera cadastrar ( com titulo, autor, editora e preço), excluir e editar, coloquei uma opção onde há um sistema de avaliação.

# Futuros updates:
- Pretendo colocar um sistema de niveis de permissao, onde so quem tem o cadastro ADM possa cadastar livros e usuarios (podendo editar e excluir livremente), e quem for USUARIO, so ver a lista de livros e conseguir avaliar (somente).

- Sistema de paginas lidas (ex: 12/300)

# Tecnologias usadas:

- ``Python``
- ``Flask``
- ``CSS``
- ``Botstrap``
- ``HTML``
- ``Banco de dados``