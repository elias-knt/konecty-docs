import os
import yaml
import csv
from datetime import datetime

def carregar_template(caminho_template):
    with open(caminho_template, 'r') as file:
        template = yaml.safe_load(file)
    return template

def exportar_para_csv(template, diretorio_saida):
    os.makedirs(diretorio_saida, exist_ok=True)

    for section, items in template.items():
        if not isinstance(items, list):
            continue

        csv_path = os.path.join(diretorio_saida, f"{section.lower().replace(' ', '_')}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            # Definindo cabeçalhos dinamicamente
            headers = set()
            for item in items:
                headers.update(item.keys())

            headers = sorted(headers)  # Ordena os cabeçalhos para consistência
            writer.writerow(headers)

            # Escrevendo os dados
            for item in items:
                row = []
                for header in headers:
                    value = item.get(header, '')
                    if isinstance(value, list):
                        row.append(', '.join(value))  # Une listas em uma string separada por vírgulas
                    else:
                        row.append(str(value))  # Converte para string caso não seja uma lista
                writer.writerow(row)

def commit_arquivos(diretorio_raiz, mensagem_commit):
    os.chdir(diretorio_raiz)
    os.system('git add .')
    os.system(f'git commit -m "{mensagem_commit}"')

# Caminhos dos arquivos
diretorio_raiz = os.environ['GITHUB_WORKSPACE']
caminho_template = os.path.join(diretorio_raiz, '.github', 'templates', 'template_documentacao.yaml')
diretorio_saida = os.path.join(diretorio_raiz, 'repo-documentation')

# Carregar o template YAML
template = carregar_template(caminho_template)

# Exportar para CSV por seção
exportar_para_csv(template, diretorio_saida)

# Fazer commit dos arquivos gerados
mensagem_commit = "Adicionando arquivos de documentação CSV por seção"
commit_arquivos(diretorio_saida, mensagem_commit)

print("Exportação para CSV por seção concluída e arquivos commitados com sucesso!")
