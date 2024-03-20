from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse
from .models import MissingPerson
import face_recognition
import cv2
import numpy as np
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import base64

@csrf_exempt
def upload_and_detect_image(request):
    if request.method == 'POST':
        uploaded_image = request.FILES['image']
        img_stream = BytesIO(uploaded_image.read())
        file_bytes = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_img)
        uploaded_img_encodings = face_recognition.face_encodings(rgb_img, face_locations)

        match_found = False
        matched_person_name = ""  

        for (top, right, bottom, left), uploaded_img_encoding in zip(face_locations, uploaded_img_encodings):
            for person in MissingPerson.objects.all():
                person_img = face_recognition.load_image_file(person.image.path)
                person_img_encodings = face_recognition.face_encodings(person_img)
                if person_img_encodings:
                    result = face_recognition.compare_faces(person_img_encodings, uploaded_img_encoding)
                    if True in result:
                        match_found = True
                        matched_person_name = person.name  
                        # Dibuja un cuadrado alrededor de la cara encontrada
                        cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                        break
            if match_found:
                break

        if match_found:
            # Convierte la imagen con la cara resaltada
            retval, buffer_img = cv2.imencode('.jpg', img)
            base64_img = base64.b64encode(buffer_img).decode()
            # Retorna la imagen codificada
            return JsonResponse({"message": "Match found", "image": base64_img, "name": matched_person_name})
        else:
            return JsonResponse({"message": "No match found."})
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

