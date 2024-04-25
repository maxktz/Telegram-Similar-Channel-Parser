from pathlib import Path
import os, sys
import uvloop
import config
from telethon import TelegramClient, functions, types
from yarl import URL
from loguru import logger


logger.remove()
logger.add(
    sink=sys.stderr, 
    format='<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> - <level>{message}</level>'
)


class SimilarChannelParser:
    
    def __init__(self):
        proxy = getattr(config, 'PROXY', None)
        if proxy:
            proxy_url = URL(proxy)
            proxy = {
                'proxy_type': proxy_url.scheme, 
                'username': proxy_url.user, 
                'password': proxy_url.password,
                'addr': proxy_url.host, 
                'port': proxy_url.port
            }

        self.client = TelegramClient(
            session=os.path.join('sessions', 'account'),
            api_id=config.TELEGRAM_API_ID,
            api_hash=config.TELEGRAM_API_HASH,
            proxy=proxy,
            device_model=config.TELEGRAM_DEVICE_MODEL,
            system_version=config.TELEGRAM_SYSTEM_VERSION,
            app_version=config.TELEGRAM_APP_VERSION,
            lang_code='en',
            system_lang_code='en',
        )
        
    async def get_similar_channels(self, channel_entity: str) -> list[str]:
        logger.info(f'Start parsing similar channels of "{channel_entity}"...')
        async with self.client: 
            try:
                req = functions.channels.GetChannelRecommendationsRequest(channel_entity)
                res: types.messages.Chats = await self.client(req)
            except (ValueError, TypeError):
                logger.error(f'No channel has "{channel_entity} as username."')
                sys.exit(0)
        channels: list[str] = [
            config.LINE_FORMAT.format(**chat.__dict__)
            for chat in res.chats
        ]
        count = getattr(res, 'count', len(channels))
        log_text = f'Parsed {len(channels)}/{count} similar channels. '
        if len(channels) < count:
            log_text += f"You may need Telegram Premium to get all {count} channels."
        logger.success(log_text)
        return channels
        
    async def main(self):
        saving_dir = Path(config.SAVING_DIRECTORY)
        if not saving_dir.exists():
            logger.error(
                f'Not found directory {saving_dir.as_posix()} to save chats in. '
                'Please try to change FILE_PATH in configuration file.'
            )
            sys.exit(0)
        
        while True:
            channel_username = input("Please input channel username (leave empty to stop): ")
            if channel_username.strip() == '':
                sys.exit(0)
            channels = await self.get_similar_channels(channel_username)
            saving_file = (saving_dir / channel_username).with_suffix('.txt')
            saving_file.write_text('\n'.join(channels))
            logger.success(
                f'Similar channels saved to "{saving_file}" in format "{config.LINE_FORMAT}".\n'
            )


if __name__ == '__main__':
    uvloop.run(SimilarChannelParser().main())