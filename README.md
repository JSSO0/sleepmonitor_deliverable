# Projeto de Monitoramento de Sono com Django

Este projeto é uma aplicação web desenvolvida em Django que utiliza a câmera do dispositivo para monitorar sinais de sonolência em tempo real.

## Funcionalidades

- Acesso à webcam do usuário através do navegador.
- Captura de frames de vídeo para análise.
- Detecção de rosto e marcos faciais utilizando dlib.
- Cálculo do "Eye Aspect Ratio" (EAR) para determinar se os olhos estão fechados.
- Alerta sonoro e visual caso o sistema detecte sonolência por um período configurado.
- Interface web simples com botão para iniciar/parar o monitoramento e visualização do feed da câmera e status.

## Estrutura do Projeto

```
/home/ubuntu/
├── sleepmonitor_project/      # Diretório principal do projeto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sleep_monitor/             # App Django para o monitoramento
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py
│   ├── static/
│   │   └── sleep_monitor/
│   │       ├── js/
│   │       │   └── main.js         # Lógica do frontend
│   │       ├── shape_predictor_68_face_landmarks.dat # Modelo dlib
│   │       └── alarme.wav          # Som de alerta
│   ├── templates/
│   │   └── sleep_monitor/
│   │       └── index.html      # Página principal
│   ├── tests.py
│   ├── urls.py
│   └── views.py              # Lógica do backend
├── manage.py                  # Utilitário de gerenciamento do Django
├── requirements.txt           # Dependências Python
└── todo.md                    # Checklist de desenvolvimento (para referência)
```

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Um navegador web moderno com suporte a `getUserMedia` (para acesso à câmera)
- Para a instalação da biblioteca `dlib`, pode ser necessário instalar dependências de compilação no seu sistema operacional. Consulte a documentação oficial do `dlib` para mais detalhes específicos do seu SO (geralmente envolve CMake e um compilador C++):
    - Linux: `sudo apt-get install build-essential cmake`
    - macOS: `brew install cmake`

## Configuração e Instalação

1.  **Clone ou baixe o projeto:**
    Descompacte o arquivo .zip fornecido em um diretório de sua escolha.

2.  **Crie e ative um ambiente virtual (recomendado):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate    # Windows
    ```

3.  **Instale as dependências Python:**
    Navegue até o diretório raiz do projeto (onde `requirements.txt` está localizado) e execute:
    ```bash
    pip install -r requirements.txt
    ```
    *Nota:* A instalação do `dlib` pode demorar um pouco, pois pode envolver compilação.

4.  **Verifique os arquivos estáticos:**
    Certifique-se de que os arquivos `shape_predictor_68_face_landmarks.dat` e `alarme.wav` estão presentes no diretório `/home/ubuntu/sleep_monitor/static/sleep_monitor/`. Se você moveu o projeto, ajuste os caminhos ou certifique-se de que eles estão na estrutura correta conforme `sleep_monitor/static/sleep_monitor/` dentro do seu diretório do projeto.

5.  **Execute as migrações do Django (necessário para a funcionalidade de sessão):**
    ```bash
    python manage.py migrate
    ```

6.  **Inicie o servidor de desenvolvimento Django:**
    ```bash
    python manage.py runserver
    ```
    Por padrão, o servidor estará acessível em `http://127.0.0.1:8000/` ou `http://localhost:8000/`.

7.  **Acesse a aplicação:**
    Abra seu navegador e vá para `http://127.0.0.1:8000/sleep_monitor/` ou o endereço raiz `http://127.0.0.1:8000/`.

## Utilização

1.  Ao abrir a página, seu navegador deverá solicitar permissão para usar a câmera. Conceda a permissão.
2.  O feed da câmera será exibido na tela.
3.  Clique no botão "Iniciar Monitoramento".
4.  O sistema começará a analisar os frames da câmera. O status será exibido abaixo do vídeo.
5.  Se o sistema detectar que seus olhos permaneceram fechados por um tempo limite, um alerta "ALERTA DE SONO!" será exibido e um som de alarme será tocado (se o arquivo `alarme.wav` estiver configurado e o navegador permitir a reprodução automática de áudio).
6.  Clique em "Parar Monitoramento" para interromper o processo.

## Observações

- **Abertura automática da guia:** O pedido original incluía abrir uma guia do navegador automaticamente. Isso pode ser implementado adicionando `import webbrowser; webbrowser.open('http://127.0.0.1:8000/sleep_monitor/')` ao final do `manage.py` (após as verificações de execução do servidor) ou em um script de inicialização separado. No entanto, isso é mais uma conveniência para desenvolvimento local e não foi incluído por padrão no `manage.py` para manter o comportamento padrão do Django.
- **Performance:** O processamento de vídeo em tempo real pode ser intensivo. A frequência de envio de frames do frontend para o backend e a complexidade da análise podem impactar a performance.
- **Precisão:** A precisão da detecção de sonolência depende de vários fatores, incluindo qualidade da câmera, iluminação, e a eficácia do algoritmo EAR.
- **Som de Alarme:** A reprodução automática de som em navegadores é frequentemente restrita e pode exigir interação do usuário com a página primeiro. O som de alarme é acionado pelo frontend.
- **Segurança CSRF:** Para simplificar o exemplo, a proteção CSRF foi desabilitada no endpoint `process_frame_view` com `@csrf_exempt`. Em um ambiente de produção, é crucial configurar a proteção CSRF corretamente.

## Arquivos Chave

- `sleep_monitor/views.py`: Contém a lógica principal do backend para processar os frames de vídeo e detectar sonolência.
- `sleep_monitor/static/sleep_monitor/js/main.js`: Contém a lógica do frontend para acessar a câmera, capturar frames, enviá-los ao backend e exibir alertas.
- `sleep_monitor/templates/sleep_monitor/index.html`: Estrutura HTML da página.
- `pasted_content.txt` (fornecido pelo usuário): Código original que serviu de base para a lógica de detecção.

Este projeto foi desenvolvido como uma prova de conceito e pode ser expandido e aprimorado com funcionalidades adicionais e otimizações.

