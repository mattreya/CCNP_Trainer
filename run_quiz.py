import asyncio
import sys
from slash_commands import quiz_me

async def main():
    kwargs = {}
    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = value
    
    result = await quiz_me(**kwargs)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
