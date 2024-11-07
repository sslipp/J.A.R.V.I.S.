import azure.cognitiveservices.speech as speechsdk

# Укажите свой ключ и регион
speech_key = "A6WSUnMWuJCajVJ66wZWYNI4ZY302r1vpJV1BzUquJVEs1UiaRtFJQQJ99AKACYeBjFXJ3w3AAAYACOGvO8G"
service_region = "eastus"

# Настройка клиента TTS
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "ru-RU-DariyaNeural"

# Исправленная SSML-разметка для задания текста и скорости
ssml_string = """
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='ru-RU'>
    <voice name='ru-RU-DariyaNeural'>
        <prosody pitch='+2Hz' rate='-2%'>
            Не буду вам мешать, сэр
        </prosody>
    </voice>
</speak>
"""
    
# Синтез текста с использованием SSML
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
result = synthesizer.speak_ssml_async(ssml_string).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Синтез успешно завершён.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Произошла ошибка синтеза речи:")
    print("Причина:", cancellation_details.reason)
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Код ошибки:", cancellation_details.error_details)
