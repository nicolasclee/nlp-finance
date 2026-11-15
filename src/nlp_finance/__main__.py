# Comandos do projeto: python -m nlp_finance.

import argparse
import json
from pathlib import Path

from .data import prepare


# Lê os argumentos do terminal e inicia a preparação dos dados.
def main() -> None:
    parser = argparse.ArgumentParser(description="Preparação do experimento BANKING77")
    subparsers = parser.add_subparsers(dest="command", required=True)
    data = subparsers.add_parser("prepare", help="Auditar e dividir os arquivos oficiais")
    data.add_argument("--train", type=Path, required=True, help="CSV do treino oficial")
    data.add_argument("--test", type=Path, required=True, help="CSV do teste oficial")
    data.add_argument("--revision", required=True, help="Revisão imutável da origem")
    data.add_argument(
        "--output", type=Path, required=True, help="Diretório novo para os artefatos"
    )
    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare(args.train, args.test, args.output, args.revision)
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
