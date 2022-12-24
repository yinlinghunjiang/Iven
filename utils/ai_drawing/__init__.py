import aiohttp
from typing import Union

"""
    Author: 银灵魂酱(Silverowo)
    :param prompt: the describtion
    :var prompt: str

"""


async def getData(prompt: str) -> Union[str, any]:
    url = "https://api-inference.huggingface.co/models/Linaqruf/anything-v3.0"
    prompts = {"inputs": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=prompts) as res:
            try:
                r = await res.text()
                return ""
            except:
                r = await res.read()
                return r
