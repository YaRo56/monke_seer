import speech_recognition as sr
import timeit

# Создаем объект распознавания речи
r = sr.Recognizer()

start_time = timeit.default_timer()

with sr.Microphone() as source:
    print("Говори!")
    audio = r.listen(source)

# Читаем файл с помощью объекта распознавания речи
try:
    # Преобразуем аудио в текст
    print(r.recognize_google(audio, language="ru"))
except sr.UnknownValueError:
    print("Не удалось распознать аудио.")
except sr.RequestError as e:
    print(f"Не удалось получить данные от сервиса распознавания речи; {e}.")

elapsed = timeit.default_timer() - start_time
print(f"Время выполнения: {elapsed:.4f} секунд.")
