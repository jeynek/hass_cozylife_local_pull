import asyncio
import time
import logging

from .utils import get_sn

_LOGGER = logging.getLogger(__name__)


class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self):
        self.transport = None
        self.queue = asyncio.Queue()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.queue.put_nowait((data, addr))


async def async_get_ips(timeout=5) -> list:
    """
    Discover device IPs via UDP broadcast.
    :return: list of unique IPs
    """
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        DiscoveryProtocol,
        local_addr=('0.0.0.0', 0),
        allow_broadcast=True
    )
    transport.sendto(b
