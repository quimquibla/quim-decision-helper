
# Aplicación interactiva de QuimDecisionHelper con interfaz web y soporte PWA

from fastapi import FastAPI, Request
from pydantic import BaseModel
import random
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class Question(BaseModel):
    question: str

class QuimDecisionHelper:
    def __init__(self):
        self.ethical_principles = [
            "La verdad es innegociable",
            "El poder debe usarse para servir, no para dominar",
            "La vulnerabilidad no es debilidad, sino acceso a la verdad",
            "La claridad emocional vale más que la aprobación externa",
            "El liderazgo empieza por la coherencia interna"
        ]

    def evaluate_decision(self, question: str):
        response = ""
        if "conflicto" in question or "discutir" in question:
            response += "Quim evitaría el conflicto directo si percibe que no hay apertura al entendimiento.\n"
            response += "Buscaría comprender primero la intención del otro y luego decidir desde la calma.\n"
        elif "liderar" in question or "guiar" in question:
            response += "Quim lideraría desde el ejemplo, no desde la imposición.\n"
            response += "Evaluaría si su motivación nace del deseo de cuidar o del ego.\n"
        elif "rendirse" in question or "abandonar" in question:
            response += "Quim distinguiría entre soltar lo que daña y rendirse por miedo.\n"
            response += "Si la causa sigue siendo justa, buscaría nuevas formas de sostenerla.\n"
        elif "amor" in question or "relación" in question:
            response += "Quim no se sostendría en vínculos que lo reducen o distorsionan.\n"
            response += "Buscaría relaciones donde se preserve la autenticidad mutua.\n"
        else:
            response += "Quim actuaría desde el centro: escuchando su cuerpo, observando su mente, y eligiendo con ética.\n"

        response += f"\nPrincipio guía: {random.choice(self.ethical_principles)}"
        return response

@app.post("/quim/decide")
def decide(question: Question):
    helper = QuimDecisionHelper()
    return {"respuesta": helper.evaluate_decision(question.question)}

@app.get("/manifest.json")
def manifest():
    return {
        "name": "Asistente Ético: Quim",
        "short_name": "Quim",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "description": "Consulta dilemas éticos con la mirada introspectiva de Quim.",
        "icons": [
            {
                "src": "https://cdn-icons-png.flaticon.com/512/535/535239.png",
                "type": "image/png",
                "sizes": "512x512"
            }
        ]
    }

@app.get("/service-worker.js", response_class=FileResponse)
def service_worker():
    return FileResponse("service-worker.js")

@app.get("/", response_class=HTMLResponse)
def root():
    return """<html>
    <head>
        <title>Quim Decision Helper</title>
        <link rel="manifest" href="/manifest.json">
        <script>
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/service-worker.js');
        }
        </script>
    </head>
    <body style='font-family:Arial;padding:20px;'>
        <h1>Asistente Ético: Quim</h1>
        <form onsubmit="handleSubmit(event)">
            <label for="question">Escribe tu pregunta o dilema:</label><br><br>
            <textarea id="question" name="question" rows="5" cols="60"></textarea><br><br>
            <input type="submit" value="Consultar a Quim">
        </form>
        <div id="respuesta" style="margin-top:20px;"></div>
        <script>
        async function handleSubmit(event) {
            event.preventDefault();
            const question = document.getElementById('question').value;
            const response = await fetch('/quim/decide', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question})
            });
            const data = await response.json();
            document.getElementById('respuesta').innerText = data.respuesta;
        }
        </script>
    </body>
    </html>"""
