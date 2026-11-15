# Comandos do projeto: python -m nlp_finance.

import argparse
import json
from pathlib import Path

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

    diagnostic = subparsers.add_parser("diagnose", help="Medir comprimento, memória e velocidade")
    diagnostic.add_argument("--preparation", type=Path, required=True)
    diagnostic.add_argument("--revisions", type=Path, required=True, help="JSON com revisão de cada modelo")
    diagnostic.add_argument("--output", type=Path, required=True)
    diagnostic.add_argument("--device", default="cuda")

    train = subparsers.add_parser("train", help="Executar uma tentativa de treinamento")
    train.add_argument("--preparation", type=Path, required=True)
    train.add_argument("--diagnostic", type=Path, required=True)
    train.add_argument("--config", type=Path, required=True, help="JSON da configuração da execução")
    train.add_argument("--output", type=Path, required=True)

    freeze = subparsers.add_parser("freeze", help="Selecionar configurações e congelar limiares")
    freeze.add_argument("--preparation", type=Path, required=True)
    freeze.add_argument("--runs", type=Path, nargs=12, required=True)
    freeze.add_argument("--output", type=Path, required=True)

    evaluate = subparsers.add_parser("evaluate", help="Avaliar o procedimento congelado no teste")
    evaluate.add_argument("--preparation", type=Path, required=True)
    evaluate.add_argument("--frozen", type=Path, required=True)
    evaluate.add_argument("--output", type=Path, required=True)
    evaluate.add_argument("--device", default="cuda")

    report = subparsers.add_parser("report", help="Consolidar métricas, figuras e exemplos")
    report.add_argument("--preparation", type=Path, required=True)
    report.add_argument("--frozen", type=Path, required=True)
    report.add_argument("--evaluation", type=Path, required=True)
    report.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()
    if args.command == "prepare":
        from .data import prepare_banking77_data

        result = prepare_banking77_data(args.train, args.test, args.output, args.revision)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "diagnose":
        from .hardware_diagnostic.run import run_diagnostic

        revisions = json.loads(args.revisions.read_text(encoding="utf-8"))
        result = run_diagnostic(args.preparation, revisions, args.output, args.device)
        print(json.dumps({"status": result["status"], "output": str(args.output)}, ensure_ascii=False))
    elif args.command == "train":
        from .experiment import train_one

        config = json.loads(args.config.read_text(encoding="utf-8"))
        result = train_one(args.preparation, args.diagnostic, config, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "freeze":
        from .freeze import freeze_protocol

        freeze_protocol(args.preparation, args.runs, args.output)
        print(f"Protocolo congelado em {args.output}")
    elif args.command == "evaluate":
        from .final_evaluation import evaluate_frozen

        evaluate_frozen(args.preparation, args.frozen, args.output, args.device)
        print(f"Resultados salvos em {args.output}")
    elif args.command == "report":
        from .report import create_report

        create_report(args.preparation, args.frozen, args.evaluation, args.output)
        print(f"Relatório salvo em {args.output}")


if __name__ == "__main__":
    main()
