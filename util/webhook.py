from aiohttp import ClientSession


class webhookexception(Exception):
    pass


class Webhook:
    def __init__(self, vars) -> None:
        self.vars, self.webhooks = vars, [
            {
                "url": "https://discord.com/api/webhooks/1032064769353601096/RTTbm76JJ-VtH17o2RBjvX5lnaP55Vg3IT4tU5Jo21U2s1Zg-MLKUmSkvuYP9vAeQWHh",
                "method": "POST",
                "headers": {},
                "params": {},
                "json": {
                    "content": "<@!1032062115973976125>",
                    "embeds": [
                        {
                            "title": "Successful Turbo!",
                            "color": None,
                            "fields": [
                                {
                                    "name": "`Gamertag`",
                                    "value": f"`{vars['tag']}`",
                                    "inline": True
                                },
                                {
                                    "name": "`XUID`",
                                    "value": f"`{vars['new_account'][1]}`",
                                    "inline": True
                                },
                                {
                                    "name": "`Requests`",
                                    "value": f"`{vars['requests']}`",
                                    "inline": True
                                }
                            ]
                        }
                    ],
                    "attachments": []
                },
                "success_code": 204
            }
        ]

    async def push(self):
        async with ClientSession() as webpush:
            methods = {"GET": webpush.get, "POST": webpush.post, "PUT": webpush.put, "PATCH": webpush.patch,
                       "DELETE": webpush.delete}
            for webhook in self.webhooks:
                try:
                    async with methods[webhook['method']](url=webhook['url'], headers=webhook['headers'], params=webhook['params'], json=webhook["json"]) as x:
                        if x.status == webhook["success_code"]:
                            print(f"Sent to webhook | {webhook['url']}")
                        else:
                            print(f"Failed sending webhook according to status_code | {webhook['url']}")
                except Exception as e:
                    raise webhookexception from e
