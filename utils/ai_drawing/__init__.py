import aiohttp
import asyncio
from typing import Union

"""
    aiohttp:发送POST请求
"""
async def getData(prompt:str) -> Union[str,any]:
    url = 'https://api-inference.huggingface.co/models/Linaqruf/anything-v3.0'
    prompts={"inputs": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(url,data=prompts) as res:
            try:
                print(await res.text())
                return ""
            except:
                r=await res.read()
                return r