from threading import Thread
from json import load, dumps
from re import match
from os import system, path
from asyncio import run
from auth import Auth
from turbo import Turbo
from concurrent.futures import ThreadPoolExecutor
configuration = load(open("configuration.json"))
system("cls||clear")
def inpppppppppppp(key, console):
    console.print(f"[[bold grey93]*[/bold grey93]] {key}: ", end="", highlight=False)
    keyinp = input()
    configuration[key] = keyinp
    with open("configuration.json", 'w') as w:
        w.write(dumps(configuration, indent=4))
    return keyinp

class Runner:
    def __init__(self) -> None:
        self.turbo = Turbo()
        self.console, self.vaild, self.gamertagSystem, self.auth, self.accounts = self.turbo.console, {"gamertagSystem": ["new", "old"], "auth": ["accounts", "tokens"]}, inpppppppppppp('gamertagSystem', self.console) if not configuration.get('gamertagSystem') else configuration["gamertagSystem"], inpppppppppppp('auth', self.console) if not configuration.get('auth') else configuration["auth"], inpppppppppppp('accounts', self.console) if not configuration.get('accounts') else configuration["accounts"]
        self.limit = 12 if self.gamertagSystem == "new" else 15
    async def check(self):
        errors = []
        for key in self.vaild:
            if configuration[key] not in self.vaild[key]:
                errors.append(f"[[bold red]-[/bold red]] {key} invaild option, vaild ones are: " + ", ".join(self.vaild[key]))
        if path.isfile(self.accounts) != True:
            errors.append("[[bold red]-[/bold red]] accounts invaild path")
        return errors

    async def start(self):
        with self.console.status(status="[bold grey85]Checking config[/bold grey85]", spinner='material'):
            errors = await self.check()
        if len(errors) != 0:
            self.console.print("\n".join(errors) + f"\n[[bold grey93]*[/bold grey93]] Edit configuration.json to fix errors\nPress enter to exit...", highlight=False)
            input()
            exit(-1)
        aU = Auth(self.accounts)
        a = len(open(self.accounts).read().splitlines())
        if self.turbo.tag == None:
            self.console.print(f"[bold grey93]{self.turbo.banner}[/bold grey93]\n[[bold grey85]*[/bold grey85]] Gamertag: ", end="", highlight=None)
            temp12831 = input().strip()
            if len(temp12831) > self.limit:
                system("cls||clear")
                self.console.print(f"[[bold red]-[/bold red]] Gamertag is greater than {self.limit}",highlight=None)
                await self.start()
            else:
                if not match("[a-zA-Z0-9 ]", temp12831) or temp12831[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or temp12831 == "": 
                    system("cls||clear")
                    self.console.print(f"[[bold red]-[/bold red]] Invaild Gamertag", highlight=None)
                    await self.start()
                else:
                    self.turbo.tag = temp12831;temp12831=None;del temp12831
                    self.turbo.rd, self.turbo.cd = {"classicGamertag": self.turbo.tag, "targetGamertagFields": "classicGamertag"} if self.limit == 15 else {"gamertag": self.turbo.tag, "targetGamertagFields": "gamertag"}, {"gamertag": {"classicGamertag": self.turbo.tag}, "preview": False, "useLegacyEntitlement": False} if self.limit == 15 else {"gamertag": {"gamertag": self.turbo.tag, "gamertagSuffix": "", "classicGamertag": self.turbo.tag}, "preview": False, "useLegacyEntitlement": False}
        
        if self.turbo.threads == None:
            self.console.print(f"[[bold grey85]*[/bold grey85]] Threads: ", end="", highlight=None)
            try:
                t = int(input());self.turbo.threads=t;t=None;del t
            except Exception as e:
                system("cls||clear")
                self.console.print(f"[[bold red]*[/bold red]] {e}",highlight=None)
                await self.start()
        
        f = ThreadPoolExecutor().submit(run, aU.combolist() if self.auth=="accounts" else aU.jwt())
        while aU.count != a:
            self.console.print(f"[[bold grey85]*[/bold grey85]] Loaded accounts: [[bold grey85]{aU.count}[/bold grey85]/[bold grey85]{a}[/bold grey85]]{' '*a}", end="\r", highlight=None)
        self.turbo.accounts, failed = f.result()
        if len(self.turbo.accounts) == 0:
            self.console.print(f"[[bold grey85]*[/bold grey85]] Get{' VAILD' if failed > 0 else ''} {'accounts' if self.auth == 'accounts' else 'tokens'} then use this.{'       '*a}", highlight=None)
            input()
            exit(-1)
        self.console.print(f"[[bold grey85]+[/bold grey85]] Loaded {len(self.turbo.accounts)} account(s){'        '*a}\n[[bold grey85]*[/bold grey85]] Failed Loading: {failed} account(s)\n", highlight=False)
        input("Press enter whenever your ready...")
        system("cls||clear")
        self.console.print(f"[bold grey93]{self.turbo.banner}[/bold grey93]")
        Thread(target=run, daemon=True, args=[self.turbo.info()]).start()
        [Thread(target=run, daemon=True, args=[self.turbo.reserve()]).start() for _ in range(self.turbo.threads)]
        while True: 
            try:
                pass
            except (KeyboardInterrupt, EOFError):
                exit(0)
run(Runner().start())
