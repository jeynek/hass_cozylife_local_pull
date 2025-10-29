import asyncio
import json
import logging

from .utils import get_sn

_LOGGER = logging.getLogger(__name__)

class TCPClient:
    def __init__(self, ip: str, port: int = 5555) -> None:
        self.ip = ip
        self.port = port
        self.reader = None
        self.writer = None
        self.device_id = None
        self.pid = None
        self.device_type_code = None
        self.device_model_name = None
        self.dpid = []

    async def async_ensure_connection(self) -> None:
        if self.writer is None or self.writer.is_closing():
            try:
                self.reader, self.writer = await asyncio.open_connection(self.ip, self.port)
            except Exception as e:
                _LOGGER.error(f"Connection to {self.ip}:{self.port} failed: {e}")
                raise

    async def async_close(self) -> None:
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.reader = None
            self.writer = None

    async def async_send_receive(self, cmd: int, payload: dict) -> dict:
        await self.async_ensure_connection()
        sn = get_sn()
        message = {'pv': 0, 'cmd': cmd, 'sn': sn, 'msg': payload}
        if cmd == 3:
            message['msg'] = {'attr': [int(k) for k in payload], 'data': payload}
        elif cmd == 2:
            message['msg'] = {'attr': [0]}
        elif cmd == 0:
            message['msg'] = {}

        send_data = json.dumps(message, separators=(',', ':')) + "\r\n"
        _LOGGER.debug(f"Sending to {self.ip}: {send_data}")
        self.writer.write(send_data.encode('utf-8'))
        await self.writer.drain()

        response = {}
        for _ in range(10):
            try:
                data = await asyncio.wait_for(self.reader.read(1024), timeout=1)
                if not data:
                    break
                payload_str = data.decode('utf-8').strip()
                _LOGGER.debug(f"Received from {self.ip}: {payload_str}")
                parsed = json.loads(payload_str)
                if parsed.get('sn') == sn and 'msg' in parsed:
                    if cmd == 0:
                        response = parsed['msg']
                    else:
                        response = {str(k): v for k, v in parsed['msg'].get('data', {}).items()}
                    break
            except Exception as e:
                _LOGGER.debug(f"Read error: {e}")

        if not response:
            _LOGGER.warning(f"No response for SN {sn}")
        return response

    async def async_query(self) -> dict:
        return await self.async_send_receive(2, {})

    async def async_control(self, commands: dict) -> None:
        await self.async_send_receive(3, commands)
