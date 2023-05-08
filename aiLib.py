# import requests
#
# url = "https://chatgpt-api.shn.hk/v1/"
#
# data = {
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "Answer with only yes or no"}, {"role": "user", "content": "Is \"Ok\" agreement"}]
# }
#
# response = requests.post(url, json=data)
#
# print("Status Code", response.status_code)
# print("JSON Response ", response.json())


# import torch
# from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
#
# tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
# model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
#
# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
# with torch.no_grad():
#     logits = model(**inputs).logits
#
# predicted_class_id = logits.argmax().item()
# print(predicted_class_id)
from selenium.webdriver.common.by import By
from googletrans import Translator
class AiClassify():
    def __init__(self):
        self.translator = Translator()

    def isCookieAccept(self, el):
        text = ' '.join(el.text.split())
        text = self.translator.translate(text).text
        text = text.lower()
        if "accept" in text or "ok" in text:
            i=0
            while el.tag_name!="body":
                el = el.find_element(By.XPATH, "./..")
                parText = el.get_attribute('textContent')
                tra = self.translator.translate(el.get_attribute('textContent')).text.lower()
                if "cookie" in self.translator.translate(el.get_attribute('textContent')).text.lower():
                    return i
                i+=1
            return -1
        return -1