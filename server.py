import json
from ping3 import ping, verbose_ping
from bs4 import BeautifulSoup
from rich import print, progress


def jsonToServers():
    try:
        with open("data.json", "r") as json_file:
            # json.load doet json data naar list data in python
            return json.load(json_file)
    except:
        return []  # als het niet werkt return een lege string


def serversToJson(data):
    with open("data.json", "w") as json_file:
        # json.dump doet alle data in json vorm
        json.dump(data, json_file, indent=2)


def serverIpFinder(serverKeuze):
    with open("data.json", "r") as json_file:
        data = json.load(json_file)
        for item in data:
            if item.get("name") == serverKeuze:
                return item.get("address")

        return item.get("address")


def pingServer(ipOfServer, nameOfServer):
    check = ping(f'{ipOfServer}')
    verbose_ping(f'{ipOfServer}')
    if check == False:
        print("[red]Host unknown, cannot resolve[/red]")
        res = "Host unknown, cannot resolve"
    elif check == None:
        print("[yellow]Request timed out, no reply[/yellow]")
        res = "Request timed out, no reply"
    # checkt of check een int of een float is
    elif isinstance(check, (float, int)):
        print("[green]Ping is gelukt, server is online![/green]")
        res = "Ping is gelukt, server is online!"
    else:
        print("[red]Er is iets fout gegaan, probeer opnieuw[/red]")
        res = "Error"
    name = nameOfServer
    address = ipOfServer
    pingToJson(name, address, res)


def pingToJson(name, address, checkResult):
    try:
        with open("check.json", "r") as json_file:
            # alles dat al bestaat uitlezen en in de data steken
            data = json.load(json_file)
    except:
        data = []
    pingData = {'name': name, 'address': address, 'result': checkResult}
    data.append(pingData)  # de nieuwe data ook toevoegen
    with open("check.json", "w") as json_file:
        # nieuwste data naar json sturen adhv json.dump
        json.dump(data, json_file, indent=2)
    updateHTML(pingData)


def updateHTML(pingData):
    with open("index.html", "r") as html_file:
        inhoud = BeautifulSoup(html_file, "html.parser")
    # credits aan internet voor BeautifulSoup te geven
    ul_tag = inhoud.find("ul")
    li_tag = inhoud.new_tag("li")
    li_tag.string = f"Name:{pingData['name']}, Address: '{pingData['address']}', Result: {pingData['result']}"

    if f"{pingData['result']}" == "Ping is gelukt, server is online!":
        li_tag['class'] = "ping ping-works"
    elif f"{pingData['result']}" == "Request timed out, no reply":
        li_tag['class'] = "ping ping-noRes"
    else:
        li_tag['class'] = "ping ping-fail"

    ul_tag.insert_after(li_tag)

    with open("index.html", "w") as html_file:
        html_file.write(inhoud.prettify())


servers = jsonToServers()


def serverToevoegen():
    name = input("Naam van de server: ")
    address = input("IP-adres van de server: ")
    server = {'name': name, 'address': address}
    servers.append(server)
    print(f"Server: '{name}' ({address}) is toegevoegd.")


def serverVerwijderen():
    serverLijst()
    invoer = input("Geef de naam van de server in om te verwijderen: ")
    for server in servers:
        if invoer == server['name']:
            del servers[servers.index(server)]


def serverLijst():
    print("[blue]Server list:[/blue]")
    for server in servers:
        print(
            f"[cyan]Naam=[/cyan] {server['name']}, [cyan]ip-adres=[/cyan] {server['address']}")
