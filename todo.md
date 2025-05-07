## Plano de Desenvolvimento: Projeto Web de Monitoramento de Sono com Django

**Objetivo:** Criar uma aplicação web Django que utiliza a câmera do dispositivo para monitorar sonolência, baseando-se em um código Python fornecido.

**Fases e Tarefas:**

1.  **[X] Análise do Código Fornecido (pasted_content.txt)**
    *   [X] Identificar bibliotecas e dependências (OpenCV, dlib, playsound, numpy).
    *   [X] Entender a lógica de detecção de sonolência (EAR, contagem de frames).
    *   [X] Identificar arquivos externos necessários (shape_predictor_68_face_landmarks.dat, alarme.wav).

2.  **[X] Definição da Estrutura do Projeto Django e Funcionalidades da Webcam**
    *   [X] Criar um novo projeto Django.
    *   [X] Criar um app Django dedicado (ex: `sleep_monitor`).
    *   [X] Configurar URLs básicas (página inicial, endpoint para processamento de vídeo).
    *   [X] Definir views iniciais (view para a página principal, view para receber frames da câmera).
    *   [X] Planejar o fluxo de dados: captura de frames no frontend (JS) -> envio para o backend (Django) -> processamento (Python/OpenCV/dlib) -> envio de resultado/alerta para o frontend.
    *   [X] Decidir como gerenciar os arquivos `shape_predictor_68_face_landmarks.dat` e `alarme.wav` (provavelmente na pasta `static` ou `media` do app).
    *   [ ] Listar dependências Python para o `requirements.txt` (Django, opencv-python, dlib, numpy, playsound).

3.  **[X] Implementação da Interface Web (Frontend)**
    *   [X] Criar template HTML básico (`index.html`).
    *   [X] Adicionar um elemento de vídeo para exibir o feed da câmera.
    *   [X] Adicionar um botão "Iniciar Monitoramento".
    *   [X] Adicionar uma área para exibir o status ou alertas.
    *   [X] Implementar JavaScript para:
        *   [X] Solicitar permissão e acessar a câmera do usuário (getUserMedia API).
        *   [X] Exibir o feed da câmera no elemento de vídeo.
        *   [X] Ao clicar em "Iniciar Monitoramento", começar a capturar frames.
        *   [X] Enviar frames para o backend (ex: via Fetch API com POST para um endpoint Django, ou WebSockets).
        *   [X] Receber e processar respostas do backend (ex: exibir alerta de sono, tocar som no frontend).

4.  **[X] Integração do Código de Monitoramento com Acesso à Câmera (Backend)**
    *   [X] Adaptar o código Python fornecido para funcionar dentro de uma view Django.
    *   [X] A view deverá receber um frame (imagem) do frontend.
    *   [X] Realizar o processamento do frame (detecção de face, marcos faciais, cálculo do EAR).
    *   [X] Manter o estado do contador de sonolência (COUNTER_EYES_CLOSED) entre as requisições (talvez na sessão do usuário ou em uma estrutura de dados no servidor associada à sessão/usuário).
    *   [X] Retornar uma resposta para o frontend (ex: JSON indicando se um alerta deve ser disparado).
    *   [X] Implementar a lógica para tocar o som de alarme. (Considerar se o som será tocado no backend com `playsound` ou se o backend apenas sinalizará o frontend para tocar o som).

5.  **[X] Garantir Compatibilidade e Instalação de Dependências**
    *   [X] Criar `requirements.txt` com todas as dependências Python.
    *   [X] Fornecer instruções para instalação do `dlib` (que pode ser complexa, envolvendo compilação ou pré-requisitos como CMake e Boost).
    *   [X] Baixar e disponibilizar o arquivo `shape_predictor_68_face_landmarks.dat`.
    *   [X] Criar ou obter um arquivo `alarme.wav`.
    *   [X] Testar em diferentes navegadores (para a parte de acesso à câmera via JS).

6.  **[X] Testes e Validação**
    *   [X] Testar a funcionalidade de acesso à câmera.
    *   [X] Testar o envio de frames para o backend.
    *   [X] Testar o processamento de sonolência no backend.
    *   [X] Testar o disparo do alerta (visual e sonoro).
    *   [X] Testar a parada do monitoramento.

7.  **[X] Empacotamento e Entrega do Projeto**
    *   [X] Organizar a estrutura de arquivos do projeto.
    *   [X] Fornecer um README.md com instruções de configuração, instalação de dependências e execução do projeto.
    *   [X] Compactar o projeto em um arquivo .zip para entrega.

**Considerações Adicionais:**
*   **Performance:** O envio contínuo de frames para o backend pode ser intensivo em termos de rede e processamento. Avaliar a frequência de envio de frames ou técnicas de streaming.
*   **Segurança/Privacidade:** Informar claramente o usuário sobre o uso da câmera.
*   **Estado entre Requisições:** Como o HTTP é stateless, o estado do `COUNTER_EYES_CLOSED` e outros estados de monitoramento precisarão ser gerenciados (ex: sessão Django, cache, ou uma solução mais robusta se múltiplos usuários/sessões concorrentes forem um requisito).
*   **Abertura automática da guia:** Pode ser feito com a biblioteca `webbrowser` do Python no `manage.py` ou em um script de inicialização, mas isso é mais para conveniência de desenvolvimento local.

