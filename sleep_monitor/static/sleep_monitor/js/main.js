document.addEventListener("DOMContentLoaded", () => {
    const videoElement = document.getElementById("webcamFeed");
    const startButton = document.getElementById("startButton");
    const statusArea = document.getElementById("statusArea");
    let stream = null;
    let monitoringInterval = null;
    // O som deve estar em sleep_monitor/static/sleep_monitor/alarme.wav
    // O JS está em sleep_monitor/static/sleep_monitor/js/main.js
    // Caminho relativo de js/main.js para alarme.wav é ../alarme.wav
    const alarmSound = new Audio("../alarme.wav"); 

    async function startWebcam() {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            videoElement.srcObject = stream;
            statusArea.textContent = "Câmera acessada. Clique em \"Iniciar Monitoramento\".";
            startButton.textContent = "Iniciar Monitoramento";
            startButton.disabled = false;
        } catch (error) {
            console.error("Erro ao acessar a webcam:", error);
            statusArea.textContent = "Erro ao acessar a webcam. Verifique as permissões.";
            alert("Não foi possível acessar a câmera. Por favor, verifique as permissões do navegador.");
        }
    }

    function stopWebcam() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            videoElement.srcObject = null;
            stream = null;
        }
        if (monitoringInterval) {
            clearInterval(monitoringInterval);
            monitoringInterval = null;
        }
        startButton.textContent = "Iniciar Monitoramento";
        statusArea.textContent = "Monitoramento parado. Clique para iniciar.";
    }

    async function captureAndSendFrame() {
        if (!stream || !stream.active) {
            console.log("Stream da câmera não está ativo.");
            statusArea.textContent = "Erro: Câmera não está ativa.";
            stopWebcam();
            return;
        }

        const imageCapture = new ImageCapture(stream.getVideoTracks()[0]);
        try {
            const blob = await imageCapture.grabFrame();
            const canvas = document.createElement("canvas");
            canvas.width = blob.width;
            canvas.height = blob.height;
            const context = canvas.getContext("2d");
            context.drawImage(blob, 0, 0);
            const imageDataUrl = canvas.toDataURL("image/jpeg");

            statusArea.textContent = "Processando...";

            fetch("/sleep_monitor/process_frame/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: new URLSearchParams({
                    "image_data": imageDataUrl
                })
            })
            .then(response => {
                if (!response.ok) {
                    // Tenta ler o corpo do erro como JSON para mais detalhes
                    return response.json().then(errData => {
                        throw new Error(`HTTP error! status: ${response.status}, message: ${errData.error || response.statusText}`);
                    }).catch(() => {
                         throw new Error(`HTTP error! status: ${response.status}, statusText: ${response.statusText}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                if (data.error) {
                    console.error("Erro do backend:", data.error);
                    statusArea.textContent = `Erro no servidor: ${data.error}`;
                    return;
                }
                if (data.alert) {
                    statusArea.textContent = "ALERTA DE SONO!";
                    alarmSound.play().catch(e => console.error("Erro ao tocar alarme:", e));
                } else {
                    statusArea.textContent = `Monitorando... EAR: ${data.ear ? data.ear.toFixed(2) : "N/A"}, Frames Fechados: ${data.frames_closed}`;
                }
            })
            .catch(error => {
                console.error("Erro ao enviar/processar frame:", error);
                statusArea.textContent = `Erro na comunicação: ${error.message}`;
            });

        } catch (error) {
            console.error("Erro ao capturar frame:", error);
            statusArea.textContent = "Erro ao capturar frame.";
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    startButton.addEventListener("click", () => {
        if (!stream) {
            startWebcam().then(() => {
                if (stream) {
                    startButton.textContent = "Parar Monitoramento";
                    statusArea.textContent = "Iniciando monitoramento...";
                    monitoringInterval = setInterval(captureAndSendFrame, 500); // Intervalo de 500ms entre frames
                }
            });
        } else {
            stopWebcam();
        }
    });
    statusArea.textContent = "Clique em \"Iniciar Monitoramento\" para acessar a câmera.";
});

