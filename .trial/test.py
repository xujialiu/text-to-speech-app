
import os
import azure.cognitiveservices.speech as speechsdk
from speech_key import SPEECH_KEY, SPEECH_REGION

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='zh-CN-XiaochenNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
text = "我是谁?"

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
    
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
            

speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

result = speech_synthesizer.speak_text_async("I'm excited to try text to speech").get()
stream = speechsdk.AudioDataStream(result)
stream.save_to_wav_file("path/to/write/file.wav")
stream.sav