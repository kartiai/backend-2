# test/test.py

from ..db.db import database, User
import logging

#logging.basicConfig(level=logging.DEBUG)

async def add_user():
    try:
        # Ensure the database is connected
        if not database.is_connected:
            await database.connect()

        # Get or create users
        await User.objects.get_or_create(active=True, email="bogdan@test.com")
        await User.objects.get_or_create(active=True, email="andrei@test.com")
        #logging.info("User data added or verified.")

    except Exception as e:
        print("error")
        #logging.error(f"Error occurred while adding users: {e}")

    # Optional: Disconnect from the database if this is the last operation
    #await database.disconnect()
