import typer

from myshopify.scraping.brother import get_product_from_product_page

app = typer.Typer()


@app.command()
def hello(name: str):
    typer.echo(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


@app.command()
def brother(url: str, dst: str) -> None:
    get_product_from_product_page(url=url)


if __name__ == "__main__":
    app().command("brother", "https://sewingcraft.brother.eu/de-at/produkte/maschinen/sewing-machines/beginner-sewing-machines/kd40")

