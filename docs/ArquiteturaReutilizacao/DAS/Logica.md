# Documento de Arquitetura de Software - Lógica


### Sumário

1.  [Introdução](#1-introdução)
    1.1 [Propósito](#11-propósito)
    1.2 [Escopo](#12-escopo)
    1.3 [Definições, Acrônimos e Abreviações](#13-definições-acrônimos-e-abreviações)
    1.4 [Referências](#14-referências)
    1.5 [Visão Geral](#15-visão-geral)
2.  [Requisitos Elicitados](#2-requisitos-elicitados)
    2.1 [Requisitos Funcionais](#21-requisitos-funcionais)
    2.2 [Requisitos Não Funcionais](#22-requisitos-não-funcionais)
3.  [Metas e Restrições Arquiteturais](#3-metas-e-restrições-arquiteturais)
4.  [Representação Arquitetural](#4-representação-arquitetural)
5.  [Funcionalidades Chave](#5-funcionalidades-chave)
6.  [Conectores](#6-conectores)
7.  [Visão de Casos de Uso](#7-visão-de-casos-de-uso)
    7.1 [Realizações de Caso de Uso](#71-realizações-de-caso-de-uso)
8.  [Visão Lógica](#8-visão-lógica)
    8.1 [Visão Geral](#81-visão-geral)
    8.2 [Pacotes de Design Arquiteturalmente Significativos](#82-pacotes-de-design-arquiteturalmente-significativos)
9.  [Visão de Processo](#9-visão-de-processo)
10. [Visão de Implantação](#10-visão-de-implantação)
11. [Visão de Implementação](#11-visão-de-implementação)
    11.1 [Visão Geral](#111-visão-geral)
    11.2 [Camadas](#112-camadas)
12. [Visão de Dados (Opcional)](#12-visão-de-dados-opcional)
13. [Tamanho e Performance](#13-tamanho-e-performance)
14. [Qualidade](#14-qualidade)

---

### 1. Introdução

Este documento oferece uma visão arquitetural abrangente do sistema **Galáxia Conectada**, utilizando diferentes perspectivas arquiteturais para ilustrar seus diversos aspectos. Ele tem como objetivo principal capturar e comunicar as decisões arquiteturais significativas tomadas para o sistema.

#### 1.1 Propósito

Este documento tem como propósito servir como um **guia técnico e de referência** para todos os envolvidos no projeto Galáxia Conectada, incluindo desenvolvedores, designers, gerentes de projeto e futuros contribuidores. Ele formaliza as escolhas de design que impactam a estrutura, o comportamento e a implantação do sistema, garantindo **alinhamento e consistência** durante o desenvolvimento e a manutenção.

#### 1.2 Escopo

Este Documento de Arquitetura de Software (DAS) aplica-se à totalidade da plataforma **Galáxia Conectada**, abrangendo suas funcionalidades de trilhas de aprendizado, jogos educativos, fórum de discussões, aba de notícias, calendário de eventos e monitoramento de promoções. O escopo definido influencia diretamente as estratégias de design, implementação, testes e implantação, garantindo que o sistema seja construído de forma **coesa e escalável** para seus objetivos educacionais e interativos.

#### 1.3 Definições, Acrônimos e Abreviações

Para garantir a clareza e padronização da terminologia utilizada neste documento, todas as definições de termos, siglas e abreviações podem ser consultadas no **Glossário** do projeto "Galáxia Conectada", disponível em [Glossário](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Base/ArtefatoGeneralista/Glossario).

#### 1.4 Referências

A elaboração deste documento baseou-se nos seguintes artefatos e referências:

* **Documentação do Projeto Galáxia Conectada:**
    * [Design Sprint: Entender (Unpack)](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/DesignSprint/Entender)
    * [Design Sprint: Esboçar (Sketch)](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/DesignSprint/Esbo%C3%A7ar)
    * [Design Sprint: Decidir (Decision)](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/DesignSprint/Decidir)
    * [Design Sprint: Prototipação (Prototype)](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/DesignSprint/Prototipo)
    * [5W+2H](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/5W2H)
    * [Brainstorming](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/BrainStorm)
    * [Rich Picture](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/RichPicture)
    * [Diagrama de Classes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaClasses)
    * [Diagrama de Componentes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaComponentes)
    * [Diagrama de Implantação](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaImplantacao)
    * [Diagrama de Atividades](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaAtividades)
    * [Diagrama de Comunicação ou Colaboração](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaComunica%C3%A7%C3%A3o)
    * [Diagrama de Estados](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaEstados)
    * [Diagrama de Casos de Uso](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemOrganizacional/DiagramaCasosUso)
    * [Diagrama de Pacotes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemOrganizacional/DiagramaPacotes)
    * [Estimativas: Risco, Custo e Tempo](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)

#### 1.5 Visão Geral

O restante deste Documento de Arquitetura de Software está organizado nas seguintes seções:

* **Seção 2: Requisitos Elicitados** – Apresenta os requisitos funcionais e não funcionais que o sistema deve atender.
* **Seção 3: Metas e Restrições Arquiteturais** – Detalha os requisitos e objetivos que impactam significativamente a arquitetura do sistema.
* **Seção 4: Representação Arquitetural** – Descreve quais visões arquiteturais são utilizadas e o propósito de cada uma no contexto do Galáxia Conectada.
* **Seção 5: Funcionalidades Chave** – Lista as principais funcionalidades que o sistema deve ter.
* **Seção 6: Conectores** – Descreve os veículos de comunicação entre os componentes e as interações.
* **Seção 7: Visão de Casos de Uso** – Apresenta os casos de uso arquiteturalmente significativos e suas realizações.
* **Seção 8: Visão Lógica** – Descreve a decomposição do modelo de design em subsistemas e pacotes, e as classes mais importantes.
* **Seção 9: Visão de Processo** – Detalha a decomposição do sistema em processos leves e pesados, e seus modos de comunicação.
* **Seção 10: Visão de Implantação** – Mostra a configuração física da rede e o mapeamento dos processos nos nós físicos.
* **Seção 11: Visão de Implementação** – Descreve a estrutura do modelo de implementação, camadas e componentes.
* **Seção 12: Visão de Dados (Opcional)** – Detalha a perspectiva de armazenamento de dados persistentes.
* **Seção 13: Tamanho e Performance** – Aborda as características de dimensionamento do software e as restrições de desempenho.
* **Seção 14: Qualidade** – Descreve como a arquitetura contribui para as qualidades do sistema (extensibilidade, confiabilidade, segurança, etc.).

---

### 2. Requisitos Elicitados

#### Sumário

* [Introdução](#introdução-1)
* [Requisitos Funcionais](#requisitos-funcionais)
* [Requisitos Não Funcionais](#requisitos-não-funcionais)
* [Conclusão](#conclusão-1)
* [Histórico de versão](#histórico-de-versão-1)

#### Introdução

O levantamento e a organização dos requisitos são etapas fundamentais no desenvolvimento do projeto Galáxia Conectada. Com isso, este documento apresenta de forma estruturada os requisitos funcionais e não funcionais que norteiam a construção da plataforma, reunidos a partir de brainstorming, análises de benchmarking com sites e plataformas semelhantes, e das necessidades específicas do público-alvo.

#### 2.1 Requisitos Funcionais

<details>
  <summary>Tabela 1: Geral de Requisitos Funcionais</summary>

| Código | Requisito Funcional | Rastreabilidade |
|---|---|---|
| RF01 | Oferecer trilhas de aprendizado organizadas por tema, nível e categoria. | Brainstorming, Plataformas Educacionais, Benchmarking Divulgação Científica |
| RF02 | Exibir aulas, artigos, vídeos e testes integrados às trilhas. | Brainstorming, Animações, Plataformas Educacionais |
| RF03 | Apresentar trilhas como missões espaciais lúdicas. | Brainstorming |
| RF04 | Armazenar o progresso dos usuários e exibir certificados de conclusão. | Brainstorming, Plataformas Educacionais |
| RF05 | Atribuir recompensas (XP, moedas, conquistas) por participação e progresso. | Brainstorming, Jogos |
| RF06 | Fornecer feedback imediato em quizzes, exercícios e jogos. | Brainstorming, Jogos, Plataformas Educacionais |
| RF07 | Exibir rankings e destaques entre usuários, com sistema de reputação. | Brainstorming, Fóruns, Jogos |
| RF08 | Oferecer jogos educativos e interativos com diferentes níveis, temas e formatos. | Brainstorming, Jogos |
| RF09 | Permitir criação de tópicos e postagens no fórum, com comentários, tags e votos. | Brainstorming, Fóruns |
| RF10 | Disponibilizar busca eficiente por conteúdos (trilhas, fóruns, artigos, jogos etc). | Divulgação Científica, Fóruns, Plataformas Educacionais |
| RF11 | Exibir calendário de eventos astronômicos com filtros e notificações. | Brainstorming, Divulgação Científica |
| RF12 | Enviar notificações personalizadas sobre eventos e promoções. | Brainstorming, Promoções |
| RF13 | Disponibilizar blog com artigos, glossário e filtros por categorias e níveis. | Brainstorming, Divulgação Científica |
| RF14 | Atualizar regularmente publicações e notícias científicas. | Brainstorming, Divulgação Científica |
| RF15 | Permitir que usuários enviem conteúdos (fotos, textos, sugestões). | Divulgação Científica |
| RF16 | Recomendar conteúdos com base no histórico e perfil do usuário. | Jogos, Plataformas Educacionais, Promoções |
| RF17 | Integrar vídeos educativos de criadores parceiros à plataforma. | Animações |
| RF18 | Incluir roteiros de experimentos práticos para casa e indicações de apps de astronomia. | Brainstorming |
| RF19 | Exibir promoções organizadas por categoria com filtros e favoritos. | Promoções |
| RF20 | Notificar promoções e novidades por bot ou push. | Brainstorming, Promoções |
| RF21 | Disponibilizar jogos e quizzes com tempo limitado. | Brainstorming |
| RF22 | Permitir acesso diário a novos desafios e atividades gamificadas. | Jogos |
| RF23 | Exibir perfil de usuário com histórico de participação, reputação e conquistas. | Fóruns, Jogos |
| RF24 | Permitir comentários e interações nos conteúdos da plataforma (aulas, artigos, vídeos etc.). | Plataformas Educacionais |
| RF25 | Apresentar seção com conteúdos populares ou mais votados. | Fóruns |

**Autora:** [Larissa Stéfane](https://github.com/SkywalkerSupreme)
</details>

#### 2.2 Requisitos Não Funcionais

<details>
  <summary>Tabela 2: Geral de Requisitos Não Funcionais</summary>

| Código | Requisito Não Funcional | Objetivo | Rastreabilidade / Origem |
|---|---|---|---|
| RNF01 | A plataforma deve ser responsiva e compatível com dispositivos móveis, tablets e desktops. | Garantir acessibilidade e boa usabilidade em diferentes telas. | Brainstorming, Animações, Divulgação Científica |
| RNF02 | O tempo de resposta das páginas e conteúdos deve ser inferior a 3 segundos. | Proporcionar fluidez e boa experiência de navegação. | Brainstorming, Animações, Educacionais |
| RNF03 | O sistema deve seguir diretrizes de acessibilidade (WCAG 2.1, contraste, leitores de tela, teclado). | Incluir pessoas com deficiência e neurodivergência. | Brainstorming, Jogos, Fóruns, Divulgação Científica |
| RNF04 | Os dados dos usuários devem ser armazenados com segurança, incluindo criptografia e backup. | Proteger informações pessoais e de progresso. | Brainstorming, Jogos, Educacionais |
| RNF05 | O sistema deve ter disponibilidade mínima de 99,5% e suportar escalabilidade. | Evitar interrupções e manter estabilidade com aumento de usuários. | Brainstorming |
| RNF06 | A interface deve ser clara, intuitiva e com linguagem acessível. | Facilitar o uso por iniciantes e melhorar a navegação geral. | Brainstorming, Divulgação Científica |
| RNF07 | A plataforma deve suportar múltiplos idiomas e adaptar-se ao idioma do usuário. | Ampliar o alcance internacional e a inclusão. | Fóruns, Animações |
| RNF08 | Os conteúdos devem ser organizados por níveis e com fácil navegação entre seções. | Apoiar o aprendizado progressivo e a orientação do usuário. | Divulgação Científica, Animações |
| RNF09 | O sistema deve ser compatível com navegadores modernos (Chrome, Firefox, Edge, Safari). | Garantir o acesso por diferentes perfis de usuários. | Brainstorming |
| RNF10 | A plataforma deve ser otimizada para mecanismos de busca (SEO). | Aumentar a visibilidade e atrair novos usuários. | Divulgação Científica, Fóruns |
| RNF11 | Recursos multimídia (como vídeos) devem carregar com rapidez e ter suporte a legendas. | Melhorar a experiência de consumo e a acessibilidade. | Animações, Educacionais |
| RNF12 | O sistema deve permitir atualizações frequentes sem comprometer o funcionamento. | Garantir evolução contínua sem prejudicar a experiência do usuário. | Brainstorming, Promoções |

**Autora:** [Larissa Stéfane](https://github.com/SkywalkerSupreme)
</details>

#### Conclusão

O levantamento e a organização dos requisitos aqui apresentados fornecem uma base sólida para o desenvolvimento da plataforma Galáxia Conectada. Os requisitos funcionais delimitam o "o quê" o sistema fará, enquanto os não funcionais determinam o "quão bem" essas funcionalidades devem ser entregues. Essa clareza será essencial para guiar as decisões de design, implementação e testes, garantindo que a plataforma atenda às expectativas dos usuários e aos objetivos do projeto.

---

### 3. Metas e Restrições Arquiteturais

As metas e restrições arquiteturais guiam as decisões de design do Galáxia Conectada, garantindo que o sistema não apenas atenda aos requisitos funcionais, mas também às qualidades essenciais para sua operação e evolução.

**Metas Arquiteturais:**

* **Engajamento do Usuário:** A arquitetura deve suportar mecanismos de gamificação e interatividade (**RF05, RF07, RF08, RF09, RF10, RF11, RF21, RF22, RF23, RF24, RF25**) para manter os usuários motivados e engajados no aprendizado de astronomia.
* **Acessibilidade e Inclusão:** O design arquitetural deve priorizar a acessibilidade para pessoas com e sem deficiência e neurodivergentes (**RNF05, RNF06, RNF10**). Isso implica na escolha de *frameworks* e componentes que facilitem a criação de interfaces acessíveis e na consideração de design responsivo.
* **Disponibilidade:** O sistema deve estar acessível de forma contínua para os usuários (**RNF04**), minimizando o tempo de inatividade.
* **Escalabilidade:** A arquitetura deve permitir que o sistema se adapte a um número crescente de usuários e dados sem degradação significativa de desempenho (**RNF07**).
* **Manutenibilidade e Extensibilidade:** A modularidade e a separação de responsabilidades devem facilitar a manutenção do código e a adição de novas funcionalidades ou módulos no futuro (**RNF08**).
* **Segurança dos Dados:** A arquitetura deve proteger os dados dos usuários e do conteúdo contra acessos não autorizados e perdas (**RNF03, RNF04**).
* **Desempenho:** As interações devem ser rápidas e responsivas, com tempo de resposta satisfatório (**RNF02**).
* **Confiança no Conteúdo:** O sistema deve garantir que o conteúdo científico veiculado seja validado e confiável (Implícito em **RF13, RF14, RF15** e as ações preventivas do [Diagrama de Ishikawa](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/DiagramasIshikawa)).

**Restrições Arquiteturais:**

* **Recursos Limitados (Projeto Acadêmico):** O projeto está sendo desenvolvido individualmente, o que impõe restrições de tempo e mão de obra ([Estimativas: Risco, Custo e Tempo](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)). A escolha de tecnologias e a complexidade das soluções devem refletir essa limitação.
* **Uso de Ferramentas Gratuitas/Open Source:** Prioridade para o uso de ferramentas de desenvolvimento e plataformas de hospedagem que sejam gratuitas ou ofereçam planos educacionais, como Figma, Draw.io, GitHub, etc. ([Estimativas: Plano de Custo](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)).
* **Prazo Definido:** O desenvolvimento está limitado ao semestre letivo 2025.1 ([Estimativas: Plano de Tempo](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)), o que exige um foco no Mínimo Produto Viável (MVP) para cada entrega.
* **Dependência de APIs/Fontes Externas:** A integração com APIs externas (ex: para notícias e eventos astronômicos) e o *scraping* de promoções podem apresentar instabilidades ou alterações que exigem adaptações na arquitetura ([Diagrama de Ishikawa: Foco no Projeto - Dificuldade na validação científica](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/DiagramasIshikawa), [Estimativas: Planos de Risco - R12, R13](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)).
* **Conhecimento Técnico da Equipe:** A experiência individual da desenvolvedora pode influenciar a escolha de tecnologias e a profundidade de certas implementações ([Diagrama de Ishikawa: Foco no Projeto - Mão de Obra](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/DiagramasIshikawa), [Estimativas: Planos de Risco - R3](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)).

---

### 4. Representação Arquitetural

Para o sistema **Galáxia Conectada**, a arquitetura de software é concebida como uma estrutura em camadas, baseada em um design modular que promove a separação de preocupações e a manutenibilidade. A arquitetura é representada através de múltiplas **visões arquiteturais da UML**, cada uma fornecendo uma perspectiva específica do sistema:

* **Visão de Casos de Uso:** Essencial para descrever a funcionalidade do sistema do ponto de vista do usuário final e de outros sistemas externos. Ela contém os **Atores** (usuários e sistemas) e os **Casos de Uso** (funcionalidades), ilustrando o que o sistema faz.
    * **Artefato:** [Diagrama de Casos de Uso](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemOrganizacional/DiagramaCasosUso)
* **Visão Lógica:** Descreve a decomposição funcional do sistema em módulos, subsistemas e pacotes de design, bem como suas classes e relacionamentos mais importantes. Foca na organização do código em um nível conceitual, como as funcionalidades são agrupadas.
    * **Artefatos:** [Diagrama de Classes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaClasses), [Diagrama de Pacotes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemOrganizacional/DiagramaPacotes)
* **Visão de Processo:** Aborda a concorrência e a distribuição das funcionalidades, descrevendo como os processos (threads, processos do sistema operacional) se comunicam e se sincronizam.
    * **Artefatos:** [Diagrama de Atividades](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaAtividades), [Diagrama de Comunicação](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaComunica%C3%A7%C3%A3o), [Diagrama de Estados](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaEstados)
* **Visão de Implantação:** Descreve a distribuição física do software em nós de hardware e software, incluindo servidores, dispositivos e as conexões entre eles.
    * **Artefato:** [Diagrama de Implantação](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaImplantacao)
* **Visão de Implementação:** Detalha a estrutura do código-fonte, a organização em componentes e a dependência entre eles. Foca na organização dos artefatos de software.
    * **Artefato:** [Diagrama de Componentes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaComponentes)

Cada uma dessas visões complementa as demais para fornecer uma compreensão holística da arquitetura do Galáxia Conectada.

---

### 5. Funcionalidades Chave

A plataforma **Galáxia Conectada** foi projetada para oferecer uma rica experiência educacional e interativa em astronomia. As funcionalidades chave, baseadas nos requisitos funcionais elicitados, incluem:

* **Trilhas de Aprendizado Gamificadas:** Permitem aos usuários progredir em tópicos de astronomia por meio de módulos estruturados, com recompensas (XP, moedas, conquistas) e feedback imediato em exercícios e quizzes (**RF01, RF02, RF03, RF04, RF05, RF06, RF21, RF22**).
* **Fórum de Discussões:** Um espaço para a comunidade interagir, criar tópicos, postar comentários, e usar um sistema de reputação e votos para engajamento (**RF07, RF09, RF23, RF24, RF25**).
* **Aba de Notícias e Artigos:** Publicação regular de conteúdo científico atualizado, incluindo artigos de blog, glossário e a possibilidade de submissão de conteúdo por usuários (**RF13, RF14, RF15**).
* **Jogos Educativos:** Oferece uma variedade de jogos e quizzes interativos para tornar o aprendizado divertido e testar conhecimentos (**RF08, RF10, RF11**).
* **Calendário de Eventos Astronômicos:** Exibe eventos locais e globais, com filtros e notificações personalizadas (**RF11, RF12**).
* **Promoções Astronômicas:** Notifica usuários sobre promoções de produtos relacionados à astronomia em lojas externas, com filtros e favoritos (**RF19, RF20**).
* **Recomendações Personalizadas:** Sugere conteúdos (trilhas, artigos, jogos) com base no histórico e perfil do usuário (**RF16**).
* **Recursos Práticos:** Inclui roteiros de experimentos caseiros e indicações de aplicativos de telescópios virtuais (**RF18, RF21**).

---

### 6. Conectores

Os **conectores** representam os veículos de comunicação e os mecanismos de interação entre os diferentes componentes do sistema Galáxia Conectada. Eles definem como os elementos da arquitetura se comunicam e colaboram para realizar as funcionalidades do sistema.

**Principais Tipos de Conectores Utilizados:**

* **Chamadas de Procedimento/Método (In-Process):**
    * **Descrição:** Ocorre quando um componente invoca diretamente um método ou procedimento em outro componente que reside no mesmo processo de execução (na mesma aplicação ou serviço). É a forma mais comum de comunicação interna em arquiteturas monolíticas ou em módulos dentro do mesmo microsserviço.
    * **Exemplo no Projeto:**
        * Um *controller* da API (`APIGateway`) chamando um método em um serviço de aplicação (`ModuloEducacional`).
        * O `ModuloEducacional` invocando métodos no `ModuloGamificacao` para atualizar o XP do usuário.
    * **Rastreabilidade:** Evidenciado nos **Diagramas de Comunicação** (mensagens entre *lifelines* no mesmo processo) e **Diagramas de Atividades** (ações sequenciais que representam chamadas internas).
* **Protocolos de Comunicação (HTTP/HTTPS - RESTful APIs):**
    * **Descrição:** Usado para comunicação entre componentes distribuídos ou entre a interface do usuário e o backend, normalmente via requisições HTTP/HTTPS. Este tipo de conector é fundamental para arquiteturas cliente-servidor e microsserviços.
    * **Exemplo no Projeto:**
        * A `WebUI` (frontend) enviando requisições GET/POST/PUT para a `APIGateway` (backend) para carregar trilhas, submeter posts no fórum ou registrar progresso.
        * Bots de importação (`BotImportadorNoticias`, `BotImportadorPromocoes`) fazendo requisições HTTP para APIs ou sites externos.
    * **Rastreabilidade:** Representado nas interações entre `WebUI` e `APIGateway` nos **Diagramas de Sequência** e **Comunicação**, e nas conexões com `APIs/Sites Externos` no **Diagrama de Implantação**.
* **Acesso a Banco de Dados (SQL/ORM):**
    * **Descrição:** O mecanismo pelo qual os componentes de aplicação e domínio interagem com o sistema de persistência de dados. Geralmente envolve *drivers* de banco de dados e, frequentemente, um *Object-Relational Mapper (ORM)* para mapear objetos para tabelas de banco de dados.
    * **Exemplo no Projeto:**
        * O `ModuloEducacional` persistindo o progresso do usuário no `BancoDeDados` após a conclusão de um módulo.
        * O `ModuloForum` buscando tópicos e postagens no `BancoDeDados`.
    * **Rastreabilidade:** Ilustrado pelas mensagens entre os módulos de aplicação e o `BancoDeDados` nos **Diagramas de Atividades** e **Sequência**. A camada de `Infraestrutura.Persistencia` no **Diagrama de Pacotes** encapsula esse conector.
* **Filas de Mensagens (Assíncronas - Futuro Opcional):**
    * **Descrição:** Permite que componentes se comuniquem de forma assíncrona, publicando eventos ou mensagens em uma fila e consumindo-os posteriormente, sem a necessidade de uma resposta imediata. Ideal para operações de *background* ou para desacoplar serviços.
    * **Exemplo no Projeto (potencial futuro):**
        * O `ModuloEducacional` publicando um evento "MóduloConcluido" em uma fila, e o `ModuloGamificacao` consumindo esse evento para calcular XP e conquistas, sem que o `ModuloEducacional` precise esperar pela resposta.
        * Bots de importação publicando "NoticiaImportada" ou "PromocaoDescoberta" para que outros serviços processem.
    * **Rastreabilidade:** Representado pelo pacote `Infraestrutura.Mensageria` no **Diagrama de Pacotes**.

Esses conectores garantem a fluidez e a integridade da comunicação através das diferentes camadas e módulos da arquitetura do Galáxia Conectada.

---

### 7. Visão de Casos de Uso

Esta seção apresenta os casos de uso que representam a funcionalidade central e arquiteturalmente significativa do sistema Galáxia Conectada, ilustrando como os diversos atores interagem com a plataforma.

Para uma representação visual detalhada dos casos de uso e seus atores, consulte o **Diagrama de Casos de Uso** completo do projeto, disponível em [Diagrama de Casos de Uso](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemOrganizacional/DiagramaCasosUso).

Alguns dos casos de uso arquiteturalmente significativos incluem:

* **Realizar Cadastro/Login:** Fundamental para a personalização e acesso a funcionalidades restritas.
* **Navegar em Trilhas de Aprendizado:** Core da experiência educacional.
* **Participar de Jogos Educativos:** Funcionalidade chave de gamificação e aprendizado lúdico.
* **Interagir no Fórum:** Essencial para a construção da comunidade e troca de conhecimentos.
* **Consultar Notícias/Artigos:** Provisão de conteúdo informativo e atualizado.
* **Visualizar Eventos Astronômicos:** Oferece informações sobre ocorrências celestes.
* **Receber Notificações:** Mecanismo para manter o usuário informado sobre novidades e progresso.
* **Gerenciar Promoções (Admin):** Permite a curadoria do conteúdo externo de promoções.
* **Importar Conteúdo Externo (Bot):** Demonstra a integração do sistema com fontes externas.

#### 7.1 Realizações de Caso de Uso

As realizações dos casos de uso mostram como os elementos do modelo de design contribuem para a funcionalidade do sistema. A interação entre a interface do usuário (WebUI), as APIs de backend e os módulos de serviço é fundamental.

Dois cenários arquiteturalmente representativos são:

1.  **Realização do Caso de Uso "Navegar em Trilhas de Aprendizado":**
    * **Descrição:** O usuário acessa a aba de trilhas, seleciona uma categoria, visualiza as trilhas disponíveis, escolhe uma trilha, navega pelos módulos e conteúdos (artigos, vídeos, quizzes), e marca o progresso.
    * **Componentes/Classes Envolvidas:** `WebUI` (para interação), `APIGateway` (para roteamento), `ModuloEducacional` (para lógica de trilhas/módulos/conteúdo), `BancoDeDados` (para persistência de trilhas, módulos, conteúdos e progresso), `ModuloGamificacao` (para atualização de XP/conquistas ao marcar módulos).
    * **Fluxo detalhado:** Este fluxo pode ser visualizado no **Diagrama de Atividades - Aba Conhecimento** e no **Diagrama de Sequência - Trilhas de Aprendizado**.
2.  **Realização do Caso de Uso "Interagir no Fórum (Criar Tópico)":**
    * **Descrição:** O usuário acessa a aba do fórum, escolhe um subfórum, preenche um formulário para criar um novo tópico com uma postagem inicial. O sistema verifica permissões, submete o conteúdo para moderação (se necessário), registra no banco de dados, atualiza a reputação do usuário, indexa o conteúdo para busca e notifica moderadores/inscritos.
    * **Componentes/Classes Envolvidas:** `WebUI` (para formulário), `APIGateway` (roteamento), `GestaoUsuarios` (verificação de permissões), `ModuloForum` (criação de tópico/postagem), `ModuloModeracao` (para fluxo de moderação), `ModuloGamificacao` (para atualização de reputação), `ServicoBusca` (indexação), `ServicoNotificacoes` (notificação), `BancoDeDados` (persistência).
    * **Fluxo detalhado:** Este fluxo pode ser visualizado no **Diagrama de Atividades - Aba Fórum** (implícito na criação, pois o diagrama focou na navegação de artigos, mas o processo é análogo para criação) e no **Diagrama de Comunicação - Fórum**.

---

### 8. Visão Lógica

#### 8.1 Visão Geral

A **Visão Lógica** do Galáxia Conectada descreve a **decomposição funcional** do sistema em termos de seus subsistemas e pacotes de design, bem como as classes e seus relacionamentos mais importantes. Esta visão se organiza em uma arquitetura em camadas, separando as preocupações de apresentação, aplicação, domínio e infraestrutura. O objetivo é fornecer uma **organização clara e modular** que facilite a compreensão, desenvolvimento e manutenção do software. O principal artefato visual que representa essa decomposição é o **Diagrama de Pacotes**.

#### 8.2 Pacotes de Design Arquiteturalmente Significativos

Os pacotes de design a seguir representam os agrupamentos lógicos mais significativos da arquitetura do Galáxia Conectada. Para uma representação visual abrangente dessas pacotes e suas dependências, consulte o **Diagrama de Pacotes** do projeto, disponível em [Diagrama de Pacotes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemOrganizacional/DiagramaPacotes).

* **`GalaxiaConectada`** (Pacote Raiz):
    * **Descrição:** O pacote principal que engloba toda a aplicação, dividindo-a em duas grandes subseções: `Apresentacao` e `Servidor`.
* **`Apresentacao`**:
    * **Descrição:** Camada responsável pela interface com o usuário (**frontend web**). Lida com a renderização das páginas, a interação com o usuário e a comunicação com o backend através da API.
    * **Classes/Responsabilidades Chave:** Gerenciamento de UI (componentes visuais, rotas de frontend), captura de inputs do usuário.
    * **Relacionamentos:** Depende do `Servidor.GatewayAPI` para todas as operações de backend.
* **`Servidor`**:
    * **Descrição:** Pacote que agrupa todos os componentes e lógica do backend. É subdividido em camadas funcionais.
    * **Sub-pacotes Significativos:**
        * **`Servidor.GatewayAPI`**:
            * **Descrição:** Atua como o **ponto de entrada da API**, roteando as requisições da camada de Apresentação para os serviços internos apropriados.
            * **Responsabilidades:** Roteamento de requisições, validação de token (autenticação básica), orquestração inicial.
        * **`Servidor.GerenciamentoUsuarios`**:
            * **Descrição:** Lógica de negócio para **autenticação, autorização, gerenciamento de perfis e papéis de usuários**.
            * **Classes/Responsabilidades Chave:** `Usuario` (gerencia cadastro, login, edição de perfil), `Perfil` (dados de progresso), `Reputacao` (pontuação do usuário).
            * **Relacionamentos:** Manipula `Dominio.Usuario`, utiliza `Infraestrutura.Persistencia`, `ServicosCompartilhados.Configuracao` e `ServicosCompartilhados.Monitoramento`.
        * **`Servidor.Dominio`**:
            * **Descrição:** Onde residem as **entidades, objetos de valor (VOs) e as regras de negócio puras** do sistema, independentes de tecnologia ou detalhes de infraestrutura.
            * **Sub-pacotes Significativos:**
                * `Dominio.Compartilhado`: Tipos base e interfaces comuns.
                * `Dominio.Usuario`: Entidades `Usuario`, `Perfil`, `Reputacao`.
                * `Dominio.Aprendizagem`: Entidades `TrilhaEducacional`, `Modulo`, `Conteudo` (abstrata), `Artigo`, `Video`, `Quiz`, `Jogo`, `ProgressoUsuarioTrilha`.
                * `Dominio.Comunidade`: Entidades `Forum`, `Subforum`, `Topico`, `Postagem`, `Comentario`, `Conquista`.
                * `Dominio.ConteudoInfo`: Entidades `Noticia`, `PromocaoExterna`, `EventoAstronomico`, `FonteDeNoticias`, `FontePromocaoExterna`.
            * **Relacionamentos:** Os pacotes de domínio são usados pelas camadas de `Aplicacao` e `Infraestrutura`.
        * **`Servidor.Aplicacao`**:
            * **Descrição:** Orquestra os casos de uso, coordenando as interações entre a camada de `Domínio`, `Infraestrutura` e os `ServicosCompartilhados`. Implementa a lógica de aplicação dos requisitos funcionais.
            * **Sub-pacotes Significativos:** `Aplicacao.Usuario`, `Aplicacao.Aprendizagem`, `Aplicacao.Comunidade`, `Aplicacao.Conteudo`, `Aplicacao.Integracao`.
            * **Relacionamentos:** Usa `Dominio.*`, `Infraestrutura.Persistencia`, e `ServicosCompartilhados.*`.
        * **`Servidor.ServicosCompartilhados`**:
            * **Descrição:** Agrupa **serviços transversais** que podem ser utilizados por múltiplas camadas ou módulos da aplicação.
            * **Sub-pacotes Significativos:** `Notificacoes`, `Busca`, `Recomendacoes`, `Certificados`, `Localizacao`, `Configuracao`, `Monitoramento`, `Cache`.
            * **Classes/Responsabilidades Chave (ex):** `ServicoNotificacoes` (envio de alertas), `ServicoBusca` (indexação e pesquisa), `ServicoLocalizacao` (traduções).
            * **Relacionamentos:** Usados pelas camadas de `Aplicacao`, `GatewayAPI` e `Infraestrutura`.
        * **`Servidor.Infraestrutura`**:
            * **Descrição:** Contém as implementações concretas e os detalhes técnicos de baixo nível, como **acesso a banco de dados, comunicação com serviços externos e serviços de cache**.
            * **Sub-pacotes Significativos:** `Persistencia`, `ClientesExternos`, `Cache (Impl)`, `Mensageria`.
            * **Classes/Responsabilidades Chave (ex):** Classes que representam `BancoDeDados`, `BotImportadorNoticias`, `BotImportadorPromocoes`.
            * **Relacionamentos:** Fornece serviços à camada de `Aplicacao` e `ServicosCompartilhados`.

---

### 9. Visão de Processo

A Visão de Processo do Galáxia Conectada descreve a decomposição do sistema em processos de execução e como eles interagem em tempo de execução, com foco na concorrência, distribuição e comunicação. Embora o projeto seja inicialmente uma aplicação monolítica (ou uma única aplicação em contêiner), a arquitetura lógica prevê a separação de responsabilidades que podem ser, no futuro, escaladas em processos independentes ou microsserviços.

* **Processos Leves (Threads):** Dentro de cada módulo de aplicação (e.g., `ModuloEducacional`, `ModuloForum`), as operações serão executadas em **threads** para lidar com requisições concorrentes de usuários. Por exemplo, múltiplas requisições de "iniciar trilha" ou "postar no fórum" serão tratadas em threads separadas pelo servidor de aplicação.
* **Processos Pesados (Serviços/Contêineres):** O sistema pode ser implantado como um conjunto de contêineres Docker, onde cada um representa um serviço principal.
    * **Processo Principal da Aplicação Web:** Engloba a `APIGateway`, `GestaoUsuarios`, `ModuloEducacional`, `ModuloDivulgacao`, `ModuloJogos`, `ModuloForum`, etc. Este será o maior processo, coordenando as operações do backend.
    * **Processo de Bots de Integração:** `BotImportadorNoticias` e `BotImportadorPromocoes` podem rodar como processos (ou jobs) agendados, independentes do ciclo de requisição HTTP principal, buscando dados em segundo plano.
    * **Processo de Banco de Dados:** O SGBD (PostgreSQL/MySQL) opera como um processo pesado separado, gerenciando a persistência dos dados.
* **Modos de Comunicação:**
    * **HTTP/HTTPS (API REST):** A comunicação primária entre a `WebUI` e a `APIGateway` (frontend-backend) e entre os módulos de backend (se forem microsserviços no futuro).
    * **Chamadas a Métodos Internos (In-Process):** Comunicação entre os módulos dentro do mesmo processo principal do backend (e.g., `ModuloEducacional` chamando `ModuloGamificacao`).
    * **Acesso a Banco de Dados (SQL/ORM):** Comunicação entre os módulos de aplicação e o `BancoDeDados` para operações de persistência.
    * **Filas de Mensagens (Opcional Futuro):** Para operações assíncronas (ex: envio de notificações em massa, processamento de dados importados por bots sem bloquear a requisição HTTP), pode-se considerar a introdução de um *broker* de mensagens (ex: RabbitMQ, Kafka) para desacoplar produtores e consumidores de eventos, conforme representado no Diagrama de Pacotes (`Infraestrutura.Mensageria`).

A orquestração desses processos é exemplificada em seus **Diagramas de Atividades** (mostrando a sequência de ações) e **Diagramas de Comunicação** (focando na troca de mensagens entre objetos em cenários específicos). Para uma visão mais detalhada dos fluxos, consulte [Diagrama de Atividades](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaAtividades) e [Diagrama de Comunicação](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemDinamica/DiagramaComunica%C3%A7%C3%A3o).

---

### 10. Visão de Implantação

Esta seção descreve a configuração física da infraestrutura de hardware e software sobre a qual o sistema Galáxia Conectada será implantado e executado.

Para uma representação visual detalhada dos nós físicos e o mapeamento dos componentes, consulte o **Diagrama de Implantação** completo do projeto, disponível em [Diagrama de Implantação](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaImplantacao).

**Nós Físicos e Configurações:**

* **Dispositivo do Usuário (`<<device>> Navegador Web`):**
    * **Descrição:** O hardware (desktop, laptop, smartphone, tablet) onde o usuário acessa a plataforma.
    * **Ambiente de Execução:** Qualquer navegador web moderno (Chrome, Firefox, Edge, Safari).
    * **Artefatos Implantados:** O Frontend da aplicação (`WebUI`), que consiste em arquivos HTML, CSS, JavaScript carregados via HTTP/HTTPS.
    * **Conexões:** Comunica-se com o `Servidor Web` via **HTTPS**.
* **Servidor Web (`<<server>> Servidor Web`):**
    * **Descrição:** Servidor que atua como ponto de entrada para todas as requisições HTTP/HTTPS, servindo os arquivos estáticos do frontend e atuando como um proxy reverso para o servidor de aplicação.
    * **Ambiente de Execução:** Sistema Operacional Linux (Ubuntu/CentOS), com Nginx ou Apache configurado como servidor web/proxy reverso. Pode ser um contêiner Docker dedicado.
    * **Artefatos Implantados:** Arquivos estáticos da `WebUI` (`static-files/`, `generated-seo-files/`), configuração do servidor web.
    * **Conexões:** Recebe requisições do `Navegador Web` (HTTPS). Encaminha requisições de API para o `Firewall` via TCP/IP.
* **Firewall (`<<firewall>> Firewall`):**
    * **Descrição:** Dispositivo ou software de rede que controla o tráfego de entrada e saída, protegendo a rede interna e filtrando acessos.
    * **Ambiente de Execução:** Firewall de rede ou software de firewall (ex: `iptables`, `firewalld`).
    * **Conexões:** Recebe tráfego do `Servidor Web` e o direciona aos `Servidores de Aplicação` e `Sistema Gerenciador de Banco de Dados` via TCP/IP.
* **Servidor de Aplicação (`<<server>> Servidor de Aplicação`):**
    * **Descrição:** Servidor(es) onde a lógica de backend da aplicação Galáxia Conectada é executada. Pode ser escalado para múltiplos nós para maior disponibilidade e performance. No diagrama, estão separados em "Serviços" e "Jogos" para ilustração de responsabilidades, mas podem coexistir no mesmo servidor ou contêiner.
    * **Ambiente de Execução:** Sistema Operacional Linux, com um ambiente de execução Java (JRE/JVM) para aplicações Java baseadas em *frameworks* como Spring Boot, ou um *runtime* Python para Flask/Django, rodando em contêineres Docker.
    * **Artefatos Implantados:** `astronomia.war` (arquivo executável do backend), `web-tools-lib.jar` (bibliotecas), `web.xml` (especificação de *deploy*), e os componentes lógicos do backend (`APIGateway`, `GestaoUsuarios`, `ModuloEducacional`, etc.).
    * **Conexões:** Recebe requisições do `Firewall` (TCP/IP). Conecta-se ao `Sistema Gerenciador de Banco de Dados` (TCP/IP). Pode se comunicar com `Serviços Externos` (HTTPS).
* **Sistema Gerenciador de Banco de Dados (`<<database>> SGBD`):**
    * **Descrição:** Servidor dedicado ao banco de dados relacional que armazena todos os dados persistentes do sistema.
    * **Ambiente de Execução:** Sistema Operacional Linux, com PostgreSQL ou MySQL.
    * **Artefatos Implantados:** O `schema.sql` (estrutura do banco de dados), e os dados do sistema (`Usuario`, `Serviços`, `Jogos`, `Artigos`, etc.).
    * **Conexões:** Recebe conexões dos `Servidores de Aplicação` (TCP/IP) através do `Firewall`.
* **Serviços Externos (`<<system>> APIs/Sites Externos`):**
    * **Descrição:** Sistemas de terceiros (como APIs da NASA, sites de *e-commerce*, serviços de *e-mail*/push notification) que o Galáxia Conectada consome ou integra.
    * **Ambiente de Execução:** Nuvem ou servidores de terceiros.
    * **Conexões:** A comunicação se dá via HTTPS/API com os `Servidores de Aplicação`.

O mapeamento dos processos da Visão de Processo para os nós físicos é direto: os processos da aplicação (API, módulos) são executados nos `Servidores de Aplicação`, enquanto os bots de integração podem ser agendados como *jobs* nesses mesmos servidores ou em um ambiente de *serverless functions*. O `Banco de Dados` é um nó separado para persistência.

---

### 11. Visão de Implementação

#### 11.1 Visão Geral

A **Visão de Implementação** descreve a estrutura geral do modelo de implementação, focando na organização do código-fonte e nos componentes físicos que constituem o sistema Galáxia Conectada. Ela detalha como o software é dividido em camadas e subsistemas implementados, e quais componentes arquiteturalmente significativos residem em cada um. A separação em camadas visa garantir a **coesão e o baixo acoplamento**, facilitando o desenvolvimento paralelo e a manutenção.

A organização da implementação reflete a arquitetura em camadas definida na Visão Lógica, com diretórios e pacotes de código correspondentes.

Para uma representação visual clara das relações entre os componentes, consulte o **Diagrama de Componentes** do projeto, disponível em [Diagrama de Componentes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaComponentes).

**Definição das Camadas e Regras de Inclusão:**

* **Camada de Apresentação (Frontend):**
    * **Conteúdo:** Contém todo o código relacionado à interface do usuário (UI), como *templates* HTML, folhas de estilo CSS, *scripts* JavaScript, e *frameworks* de *frontend* (ex: React, Vue.js, Angular ou *vanilla* JS).
    * **Regras:** Componentes desta camada só podem depender da camada de `GatewayAPI` (Backend) e de bibliotecas de *frontend*. Não devem conter lógica de negócio complexa ou acesso direto a banco de dados.
    * **Limites:** Comunicação estritamente via APIs RESTful com o backend.
* **Camada de Aplicação (Backend Core):**
    * **Conteúdo:** Abriga a lógica de negócio principal da aplicação, orquestrando as operações que implementam os casos de uso. Inclui *controllers*/endpoints da API, *services* e *managers*.
    * **Regras:** Pode depender da camada de `Domínio` (para entidades e regras de negócio), `Serviços Compartilhados` e `Infraestrutura` (para persistência e clientes externos). Não deve acessar diretamente o UI.
    * **Limites:** É a camada que coordena as interações entre as outras.
* **Camada de Domínio (Modelo de Negócio):**
    * **Conteúdo:** Classes que representam as entidades do negócio (ex: `Usuario`, `TrilhaEducacional`, `Topico`), objetos de valor, regras de negócio e interfaces de repositórios (contratos para acesso a dados).
    * **Regras:** Não deve ter dependências de camadas superiores (Apresentação, Aplicação) nem de detalhes de implementação específicos de `Infraestrutura`. Deve ser a camada mais estável e independente.
    * **Limites:** Depende apenas de bibliotecas básicas e, ocasionalmente, de um pacote de `Compartilhados` dentro do próprio domínio.
* **Camada de Serviços Compartilhados/Transversais:**
    * **Conteúdo:** Serviços que fornecem funcionalidades reutilizáveis e genéricas, como notificações, busca, *cache*, monitoramento e configurações.
    * **Regras:** Pode depender da `Infraestrutura` (para implementar o serviço, ex: cliente de *e-mail*) e de `Configuração`. É acessada por outras camadas (Apresentação, Aplicação).
    * **Limites:** Deve ser projetada para ser o mais agnóstica possível ao domínio específico e ser de fácil reutilização.
* **Camada de Infraestrutura:**
    * **Conteúdo:** Implementações concretas de interfaces de persistência (repositórios de banco de dados), clientes para APIs externas, adaptadores para sistemas de *cache*, e outras bibliotecas de baixo nível.
    * **Regras:** Pode depender de *frameworks* de banco de dados (ORM), bibliotecas HTTP, *drivers*, etc. Não deve conter lógica de negócio diretamente.
    * **Limites:** Depende de tecnologias específicas e é usada pelas camadas superiores para realizar operações técnicas.

#### 11.2 Camadas

A estrutura de camadas de implementação do Galáxia Conectada segue o modelo de camadas, com uma clara separação de responsabilidades. Os principais subsistemas e componentes lógicos são mapeados para essas camadas.

* **Camada de Apresentação:**
    * **Subsistemas/Componentes:** `WebUI` (Frontend).
    * **Diagrama de Componentes:** Mostra a `WebUI` e suas dependências de APIs de backend.
* **Camada de Aplicação:**
    * **Subsistemas/Componentes:** `Subsistema Conteudo Interativo` (com `ModuloEducacional`, `ModuloDivulgacao`, `ModuloJogos`, `ModuloRecursosPraticos`), `Subsistema Comunidade` (com `ModuloForum`, `ModuloGamificacao`, `ModuloModeracao`), `Subsistema Integrações` (com `ModuloEventos`, `ModuloPromocoes`).
    * **Diagrama de Componentes:** Ilustra os módulos e subsistemas de backend e suas interações internas e externas.
* **Camada de Domínio:**
    * **Subsistemas/Componentes:** Conceitualmente, corresponde aos pacotes de `Dominio` (`Dominio.Usuario`, `Dominio.Aprendizagem`, `Dominio.Comunidade`, `Dominio.ConteudoInfo`, `Dominio.Compartilhado`).
    * **Diagrama de Classes:** Detalha as classes e seus atributos/métodos que residem nesta camada, e seus relacionamentos.
* **Camada de Serviços Compartilhados:**
    * **Subsistemas/Componentes:** `ServicoNotificacoes`, `ServicoBusca`, `ServicoRecomendacoes`, `ServicoCertificados`, `ServicoLocalizacao`, `ServicoConfiguracao`, `ServicoMonitoramento`, `ServicoCache`.
    * **Diagrama de Componentes:** Mostra esses serviços como componentes separados e suas dependências.
* **Camada de Infraestrutura:**
    * **Subsistemas/Componentes:** `BancoDeDados`, `BotImportadorNoticias`, `BotImportadorPromocoes`, `GestorAssetsEstaticos`, `ServicoCache` (implementação).
    * **Diagrama de Componentes:** Apresenta esses componentes de infraestrutura e suas dependências de artefatos e serviços externos.

---

### 12. Visão de Dados (Opcional)

A **Visão de Dados** descreve a persistência das informações dentro do sistema Galáxia Conectada. Considerando a importância dos dados para o funcionamento de todas as funcionalidades (perfis de usuário, trilhas, jogos, *posts* de fórum, notícias, etc.), esta seção é fundamental.

A persistência de dados será implementada utilizando um **Banco de Dados Relacional** (como PostgreSQL ou MySQL). O modelo de dados reflete diretamente as classes significativas identificadas na [Diagrama de Classes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaClasses) do sistema.

As principais entidades persistidas e seus relacionamentos incluem:

* **Usuários:** Armazena informações de login, perfis (nível, XP, avatar, bio), e reputação.
    * *Tabelas:* `Usuarios`, `Perfis`, `Reputacoes`.
* **Trilhas de Aprendizado:** Dados sobre as trilhas, seus módulos, conteúdos (artigos, vídeos, quizzes, jogos).
    * *Tabelas:* `Trilhas`, `Modulos`, `Conteudos` (tabela polimórfica ou tabelas separadas para `Artigos`, `Videos`, `Quizzes`, `Jogos`), `PerguntasQuiz`, `OpcoesResposta`.
* **Progresso do Usuário:** Rastreia o avanço de cada usuário em cada trilha e módulo.
    * *Tabelas:* `ProgressoUsuarioTrilha`, `ConclusoesModulo`.
* **Comunidade (Fórum):** Armazena dados de subfóruns, tópicos, postagens e comentários.
    * *Tabelas:* `Subforums`, `Topicos`, `Postagens`, `Comentarios`.
* **Gamificação:** Informações sobre conquistas e o relacionamento entre usuários e conquistas.
    * *Tabelas:* `Conquistas`, `UsuarioConquistas`.
* **Conteúdo Informativo (Notícias/Eventos/Promoções):** Armazena artigos de blog, notícias importadas, eventos astronômicos e promoções externas.
    * *Tabelas:* `Noticias`, `FontesNoticias`, `EventosAstronomicos`, `PromocoesExternas`, `FontesPromocoesExternas`.

**Mapeamento entre o Modelo Lógico (Classes) e o Modelo Físico (Tabelas):**

O mapeamento será feito utilizando um **Object-Relational Mapper (ORM)**, que abstrai a complexidade do banco de dados e permite que os desenvolvedores trabalhem com objetos de domínio (classes) diretamente no código, enquanto o ORM cuida da conversão para operações SQL e persistência em tabelas.

Um **Diagrama de Entidade-Relacionamento (DER)** mais detalhado pode ser desenvolvido em uma fase posterior para especificar as chaves primárias, chaves estrangeiras, tipos de dados e cardinalidades exatas de cada tabela, mas o [Diagrama de Classes](https://unbarqdsw2025-1-turma02.github.io/2025.1_T02_G9_GalaxiaConectada_Entre02/#/Modelagem/ModelagemEstatica/DiagramaClasses) já serve como uma base robusta para o entendimento da estrutura de dados.

---

### 13. Tamanho e Performance

Esta seção descreve as principais características de dimensionamento do software que impactam a arquitetura, bem como as restrições de desempenho almejadas para o sistema Galáxia Conectada.

**Características de Dimensionamento:**

* **Número de Usuários Concorrentes:** Inicialmente, o sistema deve suportar dezenas a poucas centenas de usuários ativos simultaneamente. A arquitetura em camadas e a modularidade visam permitir o escalonamento horizontal para milhares ou mais, se o projeto crescer (**RNF07**).
* **Volume de Conteúdo:**
    * **Trilhas de Aprendizado:** Estimativa inicial de 5-10 trilhas completas, cada uma com 5-15 módulos, e 3-10 conteúdos por módulo. O volume pode crescer significativamente com o tempo.
    * **Notícias/Artigos:** Potencialmente centenas a milhares de artigos/notícias, com atualizações diárias por *bots*.
    * **Fórum:** Milhares de tópicos e dezenas de milhares de postagens/comentários esperados com o aumento do engajamento.
* **Dados de Usuário:** Armazenamento de perfis, progresso em trilhas, histórico de jogos e interações no fórum para cada usuário.
* **Integrações:** Frequência de importação de dados de APIs/sites externos (ex: notícias a cada hora, promoções a cada 6-24 horas).

**Restrições de Performance (RNF02):**

* **Tempo de Resposta da UI:**
    * Carregamento inicial da página: idealmente **< 3 segundos**.
    * Navegação entre páginas e carregamento de listas (trilhas, notícias): idealmente **< 2 segundos**.
    * Interações em jogos/quizzes (feedback instantâneo): idealmente **< 500 ms**.
* **Processamento de Requisições de API:**
    * Requisições de leitura (ex: obter conteúdo de uma trilha): idealmente **< 500 ms**.
    * Requisições de escrita (ex: postar no fórum, marcar módulo concluído): idealmente **< 1 segundo**.
* **Processamento de Background (Bots):**
    * *Bots* de importação de notícias/promoções: Devem completar seus ciclos dentro de **minutos** (dependendo da frequência configurada) e não impactar a performance do *frontend*.
* **Consumo de Recursos:**
    * A aplicação deve ser otimizada para um uso eficiente de CPU, memória e largura de banda, especialmente para garantir que o sistema possa rodar em ambientes de hospedagem com recursos limitados, mantendo um bom desempenho.

Para mitigar riscos relacionados a desempenho e dimensionamento ([Estimativas: Plano de Risco - R10, R13](https://unbarqdsw2025-1-turma02.github.io/2025.1-T02-_G9_GalaxiaConectada_Entre01/#/Base/ArtefatoGeneralista/Estimativas)), a arquitetura utiliza:
* **Camadas:** Para facilitar a otimização de componentes isolados.
* **Mecanismos de Cache (`ServicoCache`):** Para acelerar o acesso a dados frequentemente solicitados.
* **Indexação de Conteúdo (`ServicoBusca`):** Para pesquisas rápidas.
* **Processos Assíncronos:** Para tarefas que não precisam de resposta imediata (ex: notificações, algumas operações dos *bots*).

---

### 14. Qualidade

Esta seção detalha como a arquitetura de software do Galáxia Conectada contribui para as diversas qualidades (não funcionais) do sistema, essenciais para sua usabilidade, confiabilidade e longevidade.

* **Extensibilidade (RNF08):**
    * **Modularidade:** A divisão clara em módulos lógicos (`ModuloEducacional`, `ModuloForum`, etc.) e pacotes (Visão Lógica - Diagrama de Pacotes) permite a adição de novas funcionalidades ou módulos sem impactar significativamente outras partes do sistema.
    * **Interfaces Bem Definidas:** A comunicação entre componentes via interfaces (Diagrama de Componentes) garante baixo acoplamento, facilitando a substituição ou extensão de módulos.
    * **Padrões de Projeto:** O uso de padrões como Repositório (implícito na `Infraestrutura.Persistencia`) e Camadas (Visão Lógica) promove um código organizado e mais fácil de estender.
* **Confiabilidade (RNF04):**
    * **Tolerância a Falhas:** A separação de componentes (Diagrama de Componentes) e a potencial implantação em diferentes servidores (Diagrama de Implantação) podem, em um futuro escalonamento, isolar falhas de um módulo, evitando que afetem todo o sistema.
    * **Monitoramento (RNF05):** O `ServicoMonitoramento` registra *logs* e métricas, permitindo a detecção precoce de anomalias e falhas.
    * **Backups:** A dependência de um `BancoDeDados` centralizado facilita a implementação de estratégias de *backup* para recuperação de dados.
* **Portabilidade:**
    * **Tecnologias Cross-Platform:** O uso de tecnologias *web* padrão (HTML, CSS, JavaScript) e linguagens/*frameworks* populares (ex: Python/Flask ou Java/Spring Boot) facilita a execução do sistema em diferentes sistemas operacionais.
    * **Contêineres (Futuro):** A adoção de contêineres Docker (Visão de Implantação) garantirá que a aplicação e suas dependências sejam empacotadas de forma consistente, tornando-a portátil entre diferentes ambientes de servidor.
* **Segurança (RNF03):**
    * **Camada de Autenticação/Autorização:** O `GerenciamentoUsuarios` (`GestaoUsuarios`) centraliza a lógica de segurança, controlando o acesso a funcionalidades com base em papéis e permissões.
    * **Validação de Entrada:** A arquitetura em camadas permite que as validações de dados (tanto no *frontend* quanto no *backend*) sejam aplicadas consistentemente para prevenir ataques como injeção de SQL ou XSS.
    * **Proteção de Rede:** O `Firewall` (Diagrama de Implantação) na camada de rede protege o *backend* contra acessos não autorizados.
* **Acessibilidade (RNF05, RNF06):**
    * **Design Responsivo (RNF01):** A `WebUI` será desenvolvida com design responsivo, garantindo que o conteúdo seja acessível em diferentes dispositivos.
    * **Padronização de Interface:** A interface intuitiva e a linguagem clara (RNF06) são priorizadas para reduzir a sobrecarga cognitiva, beneficiando usuários neurodivergentes.
    * **Suporte a Localização (RNF07):** O `ServicoLocalizacao` permite que o conteúdo e a interface sejam adaptados a diferentes idiomas e, futuramente, a formatos que podem auxiliar a acessibilidade.
    * **Considerações de Contraste/Fontes:** A arquitetura não impede a implementação de diretrizes de acessibilidade visual (ex: contraste adequado, fontes legíveis), que seriam aplicadas na camada de `Apresentacao`.
* **Manutenibilidade:**
    * **Coerência de Design:** A aderência a padrões arquiteturais (camadas, módulos) e a documentação clara (Diagramas de Pacotes, Classes, Componentes) facilitam a compreensão do sistema por novos desenvolvedores.
    * **Separação de Preocupações:** Cada camada e módulo tem responsabilidades bem definidas, isolando alterações e simplificando a depuração e o desenvolvimento de novas funcionalidades.
* **Usabilidade (RNF06):**
    * A clareza da **Visão de Casos de Uso** e o foco no usuário durante o *Design Sprint* (prototipagem) se traduzem em uma arquitetura que suporta a criação de uma experiência de usuário intuitiva e agradável.
