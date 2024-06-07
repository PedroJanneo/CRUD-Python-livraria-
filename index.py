from flask import Flask, redirect,render_template, request, redirect, flash, session

from flask_sqlalchemy import SQLAlchemy

import bcrypt

app = Flask(__name__)

# a linha abaixo cria uma chave de segurança
app.secret_key = 'pythonedemais'



app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector', 
        usuario = 'aluno',
        senha = 'toor',
        servidor = 'localhost',
        database = 'livraria'
    )

db = SQLAlchemy(app)

class Livros(db.Model):
      id_livro = db.Column(db.Integer, primary_key=True,autoincrement=True)
      titulo_livro = db.Column(db.String(50), nullable=False)
      editora_livro = db.Column(db.String(40), nullable=False)
      autor_livro = db.Column(db.String(50), nullable=False)
      preco_livro = db.Column(db.Float, nullable=False)
      avaliacao = db.Column(db.String(10), nullable=True)

      def __repr__(self):
            return '<Name %r>' % self.name
      
class Usuarios(db.Model):
     id_usuario = db.Column(db.Integer, primary_key=True,autoincrement=True)
     nome_usuario = db.Column(db.String(50),nullable=False)
     email_usuario = db.Column(db.String(50),nullable=False)
     senha_usuario = db.Column(db.String(255), nullable=False)

     def __repr__(self):
            return '<Name %r>' % self.name
     
# Função para obter o nome do usuário logado
def usuario_logado():
    return session.get('usuario_logado')

# Registrar a função como um contexto global
@app.context_processor
def inject_user():
    return dict(usuario_logado=usuario_logado)

@app.route('/inicio')
def ola():
        return'<h1> Iniciando flask</h1>'


    #DADOS DO USUARIO   
@app.route('/cadastrar_usuario')
def cadastrar_usuarios():
     return render_template('cadastrar_usuario.html')

@app.route('/cadastro', methods=['POST'])
def adicionar_usuario():
    nome_usu = request.form['txtNome']
    email_usu = request.form['txtEmail']
    senha_usuario = request.form['txtSenha']
    
   
    if Usuarios.query.filter_by(nome_usuario=nome_usu).first():
        flash("Nome de usuário já está em uso. Escolha outro nome de usuário.", 'erro')
        return redirect('/cadastrar_usuario') 

    # Verifica se o e-mail já está em uso
    if Usuarios.query.filter_by(email_usuario=email_usu).first():
        flash("Este email já está registrado. Por favor, use outro endereço de email.", 'erro')
        return redirect('/cadastrar_usuario')


    senha_usu = senha_usuario.encode('utf-8')
    hashed_password = bcrypt.hashpw(senha_usu, bcrypt.gensalt())

    # Cria um novo usuário e o adiciona ao banco de dados
    novo_usuario = Usuarios(nome_usuario=nome_usu, email_usuario=email_usu, senha_usuario=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()
    flash("Usuário cadastrado com sucesso", 'success')
    
    
    return redirect('/lista_cadastrados')
@app.route('/cadastro_novo', methods=['POST'])
def adicionar_usuario_novo():
    nome_usu = request.form['txtNome']
    email_usu = request.form['txtEmail']
    senha_usuario = request.form['txtSenha']
    
    # Verifica se o nome de usuário já está em uso
    if Usuarios.query.filter_by(nome_usuario=nome_usu).first():
        flash("Nome de usuário já está em uso. Escolha outro nome de usuário.", 'erro')
        return redirect('/cadastrar_usuario')  # Altere para a rota correta

    # Verifica se o e-mail já está em uso
    if Usuarios.query.filter_by(email_usuario=email_usu).first():
        flash("Este email já está registrado. Por favor, use outro endereço de email.", 'erro')
        return redirect('/cadastrar_usuario')  # Altere para a rota correta

    # Codifica a senha do usuário em bytes e em seguida criptografa usando bcrypt
    senha_usu = senha_usuario.encode('utf-8')
    hashed_password = bcrypt.hashpw(senha_usu, bcrypt.gensalt())

    # Cria um novo usuário e o adiciona ao banco de dados
    novo_usuario = Usuarios(nome_usuario=nome_usu, email_usuario=email_usu, senha_usuario=hashed_password)
    db.session.add(novo_usuario)
    db.session.commit()
    flash("Usuário cadastrado com sucesso", 'success')
    
    
    return redirect('/lista_cadastrados')


@app.route('/login', methods=['GET'])
def exibir_formulario_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def processar_login():
    email = request.form['Email']
    senha = request.form['Senha']
    
    # Tenta encontrar o usuário pelo e-mail no banco de dados
    usuario = Usuarios.query.filter_by(email_usuario=email).first()
    if usuario:
        # Se o usuário existe, verifica se a senha não criptografada é igual à senha armazenada no banco de dados
        if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha_usuario.encode('utf-8')):
            # Se as senhas coincidirem, loga o usuário e redireciona para a página de lista
            session['usuario_logado'] = usuario.nome_usuario
            flash("Login efetuado com sucesso", 'success')
            return redirect("/lista")
    
    # Se o usuário não existir ou as senhas não coincidirem, exibe uma mensagem de erro e redireciona de volta para a página de login
    flash("E-mail ou senha incorretos", 'error')
    return redirect("/login")
@app.route('/lista_cadastrados')     
def lista_user():
         
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect('/login')
    
    contas_cadastradas = Usuarios.query.order_by(Usuarios.id_usuario)

    return render_template('lista_cadastrados.html', desc = 'Usuarios cadastrados', cadas = contas_cadastradas)

@app.route('/excluir/<int:idU>')
def excluir_user(idU):
     

    Usuarios.query.filter_by(id_usuario=idU).delete()
                           
    db.session.commit() 
    flash("Usuario EXCLUIDO com sucesso", 'success')
    return redirect('/lista_cadastrados')

@app.route('/editar/<int:idU>') 
def editar_user(idU):   

    usuario_selecionado = Usuarios.query.filter_by(id_usuario=idU).first() 

    return render_template('editar_usuario.html', usuarios = usuario_selecionado)

@app.route('/atualiza' , methods=['POST', ])
def atualiza_cadastro():
     

    usuarios = Usuarios.query.filter_by(id_usuario=request.form['txtId_usu']).first()

    usuarios.nome_usuario=request.form['txtNome']
    usuarios.email_usuario=request.form['txtEmail']
    usuarios.senha_usuario=request.form['txtSenha']

    db.session.add(usuarios)

    db.session.commit()

    flash("Usuario EDITADO com sucesso", 'success')
   
    return redirect('/lista_cadastrados')



    #DADOS LIVROS
        
@app.route('/lista')
def lista():

 
    livros_cadastrados = Livros.query.order_by(Livros.id_livro)
    return render_template('lista.html', descricao="Livros cadastrados", lista_liv=livros_cadastrados)

@app.route('/cadastrar' )
def cadastrar_livros():
    
    return render_template('cadastrar.html')

@app.route('/adiciona', methods=['POST',] )
def adicionar_livros():

    titulo_liv = request.form ['txtTitulo']

    editora_liv = request.form ['txtEditora']

    autor_liv = request.form ['txtAutor']

    preco_liv = request.form['txtPreco'].replace(',','.') 

    preco_liv = float(preco_liv)

    livro_adicionado = Livros(titulo_livro = titulo_liv, 
                             editora_livro = editora_liv, 
                             preco_livro= preco_liv,
                             autor_livro= autor_liv)


    db.session.add(livro_adicionado)

    db.session.commit()
    flash(" Livro cadastrado com sucesso!!", 'success')

    return redirect('/lista')


@app.route('/editar_livro/<int:idL>') 
def editar_livros(idL):   

    livro_selecionado = Livros.query.filter_by(id_livro=idL).first() 

    return render_template('editar.html', livros=livro_selecionado)

@app.route('/atualizar', methods=['POST'])
def atualiza_registro_livro():

    livros = Livros.query.filter_by(id_livro=request.form['txtId_liv']).first()

    livros.titulo_livro = request.form['txtTitulo']

    livros.editora_livro = request.form['txtEditora']

    livros.autor_livro = request.form['txtAutor']

    livros.preco_livro = request.form['txtPreco']

    db.session.add(livros)

    db.session.commit()

    flash("Livro editado com sucesso", 'success')

    return redirect('/lista')

@app.route('/excluir_livro/<int:idL>')
def excluir_livros(idL):

    Livros.query.filter_by(id_livro=idL).delete()

    db.session.commit() 

    flash("Livro EXCLUIDO com sucesso", 'success')

    return redirect('/lista')


@app.route('/avaliar_livros/<int:idL>', methods=['GET'])
def avaliar_livros(idL):
    livro_selecionado = Livros.query.get(idL)  
    return render_template('avaliacao.html', livros=livro_selecionado)

@app.route('/avaliar_livros/<int:idL>', methods=['POST'])
def salvar_avaliacao(idL):
    livro = Livros.query.get(idL)
    avaliacao = request.form['txtAvaliacao_{}'.format(idL)]  
    livro.avaliacao = avaliacao  
    db.session.commit()  
    flash("Avaliação salva com sucesso", 'success')
    return redirect('/lista')


app.run()
