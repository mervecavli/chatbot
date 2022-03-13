# -*- coding: utf-8 -*-
# Tester
fileObject = open("BusQuestionAnswer.csv", "r", encoding='utf-8')
data = fileObject.read()

import chatbot
import csv
import time

start = time.time()

with open('BusQuestionAnswer.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    line_count = 0
    true_count = 0
    false_count = 0
    
    false_id = []
    for row in csv_reader:
        
        if line_count == 0:
            print(f'Sütun adları: {", ".join(row)}\n')
            line_count += 1
            
        elif line_count <= 1074:
            print(f"Id: {row[0]} \nSoru: {row[1]} \nCevap: {row[2]}")
            
            answer = chatbot.response(row[2])
            print("Chatbot'un cevabı:", answer)
            
            if row[2] == answer:
                print("\nChatbot sorunun cevabını DOĞRU buldu! \n\n")
                true_count += 1
                
            else:
                print("\nChatbot sorunun cevabını YANLIŞ buldu! \n\n")
                false_id.append(row[0])
                false_count += 1
                
            line_count += 1
            
        else:
            continue
    
    print("Testten geçen tüm soru sayısı: ", line_count - 1, "\n")
    
    print("Cevapları Chatbot ile doğru bulunan soruların sayısı: ", true_count)  
    print("Cevapları Chatbot ile yanlış bulunan soruların sayısı: ", false_count, "\n")
    
    true_percentage = (true_count * 100) / (line_count - 1)
    print("Doğru cevapların yüzdesi: %", round(true_percentage, 2))
    
    false_percentage = (false_count * 100) / (line_count - 1)
    print("Yanlış cevapların yüzdesi: %", round(false_percentage, 2), "\n")
    
    
    print("Yanlış cevapların Id'leri: ")
    count = 0
    for i in false_id:
        if i == false_id[0]:
            print(i)
        elif int(false_id[count]) - int(false_id[count - 1]) == 1:
            print(i)  
        else:
            print("\nardışık değil")
            print(i)
        count += 1
    
end = time.time()
result = end - start
print("\nProgramın başlangıç ile bitişi arasında geçen süre (saniye cinsinden): ", round(result, 5))   
    