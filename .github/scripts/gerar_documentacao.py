import os
import yaml
import csv
from datetime import datetime
from github import Github  # Importe a biblioteca PyGithub para interagir com a API do GitHub

def carregar_repositorios(caminho_repos_yaml):
    with open(caminho_repos_yaml, 'r') as file:
        repos_yaml = yaml.safe_load(file)
    return repos_yaml['repos']

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

def exportar_documentacao_para_csv(repositorios):
    # Caminho do diretório de trabalho
    diretorio_raiz = os.environ['GITHUB_WORKSPACE']
    
    # Diretório de saída para os arquivos CSV
    diretorio_saida = os.path.join(diretorio_raiz, 'documentation')

    # Loop através dos repositórios listados
    for repo_info in repositorios:
        repo_nome = repo_info['name']
        repo_url = repo_info['url']

        # Diretório do repositório clonado
        diretorio_repo = os.path.join(diretorio_raiz, 'temp_repo')

        # Clonar o repositório
        os.system(f'git clone --depth 1 {repo_url} {diretorio_repo}')

        # Diretório .konecty_docs dentro do repositório clonado
        diretorio_konecty_docs = os.path.join(diretorio_repo, '.konecty_docs')

        # Verificar se o diretório .konecty_docs existe
        if os.path.exists(diretorio_konecty_docs):
            # Caminho completo para process.yaml e services.yaml
            caminho_process_yaml = os.path.join(diretorio_konecty_docs, 'process.yaml')
            caminho_services_yaml = os.path.join(diretorio_konecty_docs, 'services.yaml')

            # Verificar se os arquivos process.yaml e services.yaml existem
            if os.path.exists(caminho_process_yaml) and os.path.exists(caminho_services_yaml):
                # Criar diretório de documentação para o repositório
                diretorio_documentacao_repo = os.path.join(diretorio_saida, repo_nome)
                os.makedirs(diretorio_documentacao_repo, exist_ok=True)

                # Exportar process.yaml para CSV
                exportar_para_csv(carregar_template(caminho_process_yaml), diretorio_documentacao_repo)

                # Exportar services.yaml para CSV
                exportar_para_csv(carregar_template(caminho_services_yaml), diretorio_documentacao_repo)

                # Commit dos arquivos gerados
                mensagem_commit = f"Adicionando arquivos de documentação CSV para {repo_nome}"
                commit_arquivos(diretorio_documentacao_repo, mensagem_commit)
            else:
                print(f"Arquivos process.yaml e/ou services.yaml não encontrados em {repo_url}")
        else:
            print(f"Diretório .konecty_docs não encontrado em {repo_url}")

        # Remover o diretório temporário do repositório clonado
        os.system(f'rm -rf {diretorio_repo}')

if __name__ == "__main__":
    # Caminho do arquivo repos_documentation.yaml
    caminho_repos_yaml = os.path.join(os.environ['GITHUB_WORKSPACE'], 'repos_documentation.yaml')

    # Carregar os repositórios listados no YAML
    repositorios = carregar_repositorios(caminho_repos_yaml)

    # Exportar documentação para CSVs
    exportar_documentacao_para_csv(repositorios)

    print("Exportação de documentação para CSV concluída!")
