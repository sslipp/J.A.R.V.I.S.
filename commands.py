from assistant import play_background_music, sleep_computer, toggle_jarvis_mode, shutdown_computer, start_weekend_mode, switch_keyboard_layout, start_work_mode, minimize_window, toggle_school_protocol, stop_and_start_space, start_recorder, stop_recorder, toggle_acdc_music, adjust_volume, open_website, play_youtube_video, toggle_one_house, stop_background_music, adjust_brightness
import spotify_helper

def execute_command(command):
    command = command.lower()
    command_executed = False
    
    if "включи музыку" in command:
        play_background_music()
        command_executed = True
    elif "выключи музыку" in command:
        stop_background_music()
        command_executed = True
    elif "спящий режим" in command:
        sleep_computer()
        command_executed = True
    elif any(keyword in command for keyword in ["запусти протокол школа", "запусти протокол школы", "активируй протокол школа", "активируй протокол школы", "активируй протокол школу", "активировать протокол школа", "активировать протокол школы"]):
        toggle_school_protocol()
        command_executed = True
    elif any(keyword in command for keyword in ["выключи протокол школа", "выключи протокол школы", "деактивируй протокол школа", "деактивируй протокол школы", "деактивировать протокол школы", "деактивировать протокол школа"]):
        toggle_school_protocol()
        command_executed = True
    elif "режим джарвиса" in command:
        toggle_jarvis_mode()
        command_executed = True
    elif "сверни окно" in command:
        minimize_window()
        command_executed = True
    elif "выключи компьютер" in command:
        shutdown_computer()
        command_executed = True
    elif "смени язык" in command:
        switch_keyboard_layout()
        command_executed = True
    elif "включи запись" in command:
        start_recorder()
        command_executed = True
    elif "выключи запись" in command:
        stop_recorder()
        command_executed = True
    elif "за работу" in command:
        start_work_mode()
        command_executed = True
    elif "протокол выходной день" in command:
        start_weekend_mode()
        command_executed = True
    elif "я один дома" in command:
        toggle_one_house()
        command_executed = True
    elif "включить acdc" in command:
        toggle_acdc_music()
        command_executed = True
    elif any(keyword in command for keyword in ["громкость", "звук", "без", "сделай звук"]):
        volume_level = None
        for word in command.split():
            if word.isdigit() and 0 <= int(word) <= 100:
                volume_level = int(word)
                break
        if volume_level is not None:
            adjust_volume(volume_level)
        elif any(word in command for word in ["максимум", "на максимум", "на полную", "на сотку", "выкрути на сотку"]):
            adjust_volume(100)
        elif any(word in command for word in ["минимум", "по минимуму", "на минимум", "звука", "выкрути на 0", "выключи", "звук"]):
            adjust_volume(0)
        elif any(word in command for word in ["на половину", "на 50", "чуть тише", "тише"]):
            adjust_volume(50)
        command_executed = True
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
        command_executed = True
    elif "загугли" in command:
        search_query = command.split("загугли", 1)[1].strip()
        open_website(search_query)
        command_executed = True
    elif any(keyword in command for keyword in ["сделай яркость на", "установи яркость на", "поставь яркость на", "яркость на"]):
        if any(word in command for word in ["максимум", "на максимум", "на полную", "сотку"]):
            adjust_brightness('максимум')
        elif any(word in command for word in ["минимум", "по минимуму", "на минимум", "ноль"]):
            adjust_brightness('минимум')
        else:
            brightness_level = command.split("на")[-1].strip()
            adjust_brightness(brightness_level)
        command_executed = True
    elif "найди видео" in command:
        query = command.replace("найди видео", "").strip()
        play_youtube_video(query)
        command_executed = True
    elif "включи песню" in command:
        song_name = command.replace("включи песню", "").strip()
        spotify_helper.play_song(song_name)
        command_executed = True
    elif "выключи песню" in command:
        spotify_helper.stop_playback()
        command_executed = True
    else:
        print("Команда не распознана")

    return command_executed
