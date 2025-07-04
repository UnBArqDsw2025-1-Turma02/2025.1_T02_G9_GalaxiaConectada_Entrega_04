import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, abort, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from functools import wraps

# --- CORREÇÃO APLICADA AQUI: PROJECT_ROOT definido no escopo global ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# --- FIM DA CORREÇÃO ---

app = Flask(__name__,
            template_folder=os.path.join(PROJECT_ROOT, 'frontend'),
            static_folder=os.path.join(PROJECT_ROOT, 'frontend'))

print(f"DEBUG: Project Root: {PROJECT_ROOT}")
print(f"DEBUG: Flask Template Folder: {app.template_folder}")
print(f"DEBUG: Flask Static Folder: {app.static_folder}")


# Configurações do banco de dados
DB_DIR = os.path.join(PROJECT_ROOT, 'backend', 'db_data')
DATABASE = os.path.join(DB_DIR, 'galaxia.db')
print(f"DEBUG: Database Path: {DATABASE}")

# Chave secreta para sessões
app.secret_key = 'uma_chave_secreta_muito_segura_e_longa_para_o_galaxia_conectada' 

# Importar models aqui para evitar problemas de importação circular
from .models import Usuario, Perfil, PetBase, UserPet, PetItem, Conteudo, Artigo, Video, Quiz, Jogo, QuestaoQuiz, AlternativaQuiz, TentativaQuiz, RespostaQuiz, Curtida, Comentario, Notificacao, InscricaoCategoria, TrilhaEducacional, Modulo, ConteudoModulo, ProgressoUsuarioTrilha, ProgressoModulo, ProgressoConteudo, Conquista, UsuarioConquista, Subforum, Topico, Postagem, VotoPostagem

# Função auxiliar para conectar ao banco de dados
def get_db_connection():
    print(f"DEBUG: Tentando conectar ao DB em: {DATABASE}")
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Decoradores de Autenticação e Autorização ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('entrar'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('entrar'))
        if session.get('tipo_usuario') != 'Administrador':
            flash('Acesso negado. Você não tem permissões de administrador.', 'danger')
            abort(403) # Retorna um erro 403 Forbidden
        return f(*args, **kwargs)
    return decorated_function

def publisher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('entrar'))
        allowed_types = ['Administrador', 'Instrutor', 'ProfessorVoluntario']
        if session.get('tipo_usuario') not in allowed_types:
            flash('Acesso negado. Você não tem permissão para publicar conteúdo.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def content_creator_required(f): # Para criar/manter trilhas/módulos/conteúdos
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('entrar'))
        allowed_types = ['Administrador', 'Instrutor', 'ProfessorVoluntario']
        if session.get('tipo_usuario') not in allowed_types:
            flash('Acesso negado. Você não tem permissão para criar ou gerenciar conteúdo educacional.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('entrar'))
        allowed_types = ['Administrador', 'Moderador']
        if session.get('tipo_usuario') not in allowed_types:
            flash('Acesso negado. Você não tem permissões de moderação.', 'danger')
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

# --- Rotas Existentes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/entrar', methods=['GET', 'POST'])
def entrar():
    print("DEBUG: Rota /entrar acessada.")
    if request.method == 'POST':
        email_or_username = request.form['email_or_username']
        password = request.form['password']

        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM usuarios WHERE email = ? OR nome_usuario = ?', (email_or_username, email_or_username)).fetchone()
        conn.close()

        if user_data:
            user = Usuario(**user_data)
            if check_password_hash(user.senha_hash, password):
                session['user_id'] = user.id
                session['nome_usuario'] = user.nome_usuario
                session['tipo_usuario'] = user.tipo_usuario
                session['permissoes'] = json.loads(user_data['permissoes']) if user_data['permissoes'] else []
                flash(f'Bem-vindo, {user.nome_usuario}!', 'success')
                print(f"DEBUG: Usuário {user.nome_usuario} logado com sucesso. Redirecionando para profile.")
                
                # Redireciona para a rota genérica de perfil
                return redirect(url_for('user_profile'))
            else:
                flash('Senha incorreta.', 'danger')
                print("DEBUG: Tentativa de login falhou: senha incorreta.")
        else:
            flash('Usuário ou e-mail não encontrado.', 'danger')
            print("DEBUG: Tentativa de login falhou: usuário não encontrado.")
    
    print("DEBUG: Renderizando entrar.html.")
    return render_template('entrar.html')

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    print("DEBUG: Rota /cadastrar acessada.")
    if request.method == 'POST':
        nome_completo = request.form['nome_completo']
        email = request.form['email']
        nome_usuario = request.form['nome_usuario']
        senha = request.form['password']
        confirmar_senha = request.form['confirm_password']

        if senha != confirmar_senha:
            flash('As senhas não coincidem.', 'danger')
            print("DEBUG: Tentativa de cadastro falhou: senhas não coincidem.")
            return render_template('cadastrar.html', nome_completo=nome_completo, email=email, nome_usuario=nome_usuario)

        senha_hash = generate_password_hash(senha)
        data_cadastro = datetime.now().isoformat()
        tipo_usuario = 'Aluno' # Padrão para novos cadastros (Alunos)
        permissoes = [] 
        nivel_acesso = 1

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome_completo, email, nome_usuario, senha_hash, data_cadastro, tipo_usuario, permissoes, nivel_acesso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome_completo, email, nome_usuario, senha_hash, data_cadastro, tipo_usuario, json.dumps(permissoes), nivel_acesso))
            
            usuario_id = cursor.lastrowid
            
            cursor.execute('''
                INSERT INTO perfis (usuario_id, nivel, xp, bio)
                VALUES (?, ?, ?, ?)
            ''', (usuario_id, 1, 0, f'Olá, sou {nome_usuario} e estou explorando a Galáxia Conectada!'))

            conn.commit()
            flash('Cadastro realizado com sucesso! Faça login para começar.', 'success')
            print(f"DEBUG: Usuário {nome_usuario} cadastrado com sucesso. Redirecionando para login.")
            return redirect(url_for('entrar'))
        except sqlite3.IntegrityError:
            flash('E-mail ou nome de usuário já cadastrado.', 'danger')
            print("DEBUG: Tentativa de cadastro falhou: e-mail ou usuário já existe.")
            return render_template('cadastrar.html', nome_completo=nome_completo, email=email, nome_usuario=nome_usuario)
        except Exception as e:
            flash(f'Erro ao cadastrar: {e}', 'danger')
            print(f"DEBUG: Erro inesperado no cadastro: {e}")
            return render_template('cadastrar.html', nome_completo=nome_completo, email=email, nome_usuario=nome_usuario)
        finally:
            conn.close()
    
    return render_template('cadastrar.html', 
                           nome_completo=request.form.get('nome_completo', ''), 
                           email=request.form.get('email', ''), 
                           nome_usuario=request.form.get('nome_usuario', ''))

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        user_data = conn.execute('SELECT nome_usuario, tipo_usuario, permissoes FROM usuarios WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user_data:
            permissoes_list = json.loads(user_data['permissoes']) if user_data['permissoes'] else []
            # Contar notificações não lidas
            unread_notifications_count = 0
            notif_conn = get_db_connection()
            count_data = notif_conn.execute('SELECT COUNT(*) FROM notificacoes WHERE usuario_id = ? AND lida = 0', (user_id,)).fetchone()
            if count_data:
                unread_notifications_count = count_data[0]
            notif_conn.close()

            return dict(current_user=user_data['nome_usuario'], user_type=user_data['tipo_usuario'], logged_in=True, user_permissions=permissoes_list, unread_notifications_count=unread_notifications_count)
    return dict(current_user=None, user_type=None, logged_in=False, user_permissions=[], unread_notifications_count=0)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('nome_usuario', None)
    session.pop('tipo_usuario', None)
    session.pop('permissoes', None)
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('home'))

# --- Rota Genérica de Perfil ---
@app.route('/profile')
@login_required
def user_profile():
    user_type = session.get('tipo_usuario')
    if user_type == 'Administrador':
        return redirect(url_for('admin_profile'))
    elif user_type == 'Aluno':
        return redirect(url_for('aluno_profile'))
    elif user_type == 'Instrutor':
        return redirect(url_for('instrutor_profile'))
    elif user_type == 'ProfessorVoluntario':
        return redirect(url_for('professor_voluntario_profile'))
    elif user_type == 'Moderador':
        return redirect(url_for('moderador_profile'))
    else: # Tipo Visitante ou desconhecido
        return redirect(url_for('visitante_profile'))

# --- Rotas para o Painel do Administrador ---
@app.route('/admin/profile')
@admin_required 
def admin_profile():
    user_id = session['user_id']
    conn = get_db_connection()
    
    admin_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    admin_profile_data = conn.execute('SELECT * FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
    
    admin_user = Usuario(**admin_data) if admin_data else None
    admin_profile = Perfil(**admin_profile_data) if admin_profile_data else None

    other_users_data = conn.execute('SELECT u.id, u.nome_usuario, u.email, u.tipo_usuario, p.nivel, p.xp FROM usuarios u JOIN perfis p ON u.id = p.usuario_id WHERE u.id != ? ORDER BY u.nome_usuario', (user_id,)).fetchall()
    
    conn.close()

    users_for_management = []
    for user_row in other_users_data:
        users_for_management.append(dict(user_row))

    return render_template('admin_profile.html', 
                           admin_user=admin_user, 
                           admin_profile=admin_profile,
                           users_for_management=users_for_management,
                           user_types=['Aluno', 'Instrutor', 'ProfessorVoluntario', 'Moderador', 'Administrador', 'Visitante']) # Adicionado Visitante

@app.route('/admin/update_user_type', methods=['POST'])
@admin_required 
def update_user_type():
    user_id = request.form.get('user_id', type=int)
    new_type = request.form.get('new_type')

    if not user_id or not new_type:
        flash('Dados inválidos para atualização do tipo de usuário.', 'danger')
        return redirect(url_for('admin_profile'))

    allowed_types = ['Aluno', 'Instrutor', 'ProfessorVoluntario', 'Moderador', 'Administrador', 'Visitante']
    if new_type not in allowed_types:
        flash('Tipo de usuário inválido.', 'danger')
        return redirect(url_for('admin_profile'))

    conn = get_db_connection()
    try:
        if user_id == session['user_id']:
            flash('Você não pode alterar seu próprio tipo de usuário por aqui.', 'danger')
            return redirect(url_for('admin_profile'))

        conn.execute('UPDATE usuarios SET tipo_usuario = ? WHERE id = ?', (new_type, user_id))
        conn.commit()
        flash(f'Tipo de usuário para ID {user_id} atualizado para {new_type} com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar tipo de usuário: {e}', 'danger')
        print(f"DEBUG: Erro ao atualizar tipo de usuário: {e}")
    finally:
        conn.close()
    
    return redirect(url_for('admin_profile'))

# --- Lógica de Evolução do Pet ---
def verificar_evolucao_pet(user_pet): 
    # XP necessário para cada fase
    xp_para_fase2 = 150
    xp_para_fase3 = 300

    nova_fase = user_pet.fase_atual

    if user_pet.xp_acumulado >= xp_para_fase3:
        nova_fase = 3
    elif user_pet.xp_acumulado >= xp_para_fase2:
        nova_fase = 2
    else:
        nova_fase = 1
    
    if nova_fase != user_pet.fase_atual:
        user_pet.fase_atual = nova_fase
        return True # Houve evolução
    return False # Não houve evolução

# --- Rotas para o Perfil do Aluno ---
@app.route('/aluno/profile')
@login_required
def aluno_profile():
    if session.get('tipo_usuario') != 'Aluno' and session.get('tipo_usuario') != 'Administrador':
        flash('Acesso negado. Esta página é apenas para Alunos.', 'danger')
        abort(403)

    user_id = session['user_id']
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    profile_data = conn.execute('SELECT * FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
    
    user = Usuario(**user_data) if user_data else None
    profile = Perfil(**profile_data) if profile_data else None
    
    user_pet = None
    pet_base = None
    xp_percentage = 0 # Inicializa a porcentagem de XP

    # Tenta carregar o pet do usuário
    user_pet_data = conn.execute('SELECT * FROM user_pets WHERE usuario_id = ?', (user_id,)).fetchone()
    if user_pet_data:
        user_pet = UserPet(**user_pet_data)
        pet_base_data = conn.execute('SELECT * FROM pets_base WHERE id = ?', (user_pet.pet_base_id,)).fetchone()
        pet_base = PetBase(**pet_base_data) if pet_base_data else None
        
        # Verifica se o pet evoluiu (apenas para exibição, a atualização no DB é no add_xp)
        if pet_base:
            verificar_evolucao_pet(user_pet) # Atualiza a fase do objeto em memória
            
            # Calcula a porcentagem de XP para a barra de progresso
            # A fase 3 é o XP máximo para a barra (300 XP)
            xp_max_for_bar = 300 
            xp_percentage = min(100, max(0, round((user_pet.xp_acumulado / xp_max_for_bar) * 100)))

    conn.close()
    return render_template('aluno_profile.html', user=user, profile=profile, user_pet=user_pet, pet_base=pet_base, xp_percentage=xp_percentage)

@app.route('/aluno/choose_pet', methods=['GET', 'POST'])
@login_required
def choose_pet():
    if session.get('tipo_usuario') != 'Aluno' and session.get('tipo_usuario') != 'Administrador':
        flash('Acesso negado. Esta funcionalidade é apenas para Alunos.', 'danger')
        abort(403)

    user_id = session['user_id']
    conn = get_db_connection()
    
    # Verificar se o aluno já tem um pet
    existing_user_pet = conn.execute('SELECT id FROM user_pets WHERE usuario_id = ?', (user_id,)).fetchone()
    if existing_user_pet:
        flash('Você já tem um pet! Vá para o seu perfil para vê-lo.', 'info')
        conn.close()
        return redirect(url_for('aluno_profile'))

    # Carregar pets base disponíveis
    available_pets_data = conn.execute('SELECT * FROM pets_base').fetchall()
    available_pets = [PetBase(**row) for row in available_pets_data]

    if request.method == 'POST':
        pet_base_id = request.form.get('pet_base_id', type=int)
        nome_personalizado = request.form.get('nome_personalizado', '').strip()

        selected_pet_base = next((p for p in available_pets if p.id == pet_base_id), None)

        if not selected_pet_base:
            flash('Mascote inválido selecionado.', 'danger')
            conn.close()
            return redirect(url_for('choose_pet'))
        
        if not nome_personalizado:
            flash('Por favor, dê um nome ao seu mascote!', 'danger')
            conn.close()
            return render_template('choose_pet.html', available_pets=available_pets)

        try:
            # Inserir o novo pet na tabela user_pets
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO user_pets (usuario_id, pet_base_id, nome_personalizado, fase_atual, xp_acumulado, itens_equipados, ultima_atualizacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, selected_pet_base.id, nome_personalizado, 1, 0, json.dumps([]), datetime.now().isoformat()))
            
            conn.commit()
            flash(f'Parabéns! Você escolheu o(a) {nome_personalizado} ({selected_pet_base.nome}) como seu mascote!', 'success')
            return redirect(url_for('aluno_profile'))
        except Exception as e:
            flash(f'Erro ao escolher o mascote: {e}', 'danger')
            print(f"DEBUG: Erro ao escolher pet: {e}")
        finally:
            conn.close()

    return render_template('choose_pet.html', available_pets=available_pets)

@app.route('/aluno/pet/add_xp', methods=['POST'])
@login_required
def add_pet_xp():
    if session.get('tipo_usuario') != 'Aluno' and session.get('tipo_usuario') != 'Administrador':
        flash('Acesso negado.', 'danger')
        abort(403)

    user_id = session['user_id']
    xp_to_add = request.form.get('xp_to_add', type=int, default=0)
    moedas_to_add = request.form.get('moedas_to_add', type=int, default=0) # Nova variável para moedas

    if xp_to_add <= 0 and moedas_to_add <= 0:
        flash('Valor de XP ou moedas inválido.', 'danger')
        return redirect(url_for('aluno_profile'))

    conn = get_db_connection()
    try:
        user_pet_data = conn.execute('SELECT * FROM user_pets WHERE usuario_id = ?', (user_id,)).fetchone()
        if not user_pet_data:
            flash('Você precisa escolher um mascote primeiro!', 'info')
            return redirect(url_for('aluno_profile'))

        user_pet = UserPet(**user_pet_data)
        
        # Adiciona XP ao pet
        user_pet.xp_acumulado += xp_to_add
        
        # Verifica evolução do pet
        evoluiu = verificar_evolucao_pet(user_pet) 
        
        # Atualiza o pet no banco de dados
        conn.execute('UPDATE user_pets SET xp_acumulado = ?, fase_atual = ?, ultima_atualizacao = ? WHERE id = ?', 
                     (user_pet.xp_acumulado, user_pet.fase_atual, datetime.now().isoformat(), user_pet.id))
        
        # Adiciona XP e moedas ao perfil do usuário
        conn.execute('UPDATE perfis SET xp = xp + ? WHERE usuario_id = ?', (xp_to_add, user_id))
        # TODO: Adicionar moedas ao perfil (precisaria de uma coluna 'moedas' na tabela perfis)

        conn.commit()

        flash_message = f'Seu mascote ganhou {xp_to_add} XP!'
        if moedas_to_add > 0:
            flash_message += f' E você ganhou {moedas_to_add} Moedas Estelares!'
        if evoluiu:
            flash_message += f' E subiu para a Fase {user_pet.fase_atual}!'
        flash(flash_message, 'success')

    except Exception as e:
        flash(f'Erro ao adicionar XP/moedas ao mascote: {e}', 'danger')
        print(f"DEBUG: Erro ao adicionar XP/moedas ao pet: {e}")
    finally:
        conn.close()
    
    return redirect(url_for('aluno_profile'))

@app.route('/aluno/pet_shop')
@login_required
def pet_shop():
    if session.get('tipo_usuario') != 'Aluno' and session.get('tipo_usuario') != 'Administrador':
        flash('Acesso negado. Esta loja é apenas para Alunos.', 'danger')
        abort(403)

    user_id = session['user_id']
    conn = get_db_connection()
    
    user_pet_data = conn.execute('SELECT * FROM user_pets WHERE usuario_id = ?', (user_id,)).fetchone()
    user_pet = UserPet(**user_pet_data) if user_pet_data else None

    if not user_pet:
        flash('Você precisa ter um mascote para acessar a loja!', 'info')
        conn.close()
        return redirect(url_for('aluno_profile'))

    # Obter o tipo do pet base do usuário para filtrar itens compatíveis
    pet_base_data = conn.execute('SELECT tipo FROM pets_base WHERE id = ?', (user_pet.pet_base_id,)).fetchone()
    pet_type = pet_base_data['tipo'] if pet_base_data else 'Todos' # Fallback

    # Carregar itens compatíveis com o tipo de pet do usuário ou "Todos"
    available_items_data = conn.execute(
        'SELECT * FROM pet_items WHERE tipo_pet_compativel = ? OR tipo_pet_compativel = "Todos"', 
        (pet_type,)
    ).fetchall()
    available_items = [PetItem(**row) for row in available_items_data]

    conn.close()
    return render_template('pet_shop.html', user_pet=user_pet, available_items=available_items)

@app.route('/aluno/pet/equip_item', methods=['POST'])
@login_required
def equip_item():
    if session.get('tipo_usuario') != 'Aluno' and session.get('tipo_usuario') != 'Administrador':
        flash('Acesso negado.', 'danger')
        abort(403)

    user_id = session['user_id']
    item_id = request.form.get('item_id', type=int)

    conn = get_db_connection()
    try:
        user_pet_data = conn.execute('SELECT * FROM user_pets WHERE usuario_id = ?', (user_id,)).fetchone()
        if not user_pet_data:
            flash('Você precisa escolher um mascote primeiro!', 'info')
            return redirect(url_for('aluno_profile'))
        
        user_pet = UserPet(**user_pet_data)

        item_data = conn.execute('SELECT * FROM pet_items WHERE id = ?', (item_id,)).fetchone()
        if not item_data:
            flash('Item não encontrado.', 'danger')
            return redirect(url_for('pet_shop'))
        
        item = PetItem(**item_data)

        # Verifica se o pet tem XP suficiente para comprar o item
        if user_pet.xp_acumulado < item.preco_xp:
            flash(f'XP insuficiente para comprar {item.nome}. Você precisa de {item.preco_xp} XP.', 'danger')
            return redirect(url_for('pet_shop'))

        # Verifica se o item já está equipado
        if item.id in user_pet.itens_equipados:
            flash(f'{item.nome} já está equipado!', 'info')
            return redirect(url_for('pet_shop'))

        # Verifica compatibilidade de tipo (opcional, já filtrado na loja, mas bom para segurança)
        pet_base_data = conn.execute('SELECT tipo FROM pets_base WHERE id = ?', (user_pet.pet_base_id,)).fetchone()
        pet_type = pet_base_data['tipo'] if pet_base_data else None
        if item.tipo_pet_compativel != 'Todos' and item.tipo_pet_compativel != pet_type:
            flash(f'{item.nome} não é compatível com seu mascote {pet_type}.', 'danger')
            return redirect(url_for('pet_shop'))

        # Deduz XP e equipa o item
        user_pet.xp_acumulado -= item.preco_xp
        user_pet.itens_equipados.append(item.id)

        conn.execute('UPDATE user_pets SET xp_acumulado = ?, itens_equipados = ?, ultima_atualizacao = ? WHERE id = ?',
                     (user_pet.xp_acumulado, json.dumps(user_pet.itens_equipados), datetime.now().isoformat(), user_pet.id))
        conn.commit()
        flash(f'{item.nome} equipado com sucesso! XP restante: {user_pet.xp_acumulado}.', 'success')

    except Exception as e:
        flash(f'Erro ao equipar item: {e}', 'danger')
        print(f"DEBUG: Erro ao equipar item: {e}")
    finally:
        conn.close()
    
    return redirect(url_for('aluno_profile'))


# --- Rotas básicas para outros tipos de perfil (expansível) ---
@app.route('/instrutor/profile')
@login_required
def instrutor_profile():
    if session.get('tipo_usuario') not in ['Instrutor', 'Administrador']:
        flash('Acesso negado. Esta página é apenas para Instrutores.', 'danger')
        abort(403)
    user_id = session['user_id']
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    profile_data = conn.execute('SELECT * FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
    conn.close()
    user = Usuario(**user_data) if user_data else None
    profile = Perfil(**profile_data) if profile_data else None
    return render_template('instrutor_profile.html', user=user, profile=profile)

@app.route('/professor_voluntario/profile')
@login_required
def professor_voluntario_profile():
    if session.get('tipo_usuario') not in ['ProfessorVoluntario', 'Administrador']:
        flash('Acesso negado. Esta página é apenas para Professores Voluntários.', 'danger')
        abort(403)
    user_id = session['user_id']
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    profile_data = conn.execute('SELECT * FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
    conn.close()
    user = Usuario(**user_data) if user_data else None
    profile = Perfil(**profile_data) if profile_data else None
    return render_template('professor_voluntario_profile.html', user=user, profile=profile)

@app.route('/moderador/profile')
@login_required
def moderador_profile():
    if session.get('tipo_usuario') not in ['Moderador', 'Administrador']:
        flash('Acesso negado. Esta página é apenas para Moderadores.', 'danger')
        abort(403)
    user_id = session['user_id']
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    profile_data = conn.execute('SELECT * FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
    conn.close()
    user = Usuario(**user_data) if user_data else None
    profile = Perfil(**profile_data) if profile_data else None
    return render_template('moderador_profile.html', user=user, profile=profile)

@app.route('/visitante/profile')
@login_required
def visitante_profile():
    # Visitantes podem ver seu próprio perfil básico, mas não terão muitas funcionalidades
    user_id = session['user_id']
    conn = get_db_connection()
    user_data = conn.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,)).fetchone()
    profile_data = conn.execute('SELECT * FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
    conn.close()
    user = Usuario(**user_data) if user_data else None
    profile = Perfil(**profile_data) if profile_data else None
    return render_template('visitante_profile.html', user=user, profile=profile)

# --- Rotas de Conhecimento (Artigos/Notícias/Blog Posts) ---
@app.route('/conhecimento')
def conhecimento_home():
    conn = get_db_connection()
    # Obter as últimas 8 notícias/artigos para a home do conhecimento
    recent_content_data = conn.execute('SELECT c.*, u.nome_usuario AS autor_nome FROM conteudos c JOIN usuarios u ON c.autor_id = u.id ORDER BY c.data_publicacao DESC LIMIT 8').fetchall()
    recent_content = [Conteudo(**dict(row)) for row in recent_content_data]

    # Obter categorias únicas
    categories_data = conn.execute('SELECT DISTINCT categoria FROM conteudos ORDER BY categoria').fetchall()
    categories = [row['categoria'] for row in categories_data]

    conn.close()
    return render_template('conhecimento_home.html', recent_content=recent_content, categories=categories)

@app.route('/conhecimento/category/<category_name>')
def conhecimento_by_category(category_name):
    conn = get_db_connection()
    content_data = conn.execute('SELECT c.*, u.nome_usuario AS autor_nome FROM conteudos c JOIN usuarios u ON c.autor_id = u.id WHERE c.categoria = ? ORDER BY c.data_publicacao DESC', (category_name,)).fetchall()
    content_list = [Conteudo(**dict(row)) for row in content_data]
    
    categories_data = conn.execute('SELECT DISTINCT categoria FROM conteudos ORDER BY categoria').fetchall()
    categories = [row['categoria'] for row in categories_data]

    conn.close()
    return render_template('conhecimento_home.html', recent_content=content_list, categories=categories, current_category=category_name)

@app.route('/conhecimento/<int:content_id>')
def content_detail(content_id):
    conn = get_db_connection()
    # Busca o conteúdo base
    content_base_data = conn.execute('SELECT c.*, u.nome_usuario AS autor_nome FROM conteudos c JOIN usuarios u ON c.autor_id = u.id WHERE c.id = ?', (content_id,)).fetchone()
    
    if not content_base_data:
        flash('Conteúdo não encontrado.', 'danger')
        abort(404)
    
    # Cria a instância da classe Conteudo base
    content = Conteudo(**dict(content_base_data))

    # Busca os dados específicos do tipo de conteúdo
    specific_content_data = None
    if content.tipo_conteudo == 'Artigo':
        specific_content_data = conn.execute('SELECT * FROM artigos WHERE conteudo_id = ?', (content_id,)).fetchone()
        content = Artigo(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    elif content.tipo_conteudo == 'Video':
        specific_content_data = conn.execute('SELECT * FROM videos WHERE conteudo_id = ?', (content_id,)).fetchone()
        content = Video(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    elif content.tipo_conteudo == 'Quiz':
        specific_content_data = conn.execute('SELECT * FROM quizzes WHERE conteudo_id = ?', (content_id,)).fetchone()
        content = Quiz(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    elif content.tipo_conteudo == 'Jogo':
        specific_content_data = conn.execute('SELECT * FROM jogos WHERE conteudo_id = ?', (content_id,)).fetchone()
        content = Jogo(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    
    # Verificar se o usuário logado já curtiu este conteúdo
    is_liked = False
    if 'user_id' in session:
        like_check = conn.execute('SELECT 1 FROM curtidas WHERE usuario_id = ? AND conteudo_id = ?', (session['user_id'], content_id)).fetchone()
        if like_check:
            is_liked = True
    
    # Contar curtidas
    likes_count_data = conn.execute('SELECT COUNT(*) FROM curtidas WHERE conteudo_id = ?', (content_id,)).fetchone()
    likes_count = likes_count_data[0] if likes_count_data else 0

    # Carregar comentários
    comments_data = conn.execute('SELECT co.*, u.nome_usuario FROM comentarios co JOIN usuarios u ON co.usuario_id = u.id WHERE co.conteudo_id = ? ORDER BY co.data_comentario ASC', (content_id,)).fetchall()
    comments = [Comentario(**dict(row)) for row in comments_data]

    # Verificar se o usuário está inscrito nesta categoria
    user_subscriptions = []
    if 'user_id' in session:
        subs_data = conn.execute('SELECT categoria FROM inscricoes_categoria WHERE usuario_id = ?', (session['user_id'],)).fetchall()
        user_subscriptions = [row['categoria'] for row in subs_data]
    
    conn.close()
    return render_template('content_detail.html', content=content, is_liked=is_liked, likes_count=likes_count, comments=comments, user_subscriptions=user_subscriptions)

@app.route('/conhecimento/publish', methods=['GET', 'POST'])
@publisher_required # Apenas usuários autorizados podem publicar
def publish_content():
    categories = ['Estrelas', 'Buracos Negros', 'Missões Espaciais', 'Cosmologia', 'Física', 'Outros']
    content_types = ['Artigo', 'Video', 'Quiz', 'Jogo'] # Adicionado Video, Quiz, Jogo

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        image_url = request.form.get('image_url')
        fonte_url = request.form.get('fonte_url')
        content_type = request.form['content_type']
        
        autor_id = session['user_id']
        data_publicacao = datetime.now().isoformat()
        visibilidade = 'publico'

        if not all([title, description, category, content_type]):
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('publish_content.html', categories=categories, content_types=content_types)

        if category not in categories or content_type not in content_types:
            flash('Categoria ou tipo de conteúdo inválido.', 'danger')
            return render_template('publish_content.html', categories=categories, content_types=content_types)

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            
            # Insere na tabela base de conteudos
            cursor.execute('''
                INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, fonte_url, tipo_conteudo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, data_publicacao, visibilidade, autor_id, category, image_url, fonte_url, content_type))
            
            new_content_id = cursor.lastrowid

            # Insere na tabela específica do tipo de conteúdo
            if content_type == 'Artigo':
                text_html = request.form['text_html']
                if not text_html:
                    raise ValueError("Conteúdo HTML é obrigatório para Artigos.")
                cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (new_content_id, text_html))
            elif content_type == 'Video':
                url_video = request.form['url_video']
                duracao_segundos = request.form.get('duracao_segundos', type=int)
                transcricao = request.form.get('transcricao')
                if not url_video:
                    raise ValueError("URL do vídeo é obrigatória para Vídeos.")
                cursor.execute('INSERT INTO videos (conteudo_id, url_video, duracao_segundos, transcricao) VALUES (?, ?, ?, ?)', (new_content_id, url_video, duracao_segundos, transcricao))
            elif content_type == 'Quiz':
                tempo_limite_min = request.form.get('tempo_limite_min', type=int)
                tentativas_permitidas = request.form.get('tentativas_permitidas', type=int)
                cursor.execute('INSERT INTO quizzes (conteudo_id, tempo_limite_min, tentativas_permitidas) VALUES (?, ?, ?)', (new_content_id, tempo_limite_min, tentativas_permitidas))
                # Lógica para adicionar questões e alternativas (simplificado por enquanto)
                flash('Quiz criado! Adicione questões e alternativas na página de edição do quiz.', 'info')
            elif content_type == 'Jogo':
                url_jogo = request.form['url_jogo']
                tipo_jogo = request.form.get('tipo_jogo')
                nivel_dificuldade = request.form.get('nivel_dificuldade', type=int)
                if not url_jogo:
                    raise ValueError("URL do jogo é obrigatória para Jogos.")
                cursor.execute('INSERT INTO jogos (conteudo_id, tipo_jogo, nivel_dificuldade, url_jogo) VALUES (?, ?, ?, ?)', (new_content_id, tipo_jogo, nivel_dificuldade, url_jogo))

            conn.commit()
            flash('Conteúdo publicado com sucesso!', 'success')
            
            # --- Lógica de Notificação para inscritos na categoria ---
            subscribers = conn.execute('SELECT usuario_id FROM inscricoes_categoria WHERE categoria = ?', (category,)).fetchall()
            for sub in subscribers:
                if sub['usuario_id'] != autor_id: # Não notificar o próprio autor
                    notif_message = f'Novo conteúdo na categoria "{category}": "{title}"'
                    notif_link = url_for('content_detail', content_id=new_content_id)
                    conn.execute('INSERT INTO notificacoes (usuario_id, mensagem, link, data_envio) VALUES (?, ?, ?, ?)',
                                 (sub['usuario_id'], notif_message, notif_link, datetime.now().isoformat()))
            conn.commit()
            # --- Fim da Lógica de Notificação ---

            return redirect(url_for('content_detail', content_id=new_content_id))
        except ValueError as ve:
            flash(f'Erro de validação: {ve}', 'danger')
            print(f"DEBUG: Erro de validação ao publicar conteúdo: {ve}")
        except Exception as e:
            flash(f'Erro ao publicar conteúdo: {e}', 'danger')
            print(f"DEBUG: Erro ao publicar conteúdo: {e}")
        finally:
            conn.close()

    return render_template('publish_content.html', categories=categories, content_types=content_types)

@app.route('/conhecimento/like/<int:content_id>', methods=['POST'])
@login_required
def like_content(content_id):
    user_id = session['user_id']
    conn = get_db_connection()
    try:
        # Verifica se já curtiu
        existing_like = conn.execute('SELECT 1 FROM curtidas WHERE usuario_id = ? AND conteudo_id = ?', (user_id, content_id)).fetchone()
        if existing_like:
            # Se já curtiu, descurtir
            conn.execute('DELETE FROM curtidas WHERE usuario_id = ? AND conteudo_id = ?', (user_id, content_id))
            flash('Conteúdo descurtido.', 'info')
        else:
            # Se não curtiu, curtir
            conn.execute('INSERT INTO curtidas (usuario_id, conteudo_id, data_curtida) VALUES (?, ?, ?)', (user_id, content_id, datetime.now().isoformat()))
            flash('Conteúdo curtido!', 'success')
        conn.commit()
    except Exception as e:
        flash(f'Erro ao curtir/descurtir conteúdo: {e}', 'danger')
        print(f"DEBUG: Erro ao curtir/descurtir: {e}")
    finally:
        conn.close()
    return redirect(url_for('content_detail', content_id=content_id))

@app.route('/conhecimento/comment/<int:content_id>', methods=['POST'])
@login_required
def add_content_comment(content_id): # Renomeado para evitar conflito com add_post_comment
    user_id = session['user_id']
    comment_text = request.form.get('comment_text', '').strip()

    if not comment_text:
        flash('O comentário não pode estar vazio.', 'danger')
        return redirect(url_for('content_detail', content_id=content_id))
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO comentarios (conteudo_id, usuario_id, texto, data_comentario) VALUES (?, ?, ?, ?)',
                     (content_id, user_id, comment_text, datetime.now().isoformat()))
        conn.commit()
        flash('Comentário adicionado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar comentário: {e}', 'danger')
        print(f"DEBUG: Erro ao adicionar comentário: {e}")
    finally:
        conn.close()
    return redirect(url_for('content_detail', content_id=content_id))

# --- Rotas de Perfil para Conteúdo Curtido e Notificações ---
@app.route('/profile/favorites')
@login_required
def user_favorites():
    user_id = session['user_id']
    conn = get_db_connection()
    
    favorites_data = conn.execute('''
        SELECT c.*, u.nome_usuario AS autor_nome
        FROM curtidas cu
        JOIN conteudos c ON cu.conteudo_id = c.id
        JOIN usuarios u ON c.autor_id = u.id
        WHERE cu.usuario_id = ?
        ORDER BY cu.data_curtida DESC
    ''', (user_id,)).fetchall()
    
    favorite_contents = [Conteudo(**dict(row)) for row in favorites_data]
    conn.close()
    return render_template('user_favorites.html', favorite_contents=favorite_contents)

@app.route('/profile/notifications')
@login_required
def user_notifications():
    user_id = session['user_id']
    conn = get_db_connection()
    
    notifications_data = conn.execute('SELECT * FROM notificacoes WHERE usuario_id = ? ORDER BY data_envio DESC', (user_id,)).fetchall()
    notifications = [Notificacao(**dict(row)) for row in notifications_data]
    
    conn.close()
    return render_template('user_notifications.html', notifications=notifications)

@app.route('/notifications/mark_read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    user_id = session['user_id']
    conn = get_db_connection()
    try:
        conn.execute('UPDATE notificacoes SET lida = 1 WHERE id = ? AND usuario_id = ?', (notification_id, user_id))
        conn.commit()
    except Exception as e:
        print(f"DEBUG: Erro ao marcar notificação como lida: {e}")
    finally:
        conn.close()
    # Retorna um JSON para requisições AJAX
    return jsonify({'status': 'success'})

@app.route('/notifications/subscribe', methods=['POST'])
@login_required
def subscribe_category():
    user_id = session['user_id']
    category = request.form.get('category')
    action = request.form.get('action') # 'subscribe' or 'unsubscribe'

    if not category or not action:
        flash('Dados inválidos.', 'danger')
        return redirect(url_for('conhecimento_home'))

    conn = get_db_connection()
    try:
        if action == 'subscribe':
            conn.execute('INSERT OR IGNORE INTO inscricoes_categoria (usuario_id, categoria) VALUES (?, ?)', (user_id, category))
            flash(f'Inscrito na categoria "{category}" para notificações.', 'success')
        elif action == 'unsubscribe':
            conn.execute('DELETE FROM inscricoes_categoria WHERE usuario_id = ? AND categoria = ?', (user_id, category))
            flash(f'Desinscrito da categoria "{category}".', 'info')
        conn.commit()
    except Exception as e:
        flash(f'Erro ao gerenciar inscrição: {e}', 'danger')
        print(f"DEBUG: Erro ao gerenciar inscrição: {e}")
    finally:
        conn.close()
    return redirect(url_for('conhecimento_home'))

# --- Rotas do Fórum ---
@app.route('/forum')
def forum_home():
    conn = get_db_connection()
    subforums_data = conn.execute('SELECT * FROM subforums ORDER BY ordem_exibicao ASC').fetchall()
    subforums = [Subforum(**row) for row in subforums_data]
    conn.close()
    return render_template('forum_home.html', subforums=subforums)

@app.route('/forum/create_subforum', methods=['GET', 'POST'])
@admin_required # Apenas administradores podem criar subfóruns
def create_subforum():
    if request.method == 'POST':
        nome = request.form['nome'].strip()
        descricao = request.form['descricao'].strip()
        ordem_exibicao = request.form.get('ordem_exibicao', type=int, default=0)

        if not nome or not descricao:
            flash('Nome e descrição são obrigatórios para o subfórum.', 'danger')
            return render_template('create_subforum.html')
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO subforums (nome, descricao, ordem_exibicao) VALUES (?, ?, ?)',
                         (nome, descricao, ordem_exibicao))
            conn.commit()
            flash(f'Subfórum "{nome}" criado com sucesso!', 'success')
            return redirect(url_for('forum_home'))
        except sqlite3.IntegrityError:
            flash('Já existe um subfórum com este nome.', 'danger')
        except Exception as e:
            flash(f'Erro ao criar subfórum: {e}', 'danger')
            print(f"DEBUG: Erro ao criar subfórum: {e}")
        finally:
            conn.close()
    return render_template('create_subforum.html')

@app.route('/forum/<int:subforum_id>')
def subforum_detail(subforum_id):
    conn = get_db_connection()
    subforum_data = conn.execute('SELECT * FROM subforums WHERE id = ?', (subforum_id,)).fetchone()
    
    if not subforum_data:
        flash('Subfórum não encontrado.', 'danger')
        abort(404)
    
    subforum = Subforum(**subforum_data)

    # Obter tópicos do subfórum, fixados primeiro, depois por data do último post
    topics_data = conn.execute('''
        SELECT t.*, u.nome_usuario AS autor_nome
        FROM topicos t
        JOIN usuarios u ON t.autor_id = u.id
        WHERE t.subforum_id = ?
        ORDER BY t.fixado DESC, t.data_ult_post DESC
    ''', (subforum_id,)).fetchall()
    topics = [Topico(**dict(row)) for row in topics_data]

    conn.close()
    return render_template('subforum_detail.html', subforum=subforum, topics=topics)

@app.route('/forum/<int:subforum_id>/create_topic', methods=['GET', 'POST'])
@login_required # Qualquer usuário logado pode criar um tópico
def create_topic(subforum_id):
    conn = get_db_connection()
    subforum_data = conn.execute('SELECT * FROM subforums WHERE id = ?', (subforum_id,)).fetchone()
    
    if not subforum_data:
        flash('Subfórum não encontrado.', 'danger')
        abort(404)
    
    subforum = Subforum(**subforum_data)

    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        texto_postagem = request.form['texto'].strip() # Primeira postagem do tópico

        if not titulo or not texto_postagem:
            flash('Título e texto da postagem são obrigatórios.', 'danger')
            return render_template('create_topic.html', subforum=subforum)
        
        autor_id = session['user_id']
        data_agora = datetime.now().isoformat()

        try:
            cursor = conn.cursor()
            # Cria o tópico
            cursor.execute('''
                INSERT INTO topicos (subforum_id, autor_id, titulo, data_criacao, data_ult_post)
                VALUES (?, ?, ?, ?, ?)
            ''', (subforum_id, autor_id, titulo, data_agora, data_agora))
            
            new_topic_id = cursor.lastrowid

            # Cria a primeira postagem do tópico
            cursor.execute('''
                INSERT INTO postagens (topico_id, autor_id, texto, data_postagem)
                VALUES (?, ?, ?, ?)
            ''', (new_topic_id, autor_id, texto_postagem, data_agora))
            
            conn.commit()
            flash('Tópico criado com sucesso!', 'success')
            return redirect(url_for('topic_detail', topic_id=new_topic_id))
        except Exception as e:
            flash(f'Erro ao criar tópico: {e}', 'danger')
            print(f"DEBUG: Erro ao criar tópico: {e}")
        finally:
            conn.close()

    conn.close() # Fecha a conexão se for GET
    return render_template('create_topic.html', subforum=subforum)

@app.route('/forum/topic/<int:topic_id>')
def topic_detail(topic_id):
    conn = get_db_connection()
    topic_data = conn.execute('SELECT t.*, u.nome_usuario AS autor_nome, s.nome AS subforum_nome, s.id AS subforum_id FROM topicos t JOIN usuarios u ON t.autor_id = u.id JOIN subforums s ON t.subforum_id = s.id WHERE t.id = ?', (topic_id,)).fetchone()
    
    if not topic_data:
        flash('Tópico não encontrado.', 'danger')
        abort(404)
    
    topic = Topico(**dict(topic_data))

    # Obter postagens do tópico
    posts_data = conn.execute('''
        SELECT p.*, u.nome_usuario AS autor_nome, pr.nivel AS autor_nivel, pr.xp AS autor_xp
        FROM postagens p
        JOIN usuarios u ON p.autor_id = u.id
        JOIN perfis pr ON u.id = pr.usuario_id
        WHERE p.topico_id = ?
        ORDER BY p.data_postagem ASC
    ''', (topic_id,)).fetchall()
    posts = []
    for row in posts_data:
        post_dict = dict(row)
        # Obter votos para cada postagem
        upvotes_count = conn.execute('SELECT COUNT(*) FROM votos_postagem WHERE postagem_id = ? AND tipo_voto = "upvote"', (post_dict['id'],)).fetchone()[0]
        downvotes_count = conn.execute('SELECT COUNT(*) FROM votos_postagem WHERE postagem_id = ? AND tipo_voto = "downvote"', (post_dict['id'],)).fetchone()[0]
        post_dict['upvotes_count'] = upvotes_count
        post_dict['downvotes_count'] = downvotes_count
        
        # Verificar se o usuário logado já votou nesta postagem
        user_voted_type = None
        if 'user_id' in session:
            voted_data = conn.execute('SELECT tipo_voto FROM votos_postagem WHERE usuario_id = ? AND postagem_id = ?', (session['user_id'], post_dict['id'])).fetchone()
            if voted_data:
                user_voted_type = voted_data['tipo_voto']
        post_dict['user_voted_type'] = user_voted_type

        posts.append(Postagem(**post_dict))

    conn.close()
    return render_template('topic_detail.html', topic=topic, posts=posts)

@app.route('/forum/topic/<int:topic_id>/post', methods=['POST'])
@login_required # Qualquer usuário logado pode postar
def add_post(topic_id):
    conn = get_db_connection()
    topic_data = conn.execute('SELECT id, fechado FROM topicos WHERE id = ?', (topic_id,)).fetchone()
    
    if not topic_data:
        flash('Tópico não encontrado.', 'danger')
        abort(404)
    
    if topic_data['fechado']:
        flash('Este tópico está fechado para novas postagens.', 'danger')
        return redirect(url_for('topic_detail', topic_id=topic_id))

    post_text = request.form.get('post_text', '').strip()
    if not post_text:
        flash('A postagem não pode estar vazia.', 'danger')
        return redirect(url_for('topic_detail', topic_id=topic_id))

    autor_id = session['user_id']
    data_agora = datetime.now().isoformat()

    try:
        conn.execute('INSERT INTO postagens (topico_id, autor_id, texto, data_postagem) VALUES (?, ?, ?, ?)',
                     (topic_id, autor_id, post_text, data_agora))
        # Atualiza a data do último post no tópico
        conn.execute('UPDATE topicos SET data_ult_post = ? WHERE id = ?', (data_agora, topic_id))
        conn.commit()
        flash('Postagem adicionada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar postagem: {e}', 'danger')
        print(f"DEBUG: Erro ao adicionar postagem: {e}")
    finally:
        conn.close()
    return redirect(url_for('topic_detail', topic_id=topic_id))

@app.route('/forum/post/<int:post_id>/vote', methods=['POST'])
@login_required
def vote_post(post_id):
    user_id = session['user_id']
    vote_type = request.form.get('vote_type') # 'upvote' ou 'downvote'

    if vote_type not in ['upvote', 'downvote']:
        return jsonify({'status': 'error', 'message': 'Tipo de voto inválido.'}), 400
    
    conn = get_db_connection()
    try:
        post_data = conn.execute('SELECT autor_id, topico_id, upvotes FROM postagens WHERE id = ?', (post_id,)).fetchone()
        if not post_data:
            return jsonify({'status': 'error', 'message': 'Postagem não encontrada.'}), 404
        
        post_autor_id = post_data['autor_id']
        topic_id = post_data['topico_id']
        current_post_upvotes = post_data['upvotes']

        if user_id == post_autor_id:
            return jsonify({'status': 'error', 'message': 'Você não pode votar na sua própria postagem.'}), 403

        existing_vote = conn.execute('SELECT tipo_voto FROM votos_postagem WHERE usuario_id = ? AND postagem_id = ?', (user_id, post_id)).fetchone()

        if existing_vote:
            # Usuário já votou
            if existing_vote['tipo_voto'] == vote_type:
                # Clicou no mesmo voto novamente: remover voto
                conn.execute('DELETE FROM votos_postagem WHERE usuario_id = ? AND postagem_id = ?', (user_id, post_id))
                if vote_type == 'upvote':
                    conn.execute('UPDATE postagens SET upvotes = upvotes - 1 WHERE id = ?', (post_id,))
                else: # downvote
                    conn.execute('UPDATE postagens SET upvotes = upvotes + 1 WHERE id = ?', (post_id,)) # Downvote reverte upvote
                conn.commit()
                return jsonify({'status': 'success', 'action': 'removed', 'new_upvotes': current_post_upvotes - (1 if vote_type == 'upvote' else -1)}) # Ajustar para downvote
            else:
                # Clicou no voto oposto: mudar voto
                conn.execute('UPDATE votos_postagem SET tipo_voto = ?, data_voto = ? WHERE usuario_id = ? AND postagem_id = ?', (vote_type, datetime.now().isoformat(), user_id, post_id))
                if vote_type == 'upvote':
                    conn.execute('UPDATE postagens SET upvotes = upvotes + 2 WHERE id = ?', (post_id,)) # De down para up (+1 do voto, +1 por reverter down)
                else: # downvote
                    conn.execute('UPDATE postagens SET upvotes = upvotes + 2 WHERE id = ?', (post_id,)) # De up para down (-1 do voto, -1 por reverter up)
                conn.commit()
                return jsonify({'status': 'success', 'action': 'changed', 'new_upvotes': current_post_upvotes + (2 if vote_type == 'upvote' else -2)}) # Ajustar
        else:
            # Novo voto
            conn.execute('INSERT INTO votos_postagem (usuario_id, postagem_id, tipo_voto, data_voto) VALUES (?, ?, ?, ?)', (user_id, post_id, vote_type, datetime.now().isoformat()))
            if vote_type == 'upvote':
                conn.execute('UPDATE postagens SET upvotes = upvotes + 1 WHERE id = ?', (post_id,))
            else: # downvote
                conn.execute('UPDATE postagens SET upvotes = upvotes - 1 WHERE id = ?', (post_id,))
            conn.commit()
            return jsonify({'status': 'success', 'action': 'added', 'new_upvotes': current_post_upvotes + (1 if vote_type == 'upvote' else -1)})

    except Exception as e:
        print(f"DEBUG: Erro ao votar na postagem: {e}")
        return jsonify({'status': 'error', 'message': f'Erro interno: {e}'}), 500
    finally:
        conn.close()

# --- Rotas de Moderação do Fórum ---
@app.route('/forum/topic/<int:topic_id>/toggle_fixed', methods=['POST'])
@moderator_required
def toggle_topic_fixed(topic_id):
    conn = get_db_connection()
    try:
        topic_data = conn.execute('SELECT fixado FROM topicos WHERE id = ?', (topic_id,)).fetchone()
        if not topic_data:
            flash('Tópico não encontrado.', 'danger')
            return redirect(url_for('forum_home'))
        
        new_fixed_status = 1 if topic_data['fixado'] == 0 else 0
        conn.execute('UPDATE topicos SET fixado = ? WHERE id = ?', (new_fixed_status, topic_id))
        conn.commit()
        flash(f'Tópico {"fixado" if new_fixed_status else "desafixado"} com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao alterar status de fixação do tópico: {e}', 'danger')
        print(f"DEBUG: Erro ao alterar status de fixação do tópico: {e}")
    finally:
        conn.close()
    return redirect(request.referrer or url_for('topic_detail', topic_id=topic_id))

@app.route('/forum/topic/<int:topic_id>/toggle_closed', methods=['POST'])
@moderator_required
def toggle_topic_closed(topic_id):
    conn = get_db_connection()
    try:
        topic_data = conn.execute('SELECT fechado FROM topicos WHERE id = ?', (topic_id,)).fetchone()
        if not topic_data:
            flash('Tópico não encontrado.', 'danger')
            return redirect(url_for('forum_home'))
        
        new_closed_status = 1 if topic_data['fechado'] == 0 else 0
        conn.execute('UPDATE topicos SET fechado = ? WHERE id = ?', (new_closed_status, topic_id))
        conn.commit()
        flash(f'Tópico {"fechado" if new_closed_status else "aberto"} com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao alterar status de fechamento do tópico: {e}', 'danger')
        print(f"DEBUG: Erro ao alterar status de fechamento do tópico: {e}")
    finally:
        conn.close()
    return redirect(request.referrer or url_for('topic_detail', topic_id=topic_id))

@app.route('/forum/post/<int:post_id>/delete', methods=['POST'])
@moderator_required
def delete_post(post_id):
    conn = get_db_connection()
    try:
        post_data = conn.execute('SELECT topico_id FROM postagens WHERE id = ?', (post_id,)).fetchone()
        if not post_data:
            flash('Postagem não encontrada.', 'danger')
            return redirect(url_for('forum_home')) # Fallback
        
        topic_id = post_data['topico_id']
        
        conn.execute('DELETE FROM postagens WHERE id = ?', (post_id,))
        conn.commit()
        flash('Postagem excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir postagem: {e}', 'danger')
        print(f"DEBUG: Erro ao excluir postagem: {e}")
    finally:
        conn.close()
    return redirect(url_for('topic_detail', topic_id=topic_id))

@app.route('/forum/comment/<int:comment_id>/delete', methods=['POST'])
@moderator_required
def delete_comment(comment_id):
    conn = get_db_connection()
    try:
        comment_data = conn.execute('SELECT conteudo_id, postagem_id FROM comentarios WHERE id = ?', (comment_id,)).fetchone()
        if not comment_data:
            flash('Comentário não encontrado.', 'danger')
            return redirect(request.referrer or url_for('forum_home')) # Fallback
        
        conteudo_id = comment_data['conteudo_id']
        postagem_id = comment_data['postagem_id']

        conn.execute('DELETE FROM comentarios WHERE id = ?', (comment_id,))
        conn.commit()
        flash('Comentário excluído com sucesso!', 'success')
        
        if conteudo_id:
            return redirect(url_for('content_detail', content_id=conteudo_id))
        elif postagem_id:
            return redirect(url_for('topic_detail', topic_id=postagem_id)) # Comentário de postagem, redireciona para o tópico
        
    except Exception as e:
        flash(f'Erro ao excluir comentário: {e}', 'danger')
        print(f"DEBUG: Erro ao excluir comentário: {e}")
    finally:
        conn.close()
    return redirect(request.referrer or url_for('forum_home'))

# --- Rotas de Conhecimento (Trilhas, Módulos, Conteúdos Educacionais) ---
@app.route('/trilhas')
def trilhas_home():
    conn = get_db_connection()
    # Apenas trilhas publicadas
    trilhas_data = conn.execute('SELECT t.*, u.nome_usuario AS autor_nome FROM trilhas_educacionais t JOIN usuarios u ON t.autor_id = u.id WHERE t.publicada = 1 ORDER BY t.titulo').fetchall()
    trilhas = [TrilhaEducacional(**dict(row)) for row in trilhas_data]
    
    categories_data = conn.execute('SELECT DISTINCT categoria FROM trilhas_educacionais ORDER BY categoria').fetchall()
    categories = [row['categoria'] for row in categories_data]

    levels_data = conn.execute('SELECT DISTINCT nivel FROM trilhas_educacionais ORDER BY nivel').fetchall()
    levels = [row['nivel'] for row in levels_data]

    conn.close()
    return render_template('trilhas_home.html', trilhas=trilhas, categories=categories, levels=levels)

@app.route('/trilhas/create', methods=['GET', 'POST'])
@content_creator_required
def create_trilha():
    categories = ['Estrelas', 'Planetas', 'Cosmologia', 'Física', 'Missões Espaciais', 'Outros']
    levels = ['Iniciante', 'Intermediário', 'Avançado']

    if request.method == 'POST':
        titulo = request.form['titulo'].strip()
        descricao = request.form['descricao'].strip()
        nivel = request.form['nivel']
        categoria = request.form['categoria']
        imagem_url = request.form.get('imagem_url')
        publicada = 1 if request.form.get('publicada') == 'on' else 0
        autor_id = session['user_id']

        if not all([titulo, descricao, nivel, categoria]):
            flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
            return render_template('create_trilha.html', categories=categories, levels=levels)
        
        if nivel not in levels or categoria not in categories:
            flash('Nível ou categoria inválidos.', 'danger')
            return render_template('create_trilha.html', categories=categories, levels=levels)

        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trilhas_educacionais (titulo, descricao, nivel, categoria, publicada, imagem_url, autor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (titulo, descricao, nivel, categoria, publicada, imagem_url, autor_id))
            conn.commit()
            flash(f'Trilha "{titulo}" criada com sucesso!', 'success')
            return redirect(url_for('trilhas_home'))
        except Exception as e:
            flash(f'Erro ao criar trilha: {e}', 'danger')
            print(f"DEBUG: Erro ao criar trilha: {e}")
        finally:
            conn.close()

    return render_template('create_trilha.html', categories=categories, levels=levels)

@app.route('/trilhas/<int:trilha_id>')
def trilha_detail(trilha_id):
    conn = get_db_connection()
    trilha_data = conn.execute('SELECT t.*, u.nome_usuario AS autor_nome FROM trilhas_educacionais t JOIN usuarios u ON t.autor_id = u.id WHERE t.id = ?', (trilha_id,)).fetchone()
    
    if not trilha_data:
        flash('Trilha não encontrada.', 'danger')
        abort(404)
    
    trilha = TrilhaEducacional(**dict(trilha_data))

    # Obter módulos da trilha
    modulos_data = conn.execute('SELECT * FROM modulos WHERE trilha_id = ? ORDER BY ordem ASC', (trilha_id,)).fetchall()
    modulos = [Modulo(**row) for row in modulos_data]

    # Obter progresso do usuário na trilha (se logado)
    user_progress = None
    if 'user_id' in session:
        prog_data = conn.execute('SELECT id FROM progresso_usuario_trilha WHERE usuario_id = ? AND trilha_id = ?', (session['user_id'], trilha_id)).fetchone()
        user_progress_id = prog_data['id'] if prog_data else None
        if user_progress_id:
            user_progress_data = conn.execute('SELECT * FROM progresso_usuario_trilha WHERE id = ?', (user_progress_id,)).fetchone()
            user_progress = ProgressoUsuarioTrilha(**user_progress_data)

    conn.close()
    return render_template('trilha_detail.html', trilha=trilha, modulos=modulos, user_progress=user_progress)

@app.route('/trilhas/<int:trilha_id>/enroll', methods=['POST'])
@login_required
def enroll_trilha(trilha_id):
    user_id = session['user_id']
    conn = get_db_connection()
    try:
        # Verifica se o usuário já está inscrito
        existing_enrollment = conn.execute('SELECT usuario_id FROM progresso_usuario_trilha WHERE usuario_id = ? AND trilha_id = ?', (user_id, trilha_id)).fetchone()
        if existing_enrollment:
            flash('Você já está inscrito nesta trilha!', 'info')
            return redirect(url_for('trilha_detail', trilha_id=trilha_id))
        
        # Inscreve o usuário na trilha
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO progresso_usuario_trilha (usuario_id, trilha_id, progresso_percentual, ultimo_acesso_data, concluida)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, trilha_id, 0.0, datetime.now().isoformat(), 0))
        conn.commit()
        flash('Inscrição na trilha realizada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao inscrever na trilha: {e}', 'danger')
        print(f"DEBUG: Erro ao inscrever na trilha: {e}")
    finally:
        conn.close()
    return redirect(url_for('trilha_detail', trilha_id=trilha_id))

@app.route('/trilhas/<int:trilha_id>/modulos/<int:modulo_id>')
def modulo_detail(trilha_id, modulo_id):
    conn = get_db_connection()
    trilha_data = conn.execute('SELECT * FROM trilhas_educacionais WHERE id = ?', (trilha_id,)).fetchone()
    modulo_data = conn.execute('SELECT * FROM modulos WHERE id = ? AND trilha_id = ?', (modulo_id, trilha_id)).fetchone()

    if not trilha_data or not modulo_data:
        flash('Trilha ou Módulo não encontrados.', 'danger')
        abort(404)
    
    trilha = TrilhaEducacional(**trilha_data)
    modulo = Modulo(**modulo_data)

    # Obter conteúdos do módulo
    contents_data = conn.execute('''
        SELECT c.*, cm.ordem_no_modulo, u.nome_usuario AS autor_nome
        FROM conteudos c
        JOIN conteudo_modulo cm ON c.id = cm.conteudo_id
        JOIN usuarios u ON c.autor_id = u.id
        WHERE cm.modulo_id = ?
        ORDER BY cm.ordem_no_modulo ASC
    ''', (modulo_id,)).fetchall()
    
    contents_in_module = []
    for row in contents_data:
        content_dict = dict(row)
        # Instanciar a classe de Conteudo correta
        if content_dict['tipo_conteudo'] == 'Artigo':
            specific_data = conn.execute('SELECT * FROM artigos WHERE conteudo_id = ?', (content_dict['id'],)).fetchone()
            contents_in_module.append(Artigo(**content_dict, **dict(specific_data)) if specific_data else Conteudo(**content_dict))
        elif content_dict['tipo_conteudo'] == 'Video':
            specific_data = conn.execute('SELECT * FROM videos WHERE conteudo_id = ?', (content_dict['id'],)).fetchone()
            contents_in_module.append(Video(**content_dict, **dict(specific_data)) if specific_data else Conteudo(**content_dict))
        elif content_dict['tipo_conteudo'] == 'Quiz':
            specific_data = conn.execute('SELECT * FROM quizzes WHERE conteudo_id = ?', (content_dict['id'],)).fetchone()
            contents_in_module.append(Quiz(**content_dict, **dict(specific_data)) if specific_data else Conteudo(**content_dict))
        elif content_dict['tipo_conteudo'] == 'Jogo':
            specific_data = conn.execute('SELECT * FROM jogos WHERE conteudo_id = ?', (content_dict['id'],)).fetchone()
            contents_in_module.append(Jogo(**content_dict, **dict(specific_data)) if specific_data else Conteudo(**content_dict))
        else:
            contents_in_module.append(Conteudo(**content_dict))

    # Obter progresso do usuário no módulo e seus conteúdos
    user_prog_module = None
    user_prog_contents = {}
    if 'user_id' in session:
        prog_trilha_data = conn.execute('SELECT id FROM progresso_usuario_trilha WHERE usuario_id = ? AND trilha_id = ?', (session['user_id'], trilha_id)).fetchone()
        if prog_trilha_data:
            prog_trilha_id = prog_trilha_data['id']
            prog_modulo_data = conn.execute('SELECT * FROM progresso_modulo WHERE progresso_trilha_id = ? AND modulo_id = ?', (prog_trilha_id, modulo_id)).fetchone()
            user_prog_module = ProgressoModulo(**prog_modulo_data) if prog_modulo_data else None

            if not user_prog_module: # Se o progresso do módulo não existe, cria
                cursor = conn.cursor()
                cursor.execute('INSERT INTO progresso_modulo (progresso_trilha_id, modulo_id, concluido, data_conclusao) VALUES (?, ?, ?, ?)',
                               (prog_trilha_id, modulo_id, 0, None))
                conn.commit()
                prog_modulo_id = cursor.lastrowid
                prog_mod_data = conn.execute('SELECT * FROM progresso_modulo WHERE progresso_trilha_id = ? AND modulo_id = ?', (prog_trilha_id, modulo_id)).fetchone()
                user_prog_module = ProgressoModulo(**prog_mod_data)
            else:
                prog_modulo_id = user_prog_module.id

            prog_cont_data = conn.execute('SELECT * FROM progresso_conteudo WHERE progresso_modulo_id = ?', (prog_modulo_id,)).fetchall()
            for pc_row in prog_cont_data:
                user_prog_contents[pc_row['conteudo_id']] = ProgressoConteudo(**pc_row)
                
            # Se não houver progresso para este conteúdo, criar um registro inicial
            for content_item in contents_in_module:
                if content_item.id not in user_prog_contents:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO progresso_conteudo (progresso_modulo_id, conteudo_id, concluido, data_conclusao, xp_ganho, moedas_ganhas)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (prog_modulo_id, content_item.id, 0, None, 0, 0))
                    conn.commit()
                    prog_conteudo_data = conn.execute('SELECT * FROM progresso_conteudo WHERE progresso_modulo_id = ? AND conteudo_id = ?', (prog_modulo_id, content_item.id)).fetchone()
                    user_prog_contents[content_item.id] = ProgressoConteudo(**prog_conteudo_data)


    conn.close()
    return render_template('modulo_detail.html', trilha=trilha, modulo=modulo, contents_in_module=contents_in_module, user_prog_module=user_prog_module, user_prog_contents=user_prog_contents)

@app.route('/trilhas/modulo/<int:modulo_id>/add_content', methods=['GET', 'POST'])
@content_creator_required
def add_content_to_module(modulo_id):
    conn = get_db_connection()
    modulo_data = conn.execute('SELECT m.*, t.titulo AS trilha_titulo FROM modulos m JOIN trilhas_educacionais t ON m.trilha_id = t.id WHERE m.id = ?', (modulo_id,)).fetchone()
    if not modulo_data:
        flash('Módulo não encontrado.', 'danger')
        abort(404)
    modulo = Modulo(**modulo_data)

    # Obter todos os conteúdos existentes para seleção
    all_contents_data = conn.execute('SELECT id, titulo, tipo_conteudo FROM conteudos ORDER BY titulo').fetchall()
    all_contents = [Conteudo(**row) for row in all_contents_data]

    if request.method == 'POST':
        conteudo_id = request.form.get('conteudo_id', type=int)
        ordem_no_modulo = request.form.get('ordem_no_modulo', type=int)

        if not conteudo_id or ordem_no_modulo is None:
            flash('Selecione um conteúdo e defina a ordem.', 'danger')
            return render_template('add_content_to_module.html', modulo=modulo, all_contents=all_contents)
        
        # Verificar se o conteúdo já está no módulo
        existing_link = conn.execute('SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?', (modulo_id, conteudo_id)).fetchone()
        if existing_link:
            flash('Este conteúdo já está neste módulo.', 'info')
            return render_template('add_content_to_module.html', modulo=modulo, all_contents=all_contents)

        try:
            # Obter o tipo_conteudo_fk do conteúdo selecionado
            content_type_data = conn.execute('SELECT tipo_conteudo FROM conteudos WHERE id = ?', (conteudo_id,)).fetchone()
            if not content_type_data:
                flash('Conteúdo selecionado inválido.', 'danger')
                return render_template('add_content_to_module.html', modulo=modulo, all_contents=all_contents)
            tipo_conteudo_fk = content_type_data['tipo_conteudo']

            conn.execute('''
                INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk)
                VALUES (?, ?, ?, ?)
            ''', (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk))
            conn.commit()
            flash('Conteúdo adicionado ao módulo com sucesso!', 'success')
            return redirect(url_for('modulo_detail', trilha_id=modulo.trilha_id, modulo_id=modulo.id))
        except Exception as e:
            flash(f'Erro ao adicionar conteúdo ao módulo: {e}', 'danger')
            print(f"DEBUG: Erro ao adicionar conteúdo ao módulo: {e}")
        finally:
            conn.close()

    conn.close()
    return render_template('add_content_to_module.html', modulo=modulo, all_contents=all_contents)

@app.route('/trilhas/modulo/<int:modulo_id>/create_content', methods=['GET', 'POST'])
@content_creator_required
def create_content_for_module(modulo_id):
    conn = get_db_connection()
    modulo_data = conn.execute('SELECT m.*, t.titulo AS trilha_titulo FROM modulos m JOIN trilhas_educacionais t ON m.trilha_id = t.id WHERE m.id = ?', (modulo_id,)).fetchone()
    if not modulo_data:
        flash('Módulo não encontrado.', 'danger')
        abort(404)
    modulo = Modulo(**modulo_data)

    categories = ['Estrelas', 'Buracos Negros', 'Missões Espaciais', 'Cosmologia', 'Física', 'Outros']
    content_types = ['Artigo', 'Video', 'Quiz', 'Jogo']

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        image_url = request.form.get('image_url')
        fonte_url = request.form.get('fonte_url')
        content_type = request.form['content_type']
        ordem_no_modulo = request.form.get('ordem_no_modulo', type=int)

        autor_id = session['user_id']
        data_publicacao = datetime.now().isoformat()
        visibilidade = 'publico'

        if not all([title, description, category, content_type, ordem_no_modulo is not None]):
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return render_template('create_content_for_module.html', modulo=modulo, categories=categories, content_types=content_types)

        if category not in categories or content_type not in content_types:
            flash('Categoria ou tipo de conteúdo inválido.', 'danger')
            return render_template('create_content_for_module.html', modulo=modulo, categories=categories, content_types=content_types)

        try:
            cursor = conn.cursor()
            
            # Insere na tabela base de conteudos
            cursor.execute('''
                INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, fonte_url, tipo_conteudo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, description, data_publicacao, visibilidade, autor_id, category, image_url, fonte_url, content_type))
            
            new_content_id = cursor.lastrowid

            # Insere na tabela específica do tipo de conteúdo
            if content_type == 'Artigo':
                text_html = request.form['text_html']
                if not text_html:
                    raise ValueError("Conteúdo HTML é obrigatório para Artigos.")
                cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (new_content_id, text_html))
            elif content_type == 'Video':
                url_video = request.form['url_video']
                duracao_segundos = request.form.get('duracao_segundos', type=int)
                transcricao = request.form.get('transcricao')
                if not url_video:
                    raise ValueError("URL do vídeo é obrigatória para Vídeos.")
                cursor.execute('INSERT INTO videos (conteudo_id, url_video, duracao_segundos, transcricao) VALUES (?, ?, ?, ?)', (new_content_id, url_video, duracao_segundos, transcricao))
            elif content_type == 'Quiz':
                tempo_limite_min = request.form.get('tempo_limite_min', type=int)
                tentativas_permitidas = request.form.get('tentativas_permitidas', type=int)
                cursor.execute('INSERT INTO quizzes (conteudo_id, tempo_limite_min, tentativas_permitidas) VALUES (?, ?, ?)', (new_content_id, tempo_limite_min, tentativas_permitidas))
                flash('Quiz criado! Adicione questões e alternativas na página de edição do quiz.', 'info')
            elif content_type == 'Jogo':
                url_jogo = request.form['url_jogo']
                tipo_jogo = request.form.get('tipo_jogo')
                nivel_dificuldade = request.form.get('nivel_dificuldade', type=int)
                if not url_jogo:
                    raise ValueError("URL do jogo é obrigatória para Jogos.")
                cursor.execute('INSERT INTO jogos (conteudo_id, tipo_jogo, nivel_dificuldade, url_jogo) VALUES (?, ?, ?, ?)', (new_content_id, tipo_jogo, nivel_dificuldade, url_jogo))
            
            # Adiciona o conteúdo ao módulo
            conn.execute('''
                INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk)
                VALUES (?, ?, ?, ?)
            ''', (modulo_id, new_content_id, ordem_no_modulo, content_type))

            conn.commit()
            flash('Conteúdo criado e adicionado ao módulo com sucesso!', 'success')
            return redirect(url_for('modulo_detail', trilha_id=modulo.trilha_id, modulo_id=modulo.id))
        except ValueError as ve:
            flash(f'Erro de validação: {ve}', 'danger')
            print(f"DEBUG: Erro de validação ao criar conteúdo para módulo: {ve}")
        except Exception as e:
            flash(f'Erro ao criar conteúdo para módulo: {e}', 'danger')
            print(f"DEBUG: Erro ao criar conteúdo para módulo: {e}")
        finally:
            conn.close()

    conn.close()
    return render_template('create_content_for_module.html', modulo=modulo, categories=categories, content_types=content_types)

@app.route('/trilhas/conteudo/<int:conteudo_id>')
@login_required # Conteúdo de trilha exige login
def view_trilha_content(conteudo_id):
    user_id = session['user_id']
    conn = get_db_connection()
    
    # Busca o conteúdo base
    content_base_data = conn.execute('SELECT c.*, u.nome_usuario AS autor_nome FROM conteudos c JOIN usuarios u ON c.autor_id = u.id WHERE c.id = ?', (conteudo_id,)).fetchone()
    
    if not content_base_data:
        flash('Conteúdo não encontrado.', 'danger')
        abort(404)
    
    content = Conteudo(**dict(content_base_data))

    # Busca os dados específicos do tipo de conteúdo
    specific_content_data = None
    if content.tipo_conteudo == 'Artigo':
        specific_content_data = conn.execute('SELECT * FROM artigos WHERE conteudo_id = ?', (conteudo_id,)).fetchone()
        content = Artigo(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    elif content.tipo_conteudo == 'Video':
        specific_content_data = conn.execute('SELECT * FROM videos WHERE conteudo_id = ?', (conteudo_id,)).fetchone()
        content = Video(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    elif content.tipo_conteudo == 'Quiz':
        specific_content_data = conn.execute('SELECT * FROM quizzes WHERE conteudo_id = ?', (conteudo_id,)).fetchone()
        content = Quiz(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    elif content.tipo_conteudo == 'Jogo':
        specific_content_data = conn.execute('SELECT * FROM jogos WHERE conteudo_id = ?', (conteudo_id,)).fetchone()
        content = Jogo(**dict(content_base_data), **dict(specific_content_data)) if specific_content_data else Conteudo(**content_base_data)
    
    # Obter informações do módulo e trilha para breadcrumbs
    modulo_info = conn.execute('SELECT m.id AS modulo_id, m.titulo AS modulo_titulo, t.id AS trilha_id, t.titulo AS trilha_titulo FROM conteudo_modulo cm JOIN modulos m ON cm.modulo_id = m.id JOIN trilhas_educacionais t ON m.trilha_id = t.id WHERE cm.conteudo_id = ?', (conteudo_id,)).fetchone()

    # Lógica para progresso do conteúdo
    prog_trilha_id = None
    prog_modulo_id = None
    prog_conteudo = None

    if 'user_id' in session and modulo_info:
        prog_trilha_data = conn.execute('SELECT id FROM progresso_usuario_trilha WHERE usuario_id = ? AND trilha_id = ?', (user_id, modulo_info['trilha_id'])).fetchone()
        if prog_trilha_data:
            prog_trilha_id = prog_trilha_data['id']
            prog_modulo_data = conn.execute('SELECT id FROM progresso_modulo WHERE progresso_trilha_id = ? AND modulo_id = ?', (prog_trilha_id, modulo_info['modulo_id'])).fetchone()
            if not prog_modulo_data: # Se o progresso do módulo não existe, cria
                cursor = conn.cursor()
                cursor.execute('INSERT INTO progresso_modulo (progresso_trilha_id, modulo_id, concluido, data_conclusao) VALUES (?, ?, ?, ?)',
                               (prog_trilha_id, modulo_info['modulo_id'], 0, None))
                conn.commit()
                prog_modulo_id = cursor.lastrowid
            else:
                prog_modulo_id = prog_modulo_data['id']

            prog_conteudo_data = conn.execute('SELECT * FROM progresso_conteudo WHERE progresso_modulo_id = ? AND conteudo_id = ?', (prog_modulo_id, conteudo_id)).fetchone()
            prog_conteudo = ProgressoConteudo(**prog_conteudo_data) if prog_conteudo_data else None
            
            # Se não houver progresso para este conteúdo, criar um registro inicial
            if not prog_conteudo:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO progresso_conteudo (progresso_modulo_id, conteudo_id, concluido, data_conclusao, xp_ganho, moedas_ganhas)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (prog_modulo_id, conteudo_id, 0, None, 0, 0))
                conn.commit()
                prog_conteudo_data = conn.execute('SELECT * FROM progresso_conteudo WHERE progresso_modulo_id = ? AND conteudo_id = ?', (prog_modulo_id, conteudo_id)).fetchone()
                prog_conteudo = ProgressoConteudo(**prog_conteudo_data)


    conn.close()
    return render_template('content_view.html', content=content, modulo_info=modulo_info, prog_conteudo=prog_conteudo)

@app.route('/trilhas/conteudo/<int:conteudo_id>/complete', methods=['POST'])
@login_required
def complete_content(conteudo_id):
    user_id = session['user_id']
    xp_ganho = request.form.get('xp_ganho', type=int, default=0)
    moedas_ganhas = request.form.get('moedas_ganhas', type=int, default=0)

    conn = get_db_connection()
    try:
        # Encontrar progresso_modulo_id e progresso_trilha_id
        modulo_info = conn.execute('SELECT m.id AS modulo_id, t.id AS trilha_id FROM conteudo_modulo cm JOIN modulos m ON cm.modulo_id = m.id JOIN trilhas_educacionais t ON m.trilha_id = t.id WHERE cm.conteudo_id = ?', (conteudo_id,)).fetchone()
        if not modulo_info:
            flash('Conteúdo não associado a um módulo/trilha.', 'danger')
            return redirect(url_for('view_trilha_content', conteudo_id=conteudo_id))

        prog_trilha_data = conn.execute('SELECT id FROM progresso_usuario_trilha WHERE usuario_id = ? AND trilha_id = ?', (user_id, modulo_info['trilha_id'])).fetchone()
        if not prog_trilha_data:
            flash('Você não está inscrito nesta trilha.', 'danger')
            return redirect(url_for('view_trilha_content', conteudo_id=conteudo_id))
        prog_trilha_id = prog_trilha_data['id']

        prog_modulo_data = conn.execute('SELECT id FROM progresso_modulo WHERE progresso_trilha_id = ? AND modulo_id = ?', (prog_trilha_id, modulo_info['modulo_id'])).fetchone()
        if not prog_modulo_data:
            # Se não existe, cria o progresso do módulo
            cursor = conn.cursor()
            cursor.execute('INSERT INTO progresso_modulo (progresso_trilha_id, modulo_id, concluido, data_conclusao) VALUES (?, ?, ?, ?)',
                           (prog_trilha_id, modulo_info['modulo_id'], 0, None))
            conn.commit()
            prog_modulo_id = cursor.lastrowid
        else:
            prog_modulo_id = prog_modulo_data['id']

        # Atualiza progresso do conteúdo
        conn.execute('UPDATE progresso_conteudo SET concluido = 1, data_conclusao = ?, xp_ganho = ?, moedas_ganhas = ? WHERE progresso_modulo_id = ? AND conteudo_id = ?',
                     (datetime.now().isoformat(), xp_ganho, moedas_ganhas, prog_modulo_id, conteudo_id))
        
        # Adiciona XP e moedas ao perfil do usuário
        conn.execute('UPDATE perfis SET xp = xp + ? WHERE usuario_id = ?', (xp_ganho, user_id))
        # TODO: Adicionar moedas ao perfil (precisaria de uma coluna 'moedas' na tabela perfis)

        # Lógica para verificar e conceder conquistas (simplificada)
        # Ex: Conquista por completar 100 XP
        if xp_ganho > 0:
            user_current_xp_data = conn.execute('SELECT xp FROM perfis WHERE usuario_id = ?', (user_id,)).fetchone()
            user_current_xp = user_current_xp_data['xp'] if user_current_xp_data else 0

            if user_current_xp >= 100: # Exemplo de critério para uma conquista
                conquista_id_data = conn.execute('SELECT id FROM conquistas WHERE titulo = ?', ('Explorador Iniciante',)).fetchone()
                if conquista_id_data and not conn.execute('SELECT 1 FROM usuario_conquistas WHERE usuario_id = ? AND conquista_id = ?', (user_id, conquista_id_data['id'])).fetchone():
                    conn.execute('INSERT INTO usuario_conquistas (usuario_id, conquista_id, data_conquista) VALUES (?, ?, ?)', (user_id, conquista_id_data['id'], datetime.now().isoformat()))
                    flash('Conquista desbloqueada: Explorador Iniciante!', 'success')
                    # Notificar o usuário sobre a conquista
                    notif_message = 'Parabéns! Você desbloqueou a conquista "Explorador Iniciante"!'
                    notif_link = url_for('user_profile') # Link para o perfil ou página de conquistas
                    conn.execute('INSERT INTO notificacoes (usuario_id, mensagem, link, data_envio) VALUES (?, ?, ?, ?)', (user_id, notif_message, notif_link, datetime.now().isoformat()))


        conn.commit()
        flash('Conteúdo concluído! Você ganhou XP e moedas!', 'success')

        # Atualizar progresso do módulo e trilha
        # Contar conteúdos concluídos no módulo
        total_contents_in_module = conn.execute('SELECT COUNT(*) FROM conteudo_modulo WHERE modulo_id = ?', (modulo_info['modulo_id'],)).fetchone()[0]
        completed_contents_in_module = conn.execute('SELECT COUNT(*) FROM progresso_conteudo WHERE progresso_modulo_id = ? AND concluido = 1', (prog_modulo_id,)).fetchone()[0]
        
        if total_contents_in_module > 0 and completed_contents_in_module == total_contents_in_module:
            conn.execute('UPDATE progresso_modulo SET concluido = 1, data_conclusao = ? WHERE id = ?', (datetime.now().isoformat(), prog_modulo_id))
            # Verificar se o módulo é o último e se a trilha foi concluída
            total_modules_in_trilha = conn.execute('SELECT COUNT(*) FROM modulos WHERE trilha_id = ?', (modulo_info['trilha_id'],)).fetchone()[0]
            completed_modules_in_trilha = conn.execute('SELECT COUNT(*) FROM progresso_modulo pm JOIN progresso_usuario_trilha put ON pm.progresso_trilha_id = put.id WHERE put.usuario_id = ? AND put.trilha_id = ? AND pm.concluido = 1', (user_id, modulo_info['trilha_id'])).fetchone()[0]
            
            if total_modules_in_trilha > 0 and completed_modules_in_trilha == total_modules_in_trilha:
                conn.execute('UPDATE progresso_usuario_trilha SET concluida = 1, progresso_percentual = 100.0, ultimo_acesso_data = ? WHERE id = ?', (datetime.now().isoformat(), prog_trilha_id))
                flash('Parabéns! Você concluiu a trilha!', 'success')

        conn.commit() # Commit final para todas as atualizações de progresso
    except Exception as e:
        flash(f'Erro ao concluir conteúdo: {e}', 'danger')
        print(f"DEBUG: Erro ao concluir conteúdo: {e}")
    finally:
        conn.close()
    
    # Redireciona de volta para o módulo ou para o próximo conteúdo
    return redirect(url_for('modulo_detail', trilha_id=modulo_info['trilha_id'], modulo_id=modulo_info['modulo_id']))


# --- Rotas de Ranking e Conquistas ---
@app.route('/ranking')
def ranking():
    conn = get_db_connection()
    # Exemplo de ranking por XP
    top_users_xp_data = conn.execute('SELECT u.nome_usuario, p.xp, p.nivel FROM usuarios u JOIN perfis p ON u.id = p.usuario_id ORDER BY p.xp DESC LIMIT 10').fetchall()
    top_users_xp = [dict(row) for row in top_users_xp_data]
    
    # Exemplo de ranking por trilhas concluídas
    top_users_trilhas_data = conn.execute('''
        SELECT u.nome_usuario, COUNT(put.usuario_id) AS trilhas_concluidas
        FROM usuarios u
        JOIN progresso_usuario_trilha put ON u.id = put.usuario_id
        WHERE put.concluida = 1
        GROUP BY u.id
        ORDER BY trilhas_concluidas DESC LIMIT 10
    ''').fetchall()
    top_users_trilhas = [dict(row) for row in top_users_trilhas_data]

    conn.close()
    return render_template('ranking.html', top_users_xp=top_users_xp, top_users_trilhas=top_users_trilhas)

@app.route('/conquistas')
@login_required
def user_conquistas():
    user_id = session['user_id']
    conn = get_db_connection()
    
    user_conquistas_data = conn.execute('''
        SELECT c.*, uc.data_conquista
        FROM conquistas c
        JOIN usuario_conquistas uc ON c.id = uc.conquista_id
        WHERE uc.usuario_id = ?
        ORDER BY uc.data_conquista DESC
    ''', (user_id,)).fetchall()
    
    user_conquistas_list = [dict(row) for row in user_conquistas_data]

    # Obter todas as conquistas disponíveis para mostrar as que faltam
    all_conquistas_data = conn.execute('SELECT * FROM conquistas ORDER BY titulo').fetchall()
    all_conquistas = [Conquista(**row) for row in all_conquistas_data]

    conn.close()
    return render_template('conquistas.html', user_conquistas=user_conquistas_list, all_conquistas=all_conquistas)

@app.route('/conquistas/add_default', methods=['POST'])
@admin_required # Apenas para adicionar conquistas padrão via admin
def add_default_conquistas():
    conn = get_db_connection()
    default_conquistas = [
        {'titulo': 'Primeiro Passo Estelar', 'descricao': 'Conclua seu primeiro conteúdo educacional.', 'icone_url': 'https://placehold.co/50x50/00FFFF/000000?text=C1', 'pontos_xp_concedidos': 10},
        {'titulo': 'Explorador Iniciante', 'descricao': 'Acumule 100 XP na plataforma.', 'icone_url': 'https://placehold.co/50x50/FFD700/000000?text=C2', 'pontos_xp_concedidos': 20},
        {'titulo': 'Mestre da Galáxia', 'descricao': 'Conclua 5 trilhas de aprendizado.', 'icone_url': 'https://placehold.co/50x50/8A2BE2/FFFFFF?text=C3', 'pontos_xp_concedidos': 50},
        {'titulo': 'Comentarista Estelar', 'descricao': 'Faça 10 comentários em artigos ou fóruns.', 'icone_url': 'https://placehold.co/50x50/008000/FFFFFF?text=C4', 'pontos_xp_concedidos': 15},
    ]
    try:
        for conquista in default_conquistas:
            conn.execute('INSERT OR IGNORE INTO conquistas (titulo, descricao, icone_url, pontos_xp_concedidos) VALUES (?, ?, ?, ?)',
                         (conquista['titulo'], conquista['descricao'], conquista['icone_url'], conquista['pontos_xp_concedidos']))
        conn.commit()
        flash('Conquistas padrão adicionadas!', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar conquistas padrão: {e}', 'danger')
        print(f"DEBUG: Erro ao adicionar conquistas padrão: {e}")
    finally:
        conn.close()
    return redirect(url_for('admin_profile'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
