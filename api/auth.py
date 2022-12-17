# i skid this  | https://github.com/tropicbliss/xboxlive-auth/blob/main/src/xbox.rs
from re import search
from urllib.parse import unquote
from aiohttp import ClientSession


class Auth:
    def __init__(self, accounts) -> None:
        self.count = 0
        self.failed = 0
        self.accounts = set(open(accounts).read().splitlines())
        self.amount = len(self.accounts)

    async def combolist(self) -> tuple:
        b = []
        for account in self.accounts:
            account = account.strip("\n").split(":")
            email = account[0]
            password = ":".join(account[1:])
            async with ClientSession() as sesh:
                async with sesh.get(
                        "https://login.live.com/oauth20_authorize.srf?client_id=000000004C12AE6F&redirect_uri=https://login.live.com/oauth20_desktop.srf&scope=service::user.auth.xboxlive.com::MBI_SSL&response_type=token") as r:
                    post_url = search("urlPost:'(.*?)'", (await r.text())).group(1)
                    ppft = search("sFTTag:'(.*)value=\"(.*)\"/>", (await r.text())).groups(1)[1]
                    async with sesh.post(post_url,
                                         data={'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': ppft},
                                         allow_redirects=False) as rs:
                        if "Location" not in rs.headers:
                            self.count += 1
                            self.failed += 1
                        else:
                            async with sesh.post("https://user.auth.xboxlive.com/user/authenticate",
                                                 json={'RelyingParty': 'http://auth.xboxlive.com', 'TokenType': 'JWT',
                                                       'Properties': {'AuthMethod': 'RPS',
                                                                      'SiteName': 'user.auth.xboxlive.com',
                                                                      'RpsTicket': search("access_token=(.*)&t",
                                                                                          unquote(rs.headers[
                                                                                                      "Location"])).group(
                                                                              1).replace("&t", "")}}) as tokenr:
                                async with sesh.post("https://xsts.auth.xboxlive.com/xsts/authorize",
                                                     json={"RelyingParty": "http://xboxlive.com", "TokenType": "JWT",
                                                           "Properties": {
                                                               "UserTokens": [(await tokenr.json())["Token"]],
                                                               "SandboxId": "RETAIL"}}) as resp:
                                    if resp.status == 200:
                                        b.append(["".join(
                                            ["XBL3.0 x=", (await resp.json())["DisplayClaims"]["xui"][0]["uhs"], ";",
                                             (await resp.json())["Token"]]),
                                                  int((await resp.json())["DisplayClaims"]["xui"][0]["xid"])])
                                    else:
                                        self.failed += 1
                                    self.count += 1
        return tuple(map(tuple, b)), self.failed

    async def jwt(self) -> tuple:
        z = []
        for token in self.accounts:
            async with ClientSession() as sesh:
                async with sesh.post("https://xsts.auth.xboxlive.com/xsts/authorize",
                                     json={"RelyingParty": "http://xboxlive.com", "TokenType": "JWT",
                                           "Properties": {"UserTokens": [token.strip("\n")],
                                                          "SandboxId": "RETAIL"}}) as resp:
                    if resp.status == 200:
                        z.append(["".join(["XBL3.0 x=", (await resp.json())["DisplayClaims"]["xui"][0]["uhs"], ";",
                                           (await resp.json())["Token"]]),
                                  int((await resp.json())["DisplayClaims"]["xui"][0]["xid"])])
                    else:
                        self.failed += 1
                    self.count += 1
        return tuple(map(tuple, z)), self.failed
