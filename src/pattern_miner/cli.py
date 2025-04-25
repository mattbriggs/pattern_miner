import click
from pathlib import Path
from .miner import PatternMiner

@click.command()
@click.argument('docs_path', type=click.Path(exists=True, file_okay=False))
@click.argument('output_path', type=click.Path())
def main(docs_path, output_path):
    """Mine patterns from DOCS_PATH and write results to OUTPUT_PATH."""
    miner = PatternMiner()
    miner.mine(Path(docs_path))
    miner.export(Path(output_path))
    click.echo(f"Pattern language written to {output_path}")

if __name__ == '__main__':
    main()
