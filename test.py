import warnings
warnings.filterwarnings('ignore')
import json
from chatbot import response




jsonFile = open("./qa.json",encoding='utf-8')
jsonString = jsonFile.read()
jsonData = json.loads(jsonString)["intents"]


questions = [obj["Question"] for obj in jsonData]
answers = [obj["Answer"] for obj in jsonData]
idx = [obj["Id"] for obj in jsonData]



true_ans = 0
false_ans = 0
exception = 0

for que,ans,id in zip(questions,answers,idx):
    try:
        res = response(que.lower())
        if res == ans:
            true_ans += 1
        else:
            print(f"Yanlış cevap : {id}")
            false_ans += 1
    except:
        print(f"Kod hata fırlattı : {id}")
        exception += 1

print("Doğru cevap sayısı:" , true_ans)
print("Yanlış cevap sayısı:" , false_ans)
print("Kod hatası:" , exception)
print("Doğruluk yüzdesi:" , true_ans/len(questions))

