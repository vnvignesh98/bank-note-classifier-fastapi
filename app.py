from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from banknote import BankNote
import pickle
import uvicorn

app = FastAPI()

template = Jinja2Templates(directory='templates')

model = pickle.load(open('classifier.pkl','rb'))

@app.get('/',response_class=HTMLResponse)
async def form_get(request: Request):
    return template.TemplateResponse("index.html",{"request":request})

@app.post("/",response_class=HTMLResponse)
async def form_post(request: Request, variance: str = Form("variance"),
                     skewness: str = Form("skewness"),curtosis: str = Form("curtosis"),
                     entropy: str = Form("entropy")):
    print(variance, skewness, curtosis, entropy)
    try:
        variance = float(variance)
        skewness = float(skewness)
        curtosis = float(curtosis)
        entropy = float(entropy)
        print(variance, skewness, curtosis, entropy)
        prediction = model.predict([[variance,skewness,curtosis,entropy]])
        if prediction[0]>0.5:
            return template.TemplateResponse("index.html",{"request":request, "prediction_text":"It's a Fake Note"})
        else:
            return template.TemplateResponse("index.html",{"request":request, "prediction_text":"It's a Bank Note"})
    except:
        return template.TemplateResponse("index.html",{"request":request, "prediction_text":"Invalid Input"})

if __name__=="__main__":
    uvicorn.run("app:app",host="127.0.0.1",port=8000, reload = True)


# variance: float = Form("selected_option_variance"),
#                     skewness: float = Form("selected_option_skewness"),curtosis: float = Form("selected_option_curtosis"),
#                     entropy: float = Form("selected_option_entropy")


# async def form_post(request: Request, data:BankNote):
#     data = data.model_dump()
#     variance = data['variance']   
#     skewness = data['skewness']
#     curtosis = data['curtosis']
#     entropy = data['entropy']