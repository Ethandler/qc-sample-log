# app/cli.py
import typer
from .allocator import reserve

app = typer.Typer()

@app.command()
def allocate(material: str, qty: int = 1):
    """Reserve sample IDs for a material."""
    ids = reserve(material, qty)
    for sid in ids:
        typer.echo(sid)
