# Apresentação da Plataforma: 

# 🌌 Galáxia Conectada  
*Conhecimento que brilha como as estrelas!*

## Sumário

- [Introdução](#Introdução)
- [Sobre o Projeto](#Sobre-o-Projeto)
- [Funcionalidades Desenvolvidas](#Funcionalidades-Desenvolvidas)
- [Estrutura do Projeto](#Estrutura-do-Projeto)
- [Backend (Servidor Flask e Banco de Dados)](#Backend-Servidor-Flask-e-Banco-de-Dados)
- [Frontend (Interface do Usuário)](#Frontend-Interface-do-Usuário)
- [Usuários Cadastrados para Teste](#Usuários-Cadastrados-para-Teste)
- [Como Rodar o Projeto Localmente](#Como-Rodar-o-Projeto-Localmente)
- [Apresentação da Plataforma](#Apresentação-da-Plataforma)
- [Próximos Passos](#Próximos-Passos)
- [Conclusão](#conclusão)
- [Histórico de Versão](#Histórico-de-Versão)

## Introdução

A Galáxia Conectada é uma plataforma educacional interativa focada na divulgação científica da astronomia, inspirada em grandes referências como o Khan Academy. O objetivo é proporcionar uma experiência imersiva e acessível para entusiastas e curiosos do universo, transformando o aprendizado em uma verdadeira jornada cósmica.

Este documento apresenta o progresso do desenvolvimento da plataforma até o momento, ao cobrir as principais funcionalidades implementadas no backend e frontend, além de fornecer credenciais de usuários para teste.

## Sobre o Projeto

O projeto "Galáxia Conectada" está sendo desenvolvido como parte da disciplina de Arquitetura e Desenho de Software. Assim, busca-se criar um ambiente onde o conhecimento astronômico seja acessível através de:

- Trilhas de Aprendizado: Conteúdo estruturado por temas e níveis.

- Jogos Educativos: Aprendizado lúdico e interativo.

- Fóruns de Discussão: Comunidade para perguntas, ideias e colaboração.

- Notícias e Artigos Científicos: Atualizações e aprofundamentos no mundo da astronomia.

- Sistema de Gamificação: XP, níveis, conquistas e mascotes evolutivos para motivar o usuário.


## Funcionalidades Desenvolvidas

O projeto segue uma arquitetura modular, separando as responsabilidades de backend e frontend para facilitar o desenvolvimento e a manutenção:

      galaxia_conectada/
      ├── backend/                  
      │   ├── app.py                
      │   ├── database.py           
      │   ├── models.py             
      │   ├── db_data/              
      │   └── __init__.py           
      ├── frontend/                 
      │   ├── index.html            
      │   ├── entrar.html           
      │   ├── cadastrar.html        
      │   ├── css/                  
      │   │   └── style.css
      │   ├── img/                  
      │   ├── js/                   
      │   │   └── script.js
      │   ├── admin_profile.html    
      │   ├── aluno_profile.html    
      │   ├── instrutor_profile.html 
      │   ├── professor_voluntario_profile.html 
      │   ├── moderador_profile.html 
      │   ├── visitante_profile.html
      │   ├── choose_pet.html       
      │   ├── pet_shop.html         
      │   ├── conhecimento_home.html 
      │   ├── content_detail.html   
      │   ├── publish_content.html  
      │   ├── user_favorites.html   
      │   ├── user_notifications.html 
      │   ├── forum_home.html      
      │   ├── create_subforum.html  
      │   ├── subforum_detail.html 
      │   ├── create_topic.html     
      │   ├── topic_detail.html     
      │   ├── trilhas_home.html     
      │   ├── trilha_detail.html   
      │   ├── modulo_detail.html   
      │   ├── content_view.html     
      │   ├── ranking.html          
      │   └── conquistas.html       
      └── .gitignore               


## Backend (Servidor Flask e Banco de Dados)

* **Autenticação e Autorização**: Sistema completo de login, cadastro e logout de usuários, com hashes de senha seguros (`werkzeug.security`). Implementação de sessões para manter o estado do usuário. Rotas protegidas por decoradores (`@login_required`, `@admin_required`, `@publisher_required`, `@moderator_required`).
* **Banco de Dados SQLite**: Configuração e inicialização de um banco de dados SQLite (`galaxia.db`).
    * **Tabelas de Usuários**: `usuarios` (dados básicos, tipo, permissões), `perfis` (nível, XP, bio, dados específicos por tipo de usuário).
    * **Sistema de Mascotes (Pets)**:
        * `pets_base`: Definições dos tipos de mascotes (Lumio, Selena, Nebby, Orbix) e URLs para suas aparências em diferentes fases de evolução.
        * `user_pets`: Rastreia o mascote adotado por cada usuário, seu nome personalizado, XP e fase atual.
        * `pet_items`: Itens de personalização para os mascotes (óculos, chapéus, etc.) com custo em XP.
        * Lógica para escolha do mascote, ganho de XP e evolução com base em XP acumulado.
    * **Sistema de Conteúdo (Conhecimento)**:
        * `conteudos`: Tabela base para todo conteúdo (Artigos, Vídeos, Quizzes, Jogos), com metadados (título, descrição, autor, categoria, etc.).
        * `artigos`, `videos`, `quizzes`, `jogos`: Tabelas de extensão que armazenam os dados específicos de cada tipo de conteúdo.
        * `curtidas`: Rastreia os "likes" dos usuários em conteúdos.
        * `comentarios`: Permite que usuários comentem em conteúdos e postagens de fórum.
        * **Notificações**:
            * `notificacoes`: Armazena mensagens do sistema para usuários (novo conteúdo na categoria, conquistas, etc.).
            * `inscricoes_categoria`: Permite que usuários se inscrevam para receber notificações de categorias específicas de conteúdo.
    * **Trilhas de Aprendizado**:
        * `trilhas_educacionais`: Define as trilhas (título, descrição, nível, categoria, imagem, autor).
        * `modulos`: Agrupa conteúdos dentro de uma trilha, com ordem e descrição.
        * `conteudo_modulo`: Tabela de associação que liga conteúdos a módulos, definindo a ordem dentro do módulo.
        * **Progresso do Usuário**:
            * `progresso_usuario_trilha`: Rastreia o progresso geral de um usuário em uma trilha.
            * `progresso_modulo`: Rastreia a conclusão de módulos por usuário em uma trilha.
            * `progresso_conteudo`: Rastreia a conclusão de conteúdos por usuário em um módulo, registrando XP e moedas ganhos.
        * **Quizzes e Jogos**: Tabelas detalhadas para questões, alternativas, tentativas de quiz e sessões de jogo/pontuações, permitindo a gamificação.
        * **Conquistas**:
            * `conquistas`: Define as conquistas (título, descrição, ícone, XP concedido).
            * `usuario_conquistas`: Rastreia as conquistas desbloqueadas por cada usuário.
    * **Fórum**:
        * `subforums`: Define as seções temáticas do fórum.
        * `topicos`: Discussões iniciadas em um subfórum (título, autor, status: fixado/fechado, votos).
        * `postagens`: Contribuições em um tópico (texto, autor, data, edição, votos).
        * `votos_postagem`: Rastreia votos em postagens para evitar duplicidade e calcular pontuação.
        * Lógica para criar subfóruns/tópicos/postagens e para votar.



## Frontend (Interface do Usuário)

As imagens 1, 2 e 3 mostram um pouco do frontend do site:

<div align="center">
    Figura 1: Home
    <br>
    <img src="https://raw.githubusercontent.com/UnBArqDsw2025-1-Turma02/2025.1_T02_G9_GalaxiaConectada_Entrega_04/b5a8f8a8856cb25fb62b4af1a57a67c557e222a9/docs/ArquiteturaReutilizacao/GalaxiaConectada/Imagem/Screenshot%20from%202025-07-04%2003-09-36.png" width="1200">
    <br>
    <b>Autora:</b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.
    <br>
</div>

<div align="center">
    Figura 2: Login
    <br>
    <img src="https://raw.githubusercontent.com/UnBArqDsw2025-1-Turma02/2025.1_T02_G9_GalaxiaConectada_Entrega_04/b5a8f8a8856cb25fb62b4af1a57a67c557e222a9/docs/ArquiteturaReutilizacao/GalaxiaConectada/Imagem/Screenshot%20from%202025-07-04%2003-10-21.png" width="1200">
    <br>
    <b>Autora:</b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.
    <br>
</div>

<div align="center">
    Figura 3: Trilas Aprendizado 2
    <br>
    <img src="https://raw.githubusercontent.com/UnBArqDsw2025-1-Turma02/2025.1_T02_G9_GalaxiaConectada_Entrega_04/084cba06f7913be195540f1a5ac2797c275c86d1/docs/ArquiteturaReutilizacao/GalaxiaConectada/Imagem/Screenshot%20from%202025-07-04%2022-42-15.png" width="1200">
    <br>
    <b>Autora:</b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.
    <br>
</div>

<div align="center">
    Figura 4: Aba Científico
    <br>
    <img src="https://raw.githubusercontent.com/UnBArqDsw2025-1-Turma02/2025.1_T02_G9_GalaxiaConectada_Entrega_04/084cba06f7913be195540f1a5ac2797c275c86d1/docs/ArquiteturaReutilizacao/GalaxiaConectada/Imagem/Screenshot%20from%202025-07-04%2022-42-30.png" width="1200">
    <br>
    <b>Autora:</b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.
    <br>
</div>

<div align="center">
    Figura 5: Fórum 
    <br>
    <img src="https://raw.githubusercontent.com/UnBArqDsw2025-1-Turma02/2025.1_T02_G9_GalaxiaConectada_Entrega_04/084cba06f7913be195540f1a5ac2797c275c86d1/docs/ArquiteturaReutilizacao/GalaxiaConectada/Imagem/Screenshot%20from%202025-07-04%2022-42-46.png" width="1200">
    <br>
    <b>Autora:</b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.
    <br>
</div>


<div align="center">
    Figura 6: Tópicos no Fórum
    <br>
    <img src="https://raw.githubusercontent.com/UnBArqDsw2025-1-Turma02/2025.1_T02_G9_GalaxiaConectada_Entrega_04/084cba06f7913be195540f1a5ac2797c275c86d1/docs/ArquiteturaReutilizacao/GalaxiaConectada/Imagem/Screenshot%20from%202025-07-04%2022-43-04.png" width="1200">
    <br>
    <b>Autora:</b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.
    <br>
</div>

* **Design Consistente**: Todas as páginas seguem um tema espacial escuro, com tipografia `Montserrat` e `Orbitron`, e cores como azul escuro, dourado e azul claro, mantendo a estética inspirada no Khan Academy. Design responsivo para se adaptar a diferentes tamanhos de tela.
* **Navegação**: Menu principal com links para Home, Conhecimento, Jogos, Fórum, etc.
* **Área do Usuário Logado**: No cabeçalho, exibe o nome do usuário, seu tipo, um link direto para o "Perfil" (que redireciona para o perfil específico do tipo de usuário) e um sino de notificações com contador de mensagens não lidas.
* **Páginas de Autenticação**: Telas de `Entrar` e `Cadastrar` com opções de login social (apenas visual) e formulários funcionais.
* **Perfis de Usuário**: Páginas dedicadas para `Administrador` (com gerenciamento de usuários), `Aluno` (com mascote e progresso), `Instrutor`, `Professor Voluntário`, `Moderador` e `Visitante`, exibindo informações relevantes para cada tipo.
* **Sistema de Mascote (Aluno)**:
    * No perfil do aluno, exibe o mascote atual (com imagem da fase de evolução), nome personalizado e XP.
    * Barra de progresso de XP do mascote.
    * Botão "Escolher Meu Primeiro Mascote" que leva a uma página de seleção.
    * Loja de Acessórios para Mascotes: Permite gastar XP para equipar itens de personalização.
* **Seção de Conhecimento**:
    * Página principal (`/conhecimento`) com listagem de categorias e conteúdos recentes.
    * Páginas de detalhe de conteúdo (`/conhecimento/<id>`) exibindo artigos, vídeos incorporados (YouTube), placeholders para quizzes e jogos, com opções de curtir, comentar e se inscrever em categorias de notificação.
    * Formulário (`/conhecimento/publish`) para usuários autorizados publicarem novos conteúdos, com campos específicos para cada tipo (Artigo, Vídeo, Quiz, Jogo).
* **Trilhas de Aprendizado**:
    * Catálogo (`/trilhas`) com listagem das trilhas disponíveis, filtráveis por categoria e nível.
    * Páginas de detalhes da trilha (`/trilhas/<id>`) exibindo uma descrição, imagem, autor e listagem de seus módulos. Opção para se inscrever na trilha e acompanhar o progresso.
    * Páginas de detalhes do módulo (`/trilhas/<id_trilha>/modulos/<id_modulo>`) listando os conteúdos (artigos, vídeos, quizzes, jogos) ordenados.
    * Funcionalidade para marcar conteúdos como concluídos, atualizando XP e moedas do usuário.
* **Ranking e Conquistas**:
    * Página de `Ranking` (`/ranking`) exibindo os top 10 usuários por XP e por trilhas concluídas.
    * Página de `Conquistas` (`/conquistas`) mostrando as conquistas desbloqueadas pelo usuário e todas as conquistas disponíveis (bloqueadas/desbloqueadas).
* **Fórum**:
    * Página principal (`/forum`) listando os subfóruns disponíveis.
    * Página de detalhes do subfórum (`/forum/<id>`) listando os tópicos, com filtros e status (fixado/fechado).
    * Página de detalhes do tópico (`/forum/topic/<id>`) exibindo postagens, com sistema de votação (upvote/downvote) e comentários.
    * Formulários para criar subfóruns e tópicos.
    * Funcionalidades básicas de moderação (fixar/fechar tópicos, apagar postagens/comentários).
* **Acessibilidade**: Implementação de botões para alternar fonte disléxica e tamanho da fonte.


## Usuários Cadastrados para Teste

Para facilitar o teste das diferentes funcionalidades, os seguintes usuários foram pré-cadastrados no banco de dados (`galaxia.db`):

| Categoria | Nome Usuário | Email | Apelido | Senha | Descrição ou Permissões |
| :-------------------- | :------------- | :---------------------------------- | :------------- | :--------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Administrador** | BruceMorceguinho | `BruceWayne@gmail.com` | BruceMorceguinho | `IamBatman` | Guardião da Galáxia Conectada. Todas as permissões administrativas: gerenciar usuários, aprovar conteúdo, gerenciar promoções, alterar status de usuário, moderar fórum, gerenciar trilhas, gerenciar conteúdo, ver logs, gerenciar configurações globais, publicar conteúdo. |
| **Aluno** | Hermione | `HermioneGranger@aluno.hogwarts.com` | Hermione | `Alohomora` | Sempre pronta para aprender e explorar os mistérios do universo. Pode acessar trilhas, jogos, quizzes, fórum e gerenciar seu mascote. |
| **Aluno** | Harry Potter | `HarryPotter@aluno.hogwarts.com` | Harry Potter | `Alohomora` | O garoto que sobreviveu e agora explora a Galáxia Conectada. Pode acessar trilhas, jogos, quizzes, fórum e gerenciar seu mascote. |
| **Professor Voluntário** | Professor Snape | `SeveroSnape@professor.hogwarts.com` | Professor Snape | `Alohomora` | Mestre em Poções e entusiasta da astrofísica teórica. Pode publicar conteúdo e gerenciar trilhas/conteúdos educacionais. |
| **Moderador** | Argus Filch | `ArgusFilch@moderador.hogwarts.com` | Argus Filch | `Alohomora` | Zelador da ordem e da disciplina no fórum da Galáxia. Tem permissões de moderação de fórum (apagar postagens/comentários, fixar/fechar tópicos). |

<b> Autora: </b> <a href="https://github.com/SkywalkerSupreme">Larissa Stéfane</a>.

## Como Rodar o Projeto Localmente

Para configurar e rodar a "Galáxia Conectada" em sua máquina local, siga estes passos:

1.  **Clone o Repositório** (se ainda não o fez):
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd galaxia-conectada
    ```
2.  **Crie e Ative um Ambiente Virtual (venv)**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux/macOS
    .\venv\Scripts\activate    # Windows CMD/PowerShell
    ```
3.  **Instale as Dependências do Flask**:
    ```bash
    pip install Flask werkzeug
    ```
    *(Observação: A implementação atual usa `sqlite3` nativo do Python, então `Flask-SQLAlchemy` não é estritamente necessário.)*

4.  **Certifique-se de que o backend é um pacote Python**:
    Verifique se existe um arquivo vazio chamado `__init__.py` dentro da pasta `backend/`. Se não existir, crie-o:
    ```bash
    touch backend/__init__.py
    ```

5.  **Exclua e Inicialize o Banco de Dados**:
    Como o esquema do banco de dados mudou várias vezes, é **CRUCIAL** recriá-lo do zero.
    * **Navegue até a pasta `db_data`**:
        ```bash
        cd backend/db_data/
        ```
    * **Exclua o arquivo `galaxia.db` (se existir)**:
        * **Linux/macOS**: `rm galaxia.db`
        * **Windows (CMD)**: `del galaxia.db`
        * **Windows (PowerShell)**: `Remove-Item galaxia.db`
    * **Volte para a pasta `backend`**:
        ```bash
        cd ..
        ```
    * **Execute o script de inicialização do banco de dados**:
        ```bash
        python database.py
        ```
        Você verá mensagens no terminal confirmando a criação das tabelas e a inserção dos dados de teste.

6.  **Inicie o Servidor Flask**:
    * **Volte para a pasta raiz do projeto (`galaxia_conectada/`)**:
        ```bash
        cd ..
        ```
    * **Execute o Flask**:
        ```bash
        flask --app backend.app run --debug
        ```
        O servidor Flask deve iniciar e você verá mensagens de `DEBUG`.

7.  **Acesse o Site**:
    Abra seu navegador e vá para `http://127.0.0.1:5000/`.

## Vídeo para rodar:

Abaixo o video 1 mostra como rodar o site localmente:



## Apresentação da Plataforma

Abaixo o video 2 mostra como o site se encontra:

<iframe width="1321" height="743" src="https://www.youtube.com/embed/rBa4Pqxj1Qc" title="Apresentando a Plataforma: Galáxia Conectada" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>


## Próximos Passos

A "Galáxia Conectada" já possui uma base sólida, com funcionalidades robustas de autenticação, perfis de usuário variados, um sistema de mascotes interativo, um centro de conhecimento com artigos e trilhas, e um fórum dinâmico para a comunidade.

Para continuar aprimorando e expandindo a plataforma, os próximos passos potenciais incluem:

* **Expansão da Lógica de Quizzes e Jogos**: Implementar a jogabilidade real, submissão de respostas, cálculo de pontuação e feedback instantâneo para os quizzes. Desenvolver a integração e o funcionamento dos jogos educativos.
* **Desenvolvimento da "Loja de Promoções"**: Criar a seção dedicada a promoções e recompensas, conforme planejado no menu principal.
* **Funcionalidade de Compartilhamento**: Implementar a capacidade de compartilhar conteúdos (artigos, notícias) com amigos via e-mail ou outras plataformas de forma direta.
* **Refinamento de XP e Moedas**: Aprofundar a lógica de ganho e uso de XP e moedas, integrando-as de forma mais granular com o progresso em trilhas, interações no fórum e uso da loja de mascotes.
* **Gerenciamento de Conteúdo e Postagens**: Adicionar funcionalidades para que os próprios usuários criadores (Instrutores, Professores Voluntários) possam editar e excluir seus conteúdos e postagens, além das permissões de moderação existentes.
* **Melhorias na Experiência do Usuário (UX)**: Incorporar animações mais fluidas, transições e feedback visual aprimorado para tornar a interação com a plataforma ainda mais agradável e intuitiva.
* **Conexão Fórum-Trilhas**: Integrar as "Trilhas de Dúvidas" no fórum de forma mais direta com módulos ou conteúdos específicos, facilitando o suporte ao aprendizado.
* **Roteiros de Experimentos e Indicações de Apps**: Desenvolver e integrar conteúdos que ofereçam roteiros para experimentos domiciliares simples ou indicações de aplicativos que funcionam como telescópios virtuais.


## Conclusão

O projeto "Galáxia Conectada" demonstrou um progresso significativo na construção de uma plataforma educacional de astronomia interativa e engajadora. A arquitetura modular foi toda desenvolvida durante o semestre de 2025.1.

## Histórico de Versão

| Versão | Alteração | Responsável | Data |
| - | - | - | - |
| 1.0 | Elaboração do documento| Larissa Stéfane | 03/07/2024 |
| 1.1 | Adição da tabelas dos usuários | Larissa Stéfane | 03/07/2024 |
| 1.2 | Elaboração dos próximos passos | Larissa Stéfane | 03/07/2024 |

