# Automação de Geração de Documentação

Este repositório contém a automação para geração de documentação a partir de arquivos YAML encontrados em diferentes repositórios do GitHub. A automação é realizada por meio de GitHub Actions, que processa os arquivos YAML especificados nos repositórios listados em `repos.yaml`.

## Estrutura do Repositório

- `.github/workflows/documentation.yml`: Definição da GitHub Action responsável por executar a automação.
- `repos.yaml`: Arquivo YAML que lista os repositórios nos quais a automação buscará os arquivos de documentação.
- `documentation/`: Pasta que contém a documentação gerada.
  - `<nome_do_repo>/`: Subpasta para cada repositório listado em `repos.yaml`.
    - `services.csv`: Arquivo gerado a partir do `services.yaml` encontrado em `.konecty_docs`.
    - `process.csv`: Arquivo gerado a partir do `process.yaml` encontrado em `.konecty_docs`.

## Funcionamento da Automação

A GitHub Action definida (`documentation.yml`) é acionada em intervalos programados ou em eventos específicos (por exemplo, push para o repositório `repos.yaml`). A action realiza o seguinte processo:

1. **Leitura de `repos.yaml`:** Identifica os repositórios especificados para busca de documentação.
2. **Processamento por Repositório:**
   - Para cada repositório listado:
     - Busca pela pasta `.konecty_docs`.
     - Encontra os arquivos `services.yaml` e `process.yaml`.
     - Gera os arquivos CSV correspondentes (`services.csv` e `process.csv`).
     - Salva os arquivos gerados na pasta `documentation/<nome_do_repo>/`.
3. **Atualização da Documentação:** Os arquivos CSV gerados são automaticamente atualizados no repositório de documentação.

## Como Configurar

Para configurar ou modificar a automação, edite `repos.yaml` para adicionar ou remover repositórios. Certifique-se de que cada repositório contenha a pasta `.konecty_docs` com os arquivos `services.yaml` e `process.yaml`.

