import io
import os
from huggingface_hub import InferenceClient
from PIL import Image

# COLE SEU TOKEN DO HUGGING FACE AQUI DENTRO DAS ASPAS
HF_TOKEN = "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"

print("🚀 Conectando ao servidor gratuito do Hugging Face...")
# Iniciando o cliente apontando para o modelo FLUX.1-Schnell (gratuito por lá)
client = InferenceClient("runwayml/stable-diffusion-v1-5", token=HF_TOKEN)
Planilha de Leads instagram
# Seu prompt para a imagem
meu_prompt = "Cinematic shot of a cybernetic jaguar walking through a neon-lit Amazon rainforest, cyberpunk style, 8k resolution, photorealistic"

try:
    print("🎨 Gerando sua imagem... Aguarde uns segundos.")
    # Faz a requisição para o modelo
    image_bytes = client.text_to_image(meu_prompt)
    
    # Converte os bytes recebidos em uma imagem real e salva no seu computador
    image = Image.open(io.BytesIO(image_bytes))
    nome_arquivo = "resultado_jaguar.jpg"
    image.save(nome_arquivo)
    
    print(f"🎉 Sucesso total! A imagem foi salva na sua pasta com o nome: {nome_arquivo}")

except Exception as e:
    print(f"❌ Ocorreu um erro: {e}")