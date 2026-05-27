import os
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

app = Flask(__name__, template_folder='templates')

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

historicos = {}

catalogo = [
    {
        "nome": "Redondo",
        "imagem": "redondo.png",
        "rostos": ["quadrado", "retangulo"],
        "estilos": ["clássico", "despojado"],
        "descricao": "Suaviza traços angulares e dá um toque vintage e sofisticado."
    },
    {
        "nome": "Aviador",
        "imagem": "aviador.png",
        "rostos": ["oval", "coração"],
        "estilos": ["clássico", "esportivo"],
        "descricao": "Atemporal e versátil, combina com vários estilos e ocasiões."
    },
    {
        "nome": "Gatinho",
        "imagem": "gatinho.png",
        "rostos": ["redondo", "quadrado", "oval"],
        "estilos": ["moderno", "fashion"],
        "descricao": "Feminino e marcante, realça o olhar e valoriza o rosto."
    },
    {
        "nome": "Quadrado",
        "imagem": "quadrado.png",
        "rostos": ["oval", "redondo"],
        "estilos": ["clássico", "executivo"],
        "descricao": "Transmite seriedade e elegância, ideal para o ambiente profissional."
    },
    {
        "nome": "Retangular",
        "imagem": "retangular.png",
        "rostos": ["oval", "redondo"],
        "estilos": ["moderno", "executivo"],
        "descricao": "Clean e moderno, combina com looks casuais e formais."
    },
    {
        "nome": "Triangular",
        "imagem": "triangular.png",
        "rostos": ["oval", "quadrado"],
        "estilos": ["moderno", "fashion"],
        "descricao": "Diferenciado e estiloso, para quem quer se destacar."
    },
    {
        "nome": "Coração",
        "imagem": "coracao.png",
        "rostos": ["oval", "redondo"],
        "estilos": ["fashion", "despojado"],
        "descricao": "Divertido e único, perfeito para personalidades marcantes."
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/catalogo", methods=["GET"])
def get_catalogo():
    return jsonify(catalogo)

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
            system_instruction="Você é um assistente especialista em armações de óculos. Responda sempre em português, de forma simpática e objetiva. Ajude com dúvidas sobre armações, formatos de rosto, materiais e tendências."
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
    rosto = dados.get("rosto", "").lower()
    estilo = dados.get("estilo", "").lower()
    uso = dados.get("uso", "")

    recomendados = [
        o for o in catalogo
        if rosto in o["rostos"] or any(e in o["estilos"] for e in estilo.split("/"))
    ]

    if not recomendados:
        recomendados = catalogo[:2]

    prompt = f"Com base no formato de rosto '{rosto}', estilo '{estilo}' e uso principal '{uso}', recomende a armação de óculos ideal. Explique o porquê e diga o que evitar. Seja objetivo e simpático."

    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction="Você é um especialista em armações de óculos. Responda sempre em português."
        ),
        contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
    )

    return jsonify({
        "resposta": resposta.text,
        "recomendados": recomendados
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)