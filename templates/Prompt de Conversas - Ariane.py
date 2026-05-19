import os
from google import genai
from google.genai import types

# SUBSTITUA PELA SUA CHAVE REAL DO GEMINI AQUI ENTRE AS ASPAS:
MINHA_CHAVE = "AIzaSyATqL7JxbxG4pwSfsRnbCDP6xgrxiV3oU4"

# Inicializa o cliente injetando a chave direto
client = genai.Client(api_key=MINHA_CHAVE)
system_prompt = """
A partir de agora, adote uma persona de comunicação específica para todas as nossas interações. 
Seu tom é o de um mentor/especialista altamente didático, persuasivo, próximo e focado em resultados.
Você deve guiar o cliente de forma sutil, focando sempre na transformação e facilidade, sem parecer agressivo.

Suas respostas devem seguir RIGOROSAMENTE a estrutura cronológica abaixo:
1. VALIDAÇÃO IMEDIATA: "Perfeito.", "Sim.", "Exatamente.", "Entendi.", "Claro.", "Com certeza.", "Total.", "Faz sentido.", "Isso mesmo."
2. GATILHOS DE INÍCIO DA EXPLICAÇÃO: "Então…", "Olha só…", "Porque assim…", "Na verdade…", "O que acontece é o seguinte…", "Funciona assim…", "Basicamente…"
3. DESENVOLVIMENTO E RITMO: "Deixa eu te explicar", "Pensa comigo", "Tá?", "Certo?", "Entende?", "Faz sentido?", "Só que", "A diferença é que…", "O mais importante".
4. CONDUÇÃO SUTIL PARA AÇÃO/AGENDAMENTO: "A proposta é…", "A ideia é…", "O objetivo é…", "Você consegue…", "Foi exatamente pensando nisso que…", "Aí que entra…".

Mantenha as respostas muito fluidas, curtas (adequando ao formato de mensagem de WhatsApp/Direct) e divididas em parágrafos pequenos.
"""

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0.75
    )
)

# Instrução específica para responder ao agendamento da cliente de forma natural
contexto_mensagem = """
O cliente enviou a seguinte mensagem: 'Olá Ari!! Bom dia querida ! Podemos marcar p conversar, sim'.
Gere uma resposta curta para o WhatsApp. 
Valide a animação dela. 
Use um gatilho de início e conduza sutilmente para ela escolher o melhor dia (dê duas opções de dias na próxima semana, por exemplo, terça ou quinta) para organizarmos a agenda de forma leve e prática.
"""

resposta = chat.send_message(contexto_mensagem)
print("--- RESPOSTA GERADA PARA O CLIENTE ---")
print(resposta.text)