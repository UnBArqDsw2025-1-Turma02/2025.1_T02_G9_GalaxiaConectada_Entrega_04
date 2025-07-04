document.addEventListener('DOMContentLoaded', () => {
    // Carrossel de Notícias
    const newsCarousel = document.querySelector('.news-carousel');
    const newsPrevBtn = document.querySelector('.news-prev-btn');
    const newsNextBtn = document.querySelector('.news-next-btn');
    const scrollAmountNews = 270; // Largura de um item + gap

    if (newsCarousel && newsPrevBtn && newsNextBtn) {
        newsNextBtn.addEventListener('click', () => {
            newsCarousel.scrollBy({
                left: scrollAmountNews,
                behavior: 'smooth'
            });
        });

        newsPrevBtn.addEventListener('click', () => {
            newsCarousel.scrollBy({
                left: -scrollAmountNews,
                behavior: 'smooth'
            });
        });
    }

    // Carrossel de Trilhas
    const trailsCarousel = document.querySelector('.trails-carousel');
    const trailsPrevBtn = document.querySelector('.trails-prev-btn');
    const trailsNextBtn = document.querySelector('.trails-next-btn');
    const scrollAmountTrails = 270; // Largura de um item + gap (mesmo valor, ajuste se cards forem diferentes)

    if (trailsCarousel && trailsPrevBtn && trailsNextBtn) {
        trailsNextBtn.addEventListener('click', () => {
            trailsCarousel.scrollBy({
                left: scrollAmountTrails,
                behavior: 'smooth'
            });
        });

        trailsPrevBtn.addEventListener('click', () => {
            trailsCarousel.scrollBy({
                left: -scrollAmountTrails,
                behavior: 'smooth'
            });
        });
    }

    // Lógica para Acessibilidade e Inclusão (toggle de opções)
    const accessibilityLink = document.querySelector('.accessibility-link');
    const accessibilityOptions = document.querySelector('.accessibility-options');

    if (accessibilityLink && accessibilityOptions) {
        console.log('Botão de acessibilidade e opções encontrados.');

        accessibilityLink.addEventListener('click', (e) => {
            e.preventDefault();
            accessibilityOptions.classList.toggle('show-options'); 
            console.log('Classe show-options toggled. Current state:', accessibilityOptions.classList.contains('show-options'));
        });

        // Funcionalidade: Mudar fonte para dislexia
        const fontIcon = accessibilityOptions.querySelector('.fa-font');
        if (fontIcon) {
            console.log('Ícone de fonte para dislexia encontrado.');
            fontIcon.addEventListener('click', () => {
                document.documentElement.classList.toggle('dyslexic-font');
                fontIcon.classList.toggle('active-accessibility-option'); 
                console.log('Classe dyslexic-font toggled on HTML. Current state:', document.documentElement.classList.contains('dyslexic-font'));
            });
        }
        // Exemplo: ajustar tamanho da fonte (muito básico)
        const fontSizeIcon = accessibilityOptions.querySelector('.fa-text-height');
        if (fontSizeIcon) {
            console.log('Ícone de tamanho de fonte encontrado.');
            fontSizeIcon.addEventListener('click', () => {
                const htmlElement = document.documentElement;
                let currentFontSize = parseFloat(getComputedStyle(htmlElement).fontSize);

                if (htmlElement.classList.contains('large-font')) {
                    htmlElement.style.fontSize = '100%';
                    htmlElement.classList.remove('large-font');
                } else {
                    htmlElement.style.fontSize = '115%';
                    htmlElement.classList.add('large-font');
                }
                console.log('Tamanho da fonte ajustado. Novo tamanho:', htmlElement.style.fontSize);
            });
        }
    } else {
        console.warn('Elementos de acessibilidade ou opções não encontrados. Verifique seletores HTML/JS.');
    }

    // Lógica para os botões de "Ver Perfil" e "Excluir" no painel do administrador (se existir na página)
    document.querySelectorAll('.view-profile-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const userId = e.currentTarget.dataset.userId;
            alert(`Funcionalidade "Ver Perfil" para o usuário ID: ${userId} será implementada.`);
            // Futuramente: redirecionar para uma página de detalhes do perfil do usuário
        });
    });

    document.querySelectorAll('.delete-user-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const userId = e.currentTarget.dataset.userId;
            if (confirm(`Tem certeza que deseja excluir o usuário ID: ${userId}? Esta ação é irreversível!`)) {
                alert(`Funcionalidade "Excluir Usuário" para o usuário ID: ${userId} será implementada.`);
                // Futuramente: enviar requisição DELETE para o backend
            }
        });
    });

    // Lógica para o pet do aluno (se existir na página)
    const petSection = document.querySelector('.pet-section');
    if (petSection) {
        console.log('Seção do pet encontrada.');
        // Adicione aqui qualquer lógica JS específica para o pet, como animações ou interações
        // Por exemplo, um clique no pet pode fazer algo
        const petAvatar = petSection.querySelector('.pet-avatar');
        if (petAvatar) {
            petAvatar.addEventListener('click', () => {
                console.log('Pet clicado!');
                // Exemplo de efeito visual ao clicar no pet
                petAvatar.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    petAvatar.style.transform = 'scale(1)';
                }, 200);
            });
        }
    }

    // Lógica para marcar notificações como lidas (se existir na página de notificações)
    document.querySelectorAll('.mark-read-btn').forEach(button => {
        button.addEventListener('click', async (e) => {
            const notificationItem = e.target.closest('.notification-item');
            const notificationId = notificationItem.dataset.notificationId;

            try {
                const response = await fetch(`/notifications/mark_read/${notificationId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();
                if (data.status === 'success') {
                    notificationItem.classList.remove('unread');
                    e.target.remove(); // Remove o botão "Marcar como Lida"
                    // Opcional: Atualizar a contagem de notificações no sino
                    const notificationCountSpan = document.querySelector('.notification-count');
                    if (notificationCountSpan) {
                        let currentCount = parseInt(notificationCountSpan.innerText);
                        if (currentCount > 0) {
                            currentCount--;
                            notificationCountSpan.innerText = currentCount;
                            if (currentCount === 0) {
                                notificationCountSpan.style.display = 'none';
                            }
                        }
                    }
                } else {
                    alert('Erro ao marcar notificação como lida.');
                }
            } catch (error) {
                console.error('Erro ao marcar notificação como lida:', error);
                alert('Erro de rede ao marcar notificação como lida.');
            }
        });
    });

    // Lógica para o botão de Compartilhar (se existir na página de detalhes do conteúdo)
    const shareBtn = document.querySelector('.share-btn');
    if (shareBtn) {
        shareBtn.addEventListener('click', () => {
            const contentTitle = document.querySelector('.content-title').innerText;
            const contentUrl = window.location.href;
            if (navigator.share) {
                navigator.share({
                    title: contentTitle,
                    url: contentUrl
                }).then(() => {
                    console.log('Conteúdo compartilhado com sucesso!');
                }).catch((error) => {
                    console.error('Erro ao compartilhar:', error);
                });
            } else {
                // Fallback para navegadores que não suportam a API Web Share
                prompt("Copie o link para compartilhar:", contentUrl);
            }
        });
    }
});
