import asyncio
import logging

from .utils import get_sn

_LOGGER = logging.getLogger(__name__)

class DiscoveryProtocol(asyncio.DatagramProtocol):
    def __init__(self, queue):
        self.queue = queue

    def datagram_received(self, data, addr):
        self.queue.put_nowait(addr[0])

async def async_discover_ips(timeout=5) -> list:
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: DiscoveryProtocol(queue),
        local_addr=('0.0.0.0', 0),
        allow_broadcast=True
    )

    sn = get_sn()
    message = f'{{"cmd":0,"pv":0,"sn":"{sn}","msg":{{}}}}'.encode('utf-8')

    for _ in range(3):
        transport.sendto(message, ('255.255.255.255', 6095))
        await asyncio.sleep(0.03)

    ips = set()
    start = time.time()
    while time.time() - start < timeout:
        try:
            ip = await asyncio.wait_for(queue.get(), 0.1)
            if ip not in ips:
                ips.add(ip)
                _LOGGER.debug(f"Discovered IP: {ip}")
        except asyncio.TimeoutError:
            continue

    transport.close()
    return list(ips)
