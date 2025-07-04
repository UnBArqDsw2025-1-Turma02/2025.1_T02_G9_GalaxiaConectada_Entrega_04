import json
from datetime import datetime

class Usuario:
    def __init__(self, id, nome_completo, email, nome_usuario, senha_hash, data_cadastro, tipo_usuario='Visitante', permissoes='[]', nivel_acesso=1):
        self.id = id
        self.nome_completo = nome_completo
        self.email = email
        self.nome_usuario = nome_usuario
        self.senha_hash = senha_hash
        self.data_cadastro = data_cadastro # String ISO format
        self.tipo_usuario = tipo_usuario
        self.permissoes = json.loads(permissoes) if isinstance(permissoes, str) else permissoes
        self.nivel_acesso = nivel_acesso

    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'email': self.email,
            'nome_usuario': self.nome_usuario,
            'data_cadastro': self.data_cadastro,
            'tipo_usuario': self.tipo_usuario,
            'permissoes': self.permissoes,
            'nivel_acesso': self.nivel_acesso
        }

class Perfil:
    def __init__(self, usuario_id, nivel=1, xp=0, linguagem_pref='pt-BR', avatar_url='default_avatar.png', bio='',
                 progresso_geral=0.0, ultimo_acesso_trilha=None,
                 biografia_curta=None, avaliacao_media=0.0, especialidades='[]',
                 area_especialidade=None, artigos_revisados=0,
                 nivel_moderacao=None, data_inicio_moderacao=None):
        
        self.usuario_id = usuario_id
        self.nivel = nivel
        self.xp = xp
        self.linguagem_pref = linguagem_pref
        self.avatar_url = avatar_url
        self.bio = bio
        
        # Campos específicos para Aluno
        self.progresso_geral = progresso_geral
        self.ultimo_acesso_trilha = ultimo_acesso_trilha
        
        # Campos específicos para Instrutor
        self.biografia_curta = biografia_curta
        self.avaliacao_media = avaliacao_media
        self.especialidades = json.loads(especialidades) if isinstance(especialidades, str) else especialidades
        
        # Campos específicos para Professor Voluntário
        self.area_especialidade = area_especialidade
        self.artigos_revisados = artigos_revisados
        
        # Campos específicos para Moderador
        self.nivel_moderacao = nivel_moderacao
        self.data_inicio_moderacao = data_inicio_moderacao
    
    def to_dict(self):
        data = {
            'usuario_id': self.usuario_id,
            'nivel': self.nivel,
            'xp': self.xp,
            'linguagem_pref': self.linguagem_pref,
            'avatar_url': self.avatar_url,
            'bio': self.bio
        }
        if self.progresso_geral is not None: data['progresso_geral'] = self.progresso_geral
        if self.ultimo_acesso_trilha: data['ultimo_acesso_trilha'] = self.ultimo_acesso_trilha
        if self.biografia_curta: data['biografia_curta'] = self.biografia_curta
        if self.avaliacao_media is not None: data['avaliacao_media'] = self.avaliacao_media
        if self.especialidades: data['especialidades'] = self.especialidades
        if self.area_especialidade: data['area_especialidade'] = self.area_especialidade
        if self.artigos_revisados is not None: data['artigos_revisados'] = self.artigos_revisados
        if self.nivel_moderacao: data['nivel_moderacao'] = self.nivel_moderacao
        if self.data_inicio_moderacao: data['data_inicio_moderacao'] = self.data_inicio_moderacao
        
        return data

class PetBase:
    def __init__(self, id, nome, tipo, aparencia_url_fase1, aparencia_url_fase2, aparencia_url_fase3, descricao):
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.aparencia_url_fase1 = aparencia_url_fase1
        self.aparencia_url_fase2 = aparencia_url_fase2
        self.aparencia_url_fase3 = aparencia_url_fase3
        self.descricao = descricao

    def get_aparencia_url(self, fase):
        if fase == 1:
            return self.aparencia_url_fase1
        elif fase == 2:
            return self.aparencia_url_fase2
        elif fase == 3:
            return self.aparencia_url_fase3
        return self.aparencia_url_fase1 # Fallback

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tipo': self.tipo,
            'aparencia_url_fase1': self.aparencia_url_fase1,
            'aparencia_url_fase2': self.aparencia_url_fase2,
            'aparencia_url_fase3': self.aparencia_url_fase3,
            'descricao': self.descricao
        }

class UserPet:
    def __init__(self, id, usuario_id, pet_base_id, nome_personalizado, fase_atual=1, xp_acumulado=0, itens_equipados='[]', ultima_atualizacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.pet_base_id = pet_base_id
        self.nome_personalizado = nome_personalizado
        self.fase_atual = fase_atual
        self.xp_acumulado = xp_acumulado
        self.itens_equipados = json.loads(itens_equipados) if isinstance(itens_equipados, str) else itens_equipados
        self.ultima_atualizacao = ultima_atualizacao if ultima_atualizacao else datetime.now().isoformat()

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'pet_base_id': self.pet_base_id,
            'nome_personalizado': self.nome_personalizado,
            'fase_atual': self.fase_atual,
            'xp_acumulado': self.xp_acumulado,
            'itens_equipados': self.itens_equipados,
            'ultima_atualizacao': self.ultima_atualizacao
        }

class PetItem:
    def __init__(self, id, nome, descricao, tipo_pet_compativel, aparencia_url, preco_xp):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.tipo_pet_compativel = tipo_pet_compativel
        self.aparencia_url = aparencia_url
        self.preco_xp = preco_xp

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'tipo_pet_compativel': self.tipo_pet_compativel,
            'aparencia_url': self.aparencia_url,
            'preco_xp': self.preco_xp
        }

class Conteudo: # Classe base para Artigo, Video, Quiz, Jogo
    def __init__(self, id, titulo, descricao, data_publicacao, visibilidade, autor_id, categoria, imagem_url=None, fonte_url=None, tipo_conteudo='Artigo', **kwargs):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.data_publicacao = data_publicacao
        self.visibilidade = visibilidade
        self.autor_id = autor_id
        self.categoria = categoria
        self.imagem_url = imagem_url
        self.fonte_url = fonte_url
        self.tipo_conteudo = tipo_conteudo
        # Adicionar autor_nome para facilitar a exibição
        self.autor_nome = kwargs.get('autor_nome') # Vem do JOIN no app.py

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data_publicacao': self.data_publicacao,
            'visibilidade': self.visibilidade,
            'autor_id': self.autor_id,
            'categoria': self.categoria,
            'imagem_url': self.imagem_url,
            'fonte_url': self.fonte_url,
            'tipo_conteudo': self.tipo_conteudo,
            'autor_nome': self.autor_nome
        }

class Artigo: # Subclasse de Conteudo
    def __init__(self, conteudo_id, texto_html, **kwargs):
        self.conteudo_id = conteudo_id
        self.texto_html = texto_html
        # Permite que Artigo seja inicializado com dados do Conteudo base
        self.__dict__.update(kwargs)

    def to_dict(self):
        data = {'conteudo_id': self.conteudo_id, 'texto_html': self.texto_html}
        data.update({k: v for k, v in self.__dict__.items() if k not in ['conteudo_id', 'texto_html']})
        return data

class Video: # Subclasse de Conteudo
    def __init__(self, conteudo_id, url_video, duracao_segundos=None, transcricao=None, **kwargs):
        self.conteudo_id = conteudo_id
        self.url_video = url_video
        self.duracao_segundos = duracao_segundos
        self.transcricao = transcricao
        self.__dict__.update(kwargs)

    def to_dict(self):
        data = {'conteudo_id': self.conteudo_id, 'url_video': self.url_video, 'duracao_segundos': self.duracao_segundos, 'transcricao': self.transcricao}
        data.update({k: v for k, v in self.__dict__.items() if k not in ['conteudo_id', 'url_video', 'duracao_segundos', 'transcricao']})
        return data

class Quiz: # Subclasse de Conteudo
    def __init__(self, conteudo_id, tempo_limite_min=None, tentativas_permitidas=None, **kwargs):
        self.conteudo_id = conteudo_id
        self.tempo_limite_min = tempo_limite_min
        self.tentativas_permitidas = tentativas_permitidas
        self.__dict__.update(kwargs)

    def to_dict(self):
        data = {'conteudo_id': self.conteudo_id, 'tempo_limite_min': self.tempo_limite_min, 'tentativas_permitidas': self.tentativas_permitidas}
        data.update({k: v for k, v in self.__dict__.items() if k not in ['conteudo_id', 'tempo_limite_min', 'tentativas_permitidas']})
        return data

class QuestaoQuiz:
    def __init__(self, id, quiz_id, texto_questao, tipo_questao):
        self.id = id
        self.quiz_id = quiz_id
        self.texto_questao = texto_questao
        self.tipo_questao = tipo_questao

    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'texto_questao': self.texto_questao,
            'tipo_questao': self.tipo_questao
        }

class AlternativaQuiz:
    def __init__(self, id, questao_id, texto_alternativa, correta):
        self.id = id
        self.questao_id = questao_id
        self.texto_alternativa = texto_alternativa
        self.correta = correta # 0 ou 1

    def to_dict(self):
        return {
            'id': self.id,
            'questao_id': self.questao_id,
            'texto_alternativa': self.texto_alternativa,
            'correta': self.correta
        }

class TentativaQuiz:
    def __init__(self, id, usuario_id, quiz_id, data_tentativa, pontuacao, concluida):
        self.id = id
        self.usuario_id = usuario_id
        self.quiz_id = quiz_id
        self.data_tentativa = data_tentativa
        self.pontuacao = pontuacao
        self.concluida = concluida # 0 ou 1

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'quiz_id': self.quiz_id,
            'data_tentativa': self.data_tentativa,
            'pontuacao': self.pontuacao,
            'concluida': self.concluida
        }

class RespostaQuiz:
    def __init__(self, id, tentativa_id, questao_id, alternativa_selecionada_id=None, resposta_texto=None):
        self.id = id
        self.tentativa_id = tentativa_id
        self.questao_id = questao_id
        self.alternativa_selecionada_id = alternativa_selecionada_id
        self.resposta_texto = resposta_texto

    def to_dict(self):
        return {
            'id': self.id,
            'tentativa_id': self.tentativa_id,
            'questao_id': self.questao_id,
            'alternativa_selecionada_id': self.alternativa_selecionada_id,
            'resposta_texto': self.resposta_texto
        }

class Jogo: # Subclasse de Conteudo
    def __init__(self, conteudo_id, tipo_jogo=None, nivel_dificuldade=None, url_jogo=None, **kwargs):
        self.conteudo_id = conteudo_id
        self.tipo_jogo = tipo_jogo
        self.nivel_dificuldade = nivel_dificuldade
        self.url_jogo = url_jogo
        self.__dict__.update(kwargs)

    def to_dict(self):
        data = {'conteudo_id': self.conteudo_id, 'tipo_jogo': self.tipo_jogo, 'nivel_dificuldade': self.nivel_dificuldade, 'url_jogo': self.url_jogo}
        data.update({k: v for k, v in self.__dict__.items() if k not in ['conteudo_id', 'tipo_jogo', 'nivel_dificuldade', 'url_jogo']})
        return data

class SessaoJogo:
    def __init__(self, id, usuario_id, jogo_id, data_inicio, data_fim=None, pontuacao=None):
        self.id = id
        self.usuario_id = usuario_id
        self.jogo_id = jogo_id
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.pontuacao = pontuacao

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'jogo_id': self.jogo_id,
            'data_inicio': self.data_inicio,
            'data_fim': self.data_fim,
            'pontuacao': self.pontuacao
        }

class PontuacaoJogo:
    def __init__(self, id, usuario_id, jogo_id, melhor_pontuacao, data_recorde):
        self.id = id
        self.usuario_id = usuario_id
        self.jogo_id = jogo_id
        self.melhor_pontuacao = melhor_pontuacao
        self.data_recorde = data_recorde

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'jogo_id': self.jogo_id,
            'melhor_pontuacao': self.melhor_pontuacao,
            'data_recorde': self.data_recorde
        }

class Curtida:
    def __init__(self, usuario_id, conteudo_id, data_curtida):
        self.usuario_id = usuario_id
        self.conteudo_id = conteudo_id
        self.data_curtida = data_curtida

    def to_dict(self):
        return {
            'usuario_id': self.usuario_id,
            'conteudo_id': self.conteudo_id,
            'data_curtida': self.data_curtida
        }

class Comentario:
    def __init__(self, id, usuario_id, texto, data_comentario, conteudo_id=None, postagem_id=None, editado=0, data_edicao=None, upvotes=0, **kwargs):
        self.id = id
        self.conteudo_id = conteudo_id
        self.postagem_id = postagem_id
        self.usuario_id = usuario_id
        self.texto = texto
        self.data_comentario = data_comentario
        self.editado = editado
        self.data_edicao = data_edicao
        self.upvotes = upvotes
        self.nome_usuario = kwargs.get('nome_usuario') # Para exibir o nome do autor do comentário

    def to_dict(self):
        return {
            'id': self.id,
            'conteudo_id': self.conteudo_id,
            'postagem_id': self.postagem_id,
            'usuario_id': self.usuario_id,
            'texto': self.texto,
            'data_comentario': self.data_comentario,
            'editado': self.editado,
            'data_edicao': self.data_edicao,
            'upvotes': self.upvotes,
            'nome_usuario': self.nome_usuario
        }

class Notificacao:
    def __init__(self, id, usuario_id, mensagem, link, data_envio, lida=0):
        self.id = id
        self.usuario_id = usuario_id
        self.mensagem = mensagem
        self.link = link
        self.data_envio = data_envio
        self.lida = lida # 0 para não lida, 1 para lida

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'mensagem': self.mensagem,
            'link': self.link,
            'data_envio': self.data_envio,
            'lida': self.lida
        }

class InscricaoCategoria:
    def __init__(self, usuario_id, categoria):
        self.usuario_id = usuario_id
        self.categoria = categoria

    def to_dict(self):
        return {
            'usuario_id': self.usuario_id,
            'categoria': self.categoria
        }

class TrilhaEducacional:
    def __init__(self, id, titulo, descricao, nivel, categoria, publicada=0, imagem_url=None, autor_id=None, **kwargs):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.nivel = nivel
        self.categoria = categoria
        self.publicada = publicada
        self.imagem_url = imagem_url
        self.autor_id = autor_id
        self.autor_nome = kwargs.get('autor_nome') # Vem do JOIN no app.py

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'nivel': self.nivel,
            'categoria': self.categoria,
            'publicada': self.publicada,
            'imagem_url': self.imagem_url,
            'autor_id': self.autor_id,
            'autor_nome': self.autor_nome
        }

class Modulo:
    def __init__(self, id, trilha_id, titulo, ordem, descricao_breve):
        self.id = id
        self.trilha_id = trilha_id
        self.titulo = titulo
        self.ordem = ordem
        self.descricao_breve = descricao_breve

    def to_dict(self):
        return {
            'id': self.id,
            'trilha_id': self.trilha_id,
            'titulo': self.titulo,
            'ordem': self.ordem,
            'descricao_breve': self.descricao_breve
        }

class ConteudoModulo: # Classe de associação para Conteúdo dentro de Módulos
    def __init__(self, modulo_id, conteudo_id, ordem_no_modulo, tipo_conteudo_fk):
        self.modulo_id = modulo_id
        self.conteudo_id = conteudo_id
        self.ordem_no_modulo = ordem_no_modulo
        self.tipo_conteudo_fk = tipo_conteudo_fk

    def to_dict(self):
        return {
            'modulo_id': self.modulo_id,
            'conteudo_id': self.conteudo_id,
            'ordem_no_modulo': self.ordem_no_modulo,
            'tipo_conteudo_fk': self.tipo_conteudo_fk
        }

class ProgressoUsuarioTrilha:
    def __init__(self, id, usuario_id, trilha_id, progresso_percentual=0.0, ultimo_acesso_data=None, concluida=0):
        self.id = id
        self.usuario_id = usuario_id
        self.trilha_id = trilha_id
        self.progresso_percentual = progresso_percentual
        self.ultimo_acesso_data = ultimo_acesso_data if ultimo_acesso_data else datetime.now().isoformat()
        self.concluida = concluida # 0 ou 1

    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'trilha_id': self.trilha_id,
            'progresso_percentual': self.progresso_percentual,
            'ultimo_acesso_data': self.ultimo_acesso_data,
            'concluida': self.concluida
        }

class ProgressoModulo:
    def __init__(self, id, progresso_trilha_id, modulo_id, concluido=0, data_conclusao=None):
        self.id = id
        self.progresso_trilha_id = progresso_trilha_id
        self.modulo_id = modulo_id
        self.concluido = concluido # 0 ou 1
        self.data_conclusao = data_conclusao

    def to_dict(self):
        return {
            'id': self.id,
            'progresso_trilha_id': self.progresso_trilha_id,
            'modulo_id': self.modulo_id,
            'concluido': self.concluido,
            'data_conclusao': self.data_conclusao
        }

class ProgressoConteudo:
    def __init__(self, id, progresso_modulo_id, conteudo_id, concluido=0, data_conclusao=None, xp_ganho=0, moedas_ganhas=0):
        self.id = id
        self.progresso_modulo_id = progresso_modulo_id
        self.conteudo_id = conteudo_id
        self.concluido = concluido # 0 ou 1
        self.data_conclusao = data_conclusao
        self.xp_ganho = xp_ganho
        self.moedas_ganhas = moedas_ganhas

    def to_dict(self):
        return {
            'id': self.id,
            'progresso_modulo_id': self.progresso_modulo_id,
            'conteudo_id': self.conteudo_id,
            'concluido': self.concluido,
            'data_conclusao': self.data_conclusao,
            'xp_ganho': self.xp_ganho,
            'moedas_ganhas': self.moedas_ganhas
        }

class Conquista:
    def __init__(self, id, titulo, descricao, icone_url, pontos_xp_concedidos):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.icone_url = icone_url
        self.pontos_xp_concedidos = pontos_xp_concedidos

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'icone_url': self.icone_url,
            'pontos_xp_concedidos': self.pontos_xp_concedidos
        }

class UsuarioConquista:
    def __init__(self, usuario_id, conquista_id, data_conquista, progresso_origem_id=None):
        self.usuario_id = usuario_id
        self.conquista_id = conquista_id
        self.data_conquista = data_conquista
        self.progresso_origem_id = progresso_origem_id

    def to_dict(self):
        return {
            'usuario_id': self.usuario_id,
            'conquista_id': self.conquista_id,
            'data_conquista': self.data_conquista,
            'progresso_origem_id': self.progresso_origem_id
        }

# --- Classes para o Fórum (já existentes, reconfirmando) ---
class Subforum:
    def __init__(self, id, nome, descricao, ordem_exibicao=0):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.ordem_exibicao = ordem_exibicao

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'ordem_exibicao': self.ordem_exibicao
        }

class Topico:
    def __init__(self, id, subforum_id, autor_id, titulo, data_criacao, data_ult_post, fixado=0, fechado=0, upvotes=0, **kwargs):
        self.id = id
        self.subforum_id = subforum_id
        self.autor_id = autor_id
        self.titulo = titulo
        self.data_criacao = data_criacao
        self.data_ult_post = data_ult_post
        self.fixado = fixado
        self.fechado = fechado
        self.upvotes = upvotes
        self.autor_nome = kwargs.get('autor_nome') # Para exibir o nome do autor do tópico
        self.subforum_nome = kwargs.get('subforum_nome') # Para exibir o nome do subfórum

    def to_dict(self):
        return {
            'id': self.id,
            'subforum_id': self.subforum_id,
            'autor_id': self.autor_id,
            'titulo': self.titulo,
            'data_criacao': self.data_criacao,
            'data_ult_post': self.data_ult_post,
            'fixado': self.fixado,
            'fechado': self.fechado,
            'upvotes': self.upvotes,
            'autor_nome': self.autor_nome,
            'subforum_nome': self.subforum_nome
        }

class Postagem:
    def __init__(self, id, topico_id, autor_id, texto, data_postagem, editado=0, data_edicao=None, upvotes=0, **kwargs):
        self.id = id
        self.topico_id = topico_id
        self.autor_id = autor_id
        self.texto = texto
        self.data_postagem = data_postagem
        self.editado = editado
        self.data_edicao = data_edicao
        self.upvotes = upvotes
        self.autor_nome = kwargs.get('autor_nome') # Para exibir o nome do autor da postagem
        self.autor_nivel = kwargs.get('autor_nivel') # Nível do autor
        self.autor_xp = kwargs.get('autor_xp') # XP do autor
        self.user_voted_type = kwargs.get('user_voted_type') # Tipo de voto do usuário logado na postagem
        self.upvotes_count = kwargs.get('upvotes_count') # Contagem de upvotes
        self.downvotes_count = kwargs.get('downvotes_count') # Contagem de downvotes

    def to_dict(self):
        return {
            'id': self.id,
            'topico_id': self.topico_id,
            'autor_id': self.autor_id,
            'texto': self.texto,
            'data_postagem': self.data_postagem,
            'editado': self.editado,
            'data_edicao': self.data_edicao,
            'upvotes': self.upvotes,
            'autor_nome': self.autor_nome,
            'autor_nivel': self.autor_nivel,
            'autor_xp': self.autor_xp,
            'user_voted_type': self.user_voted_type,
            'upvotes_count': self.upvotes_count,
            'downvotes_count': self.downvotes_count
        }

class VotoPostagem:
    def __init__(self, usuario_id, postagem_id, tipo_voto, data_voto):
        self.usuario_id = usuario_id
        self.postagem_id = postagem_id
        self.tipo_voto = tipo_voto
        self.data_voto = data_voto

    def to_dict(self):
        return {
            'usuario_id': self.usuario_id,
            'postagem_id': self.postagem_id,
            'tipo_voto': self.tipo_voto,
            'data_voto': self.data_voto
        }
