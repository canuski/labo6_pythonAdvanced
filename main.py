import sys
from server import *


def keuzeMenu():
    while True:
        print("[bold green]a)[/bold green] Servers toevoegen")
        print("[bold yellow]b)[/bold yellow] Servers verwijderen")
        print("[bold blue]c)[/bold blue] Lijst tonen van de servers")
        print(
            "[bold magenta]d)[/bold magenta] Toon de opties voor commandline-argumenten")
        print("[bold red]e)[/bold red] Exit en slaag op in json")
        keuze = input("Geef je keuze in: ")

        if keuze == "a":
            serverToevoegen()
        elif keuze == "b":
            serverVerwijderen()
        elif keuze == "c":
            serverLijst()
        elif keuze == "d":
            keuzeCmdLine()
        elif keuze == "e":
            serversToJson(servers)
            print("[bold]bye[/bold]")
            break
        else:
            print("[bold red]Ongeldige keuze. Probeer opnieuw.[/bold red]")


def keuzeCmdLine():
    opties = ['toevoegen', 'verwijder', 'lijst', 'check', 'admin']
    print("Gebruik deze argumenten bij het opstarten van de script (python main.py toevoegen)")
    print("Opties:")
    for item in opties:
        print(item)


def cmdLine(argv):
    if len(argv) > 1:
        actie = argv[1]
        if actie == 'toevoegen':
            serverToevoegen()
        elif actie == 'verwijder':
            serverVerwijderen()
        elif actie == 'lijst':
            serverLijst()
        elif actie == 'check':
            serverLijst()
            serverKeuze = input(
                "Geef de naam van de server die je wil pingen: ")
            addressKeuze = serverIpFinder(serverKeuze)
            print(f'De server {serverKeuze}, met ip adres {addressKeuze}')
            pingServer(addressKeuze, serverKeuze)
        elif actie == 'admin':
            keuzeMenu()
        else:
            print("Ongeldige keuze, probeer opnieuw")
    else:
        keuzeMenu()  # als er geen cmd is dan voer dit uit


cmdLine(sys.argv)
