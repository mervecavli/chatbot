# -*- coding:utf-8 -*-
import nltk
import random
import string
import warnings
warnings.filterwarnings('ignore')
import json
import speech_recognition as sr
r = sr.Recognizer()
import os
from gtts import gTTS


jsonFile = open("./qa.json",encoding='utf-8')
jsonString = jsonFile.read()
jsonData = json.loads(jsonString)["intents"]


questions = [obj["Question"] for obj in jsonData]
answers = [obj["Answer"] for obj in jsonData]


lemmer = nltk.stem.WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

#karşılama
greeting_inputs = ("merhaba","Selamünaleyküm","selam", "sa", "selamınaleyküm", "mrb", "iyi günler")
greeting_responses = ["merhaba, nasıl yardımcı olabilirim?", "hoş geldiniz, nasıl yardımcı olabilirim?", "merhaba, neyi merak ediyorsunuz?", "selam, nasıl yardımcı olabilirim?"]

def greeting(scentence):
    
    for word in scentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_responses)
        


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def response(user_response):
    chatbot_response = ''
    questions.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize)
    tfidf = TfidfVec.fit_transform(questions)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf == 0 and user_response != "1"):
        chatbot_response = chatbot_response + "Üzgünüm, bu sorunuzu yanıtlayamıyorum."
        return chatbot_response
    
    else:

        chatbot_response=answers[idx]+chatbot_response
        return chatbot_response

if __name__ == "__main__":
    flag = True
    tts = gTTS(text = "Merhaba, ben Chatbot. Aydın'da ulaşımla alakalı sorularınızı cevaplıyorum.Mikrofonu kullanmak için 1'e basın. Çıkmak için Çıkış yazın." , lang='tr')
    tts.save("speech.mp3")
    os.system("speech.mp3")

    print("Merhaba, ben Chatbot. Aydın'da ulaşımla alakalı sorularınızı cevaplıyorum.Mikrofonu kullanmak için 1'e basın. Çıkmak için Çıkış yazın.")
    while(flag==True):
        user_response = input("Siz:")
        user_response = user_response.lower()
        if(user_response == "1"):
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Konuşun...")
                data = r.record(source, duration=5)
                print("Sesinizi Metne Dönüştürülüyor…")
                text = r.recognize_google(data,language='tr')
                print(text)
                user_response = text
        if(user_response!='çıkış'):
            if user_response == 'teşekkürler' or user_response == 'teşekkür ederim':
                flag = False
                print("Chatbot: Rica ederim!")
                tts = gTTS(text="Rica ederim!", lang='tr')
                tts.save("speech.mp3")
                os.system("speech.mp3")
            else:
                if(greeting(user_response)!=None):
                    print("Chatbot:" +greeting(user_response))
                    tts = gTTS((greeting(user_response)), lang='tr')
                    tts.save("speech.mp3")
                    os.system("speech.mp3")
                else:
                    print("Chatbot:")
                    print(response(user_response))
                    questions.remove(user_response)
                    tts = gTTS((response(user_response)), lang='tr')
                    tts.save("speech.mp3")
                    os.system("speech.mp3")
        else:
            flag = False
            print("Chatbot:Çıkış yapılıyor...Hoşça kalın!" )
            tts = gTTS(text="Çıkış yapılıyor...Hoşça kalın!", lang='tr')
            tts.save("speech.mp3")
            os.system("speech.mp3")
             