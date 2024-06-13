from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError, SessionPasswordNeededError
import asyncio
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your actual credentials
api_id = 23142306
api_hash = 'a5743330c99fe35b67c19f02a3cdc0fd'
session_string = '1BVtsOKYBu47VWS2oT_YjB_RnVdXlN5W1HTxXUw4vrQCzN2EBj0WKR3yDRrfFxANYWNCzNIG_GwQW72c_qnk4X4WCKnjpY_SRkLbfwyVsonCz5cxQAQ3b7I-qrTJabAtrGaDHXvJWijpYM8Gyef6usLcREUmQkeC2LRl-k4Kr7gKZ4lpP4Qxw5G-x7l7rDCdFU2MZOnzpvCLlVBX9ugT09l62IWgsB8_Ea336cWV5UvF3Q9l3edm8cKWO2eTBBq06oJB0BFvUC-vxwIPjYK125VQQXrGKjkcVhlNgB2DnV9M7_Qbfj7MmoltYu-52CKbsSMWqKpYHsxJzMCsQ6Hkf7KlMSRuGrQg='

# Replace with channel and bot usernames
channel_username = '@loot_deals_offer'
bot_username = '@ekconverter5bot'

# Delay between message forwards (adjust as needed)
forward_delay = 5  # Seconds

# Maximum number of retries for failed forwards
max_retries = 3

# Create a TelegramClient instance
client = TelegramClient(StringSession(session_string), api_id, api_hash)

# Define the event handler function
@client.on(events.NewMessage(chats=channel_username))
async def forward_to_bot(event):
    message = event.message
    retries = 0
    while retries < max_retries:
        try:
            # Handle messages with media
            if message.media:
                if hasattr(message.media, 'webpage'):
                    caption = message.text if message.text else None
                    await client.send_message(bot_username, f"{message.media.webpage.url}\n\n{caption}")
                else:
                    caption = message.text if message.text else None
                    await client.send_file(bot_username, message.media, caption=caption)
            # Handle messages without media (including other types)
            else:
                # Extract text content and handle additional message types
                text_content = message.text or (message.poll.poll.question if hasattr(message, 'poll') else None)
                if text_content:
                    await client.send_message(bot_username, text_content)
            # Add a delay between forwards to avoid rate limits
            await asyncio.sleep(forward_delay)
            break  # Exit the loop if the forward was successful
        except FloodWaitError as e:
            # Handle rate limit errors
            logging.warning(f"Rate limit reached, waiting {e.wait_time} seconds...")
            await asyncio.sleep(e.wait_time)
            retries += 1
        except Exception as e:
            # Handle any other exceptions during message forwarding
            logging.error(f"Error forwarding message: {e}")
            retries += 1
            time.sleep(5)  # Wait for 5 seconds before retrying
    else:
        logging.error(f"Failed to forward message after {max_retries} retries.")

async def main():
    try:
        await client.start()
        logging.info("Bot started!")

        # Run the client until disconnected
        await client.run_until_disconnected()
    except SessionPasswordNeededError:
        # Handle the case where a password is required to use the session
        logging.error("Session password is needed. Please provide it and try again.")
    except Exception as e:
        # Handle any other unexpected exceptions
        logging.error(f"Unexpected error: {e}")

# Run the main function
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
