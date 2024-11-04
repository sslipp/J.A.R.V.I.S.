from assistant import play_background_music, toggle_jarvis_mode, toggle_school_protocol, stop_and_start_space, start_recorder, stop_recorder, toggle_acdc_music, adjust_volume, open_website, play_youtube_video, toggle_one_house, stop_background_music, adjust_brightness
import spotify_helper

def execute_command(command):
    command = command.lower()
    
    if "включи музыку" in command:
        play_background_music()
    elif "выключи музыку" in command:
        stop_background_music()
    elif any(keyword in command for keyword in ["запусти протокол школа", "запусти протокол школы", "активируй протокол школа", "активируй протокол школы", "активировать протокол школа", "активировать протокол школы"]):
        toggle_school_protocol()
    elif any(keyword in command for keyword in ["выключи протокол школа", "выключи протокол школы", "деактивируй протокол школа", "деактивируй протокол школы", "деактивировать протокол школы", "деактивировать протокол школа"]):
        toggle_school_protocol()
    elif "режим джарвиса" in command:
        toggle_jarvis_mode()
    elif "включи запись" in command:
        start_recorder()
    elif "выключи запись" in command:
        stop_recorder()
    elif "я один дома" in command:
        toggle_one_house()
    elif any(keyword in command for keyword in ["стоп", "старт", "останови", "запусти", "пауза", "поставь на паузу", "плей", "play"]):
        stop_and_start_space()
    elif "включить acdc" in command:
        toggle_acdc_music()
    elif any(keyword in command for keyword in ["громкость", "звук", "без"]):
        if any(word in command for word in ["максимум", "на максимум", "на полную", "на сотку"]):
            adjust_volume('maximum')
        elif any(word in command for word in ["минимум", "по минимуму", "на минимум", "звука"]):
            adjust_volume('minimum')
        elif any(word in command for word in ["на половину", "на 50", "чуть тише", "тише"]):
            adjust_volume('middle')
    elif "открой" in command:
        if "почту" in command:
            open_website("mail")
        elif "ютуб" in command:
            open_website("youtube")
        elif "нетфликс" in command:
            open_website("netflix")
        else:
            site_name = command.split("открыть")[1].strip()
            open_website(site_name)
    elif any(keyword in command for keyword in ["сделай яркость на", "установи яркость на", "поставь яркость на", "яркость на"]):
        if any(word in command for word in ["максимум", "на максимум", "на полную", "сотку"]):
            adjust_brightness('максимум')
        elif any(word in command for word in ["минимум", "по минимуму", "на минимум", "ноль"]):
            adjust_brightness('минимум')
        else:
            brightness_level = command.split("на")[-1].strip()
            adjust_brightness(brightness_level)
    elif "найди видео" in command:
        query = command.replace("найди видео", "").strip()
        play_youtube_video(query)
    elif "включи песню" in command:
        song_name = command.replace("включи песню", "").strip()
        spotify_helper.play_song(song_name)
    elif "выключи песню" in command:
        spotify_helper.stop_playback()
    else:
        print("Команда не распознана")
