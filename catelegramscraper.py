from telethon import TelegramClient, events
import json
import re


def loadteledetails():
    f = open('telegramconfig.json')
    if bool(f):
        e = json.load(f)
        return e
    else:
        return {}


def returnlockedwords(sentence, lockedword):
    if lockedword:
        return sentence.find(lockedword)
    else:
        return -1


def replace(text, rep):
    for i, j in rep.items():
        text = text.replace(i, j)
    return text


if __name__ == '__main__':
    data = loadteledetails()
    if bool(data):
        api_id = data['telegram_id']
        api_hash = data['telegram_hash']
        channel = data['telegramlink']
        if api_id == '' or api_hash == '' or api_hash == '':
            print("Please enter all necessary details in the configuration file!")
        else:
            client = TelegramClient('anon', api_id, api_hash)
            print("Looking for CAs in new pinned messages on group link: " + channel + "...")


            @client.on(events.ChatAction(chats=channel))
            async def my_event_handler(event):
                pinned = await event.get_pinned_messages()
                pinnedmessage = pinned[0].raw_text
                addy = re.sub(r'[^a-zA-Z0-9]', '', pinnedmessage)
                rep = {"ONE": "1", "one": "1", "TWO": "2", "two": "2", "THREE": "3", "three": "3", "FOUR": "4",
                       "four": "4",
                       "FIVE": "5", "five": "5", "SIX": "6", "six": "6", "SEVEN": "7", "seven": "7", "EIGHT": "8",
                       "eight": "8",
                       "NINE": "9", "nine": "9", "ZERO": "0", "zero": "0"}
                removed = replace(addy, rep)
                pancakeswap = removed.find("pancakeswap")
                splitit = removed.find("0x")
                ca = ''
                disconnect = None
                if pancakeswap > -1 and (
                        (returnlockedwords(removed, "mudra") and returnlockedwords(removed, "dxsale") and returnlockedwords(
                            removed, "pinksale") and returnlockedwords(removed, "deeplock")) > pancakeswap):
                    ca = removed[splitit:splitit + 42]
                    disconnect = True
                elif pancakeswap == -1 and (
                        returnlockedwords(removed, "mudra") and returnlockedwords(removed, "dxsale") and returnlockedwords(
                    removed, "pinksale") and returnlockedwords(removed, "deeplock")) == -1:
                    ca = removed[splitit:splitit + 42]
                    disconnect = True
                elif pancakeswap > -1 and (
                        returnlockedwords(removed, "mudra") and returnlockedwords(removed, "dxsale") and returnlockedwords(
                    removed, "pinksale") and returnlockedwords(removed, "deeplock")) == -1:
                    ca = removed[splitit:splitit + 42]
                    disconnect = True
                if disconnect:
                    with open('catext.txt', 'w') as out:
                        out.write(ca)
                    print("CA detected! Added to catext.txt.")
                    await client.disconnect()


            client.start()
            client.run_until_disconnected()
    else:
        print("Please ensure that telegramconfig.json is created. Contact @koi or @gabtheape on discord.")
