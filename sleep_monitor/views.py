from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Para simplificar, mas em produção, use CSRF corretamente
import cv2
import dlib
import numpy as np
import base64
import os
from scipy.spatial import distance as dist

# Configurações (substituir argparse)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Assumindo que o shape_predictor e o alarme estarão na pasta static do app sleep_monitor
# É importante garantir que esses arquivos existam nesses caminhos.
SHAPE_PREDICTOR_PATH = os.path.join(BASE_DIR, "sleep_monitor", "static", "sleep_monitor", "shape_predictor_68_face_landmarks.dat")
ALARM_SOUND_PATH = os.path.join(BASE_DIR, "sleep_monitor", "static", "sleep_monitor", "alarme.wav")

# Constantes do algoritmo de detecção de sono
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 36 # Quantidade de frames com olho fechado para disparar o alarme

# Inicialização do dlib (carregar apenas uma vez)
try:
    detector = dlib.get_frontal_face_detector()
    if not os.path.exists(SHAPE_PREDICTOR_PATH):
        print(f"ALERTA: Arquivo shape_predictor_68_face_landmarks.dat não encontrado em {SHAPE_PREDICTOR_PATH}")
        # Em um cenário real, você pode querer levantar uma exceção ou lidar com isso de forma mais robusta.
        predictor = None
    else:
        predictor = dlib.shape_predictor(SHAPE_PREDICTOR_PATH)
except Exception as e:
    print(f"Erro ao inicializar dlib: {e}")
    detector = None
    predictor = None

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def index(request):
    # Inicializa o contador de olhos fechados na sessão se não existir
    request.session["eye_closed_counter"] = 0
    return render(request, "sleep_monitor/index.html")

@csrf_exempt # Desabilitar CSRF para este endpoint de API para simplificar. Em produção, configure corretamente.
def process_frame_view(request):
    if request.method == "POST":
        try:
            # Recebe a imagem em base64 do frontend
            image_data_url = request.POST.get("image_data")
            if not image_data_url or not predictor:
                return JsonResponse({"error": "Dados de imagem não fornecidos ou preditor não carregado"}, status=400)

            # Decodifica a imagem base64
            # Formato esperado: "data:image/jpeg;base64,/9j/..."
            header, encoded = image_data_url.split(",", 1)
            image_data = base64.b64decode(encoded)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is None:
                return JsonResponse({"error": "Não foi possível decodificar a imagem"}, status=400)

            # Redimensiona o frame (opcional, mas pode ajudar na performance)
            # frame = cv2.resize(frame, (450, 300))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            alert_triggered = False
            # Recupera o contador da sessão
            counter_eyes_closed = request.session.get("eye_closed_counter", 0)

            rects = detector(gray, 0) # Usar 0 para não upsample, pode ser mais rápido

            for rect in rects:
                shape = predictor(gray, rect)
                shape_np = np.array([[shape.part(i).x, shape.part(i).y] for i in range(68)])
                
                leftEAR = eye_aspect_ratio(shape_np[42:48])
                rightEAR = eye_aspect_ratio(shape_np[36:42])
                ear = (leftEAR + rightEAR) / 2.0

                if ear < EYE_AR_THRESH:
                    counter_eyes_closed += 1
                    if counter_eyes_closed >= EYE_AR_CONSEC_FRAMES:
                        alert_triggered = True
                        # O som será tocado pelo frontend com base neste alerta
                else:
                    counter_eyes_closed = 0 # Reseta o contador se os olhos estiverem abertos
            
            # Atualiza o contador na sessão
            request.session["eye_closed_counter"] = counter_eyes_closed
            
            return JsonResponse({"alert": alert_triggered, "ear": ear if 'ear' in locals() else -1, "frames_closed": counter_eyes_closed})

        except Exception as e:
            print(f"Erro no processamento do frame: {e}")
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Método não permitido"}, status=405)

# Nota: A funcionalidade de tocar som com playsound foi removida do backend.
# O frontend deve ser responsável por tocar o som quando receber {"alert": true}.
# O arquivo alarme.wav deve estar acessível ao frontend, por exemplo, na pasta static.

