import torch
from flask import Flask, render_template, request
from transformers import BertTokenizer
from transformers import BertModel
from torch import nn



class BertClassifier(nn.Module):

    def __init__(self, dropout=0.5):
        super(BertClassifier, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-cased')
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(768, 5)
        self.relu = nn.ReLU()

    def forward(self, input_id, mask):
        _, pooled_output = self.bert(input_ids= input_id, attention_mask=mask,return_dict=False)
        dropout_output = self.dropout(pooled_output)
        linear_output = self.linear(dropout_output)
        final_layer = self.relu(linear_output)
        return final_layer


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_genre', methods=['POST'])
def predict():
    val = request.form.get('plot')
    model = torch.load('max-bert-model.txt', map_location=torch.device('cpu'))
    model.predict('hello world')
    t = model("test", '1')
    return f'<h2>{t}</h2>'

###app.run(host='0.0.0.0', port=8000)


model = torch.load('max-bert-model.txt', map_location=torch.device('cpu'))
tokenizer = BertTokenizer.from_pretrained('bert-base-cased')


comedy_sample = "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy's heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences."
input = tokenizer(comedy_sample, 
                               padding='max_length', max_length = 512, truncation=True,
                                return_tensors="pt")
t = model(input['attention_mask'],input['input_ids']).detach().cpu().numpy()
print(t)