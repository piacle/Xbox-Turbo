from threading import Thread
from json import load, dumps
from re import match
from os import path
import warnings

from asyncio import run
from concurrent.futures import ThreadPoolExecutor
from textual.app import App, ComposeResult
from textual.widgets import Input


from api import Auth, Turbo
from util.alignment import center, center_y
warnings.simplefilter("ignore", ResourceWarning)
configuration = load(open("data/configuration.json"))
placeholder = ""
limit = 0



class InputTextbox(App):
    CSS_PATH = "input.css"

    @staticmethod
    def valid(value) -> bool:
        if placeholder == "Gamertag":
            return not match("[a-zA-Z0-9 ]", value) or value[0] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                                                        '9']
        elif placeholder == "Threads":
            try:
                int(value)
            except ValueError:
                return False
            else:
                return int(value) >= 1

    @staticmethod
    def compose() -> ComposeResult:
        yield Input(placeholder=placeholder, id="inp")

    async def on_input_changed(self, message: Input.Changed):
        if placeholder == "Gamertag" and len(message.value) > limit:
            self.query_one("#inp", Input).value = message.value[:limit].strip()

    async def on_input_submitted(self):
        if self.valid(self.query_one("#inp", Input).value.strip()):
            self.exit(self.query_one('#inp', Input).value.strip())
        else:
            self.console.print(
                "Invalid Value!", justify='right', style='white on #000000')


def configure(key, console):
    console.print(
        f"[[bold grey93]*[/bold grey93]] {key}: ", end="", highlight=False)
    btc = input()
    configuration[key] = btc
    with open("data/configuration.json", 'w') as w:
        w.write(dumps(configuration, indent=4))
    return btc


class Runner:
    def __init__(self):
        global limit
        self.turbo = Turbo()
        self.console, self.valid, self.gamertagSystem, self.auth, self.accounts = self.turbo.console, {
            "gamertagSystem": ["new", "old"], "auth": ["accounts", "tokens"]}, configure('gamertagSystem',
                                                                                         self.console) if not configuration.get(
            'gamertagSystem') else configuration["gamertagSystem"], configure('auth',
                                                                              self.console) if not configuration.get(
            'auth') else configuration["auth"], configure('accounts', self.console) if not configuration.get(
            'accounts') else configuration["accounts"]
        limit = 12 if self.gamertagSystem == "new" else 15
        self.console.clear()

    def check(self):
        errors = [
            f"[-] {key} invalid option, valid ones are: " +
            ", ".join(self.valid[key])
            for key in self.valid
            if configuration[key] not in self.valid[key]
        ]
        if not path.isfile(self.accounts):
            errors.append("[[bold red]-[/bold red]] accounts invalid path")
        return errors

    def start(self):
        global placeholder
        errors = self.check()
        if len(errors) != 0:
            self.console.print(center("\n".join(
                errors) + "\n[*] Edit data/configuration.json to fix errors\nPress enter to exit..."),
                highlight=False)
            input()
            exit(-1)

        if self.turbo.tag is None:
            placeholder = "Gamertag"
            inputt = InputTextbox()
            capturedinput100 = inputt.run()
            if capturedinput100 is None:
                raise SystemExit
            self.turbo.tag = capturedinput100
            del capturedinput100
            self.turbo.rd, self.turbo.cd = {"classicGamertag": self.turbo.tag,
                                            "targetGamertagFields": "classicGamertag"} if limit == 15 else {
                "gamertag": self.turbo.tag, "targetGamertagFields": "gamertag"}, {
                "gamertag": {"classicGamertag": self.turbo.tag}, "preview": False,
                "useLegacyEntitlement": False} if limit == 15 else {
                "gamertag": {"gamertag": self.turbo.tag, "gamertagSuffix": "", "classicGamertag": self.turbo.tag},
                "preview": False, "useLegacyEntitlement": False}
        
        self.console.clear()

        if self.turbo.threads is None:
            placeholder = "Threads"
            capturedinput100 = InputTextbox().run()
            if capturedinput100 is None:
                raise SystemExit
            self.turbo.threads = int(capturedinput100)
            del capturedinput100
        
        load_accounts = Auth(self.accounts)
        f = ThreadPoolExecutor().submit(run, load_accounts.combolist() if self.auth == "accounts" else load_accounts.jwt())
        while load_accounts.count != load_accounts.amount:
            self.console.print(
                f"[[bold grey85]*[/bold grey85]] Loaded accounts: [[bold grey85]{load_accounts.count}[/bold grey85]/[bold grey85]{load_accounts.amount}[/bold grey85]]{' ' * load_accounts.amount}", end="\r", highlight=None)

        self.turbo.accounts, failed = f.result()
        self.console.clear()
        if len(self.turbo.accounts) == 0:
            self.console.print(
                f"{center_y()}[[bold grey85]*[/bold grey85]] Get{' VALID' if failed > 0 else ''} {'accounts' if self.auth == 'accounts' else 'tokens'} then use this.\nPress enter to exit.", highlight=None, justify='center')
            input()
            exit(-1)
        self.console.print(
            f"{center_y()}[[bold grey85]+[/bold grey85]] Loaded {len(self.turbo.accounts)} account(s)\n[[bold grey85]*[/bold grey85]] Failed Loading: {failed} account(s)\nPress enter to start.\n\n{self.turbo.accounts}", highlight=False, justify='center')
        self.console.input()
        self.console.clear()
        self.console.print(
            f"{center_y()}[bold grey85]{self.turbo.banner}[/bold grey85]\n", justify='center')
        Thread(target=run, daemon=True, args=[self.turbo.info()]).start()
        [Thread(target=run, daemon=True, args=[self.turbo.reserve()]).start()
         for _ in range(self.turbo.threads)]
        while True:
            try:
                pass
            except (KeyboardInterrupt, EOFError):
                exit(0)


if __name__ == '__main__':
     Runner().start()
