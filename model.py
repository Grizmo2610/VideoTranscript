import assemblyai as aai
import google.generativeai as genai
import os


class MyTranscript:
    def __init__(self,language_code = 'vi', key = ...) -> None:
        if key == ...:
            self.key = os.environ["API_KEY"]
        else:
            self.key = key
        aai.settings.api_key = self.key
        self.config = aai.TranscriptionConfig(speaker_labels=True, language_code=language_code)

    def set_language(self, language_code):
        self.config = aai.TranscriptionConfig(speaker_labels=True, language_code=language_code)

    def set_api_key(self, key):
        self.key = key
        aai.settings.api_key = self.key
    
    def transcript(self, url, speaker: bool = False):
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(url,config=self.config)
        return self.__to_text(transcript.utterances, speaker)
    
    def __to_text(self, utterances, speaker):
        respone_text = ''
        for utterance in utterances:
            respone_text += f"{f'Speaker {utterance.speaker}: ' if speaker else ''}{utterance.text.strip()}\n"
        return respone_text.strip()
    def videos_to_text(self, Video_URL):
        print('Processing: ' + Video_URL)
        return self.__to_text(self.transcript(Video_URL))
    


class GeminiTranscript:
    def __init__(self, model = 'gemini-1.5-flash', key = ...) -> None:
        self.model = genai.GenerativeModel(model)
        try:
            if key == ...:
                self.key = os.environ["API_KEY"]
            else:
                self.key = key
        except Exception as e:
            self.key = '' # Input your Gemini API KEY
        genai.configure(api_key=self.key)
        
    def set_key(self, key):
        self.key = key
        genai.configure(api_key=self.key)
    
    def respone(self, text):
        prompt = "Please correct the spelling of the following text. Only correct and return the original text. Do not add notes or mention what has been corrected. Return the text in its original language. Correct the punctuation appropriately, but do not change the text:"
        if self.key != '':
            try:
                response =  self.model.generate_content(f"{prompt}\n{text}\n")
                final = ''
                for chunk in response:
                    final += chunk.text + '\n'
                return final.strip()
            except Exception as e:
                print('Somthing Wrong with model respone!')
        return '=====You need a valid Gemini API Key to use this====='
