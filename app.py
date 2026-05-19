import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__, template_folder='templates')

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

historicos = {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    dados = request.json
    sessao = dados.get("sessao", "default")
    mensagem = dados.get("mensagem", "")

    if sessao not in historicos:
        historicos[sessao] = []

    historicos[sessao].append(
        types.Content(role="user", parts=[types.Part(text=mensagem)])
    )

    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="Você é um assistente especialista em armações de óculos. Responda sempre em português, de forma simpática e objetiva."
        ),
        contents=historicos[sessao]
    )

    texto = resposta.text
    historicos[sessao].append(
        types.Content(role="model", parts=[types.Part(text=texto)])
    )

    return jsonify({"resposta": texto})

@app.route("/recomendar", methods=["POST"])
def recomendar():
    dados = request.json
    rosto = dados.get("rosto")
    estilo = dados.get("estilo")
    uso = dados.get("uso")

    prompt = f"Com base no formato de rosto '{rosto}', estilo '{estilo}' e uso principal '{uso}', recomende a armação de óculos ideal. Explique o porquê e diga o que evitar. Seja objetivo e simpático."

    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="Você é um especialista em armações de óculos. Responda sempre em português."
        ),
        contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
    )

    return jsonify({"resposta": resposta.text})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)