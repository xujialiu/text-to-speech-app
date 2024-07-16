import azure.cognitiveservices.speech as speechsdk
import pyaudio
import multiprocessing
import queue


class MyAudioPlayer(multiprocessing.Process):
    def __init__(self, audio_queue, is_converting, is_paused):
        super().__init__()
        self.audio_queue = audio_queue
        self.is_converting = is_converting
        self.is_paused = is_paused

    def run(self):
        p = pyaudio.PyAudio()
        audio_stream = p.open(
            format=pyaudio.paInt16, channels=1, rate=16000, output=True
        )

        while self.is_converting.value:
            if not self.is_paused.value:
                try:
                    audio_chunk = self.audio_queue.get(timeout=0.1)
                    audio_stream.write(audio_chunk)
                except queue.Empty:
                    pass

        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()


class MySpeechSynthesizer(multiprocessing.Process):
    def __init__(self, speech_key, service_region, audio_queue, ssml):
        super().__init__()
        self.speech_key = speech_key
        self.service_region = service_region
        self.audio_queue = audio_queue
        self.ssml = ssml

    def run(self):
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key, region=self.service_region
        )
        self.speech_synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=None
        )

        def synthesis_callback(evt):
            audio_data = evt.result.audio_data
            # self.audio_queue.put(audio_data.split(b"data")[1][4:])
            self.audio_queue.put(audio_data[46:])

        self.speech_synthesizer.synthesizing.connect(synthesis_callback)

        # 这里不要用speak_text_async, 它会产生一个我没法控制的额外进程
        # 这里直接用speak_text, 它会阻塞本进程, 但是没有关系, 需要的时候terminate关闭该进程即可
        self.speech_synthesizer.speak_ssml(self.ssml)
