#!/usr/bin/env python3
"""
Session String Generator for Telegram Unzip Bot
This script helps you generate a Pyrogram session string for your user account
"""

from pyrogram import Client
import asyncio

print("""
╔═══════════════════════════════════════════════╗
║  Telegram Session String Generator           ║
║  For Unzip Bot - Large File Upload Support   ║
╚═══════════════════════════════════════════════╝

📌 This session string allows the bot to upload files
   larger than 50MB (up to 4GB) using your user account.

⚠️  IMPORTANT SECURITY NOTES:
   - Never share your session string with anyone
   - Keep it private like a password
   - This gives full access to your Telegram account
   - Only use with trusted bots
""")

def get_input(prompt):
    """Get user input with prompt"""
    try:
        return input(prompt).strip()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        exit(0)
    except EOFError:
        print("\n\n❌ Input error")
        exit(1)

# Get API credentials
print("\n📝 Step 1: Get your API credentials from https://my.telegram.org\n")
api_id = get_input("Enter your API_ID: ")
api_hash = get_input("Enter your API_HASH: ")

if not api_id or not api_hash:
    print("\n❌ Error: API_ID and API_HASH are required!")
    exit(1)

try:
    api_id = int(api_id)
except ValueError:
    print("\n❌ Error: API_ID must be a number!")
    exit(1)

print("\n📱 Step 2: We'll send you a login code on Telegram\n")

async def generate_session():
    """Generate session string"""
    try:
        async with Client(
            name="session_generator",
            api_id=api_id,
            api_hash=api_hash,
            in_memory=True
        ) as app:
            session_string = await app.export_session_string()
            
            print("\n" + "="*60)
            print("✅ SESSION STRING GENERATED SUCCESSFULLY!")
            print("="*60)
            print("\n📋 Your Session String:\n")
            print(f"{session_string}\n")
            print("="*60)
            print("\n💾 SAVE THIS SESSION STRING:")
            print("   1. Copy the session string above")
            print("   2. Add it to your .env file as SESSION_STRING")
            print("   3. Never share it with anyone!")
            print("\n✨ Your bot can now upload files up to 4GB!")
            print("="*60)
            
            # Save to file
            with open("session_string.txt", "w") as f:
                f.write(session_string)
            
            print("\n📁 Session string also saved to: session_string.txt")
            print("\n⚠️  Remember to delete session_string.txt after copying it!")
            
    except Exception as e:
        print(f"\n❌ Error generating session: {e}")
        print("\nCommon issues:")
        print("  - Invalid API_ID or API_HASH")
        print("  - Wrong phone number format")
        print("  - Incorrect verification code")
        exit(1)

# Run the async function
if __name__ == "__main__":
    try:
        asyncio.run(generate_session())
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
