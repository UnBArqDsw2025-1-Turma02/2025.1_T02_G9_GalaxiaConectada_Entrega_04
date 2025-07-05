import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
import json


# Define o caminho para a pasta db_data e o arquivo do banco de dados
DB_DIR = os.path.join(os.path.dirname(__file__), 'db_data')
DATABASE = os.path.join(DB_DIR, 'galaxia.db')

def init_db():
    # Cria a pasta db_data se ela não existir
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Tabela Usuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            nome_usuario TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            data_cadastro TEXT NOT NULL,
            tipo_usuario TEXT DEFAULT 'Visitante' NOT NULL, -- Alterado para 'Visitante' como padrão
            permissoes TEXT DEFAULT '[]', -- Armazenar como JSON string
            nivel_acesso INTEGER DEFAULT 1 -- Novo campo para Nível de Acesso
        )
    ''')

    # Tabela Perfil (dados adicionais do usuário)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS perfis (
            usuario_id INTEGER PRIMARY KEY,
            nivel INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            linguagem_pref TEXT DEFAULT 'pt-BR',
            avatar_url TEXT DEFAULT 'default_avatar.png',
            bio TEXT,
            -- Campos específicos para Aluno
            progresso_geral REAL DEFAULT 0.0,
            ultimo_acesso_trilha TEXT,
            -- Campos específicos para Instrutor
            biografia_curta TEXT,
            avaliacao_media REAL DEFAULT 0.0,
            especialidades TEXT DEFAULT '[]', -- Armazenar como JSON string
            -- Campos específicos para Professor Voluntário
            area_especialidade TEXT,
            artigos_revisados INTEGER DEFAULT 0,
            -- Campos específicos para Moderador
            nivel_moderacao TEXT,
            data_inicio_moderacao TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Pets Base (definições dos tipos de pet)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL, -- Ex: 'Sol', 'Lua', 'Gato', 'Robo'
            aparencia_url_fase1 TEXT NOT NULL,
            aparencia_url_fase2 TEXT NOT NULL,
            aparencia_url_fase3 TEXT NOT NULL,
            descricao TEXT NOT NULL
        )
    ''')

    # Tabela para Pets do Usuário (instância do pet que o usuário possui)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER UNIQUE NOT NULL, -- Um pet por usuário
            pet_base_id INTEGER NOT NULL,
            nome_personalizado TEXT, -- Nome que o usuário dá ao pet
            fase_atual INTEGER DEFAULT 1,
            xp_acumulado INTEGER DEFAULT 0,
            itens_equipados TEXT DEFAULT '[]', -- JSON string de IDs de itens
            ultima_atualizacao TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (pet_base_id) REFERENCES pets_base(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Itens de Personalização de Pets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pet_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            tipo_pet_compativel TEXT, -- 'Sol', 'Lua', 'Gato', 'Robo' ou 'Todos'
            aparencia_url TEXT NOT NULL,
            preco_xp INTEGER NOT NULL
        )
    ''')

    # Tabela para Conteúdos (Artigos, Notícias, Blog Posts - BASE)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conteudos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL, -- Resumo/snippet
            data_publicacao TEXT NOT NULL,
            visibilidade TEXT DEFAULT 'publico' NOT NULL, -- 'publico', 'privado'
            autor_id INTEGER NOT NULL,
            categoria TEXT NOT NULL, -- 'estrelas', 'buracos negros', 'missões espaciais', etc.
            imagem_url TEXT, -- Imagem principal do conteúdo
            fonte_url TEXT, -- URL da fonte original (opcional)
            tipo_conteudo TEXT NOT NULL, -- 'Artigo', 'Video', 'Quiz', 'Jogo', 'Blog Post'
            FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Artigos (Extensão de Conteudos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artigos (
            conteudo_id INTEGER PRIMARY KEY,
            texto_html TEXT NOT NULL,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Vídeos (Extensão de Conteudos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            conteudo_id INTEGER PRIMARY KEY,
            url_video TEXT NOT NULL,
            duracao_segundos INTEGER,
            transcricao TEXT,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Quizzes (Extensão de Conteudos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quizzes (
            conteudo_id INTEGER PRIMARY KEY,
            tempo_limite_min INTEGER,
            tentativas_permitidas INTEGER,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Questões de Quiz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS questoes_quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quiz_id INTEGER NOT NULL,
            texto_questao TEXT NOT NULL,
            tipo_questao TEXT NOT NULL, -- 'multipla_escolha', 'verdadeiro_falso'
            FOREIGN KEY (quiz_id) REFERENCES quizzes(conteudo_id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Alternativas de Quiz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alternativas_quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            questao_id INTEGER NOT NULL,
            texto_alternativa TEXT NOT NULL,
            correta INTEGER NOT NULL, -- 0 para false, 1 para true
            FOREIGN KEY (questao_id) REFERENCES questoes_quiz(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Tentativas de Quiz
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tentativas_quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            data_tentativa TEXT NOT NULL,
            pontuacao REAL NOT NULL,
            concluida INTEGER NOT NULL, -- 0 para false, 1 para true
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(conteudo_id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Respostas de Quiz (detalhes da tentativa)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respostas_quiz (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tentativa_id INTEGER NOT NULL,
            questao_id INTEGER NOT NULL,
            alternativa_selecionada_id INTEGER, -- NULL para verdadeiro/falso ou resposta aberta
            resposta_texto TEXT, -- Para respostas abertas
            FOREIGN KEY (tentativa_id) REFERENCES tentativas_quiz(id) ON DELETE CASCADE,
            FOREIGN KEY (questao_id) REFERENCES questoes_quiz(id) ON DELETE CASCADE,
            FOREIGN KEY (alternativa_selecionada_id) REFERENCES alternativas_quiz(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Jogos (Extensão de Conteudos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jogos (
            conteudo_id INTEGER PRIMARY KEY,
            tipo_jogo TEXT,
            nivel_dificuldade INTEGER,
            url_jogo TEXT NOT NULL,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Sessões de Jogo (registra cada vez que um usuário joga)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessoes_jogo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            jogo_id INTEGER NOT NULL,
            data_inicio TEXT NOT NULL,
            data_fim TEXT,
            pontuacao INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (jogo_id) REFERENCES jogos(conteudo_id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Pontuações de Jogo (melhores pontuações para ranking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pontuacoes_jogo (
            usuario_id INTEGER NOT NULL,
            jogo_id INTEGER NOT NULL,
            melhor_pontuacao INTEGER NOT NULL,
            data_recorde TEXT NOT NULL,
            PRIMARY KEY (usuario_id, jogo_id), -- Um recorde por usuário por jogo
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (jogo_id) REFERENCES jogos(conteudo_id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Curtidas em Conteúdos 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS curtidas (
            usuario_id INTEGER NOT NULL,
            conteudo_id INTEGER NOT NULL,
            data_curtida TEXT NOT NULL,
            PRIMARY KEY (usuario_id, conteudo_id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Comentários 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comentarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conteudo_id INTEGER,
            postagem_id INTEGER,
            usuario_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            data_comentario TEXT NOT NULL,
            editado INTEGER DEFAULT 0 NOT NULL,
            data_edicao TEXT,
            upvotes INTEGER DEFAULT 0 NOT NULL,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE,
            FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            CONSTRAINT chk_conteudo_or_postagem CHECK (
                (conteudo_id IS NOT NULL AND postagem_id IS NULL) OR
                (conteudo_id IS NULL AND postagem_id IS NOT NULL)
            )
        )
    ''')

    # Tabela para Notificações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notificacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            mensagem TEXT NOT NULL,
            link TEXT,
            data_envio TEXT NOT NULL,
            lida INTEGER DEFAULT 0 NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Inscrições em Categorias 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscricoes_categoria (
            usuario_id INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            PRIMARY KEY (usuario_id, categoria),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Trilhas Educacionais
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trilhas_educacionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            nivel TEXT NOT NULL, -- 'Iniciante', 'Intermediário', 'Avançado'
            categoria TEXT NOT NULL, -- 'Estrelas', 'Planetas', 'Cosmologia'
            publicada INTEGER DEFAULT 0 NOT NULL, -- 0 para false, 1 para true
            imagem_url TEXT,
            autor_id INTEGER NOT NULL,
            FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Módulos (dentro de Trilhas)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS modulos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trilha_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            ordem INTEGER NOT NULL,
            descricao_breve TEXT,
            FOREIGN KEY (trilha_id) REFERENCES trilhas_educacionais(id) ON DELETE CASCADE
        )
    ''')

    # Tabela de Associação: Conteúdo dentro de Módulos de Trilhas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conteudo_modulo (
            modulo_id INTEGER NOT NULL,
            conteudo_id INTEGER NOT NULL,
            ordem_no_modulo INTEGER NOT NULL,
            tipo_conteudo_fk TEXT NOT NULL, -- 'Artigo', 'Video', 'Quiz', 'Jogo'
            PRIMARY KEY (modulo_id, conteudo_id),
            FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela de Progresso do Usuário em Trilhas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso_usuario_trilha (
            usuario_id INTEGER NOT NULL,
            trilha_id INTEGER NOT NULL,
            progresso_percentual REAL DEFAULT 0.0 NOT NULL,
            ultimo_acesso_data TEXT NOT NULL,
            concluida INTEGER DEFAULT 0 NOT NULL, -- 0 para false, 1 para true
            PRIMARY KEY (usuario_id, trilha_id), -- Um progresso por usuário por trilha
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (trilha_id) REFERENCES trilhas_educacionais(id) ON DELETE CASCADE
        )
    ''')

    # Tabela de Progresso do Usuário em Módulos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso_modulo (
            progresso_trilha_id INTEGER NOT NULL,
            modulo_id INTEGER NOT NULL,
            concluido INTEGER DEFAULT 0 NOT NULL,
            data_conclusao TEXT,
            PRIMARY KEY (progresso_trilha_id, modulo_id),
            FOREIGN KEY (progresso_trilha_id) REFERENCES progresso_usuario_trilha(id) ON DELETE CASCADE,
            FOREIGN KEY (modulo_id) REFERENCES modulos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela de Progresso do Usuário em Conteúdos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS progresso_conteudo (
            progresso_modulo_id INTEGER NOT NULL,
            conteudo_id INTEGER NOT NULL,
            concluido INTEGER DEFAULT 0 NOT NULL,
            data_conclusao TEXT,
            xp_ganho INTEGER DEFAULT 0 NOT NULL,
            moedas_ganhas INTEGER DEFAULT 0 NOT NULL,
            PRIMARY KEY (progresso_modulo_id, conteudo_id),
            FOREIGN KEY (progresso_modulo_id) REFERENCES progresso_modulo(id) ON DELETE CASCADE,
            FOREIGN KEY (conteudo_id) REFERENCES conteudos(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Conquistas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conquistas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL UNIQUE,
            descricao TEXT NOT NULL,
            icone_url TEXT NOT NULL,
            pontos_xp_concedidos INTEGER NOT NULL
        )
    ''')

    # Tabela de Associação: Usuário e Conquistas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario_conquistas (
            usuario_id INTEGER NOT NULL,
            conquista_id INTEGER NOT NULL,
            data_conquista TEXT NOT NULL,
            progresso_origem_id INTEGER, -- FK opcional para progresso_usuario_trilha ou outro
            PRIMARY KEY (usuario_id, conquista_id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (conquista_id) REFERENCES conquistas(id) ON DELETE CASCADE,
            FOREIGN KEY (progresso_origem_id) REFERENCES progresso_usuario_trilha(id) ON DELETE SET NULL
        )
    ''')

 # Tabela para Subfóruns
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subforums (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            ordem_exibicao INTEGER DEFAULT 0
        )
    ''')
    conn.commit()

    # Tabela para Tópicos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS topicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subforum_id INTEGER NOT NULL,
            autor_id INTEGER NOT NULL,
            titulo TEXT NOT NULL,
            data_criacao TEXT NOT NULL,
            data_ult_post TEXT NOT NULL,
            fixado INTEGER DEFAULT 0 NOT NULL,
            fechado INTEGER DEFAULT 0 NOT NULL,
            upvotes INTEGER DEFAULT 0 NOT NULL,
            FOREIGN KEY (subforum_id) REFERENCES subforums(id) ON DELETE CASCADE,
            FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Postagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS postagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topico_id INTEGER NOT NULL,
            autor_id INTEGER NOT NULL,
            texto TEXT NOT NULL,
            data_postagem TEXT NOT NULL,
            editado INTEGER DEFAULT 0 NOT NULL,
            data_edicao TEXT,
            upvotes INTEGER DEFAULT 0 NOT NULL,
            FOREIGN KEY (topico_id) REFERENCES topicos(id) ON DELETE CASCADE,
            FOREIGN KEY (autor_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
    ''')

    # Tabela para Votos em Postagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS votos_postagem (
            usuario_id INTEGER NOT NULL,
            postagem_id INTEGER NOT NULL,
            tipo_voto TEXT NOT NULL, -- 'upvote' ou 'downvote'
            data_voto TEXT NOT NULL,
            PRIMARY KEY (usuario_id, postagem_id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
            FOREIGN KEY (postagem_id) REFERENCES postagens(id) ON DELETE CASCADE
        )
    ''')

    # Inserir os Pets Base (se não existirem)
    pets_data = [
        ('Lumio', 'Sol', 
         'https://placehold.co/150x150/FFD700/000000?text=Lumio+F1',
         'https://placehold.co/150x150/FFD700/000000?text=Lumio+F2',
         'https://placehold.co/150x150/FFD700/000000?text=Lumio+F3',
         'Um pet dourado, sempre sorridente, com olhos brilhantes e uma aura que muda de intensidade conforme evolui.'),
        ('Selena', 'Lua',
         'https://placehold.co/150x150/C0C0C0/000000?text=Selena+F1',
         'https://placehold.co/150x150/C0C0C0/000000?text=Selena+F2',
         'https://placehold.co/150x150/C0C0C0/000000?text=Selena+F3',
         'Um pet cinza-prateado com orelhinhas de coelho. Sempre muda sua forma em fases.'),
        ('Nebby', 'Gato',
         'https://placehold.co/150x150/8A2BE2/FFFFFF?text=Nebby+F1',
         'https://placehold.co/150x150/8A2BE2/FFFFFF?text=Nebby+F2',
         'https://placehold.co/150x150/8A2BE2/FFFFFF?text=Nebby+F3',
         'Um gato espacial feito de poeira cósmica e estrelas cintilantes. Muda de cor conforme o humor.'),
        ('Orbix', 'Robo',
         'https://placehold.co/150x150/4682B4/FFFFFF?text=Orbix+F1',
         'https://placehold.co/150x150/4682B4/FFFFFF?text=Orbix+F2',
         'https://placehold.co/150x150/4682B4/FFFFFF?text=Orbix+F3',
         'Um pet redondo com anéis orbitais e aparência meio robótica. Inteligente e leal.')
    ]

    for nome, tipo, url1, url2, url3, descricao in pets_data:
        cursor.execute("SELECT id FROM pets_base WHERE nome = ?", (nome,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO pets_base (nome, tipo, aparencia_url_fase1, aparencia_url_fase2, aparencia_url_fase3, descricao)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, tipo, url1, url2, url3, descricao))
            conn.commit()
            print(f"Pet base '{nome}' inserido.")
        else:
            print(f"Pet base '{nome}' já existe.")

    # Inserir Itens de Personalização 
    item_data = [
        ('Óculos de Sol', 'Óculos escuros para o Lumio.', 'Sol', 'https://placehold.co/50x50/000000/FFFFFF?text=Oculos', 80),
        ('Chapéu de Explorador', 'Um chapéu estiloso para aventuras.', 'Sol', 'https://placehold.co/50x50/8B4513/FFFFFF?text=Chapeu', 120),
        ('Lacinhos Estelares', 'Lacinhos fofos para a Selena.', 'Lua', 'https://placehold.co/50x50/FFC0CB/000000?text=Laco', 70),
        ('Máscara de Dormir', 'Para os momentos de descanso da Selena.', 'Lua', 'https://placehold.co/50x50/000000/FFFFFF?text=Mascara', 90),
        ('Anteninhas Alienígenas', 'Anteninhas para o Nebby.', 'Gato', 'https://placehold.co/50x50/00FF00/000000?text=Antenas', 100),
        ('Coleira Estelar', 'Uma coleira que brilha no escuro para o Nebby.', 'Gato', 'https://placehold.co/50x50/0000FF/FFFFFF?text=Coleira', 110),
        ('Propulsores', 'Para o Orbix voar mais rápido.', 'Robo', 'https://placehold.co/50x50/FF0000/FFFFFF?text=Propulsor', 150),
        ('Óculos RA', 'Óculos de Realidade Aumentada para o Orbix.', 'Robo', 'https://placehold.co/50x50/00FFFF/000000?text=RA', 130),
        ('Mochila de Telescópio', 'Uma mochila para o Astromiau levar seu telescópio.', 'Gato', 'https://placehold.co/50x50/A0522D/FFFFFF?text=Mochila', 180)
    ]

    for nome, descricao, tipo_compativel, url, preco_xp in item_data:
        cursor.execute("SELECT id FROM pet_items WHERE nome = ?", (nome,))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO pet_items (nome, descricao, tipo_pet_compativel, aparencia_url, preco_xp)
                VALUES (?, ?, ?, ?, ?)
            ''', (nome, descricao, tipo_compativel, url, preco_xp))
            conn.commit()
            print(f"Item '{nome}' inserido.")
        else:
            print(f"Item '{nome}' já existe.")


    # Inserir o usuário Administrador (Bruce Wayne)
    senha_hashed_bruce = generate_password_hash("IamBatman")
    data_cadastro_bruce = datetime(2025, 7, 1).isoformat()
    
    permissoes_admin = json.dumps([
        "gerenciar_usuarios", "aprovar_conteudo", "gerenciar_promocoes", 
        "alterar_status_usuario", "moderar_forum", "gerenciar_trilhas", 
        "gerenciar_conteudo", "ver_logs", "gerenciar_configuracoes_globais",
        "publicar_conteudo" 
    ])
    nivel_acesso_admin = 5 

    try:
        cursor.execute("SELECT id FROM usuarios WHERE nome_usuario = ? OR email = ?", ('BruceMorceguinho', 'BruceWayne@gmail.com'))
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute('''
                INSERT INTO usuarios (nome_completo, email, nome_usuario, senha_hash, data_cadastro, tipo_usuario, permissoes, nivel_acesso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', ('Bruce Wayne', 'BruceWayne@gmail.com', 'BruceMorceguinho', senha_hashed_bruce, data_cadastro_bruce, 'Administrador', permissoes_admin, nivel_acesso_admin))
            
            cursor.execute('''
                INSERT INTO perfis (usuario_id, nivel, xp, bio)
                VALUES (?, ?, ?, ?)
            ''', (cursor.lastrowid, 99, 10000, 'Guardião da Galáxia Conectada.'))
            
            conn.commit()
            print("Banco de dados inicializado e usuário Administrador 'Bruce Wayne' criado com sucesso.")
        else:
            print("Usuário 'BruceMorceguinho' ou 'BruceWayne@gmail.com' já existe. Banco de dados já inicializado com o administrador.")
    except sqlite3.IntegrityError as e:
        print(f"Erro de integridade ao inicializar DB: {e}. Provavelmente usuário já existe.")
    except Exception as e:
        print(f"Erro inesperado ao inicializar DB: {e}")
    finally:
        pass

    # --- Adicionar novos usuários ---
    users_to_add = [
        {
            'nome_completo': 'Hermione Granger',
            'email': 'HermioneGranger@aluno.hogwarts.com',
            'nome_usuario': 'Hermione',
            'senha': 'Alohomora',
            'tipo_usuario': 'Aluno',
            'permissoes': [],
            'nivel_acesso': 1,
            'perfil_bio': 'Sempre pronta para aprender e explorar os mistérios do universo.'
        },
        {
            'nome_completo': 'Harry Potter',
            'email': 'HarryPotter@aluno.hogwarts.com',
            'nome_usuario': 'Harry Potter',
            'senha': 'Alohomora',
            'tipo_usuario': 'Aluno',
            'permissoes': [],
            'nivel_acesso': 1,
            'perfil_bio': 'O garoto que sobreviveu e agora explora a Galáxia Conectada.'
        },
        {
            'nome_completo': 'Severo Snape',
            'email': 'SeveroSnape@professor.hogwarts.com',
            'nome_usuario': 'Professor Snape',
            'senha': 'Alohomora',
            'tipo_usuario': 'ProfessorVoluntario',
            'permissoes': ["publicar_conteudo", "gerenciar_trilhas", "gerenciar_conteudo"],
            'nivel_acesso': 3,
            'perfil_bio': 'Mestre em Poções e entusiasta da astrofísica teórica.',
            'area_especialidade': 'Astrofísica Teórica',
            'artigos_revisados': 5
        },
        {
            'nome_completo': 'Argus Filch',
            'email': 'ArgusFilch@moderador.hogwarts.com',
            'nome_usuario': 'Argus Filch',
            'senha': 'Alohomora',
            'tipo_usuario': 'Moderador',
            'permissoes': ["moderar_forum"],
            'nivel_acesso': 2,
            'perfil_bio': 'Zelador da ordem e da disciplina no fórum da Galáxia.',
            'nivel_moderacao': 'Básico',
            'data_inicio_moderacao': datetime.now().isoformat()
        }
    ]

    user_ids = {} # Para armazenar os IDs dos usuários recém-criados

    for user_data in users_to_add:
        senha_hashed = generate_password_hash(user_data['senha'])
        data_cadastro = datetime.now().isoformat()
        
        cursor.execute("SELECT id FROM usuarios WHERE nome_usuario = ? OR email = ?", (user_data['nome_usuario'], user_data['email']))
        existing_user = cursor.fetchone()

        if not existing_user:
            cursor.execute('''
                INSERT INTO usuarios (nome_completo, email, nome_usuario, senha_hash, data_cadastro, tipo_usuario, permissoes, nivel_acesso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_data['nome_completo'], user_data['email'], user_data['nome_usuario'], senha_hashed, data_cadastro, user_data['tipo_usuario'], json.dumps(user_data['permissoes']), user_data['nivel_acesso']))
            
            user_id = cursor.lastrowid
            user_ids[user_data['nome_usuario']] = user_id

            # Inserir perfil com dados específicos do tipo de usuário
            profile_params = {
                'usuario_id': user_id,
                'nivel': 1,
                'xp': 0,
                'bio': user_data['perfil_bio']
            }
            if user_data['tipo_usuario'] == 'ProfessorVoluntario':
                profile_params['area_especialidade'] = user_data['area_especialidade']
                profile_params['artigos_revisados'] = user_data['artigos_revisados']
            elif user_data['tipo_usuario'] == 'Moderador':
                profile_params['nivel_moderacao'] = user_data['nivel_moderacao']
                profile_params['data_inicio_moderacao'] = user_data['data_inicio_moderacao']
            
            # Construir a query de INSERT dinamicamente para perfis
            columns = ', '.join(profile_params.keys())
            placeholders = ', '.join(['?'] * len(profile_params))
            values = tuple(profile_params.values())

            cursor.execute(f'''
                INSERT INTO perfis ({columns})
                VALUES ({placeholders})
            ''', values)
            
            conn.commit()
            print(f"Usuário '{user_data['nome_usuario']}' ({user_data['tipo_usuario']}) criado com sucesso.")
        else:
            user_ids[user_data['nome_usuario']] = existing_user[0] # Armazena o ID do usuário existente
            print(f"Usuário '{user_data['nome_usuario']}' já existe. Ignorando inserção.")
    
    # --- Inserir Subfórum, Tópico e Postagens ---
    try:
        # Inserir Subfórum
        cursor.execute("SELECT id FROM subforums WHERE nome = ?", ('Astronomia Geral',))
        subforum_exists = cursor.fetchone()
        if not subforum_exists:
            cursor.execute('''
                INSERT INTO subforums (nome, descricao, ordem_exibicao)
                VALUES (?, ?, ?)
            ''', ('Astronomia Geral', 'Espaço para discutir tudo sobre o universo, desde os planetas até as galáxias mais distantes.', 1))
            conn.commit()
            subforum_id = cursor.lastrowid
            print("Subfórum 'Astronomia Geral' criado.")
        else:
            subforum_id = subforum_exists[0]
            print("Subfórum 'Astronomia Geral' já existe.")

        # Inserir Tópico
        cursor.execute("SELECT id FROM topicos WHERE titulo = ?", ('Qual a sua teoria favorita sobre o Big Bang?',))
        topic_exists = cursor.fetchone()
        if not topic_exists:
            autor_id_snape = user_ids.get('Professor Snape')
            if autor_id_snape:
                data_criacao_topico = datetime.now().isoformat()
                cursor.execute('''
                    INSERT INTO topicos (subforum_id, autor_id, titulo, data_criacao, data_ult_post)
                    VALUES (?, ?, ?, ?, ?)
                ''', (subforum_id, autor_id_snape, 'Qual a sua teoria favorita sobre o Big Bang?', data_criacao_topico, data_criacao_topico))
                conn.commit()
                topic_id = cursor.lastrowid
                print("Tópico 'Qual a sua teoria favorita sobre o Big Bang?' criado.")
            else:
                print("Professor Snape não encontrado para criar o tópico.")
                topic_id = None
        else:
            topic_id = topic_exists[0]
            print("Tópico 'Qual a sua teoria favorita sobre o Big Bang?' já existe.")

        # Inserir Postagens no Tópico (se o tópico foi criado ou já existe)
        if topic_id:
            posts_to_add = [
                {
                    'autor_nome': 'Professor Snape',
                    'texto': 'Gostaria de iniciar uma discussão sobre as diversas teorias do Big Bang. Qual delas vocês acham mais plausível e por quê? Pessoalmente, acho a teoria da Inflação Cósmica fascinante por resolver alguns problemas do modelo padrão.'
                },
                {
                    'autor_nome': 'Hermione',
                    'texto': 'Eu concordo com o Professor Snape! A Inflação Cósmica realmente parece explicar a homogeneidade e a planicidade do universo de forma elegante. Além disso, a ideia de um multiverso que surge a partir dela é intrigante, não acham?'
                },
                {
                    'autor_nome': 'Harry Potter',
                    'texto': 'Eu sempre me interessei pela teoria do Universo Oscilante, mesmo que ela tenha sido desfavorecida. A ideia de um ciclo de expansão e contração é bem legal para pensar, como um fôlego cósmico. Alguém mais gosta dessa?'
                }
            ]

            for post_data in posts_to_add:
                autor_id = user_ids.get(post_data['autor_nome'])
                if autor_id:
                    cursor.execute("SELECT id FROM postagens WHERE topico_id = ? AND autor_id = ? AND texto = ?", (topic_id, autor_id, post_data['texto']))
                    post_exists = cursor.fetchone()
                    if not post_exists:
                        data_postagem = datetime.now().isoformat()
                        cursor.execute('''
                            INSERT INTO postagens (topico_id, autor_id, texto, data_postagem)
                            VALUES (?, ?, ?, ?)
                        ''', (topic_id, autor_id, post_data['texto'], data_postagem))
                        conn.commit()
                        print(f"Postagem de '{post_data['autor_nome']}' adicionada ao tópico.")
                    else:
                        print(f"Postagem de '{post_data['autor_nome']}' já existe no tópico. Ignorando inserção.")
                else:
                    print(f"Autor '{post_data['autor_nome']}' não encontrado para adicionar postagem.")
        
    except Exception as e:
        print(f"Erro ao inserir dados do fórum: {e}")
    finally:
        pass 

    # --- Inserir Trilhas de Aprendizado ---
    autor_id_snape = user_ids.get('Professor Snape')
    if autor_id_snape:
        # Trilha 1: Desvendando o Sistema Solar
        trilha_id_solar = None
        cursor.execute("SELECT id FROM trilhas_educacionais WHERE titulo = ?", ("Desvendando o Sistema Solar",))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO trilhas_educacionais (titulo, descricao, nivel, categoria, publicada, imagem_url, autor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('Desvendando o Sistema Solar', 'Uma jornada completa pelos planetas, luas e outros corpos celestes que compõem nosso lar cósmico.', 'Iniciante', 'Planetas', 1, 'https://placehold.co/600x400/4682B4/FFFFFF?text=Sistema+Solar', autor_id_snape))
            conn.commit()
            trilha_id_solar = cursor.lastrowid
            print("Trilha 'Desvendando o Sistema Solar' criada.")
        else:
            trilha_id_solar = cursor.fetchone()[0]
            print("Trilha 'Desvendando o Sistema Solar' já existe.")

        if trilha_id_solar:
            # Módulo 1: O Sol e os Planetas Internos
            modulo_id_sol_internos = None
            cursor.execute("SELECT id FROM modulos WHERE trilha_id = ? AND titulo = ?", (trilha_id_solar, "O Sol e os Planetas Internos"))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO modulos (trilha_id, titulo, ordem, descricao_breve)
                    VALUES (?, ?, ?, ?)
                ''', (trilha_id_solar, 'O Sol e os Planetas Internos', 1, 'Explore a estrela que nos dá vida e os mundos rochosos mais próximos a ela.'))
                conn.commit()
                modulo_id_sol_internos = cursor.lastrowid
                print("Módulo 'O Sol e os Planetas Internos' criado.")
            else:
                modulo_id_sol_internos = cursor.fetchone()[0]
                print("Módulo 'O Sol e os Planetas Internos' já existe.")

            if modulo_id_sol_internos:
                # Conteúdo 1.1: Artigo "O Coração do Nosso Sistema: O Sol"
                conteudo_id_sol = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("O Coração do Nosso Sistema: O Sol",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('O Coração do Nosso Sistema: O Sol', 'Descubra os segredos da nossa estrela, sua composição e importância para a vida.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Estrelas', 'https://placehold.co/400x250/FFD700/000000?text=O+Sol', 'Artigo'))
                    conn.commit()
                    conteudo_id_sol = cursor.lastrowid
                    cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (conteudo_id_sol, '<p>O Sol é o centro do nosso Sistema Solar e a estrela mais próxima da Terra. Ele é uma esfera gigante de plasma quente, com um diâmetro de cerca de 1,39 milhão de quilômetros, cerca de 109 vezes o diâmetro da Terra.</p><p>A energia do Sol é gerada por reações de fusão nuclear em seu núcleo, onde átomos de hidrogênio se fundem para formar hélio, liberando uma quantidade imensa de energia. Essa energia viaja para fora, através das camadas do Sol, e é emitida como luz e calor.</p><p>A luz solar leva cerca de 8 minutos e 20 segundos para chegar à Terra. Sem o Sol, não haveria vida em nosso planeta, pois ele é a fonte primária de energia para a fotossíntese e para manter a temperatura da Terra em níveis habitáveis.</p>'))
                    conn.commit()
                    print("Conteúdo 'O Coração do Nosso Sistema: O Sol' criado.")
                else:
                    conteudo_id_sol = cursor.fetchone()[0]
                    print("Conteúdo 'O Coração do Nosso Sistema: O Sol' já existe.")
                
                if conteudo_id_sol:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_sol_internos, conteudo_id_sol))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_sol_internos, conteudo_id_sol, 1, 'Artigo'))
                        conn.commit()
                        print("Conteúdo 'O Coração do Nosso Sistema: O Sol' adicionado ao módulo.")

                # Conteúdo 1.2: Vídeo "Mercúrio e Vênus: Os Vizinhos Mais Próximos"
                conteudo_id_mercurio_venus = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Mercúrio e Vênus: Os Vizinhos Mais Próximos",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Mercúrio e Vênus: Os Vizinhos Mais Próximos', 'Conheça os dois primeiros planetas do Sistema Solar, suas características e curiosidades.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Planetas', 'https://placehold.co/400x250/808080/FFFFFF?text=Mercurio+Venus', 'Video'))
                    conn.commit()
                    conteudo_id_mercurio_venus = cursor.lastrowid
                    cursor.execute('INSERT INTO videos (conteudo_id, url_video, duracao_segundos, transcricao) VALUES (?, ?, ?, ?)', (conteudo_id_mercurio_venus, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 180, 'Uma breve introdução aos planetas Mercúrio e Vênus, suas atmosferas e superfícies.'))
                    conn.commit()
                    print("Conteúdo 'Mercúrio e Vênus: Os Vizinhos Mais Próximos' criado.")
                else:
                    conteudo_id_mercurio_venus = cursor.fetchone()[0]
                    print("Conteúdo 'Mercúrio e Vênus: Os Vizinhos Mais Próximos' já existe.")
                
                if conteudo_id_mercurio_venus:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_sol_internos, conteudo_id_mercurio_venus))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_sol_internos, conteudo_id_mercurio_venus, 2, 'Video'))
                        conn.commit()
                        print("Conteúdo 'Mercúrio e Vênus: Os Vizinhos Mais Próximos' adicionado ao módulo.")

                # Conteúdo 1.3: Quiz "Teste seus Conhecimentos sobre Planetas Rochosos"
                conteudo_id_quiz_rochosos = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Teste seus Conhecimentos sobre Planetas Rochosos",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Teste seus Conhecimentos sobre Planetas Rochosos', 'Um quiz rápido para testar o que você aprendeu sobre os planetas internos.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Planetas', 'https://placehold.co/400x250/FF8C00/000000?text=Quiz', 'Quiz'))
                    conn.commit()
                    conteudo_id_quiz_rochosos = cursor.lastrowid
                    cursor.execute('INSERT INTO quizzes (conteudo_id, tempo_limite_min, tentativas_permitidas) VALUES (?, ?, ?)', (conteudo_id_quiz_rochosos, 5, 3))
                    conn.commit()
                    print("Conteúdo 'Teste seus Conhecimentos sobre Planetas Rochosos' criado.")
                else:
                    conteudo_id_quiz_rochosos = cursor.fetchone()[0]
                    print("Conteúdo 'Teste seus Conhecimentos sobre Planetas Rochosos' já existe.")
                
                if conteudo_id_quiz_rochosos:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_sol_internos, conteudo_id_quiz_rochosos))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_sol_internos, conteudo_id_quiz_rochosos, 3, 'Quiz'))
                        conn.commit()
                        print("Conteúdo 'Teste seus Conhecimentos sobre Planetas Rochosos' adicionado ao módulo.")
                    
                    # Adicionar questões e alternativas para o quiz
                    cursor.execute("SELECT id FROM questoes_quiz WHERE quiz_id = ? AND texto_questao = ?", (conteudo_id_quiz_rochosos, "Qual é o planeta mais quente do Sistema Solar?"))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO questoes_quiz (quiz_id, texto_questao, tipo_questao) VALUES (?, ?, ?)', (conteudo_id_quiz_rochosos, "Qual é o planeta mais quente do Sistema Solar?", "multipla_escolha"))
                        questao_id_1 = cursor.lastrowid
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_1, 'Mercúrio', 0))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_1, 'Vênus', 1))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_1, 'Terra', 0))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_1, 'Marte', 0))
                        conn.commit()
                        print("Questão 1 do quiz adicionada.")

                    cursor.execute("SELECT id FROM questoes_quiz WHERE quiz_id = ? AND texto_questao = ?", (conteudo_id_quiz_rochosos, "A atmosfera de Vênus é composta principalmente por dióxido de carbono."))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO questoes_quiz (quiz_id, texto_questao, tipo_questao) VALUES (?, ?, ?)', (conteudo_id_quiz_rochosos, "A atmosfera de Vênus é composta principalmente por dióxido de carbono.", "verdadeiro_falso"))
                        questao_id_2 = cursor.lastrowid
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_2, 'Verdadeiro', 1))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_2, 'Falso', 0))
                        conn.commit()
                        print("Questão 2 do quiz adicionada.")

            # Módulo 2: Os Gigantes Gasosos e Além
            modulo_id_gigantes = None
            cursor.execute("SELECT id FROM modulos WHERE trilha_id = ? AND titulo = ?", (trilha_id_solar, "Os Gigantes Gasosos e Além"))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO modulos (trilha_id, titulo, ordem, descricao_breve)
                    VALUES (?, ?, ?, ?)
                ''', (trilha_id_solar, 'Os Gigantes Gasosos e Além', 2, 'Aprofunde-se nos maiores planetas do nosso sistema e nos mistérios dos confins gelados.'))
                conn.commit()
                modulo_id_gigantes = cursor.lastrowid
                print("Módulo 'Os Gigantes Gasosos e Além' criado.")
            else:
                modulo_id_gigantes = cursor.fetchone()[0]
                print("Módulo 'Os Gigantes Gasosos e Além' já existe.")

            if modulo_id_gigantes:
                # Conteúdo 2.1: Artigo "Júpiter e Saturno: Os Gigantes do Gás"
                conteudo_id_jupiter_saturno = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Júpiter e Saturno: Os Gigantes do Gás",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Júpiter e Saturno: Os Gigantes do Gás', 'Conheça os maiores planetas do Sistema Solar, suas luas e anéis espetaculares.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Planetas', 'https://placehold.co/400x250/FF4500/FFFFFF?text=Jupiter+Saturno', 'Artigo'))
                    conn.commit()
                    conteudo_id_jupiter_saturno = cursor.lastrowid
                    cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (conteudo_id_jupiter_saturno, '<p>Júpiter é o maior planeta do nosso Sistema Solar, com uma massa duas vezes e meia maior que a de todos os outros planetas combinados. É conhecido por sua Grande Mancha Vermelha, uma tempestade gigante que dura séculos.</p><p>Saturno é o segundo maior planeta e é famoso por seus impressionantes anéis, que são compostos por bilhões de pedaços de gelo e rocha. Ambos os planetas são gigantes gasosos, sem uma superfície sólida definida.</p>'))
                    conn.commit()
                    print("Conteúdo 'Júpiter e Saturno: Os Gigantes do Gás' criado.")
                else:
                    conteudo_id_jupiter_saturno = cursor.fetchone()[0]
                    print("Conteúdo 'Júpiter e Saturno: Os Gigantes do Gás' já existe.")
                
                if conteudo_id_jupiter_saturno:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_gigantes, conteudo_id_jupiter_saturno))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_gigantes, conteudo_id_jupiter_saturno, 1, 'Artigo'))
                        conn.commit()
                        print("Conteúdo 'Júpiter e Saturno: Os Gigantes do Gás' adicionado ao módulo.")

                # Conteúdo 2.2: Jogo "Missão a Marte: Desafio de Conhecimento"
                conteudo_id_jogo_marte = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Missão a Marte: Desafio de Conhecimento",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Missão a Marte: Desafio de Conhecimento', 'Um jogo interativo onde você gerencia uma missão a Marte, tomando decisões baseadas em seu conhecimento.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Missões Espaciais', 'https://placehold.co/400x250/A52A2A/FFFFFF?text=Jogo+Marte', 'Jogo'))
                    conn.commit()
                    conteudo_id_jogo_marte = cursor.lastrowid
                    cursor.execute('INSERT INTO jogos (conteudo_id, tipo_jogo, nivel_dificuldade, url_jogo) VALUES (?, ?, ?, ?)', (conteudo_id_jogo_marte, 'Simulação', 2, 'https://www.nasa.gov/interactive-mars-game-placeholder')) # Placeholder URL
                    conn.commit()
                    print("Conteúdo 'Missão a Marte: Desafio de Conhecimento' criado.")
                else:
                    conteudo_id_jogo_marte = cursor.fetchone()[0]
                    print("Conteúdo 'Missão a Marte: Desafio de Conhecimento' já existe.")

                if conteudo_id_jogo_marte:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_gigantes, conteudo_id_jogo_marte))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_gigantes, conteudo_id_jogo_marte, 2, 'Jogo'))
                        conn.commit()
                        print("Conteúdo 'Missão a Marte: Desafio de Conhecimento' adicionado ao módulo.")

                # Conteúdo 2.3: Vídeo "Urano e Netuno: Os Gigantes de Gelo"
                conteudo_id_urano_netuno = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Urano e Netuno: Os Gigantes de Gelo",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Urano e Netuno: Os Gigantes de Gelo', 'Descubra os planetas mais distantes e gelados do nosso sistema solar.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Planetas', 'https://placehold.co/400x250/ADD8E6/000000?text=Urano+Netuno', 'Video'))
                    conn.commit()
                    conteudo_id_urano_netuno = cursor.lastrowid
                    cursor.execute('INSERT INTO videos (conteudo_id, url_video, duracao_segundos, transcricao) VALUES (?, ?, ?, ?)', (conteudo_id_urano_netuno, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 240, 'Um tour pelos planetas Urano e Netuno, suas atmosferas e luas geladas.'))
                    conn.commit()
                    print("Conteúdo 'Urano e Netuno: Os Gigantes de Gelo' criado.")
                else:
                    conteudo_id_urano_netuno = cursor.fetchone()[0]
                    print("Conteúdo 'Urano e Netuno: Os Gigantes de Gelo' já existe.")

                if conteudo_id_urano_netuno:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_gigantes, conteudo_id_urano_netuno))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_gigantes, conteudo_id_urano_netuno, 3, 'Video'))
                        conn.commit()
                        print("Conteúdo 'Urano e Netuno: Os Gigantes de Gelo' adicionado ao módulo.")


        # Trilha 2: Introdução à Astrofísica
        trilha_id_astrofisica = None
        cursor.execute("SELECT id FROM trilhas_educacionais WHERE titulo = ?", ("Introdução à Astrofísica",))
        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO trilhas_educacionais (titulo, descricao, nivel, categoria, publicada, imagem_url, autor_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ('Introdução à Astrofísica', 'Desvende os princípios fundamentais da física por trás dos fenômenos cósmicos e da estrutura do universo.', 'Intermediário', 'Astrofísica', 1, 'https://placehold.co/600x400/8A2BE2/FFFFFF?text=Astrofisica', autor_id_snape))
            conn.commit()
            trilha_id_astrofisica = cursor.lastrowid
            print("Trilha 'Introdução à Astrofísica' criada.")
        else:
            trilha_id_astrofisica = cursor.fetchone()[0]
            print("Trilha 'Introdução à Astrofísica' já existe.")

        if trilha_id_astrofisica:
            # Módulo 1: Estrelas: Nascimento, Vida e Morte
            modulo_id_estrelas = None
            cursor.execute("SELECT id FROM modulos WHERE trilha_id = ? AND titulo = ?", (trilha_id_astrofisica, "Estrelas: Nascimento, Vida e Morte"))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO modulos (trilha_id, titulo, ordem, descricao_breve)
                    VALUES (?, ?, ?, ?)
                ''', (trilha_id_astrofisica, 'Estrelas: Nascimento, Vida e Morte', 1, 'Entenda o ciclo de vida das estrelas, desde sua formação até seus destinos finais.'))
                conn.commit()
                modulo_id_estrelas = cursor.lastrowid
                print("Módulo 'Estrelas: Nascimento, Vida e Morte' criado.")
            else:
                modulo_id_estrelas = cursor.fetchone()[0]
                print("Módulo 'Estrelas: Nascimento, Vida e Morte' já existe.")

            if modulo_id_estrelas:
                # Conteúdo 1.1: Artigo "Ciclo de Vida Estelar"
                conteudo_id_ciclo_estelar = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Ciclo de Vida Estelar",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Ciclo de Vida Estelar', 'Aprenda sobre as diferentes fases da vida de uma estrela, do nascimento à morte.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Estrelas', 'https://placehold.co/400x250/FF6347/FFFFFF?text=Ciclo+Estelar', 'Artigo'))
                    conn.commit()
                    conteudo_id_ciclo_estelar = cursor.lastrowid
                    cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (conteudo_id_ciclo_estelar, '<p>As estrelas nascem de nuvens de gás e poeira que colapsam sob a própria gravidade. Em seu núcleo, a fusão nuclear de hidrogênio em hélio gera a energia que as faz brilhar.</p><p>A vida de uma estrela depende de sua massa. Estrelas pequenas vivem por bilhões de anos, enquanto estrelas massivas têm vidas curtas e espetaculares, terminando em supernovas ou buracos negros.</p>'))
                    conn.commit()
                    print("Conteúdo 'Ciclo de Vida Estelar' criado.")
                else:
                    conteudo_id_ciclo_estelar = cursor.fetchone()[0]
                    print("Conteúdo 'Ciclo de Vida Estelar' já existe.")

                if conteudo_id_ciclo_estelar:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_estrelas, conteudo_id_ciclo_estelar))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_estrelas, conteudo_id_ciclo_estelar, 1, 'Artigo'))
                        conn.commit()
                        print("Conteúdo 'Ciclo de Vida Estelar' adicionado ao módulo.")

                # Conteúdo 1.2: Vídeo "Supernovas: O Fim Espetacular de uma Estrela"
                conteudo_id_supernovas = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Supernovas: O Fim Espetacular de uma Estrela",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Supernovas: O Fim Espetacular de uma Estrela', 'Entenda o que acontece quando uma estrela massiva chega ao fim de sua vida em uma explosão colossal.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Estrelas', 'https://placehold.co/400x250/FF00FF/FFFFFF?text=Supernova', 'Video'))
                    conn.commit()
                    conteudo_id_supernovas = cursor.lastrowid
                    cursor.execute('INSERT INTO videos (conteudo_id, url_video, duracao_segundos, transcricao) VALUES (?, ?, ?, ?)', (conteudo_id_supernovas, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 300, 'Explicação detalhada sobre supernovas e seu papel na formação de elementos pesados.'))
                    conn.commit()
                    print("Conteúdo 'Supernovas: O Fim Espetacular de uma Estrela' criado.")
                else:
                    conteudo_id_supernovas = cursor.fetchone()[0]
                    print("Conteúdo 'Supernovas: O Fim Espetacular de uma Estrela' já existe.")

                if conteudo_id_supernovas:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_estrelas, conteudo_id_supernovas))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_estrelas, conteudo_id_supernovas, 2, 'Video'))
                        conn.commit()
                        print("Conteúdo 'Supernovas: O Fim Espetacular de uma Estrela' adicionado ao módulo.")

            # Módulo 2: Buracos Negros e o Espaço-Tempo
            modulo_id_buracos_negros = None
            cursor.execute("SELECT id FROM modulos WHERE trilha_id = ? AND titulo = ?", (trilha_id_astrofisica, "Buracos Negros e o Espaço-Tempo"))
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO modulos (trilha_id, titulo, ordem, descricao_breve)
                    VALUES (?, ?, ?, ?)
                ''', (trilha_id_astrofisica, 'Buracos Negros e o Espaço-Tempo', 2, 'Aprenda sobre os objetos mais misteriosos do universo e como eles distorcem o tecido do espaço-tempo.'))
                conn.commit()
                modulo_id_buracos_negros = cursor.lastrowid
                print("Módulo 'Buracos Negros e o Espaço-Tempo' criado.")
            else:
                modulo_id_buracos_negros = cursor.fetchone()[0]
                print("Módulo 'Buracos Negros e o Espaço-Tempo' já existe.")

            if modulo_id_buracos_negros:
                # Conteúdo 2.1: Artigo "O Que São Buracos Negros?"
                conteudo_id_buracos_negros_artigo = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("O Que São Buracos Negros?",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('O Que São Buracos Negros?', 'Descubra a ciência por trás dos buracos negros, sua formação e seus diferentes tipos.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Buracos Negros', 'https://placehold.co/400x250/000000/FFFFFF?text=Buraco+Negro', 'Artigo'))
                    conn.commit()
                    conteudo_id_buracos_negros_artigo = cursor.lastrowid
                    cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (conteudo_id_buracos_negros_artigo, '<p>Buracos negros são regiões do espaço-tempo onde a gravidade é tão forte que nada, nem mesmo a luz, pode escapar. Eles se formam a partir do colapso de estrelas muito massivas.</p><p>Existem diferentes tipos de buracos negros, incluindo buracos negros estelares (formados por estrelas) e buracos negros supermassivos (encontrados no centro da maioria das galáxias).</p>'))
                    conn.commit()
                    print("Conteúdo 'O Que São Buracos Negros?' criado.")
                else:
                    conteudo_id_buracos_negros_artigo = cursor.fetchone()[0]
                    print("Conteúdo 'O Que São Buracos Negros?' já existe.")

                if conteudo_id_buracos_negros_artigo:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_buracos_negros, conteudo_id_buracos_negros_artigo))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_buracos_negros, conteudo_id_buracos_negros_artigo, 1, 'Artigo'))
                        conn.commit()
                        print("Conteúdo 'O Que São Buracos Negros?' adicionado ao módulo.")

                # Conteúdo 2.2: Quiz "Buracos Negros: Mitos e Verdades"
                conteudo_id_quiz_buracos_negros = None
                cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", ("Buracos Negros: Mitos e Verdades",))
                if not cursor.fetchone():
                    cursor.execute('''
                        INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, tipo_conteudo)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', ('Buracos Negros: Mitos e Verdades', 'Teste seu conhecimento sobre os buracos negros e desfaça alguns mitos populares.', datetime.now().isoformat(), 'publico', autor_id_snape, 'Buracos Negros', 'https://placehold.co/400x250/4B0082/FFFFFF?text=Quiz+BN', 'Quiz'))
                    conn.commit()
                    conteudo_id_quiz_buracos_negros = cursor.lastrowid
                    cursor.execute('INSERT INTO quizzes (conteudo_id, tempo_limite_min, tentativas_permitidas) VALUES (?, ?, ?)', (conteudo_id_quiz_buracos_negros, 7, 2))
                    conn.commit()
                    print("Conteúdo 'Buracos Negros: Mitos e Verdades' criado.")
                else:
                    conteudo_id_quiz_buracos_negros = cursor.fetchone()[0]
                    print("Conteúdo 'Buracos Negros: Mitos e Verdades' já existe.")
                
                if conteudo_id_quiz_buracos_negros:
                    cursor.execute("SELECT 1 FROM conteudo_modulo WHERE modulo_id = ? AND conteudo_id = ?", (modulo_id_buracos_negros, conteudo_id_quiz_buracos_negros))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO conteudo_modulo (modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk) VALUES (?, ?, ?, ?)', (modulo_id_buracos_negros, conteudo_id_quiz_buracos_negros, 2, 'Quiz'))
                        conn.commit()
                        print("Conteúdo 'Buracos Negros: Mitos e Verdades' adicionado ao módulo.")
                    
                    # Adicionar questões e alternativas para o quiz
                    cursor.execute("SELECT id FROM questoes_quiz WHERE quiz_id = ? AND texto_questao = ?", (conteudo_id_quiz_buracos_negros, "Um buraco negro é um buraco no espaço."))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO questoes_quiz (quiz_id, texto_questao, tipo_questao) VALUES (?, ?, ?)', (conteudo_id_quiz_buracos_negros, "Um buraco negro é um buraco no espaço.", "verdadeiro_falso"))
                        questao_id_3 = cursor.lastrowid
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_3, 'Verdadeiro', 0))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_3, 'Falso', 1))
                        conn.commit()
                        print("Questão 1 do quiz de buracos negros adicionada.")

                    cursor.execute("SELECT id FROM questoes_quiz WHERE quiz_id = ? AND texto_questao = ?", (conteudo_id_quiz_buracos_negros, "Qual o nome da fronteira de um buraco negro onde a fuga é impossível?"))
                    if not cursor.fetchone():
                        cursor.execute('INSERT INTO questoes_quiz (quiz_id, texto_questao, tipo_questao) VALUES (?, ?, ?)', (conteudo_id_quiz_buracos_negros, "Qual o nome da fronteira de um buraco negro onde a fuga é impossível?", "multipla_escolha"))
                        questao_id_4 = cursor.lastrowid
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_4, 'Singularidade', 0))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_4, 'Horizonte de Eventos', 1))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_4, 'Ergosfera', 0))
                        cursor.execute('INSERT INTO alternativas_quiz (questao_id, texto_alternativa, correta) VALUES (?, ?, ?)', (questao_id_4, 'Ponto de Lagrange', 0))
                        conn.commit()
                        print("Questão 2 do quiz de buracos negros adicionada.")

    else:
        print("Professor Snape não encontrado para criar as trilhas.")

    # --- Inserir Notícias da NASA ---
    autor_id_bruce = user_ids.get('BruceMorceguinho') # Usar o ID do administrador para as notícias
    if not autor_id_bruce:
        # Se BruceMorceguinho não foi encontrado, tenta buscar pelo email (caso o nome de usuário tenha mudado)
        cursor.execute("SELECT id FROM usuarios WHERE email = ?", ('BruceWayne@gmail.com',))
        bruce_data = cursor.fetchone()
        if bruce_data:
            autor_id_bruce = bruce_data[0]
        else:
            print("Administrador (Bruce Wayne) não encontrado para inserir notícias.")
            autor_id_bruce = 1 # Fallback para ID 1 se não encontrar

    if autor_id_bruce:
        news_articles = [
            {
                'titulo': 'NASA descobre cometa interestelar se movendo pelo sistema solar',
                'descricao': 'A sonda mais distante da Terra continua a surpreender cientistas com leituras anômalas.',
                'texto_html': '<p>Em 1º de julho, o telescópio de pesquisa ATLAS (Asteroid Terrestrial-impact Last Alert System), financiado pela NASA, em Rio Hurtado, Chile, relatou pela primeira vez observações de um cometa originário do espaço interestelar. Vindo da direção da constelação de Sagitário, o cometa interestelar foi oficialmente denominado 3I/ATLAS. Atualmente, ele está localizado a cerca de 670 milhões de quilômetros de distância.</p><p>Desde esse primeiro relato, observações anteriores à descoberta foram coletadas dos arquivos de três telescópios ATLAS diferentes ao redor do mundo e do Zwicky Transient Facility, no Observatório Palomar, no Condado de San Diego, Califórnia. Essas observações "pré-descoberta" remontam a 14 de junho. Inúmeros telescópios relataram observações adicionais desde que o objeto foi relatado pela primeira vez.</p><p>O cometa não representa nenhuma ameaça à Terra e permanecerá a uma distância de pelo menos 1,6 unidades astronômicas (cerca de 240 milhões de quilômetros). Atualmente, está a cerca de 4,5 UA (cerca de 670 milhões de km) do Sol. O 3I/ATLAS atingirá sua maior aproximação do Sol por volta de 30 de outubro, a uma distância de 1,4 UA (cerca de 210 milhões de km) — logo dentro da órbita de Marte.</p><p>O tamanho e as propriedades físicas do cometa interestelar estão sendo investigados por astrônomos em todo o mundo. O 3I/ATLAS deve permanecer visível a telescópios terrestres até setembro, após o qual passará muito perto do Sol para ser observado. Espera-se que reapareça do outro lado do Sol no início de dezembro, permitindo novas observações.</p>',
                'categoria': 'Atronomia',
                'imagem_url': 'https://assets.science.nasa.gov/dynamicimage/assets/science/psd/planetary-defense/3I_interstellar%20comet%20orbit.jpg?w=1840&h=1200&fit=clip&crop=faces%2Cfocalpoint',
                'fonte_url': 'https://science.nasa.gov/blogs/planetary-defense/2025/07/02/nasa-discovers-interstellar-comet-moving-through-solar-system/'
            },
            {
                'titulo': 'Descoberta de Nova Supernova Próxima Promete Revelações Cósmicas',
                'descricao': 'Astrônomos observam a explosão de uma estrela em uma galáxia vizinha, fornecendo dados valiosos.',
                'texto_html': '<p>Uma supernova recentemente detectada na galáxia M82, apelidada de "Galáxia do Charuto", está gerando grande entusiasmo na comunidade astronômica. A proximidade relativa do evento permite observações detalhadas, que podem aprimorar nossa compreensão sobre a morte de estrelas massivas e a formação de elementos pesados no universo.</p><p>A explosão estelar, visível até mesmo com telescópios amadores mais potentes, está sendo monitorada por observatórios em todo o mundo. Os dados coletados ajudarão a refinar modelos de evolução estelar e a entender melhor os processos que enriquecem o cosmos com os elementos necessários para a vida.</p>',
                'categoria': 'Estrelas',
                'imagem_url': 'https://assets.science.nasa.gov/dynamicimage/assets/science/cds/open-science/article-media/RCW36.jpg?w=3406&h=1684&fit=clip&crop=faces%2Cfocalpoint',
                'fonte_url': 'https://science.nasa.gov/open-science/spherex-universe-map/'
            },
            
        ]

        for article_data in news_articles:
            cursor.execute("SELECT id FROM conteudos WHERE titulo = ?", (article_data['titulo'],))
            content_exists = cursor.fetchone()
            if not content_exists:
                cursor.execute('''
                    INSERT INTO conteudos (titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url, fonte_url, tipo_conteudo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (article_data['titulo'], article_data['descricao'], datetime.now().isoformat(), 'publico', autor_id_bruce, article_data['categoria'], article_data['imagem_url'], article_data['fonte_url'], 'Artigo'))
                
                new_content_id = cursor.lastrowid
                cursor.execute('INSERT INTO artigos (conteudo_id, texto_html) VALUES (?, ?)', (new_content_id, article_data['texto_html']))
                conn.commit()
                print(f"Notícia '{article_data['titulo']}' inserida.")
            else:
                print(f"Notícia '{article_data['titulo']}' já existe. Ignorando inserção.")
    else:
        print("Administrador (Bruce Wayne) não encontrado para inserir notícias.")

    conn.close() # Fechar a conexão no final de tudo
    print("Inicialização do banco de dados concluída.")

if __name__ == '__main__':
    init_db()
