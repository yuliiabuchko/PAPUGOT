from typing import Dict, Any
from pathlib import Path
import os
import random


class Papugot(object):
    META = {
        'name': 'sfiBot',
        'description': 'Bot to send memes.',
    }

    def usage(self) -> str:
        return '''
        This is zulip bot for SFI - Student IT Festival. Every time the bot
        is @-mentioned, it will send meme.
        '''

    @staticmethod
    def choose_meme(path_to_memes):
        curr = os.getcwd()
        os.chdir(path_to_memes)
        paths = []
        for filename in Path(".").rglob('*.*'):
            paths.append(os.path.join(path_to_memes, filename))
        os.chdir(curr)
        return random.choice(paths)

    def initialize(self, bot_handler: Any) -> None:
        storage = bot_handler.storage
        if not storage.contains('memes_path'):
            storage.put('memes_path', "memes")

    def handle_message(self, message: Dict[str, str], bot_handler: Any) -> None:
        storage = bot_handler.storage
        content = self.choose_meme(storage.get('memes_path'))
        path = Path(os.path.join(os.getcwd(), content))

        if not path.is_file():
            bot_handler.send_reply(message, 'File `{}` not found'.format(content))
            return

        path = path.resolve()
        upload = bot_handler.upload_file_from_path(str(path))
        if upload['result'] != 'success':
            msg = upload['msg']
            bot_handler.send_reply(message, 'Failed to upload `{}` file: {}'.format(path, msg))
            return

        uploaded_file_reply = '[]({})'.format(upload['uri'])
        bot_handler.send_reply(message, uploaded_file_reply)


handler_class = Papugot
