import logging
from gtts import gTTS
from tempfile import TemporaryFile

log = logging.getLogger(__name__)


def speak_bot_speak(string_to_speak, lang='en'):
    tts = gTTS(text=string_to_speak, lang=lang)
    f = TemporaryFile()
    tts.write_to_fp(f)
    f.seek(0, 0)
    return f


if __name__ == "__main__":
    LOG_FORMAT = '%(asctime)s %(name)s [%(levelname)s] %(message)s'
    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO,
                        format=LOG_FORMAT)
    f = speak_bot_speak('test')
    f.close()
