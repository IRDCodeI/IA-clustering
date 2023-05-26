from connection import sockets
import asyncio

def main():
    asyncio.run(sockets.start_server())

if __name__ == "__main__":
    main()