import typer
from typing import Optional
from pathlib import Path
from typer.colors import RED, WHITE

app = typer.Typer()


@app.command('run')
def main(extension : str, 
         directory : Optional[str] = typer.Argument(None, help="Le chemin dans lequel chercher"),
         delete : bool = typer.Option(False, help="Supprime les fichiers trouvés")):
    """Main script"""

    if not directory:
        directory = Path.cwd()  # chemin depuis lequel on lance le script
    else:
        directory = Path(directory)

    if not directory.exists():
        typer.secho(f"Le dossier {directory} n'existe pas.", fg=typer.colors.RED)
        raise typer.Exit()

    files=directory.rglob(f"*.{extension}")
    if delete:
        typer.confirm("Souhaitez-vous vraiment supprimer les fichiers ?", abort=True)
        for file in files:
            file.unlink()
            typer.secho(f"Le fichier {file} a bien été supprimé !", 
                        fg=typer.colors.RED, bold=True)
    else:
        typer.secho(f"Fcihiers trouvés avec l'extension {extension} : ", bold=True, 
        bg=typer.colors.BRIGHT_BLUE, fg=typer.colors.WHITE)
        for file in files:
            typer.echo(file)


@app.command()
def search(extension: str):
    """Cherche les fichiers avec extension donnée."""
    main(extension=extension, directory=None, delete=False)


@app.command()
def delete(extension: str):
    """Supprime les fichiers avec extension donnée"""
    main(extension=extension, directory=None, delete=True)


if __name__ == "__main__":
    app()
