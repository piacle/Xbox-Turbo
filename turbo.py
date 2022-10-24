from os import name, system
from random import randint
if name == "nt":
    from asyncio import set_event_loop_policy, WindowsSelectorEventLoopPolicy, sleep
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())
else:
    from asyncio import sleep
from aiohttp import ClientSession
from rich.console import Console
from webhook import Webhook

class Turbo:
    def __init__(self) -> None:
        self.reservation, self.claim, self.requests, self.ratelimits, self.errors, self.claimed, self.console, self.accounts, self.threads, self.tag, self.rd, self.cd, self.new_account, self.banner = "https://gamertag.xboxlive.com/gamertags/reserve", "https://accounts.xboxlive.com/users/current/profile/gamertag", 0, 0, 0, False, Console(), [], None, None, {}, {}, None, '\n⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⣠⠾⠛⠶⣄⢀⣠⣤⠴⢦⡀⠀⠀⠀⠀\n⠀⠀⠀⢠⡿⠉⠉⠉⠛⠶⠶⠖⠒⠒⣾⠋⠀⢀⣀⣙⣯⡁⠀⠀⠀⣿⠀⠀⠀⠀\n⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⢸⡏⠀⠀⢯⣼⠋⠉⠙⢶⠞⠛⠻⣆⠀⠀⠀\n⠀⠀⠀⢸⣧⠆⠀⠀⠀⠀⠀⠀⠀⠀⠻⣦⣤⡤⢿⡀⠀⢀⣼⣷⠀⠀⣽⠀⠀⠀\n⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⢏⡉⠁⣠⡾⣇⠀⠀⠀\n⠀⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠋⠉⠀⢻⡀⠀⠀\n⣀⣠⣼⣧⣤⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠐⠖⢻⡟⠓⠒\n⠀⠀⠈⣷⣀⡀⠀⠘⠿⠇⠀⠀⠀⢀⣀⣀⠀⠀⠀⠀⠿⠟⠀⠀⠀⠲⣾⠦⢤⠀\n⠀⠀⠋⠙⣧⣀⡀⠀⠀⠀⠀⠀⠀⠘⠦⠼⠃⠀⠀⠀⠀⠀⠀⠀⢤⣼⣏⠀⠀⠀\n⠀⠀⢀⠴⠚⠻⢧⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠞⠉⠉⠓⠀⠀\n⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠛⠶⠶⠶⣶⣤⣴⡶⠶⠶⠟⠛⠉⠀⠀⠀⠀⠀⠀⠀\n'

    async def success(self, opttext=""):
        [system("cls||clear") for _ in range(10)]
        self.console.print(f"[bold grey93]{self.banner}[/bold grey93]\n[[bold grey85]*[/bold grey85]] Request(s): [bold grey85]{self.requests}[/bold grey85] | R/s: [bold grey85]{self.rn}[/bold grey85] | Ratelimit(s): [bold grey85]{self.ratelimits}[/bold grey85] | Errors: [bold grey85]{self.errors}[/bold grey85] | Threads: [bold grey85]{self.threads}[/bold grey85]\n\n[[bold grey85]*[/bold grey85]] Claimed: {self.tag}\n[[bold grey85]*[/bold grey85]] Email: {self.new_account[0]}\n[[bold grey85]*[/bold grey85]] XUID: {self.new_account[1]}\n{opttext}", end="​"*24+"\n", highlight=False)
        try:
            await Webhook(vars(self)).push()
        except:
            self.console.print("[[bold grey85]-[/bold grey85]] Failed sending message to webhook(s)", end="​"*24+"\n", highlight=False)
        input()
        exit(0)
    async def X_X(self, session, token,resid,xuid,mscv):
        async with session.post(self.reservation, headers={'MS-CV':mscv, 'x-xbl-contract-version': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'Authorization': token}, json={"gamertag": self.tag, "targetGamertagFields": "gamertag", "reservationId": resid}) as rxy4:
            self.requests += 1
            if rxy4.status == 200:
                await self.claimgt(session,token,resid,xuid,mscv,"[[bold grey85]*[/bold grey85]] Had to use new gamertag system sorry :/")
            elif rxy4.status == 429:
                self.ratelimits += 1
                await sleep((await rxy4.json())["periodInSeconds"])
                await self.X_X(session, token, resid, xuid, mscv)
            else:
                self.errors += 1
                await self.X_X(session, token, resid, xuid, mscv)
    async def uuiderrorthing(self, session, token, resid, xuid, mscv):
        async with session.post(self.reservation, headers={'MS-CV':mscv, 'x-xbl-contract-version': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'Authorization': token}, json={**self.rd, "reservationId": resid}) as rx:
            self.requests += 1
            if rx.status == 200:
                if (await rx.json())["classicGamertag"] == self.tag:
                    fuhhh, fuhhhh = {
                        **self.rd, "reservationId": resid}, {**self.cd, "reservationId": resid}
                    async with session.post(self.claim, headers={'MS-CV':mscv, 'x-xbl-contract-version': '6', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'Authorization': token},json={"reservationId":0,"gamertag":"","preview":True,"useLegacyEntitlement":False}) as t3:
                        if (t3.status == 200 and (await t3.json())["hasModernGamertag"] == False) and len(self.tag) <= 12:
                                self.cd = {"gamertag": {"gamertag": self.tag, "gamertagSuffix": "", "classicGamertag": self.tag}, "preview": False, "useLegacyEntitlement": False}
                                await self.X_X(session,token,resid,xuid,mscv)
                        else:
                            self.claimed = True
                            system("cls||clear")
                            self.console.print(f"[bold grey93]{self.banner}[/bold grey93]\n[[bold grey85]*[/bold grey85]] Now I dont know what this shit is and I'm too lazy to find out but its on the reservation id {resid} its prob payment required\nIf the account changed to the new system go to [link=https://social.xbox.com]social.xbox.com/changegamertag[/link] with the account that has the xuid of {xuid}\nChange the body in the reserve request to {fuhhh} and proceed\nChange request body for reference: {fuhhhh}\nIf not retry in a hour i think because im retard xDDDDD (would've changed to new gamertag system if 12 chars or less + I dont even know if the thing i said works LOL!)\n")

            elif rx.status == 429:
                await sleep((await rx.json())["periodInSeconds"])
                await self.uuiderrorthing(session, token, resid, xuid, mscv)
            else:
                self.errors += 1
                await self.uuiderrorthing(session, token, resid, xuid, mscv)

    async def info(self):
        while self.claimed is False:
            self.rn = self.requests
            await sleep(1)
            self.rn = self.requests - self.rn
            self.console.print(f"[[bold grey85]*[/bold grey85]] Request(s): [bold grey85]{self.requests}[/bold grey85] | R/s: [bold grey85]{self.rn}[/bold grey85] | Ratelimit(s): [bold grey85]{self.ratelimits}[/bold grey85] | Errors: [bold grey85]{self.errors}[/bold grey85] | Threads: [bold grey85]{self.threads}[/bold grey85] | Gamertag: [bold grey85]{self.tag}[/bold grey85]", end="\r", highlight=False)
        exit(0)

    async def claimgt(self, session, token, resid, xuid, mscv, opttext=""):
        async with session.post(self.claim, headers={"MS-CV":mscv,"Authorization": token, "x-xbl-contract-version": "6", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}, json={**self.cd, "reservationId": resid}) as r:
            self.requests += 1
            if r.status == 200:
                self.claimed = True
                async with session.get("https://accounts.xboxlive.com/users/current/profile", headers={"Authorization": token, "x-xbl-contract-version": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}) as rsp:
                    self.new_account = [(await rsp.json())["email"], xuid]
                await self.success(opttext)
            elif r.status == 429:
                self.ratelimits += 1
            elif r.status == 403:
                if (await r.json())["code"] == 5025 and (await r.json())["description"] == "272abc3c-8b49-469f-b589-72eaa902fa64":
                    await self.uuiderrorthing(session, token, resid, xuid, mscv)
            else:
                self.errors += 1

    async def reserve(self):
        async with ClientSession() as session:
            while self.claimed is False:
                try:
                    for token, xuid in self.accounts:
                        resid = str(randint(xuid*2, xuid*4))
                        async with session.post(self.reservation, headers={'x-xbl-contract-version': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36', 'Authorization': token}, json={**self.rd, "reservationId": resid}) as r:
                            self.requests += 1
                            if (r.status == 200 and (await r.json())["classicGamertag"] == self.tag):
                                await self.claimgt(session, token, resid, xuid, r.headers["MS-CV"])
                            elif r.status == 429:
                                self.ratelimits += 1
                            elif r.status == 409:
                                pass
                            else:
                                self.errors += 1
                except Exception as e:
                    print(e)
        exit(0)
