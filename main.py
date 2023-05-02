import speech_recognition as sr
import timeit
from recorder import recording

recording(3)

# Создаем объект распознавания речи
r = sr.Recognizer()

start_time = timeit.default_timer()

# Открываем аудиофайл
with sr.AudioFile('example.wav') as source:
    # Читаем файл с помощью объекта распознавания речи
    audio_text = r.record(source)

    try:
        # Преобразуем аудио в текст
        text = r.recognize_google(audio_text, language="ru")
        print(f"Текст из файла 'example.wav': {text}")
    except sr.UnknownValueError:
        print("Не удалось распознать аудио.")
    except sr.RequestError as e:
        print(f"Не удалось получить данные от сервиса распознавания речи; {e}.")

elapsed = timeit.default_timer() - start_time
print(f"Время выполнения: {elapsed:.4f} секунд.")