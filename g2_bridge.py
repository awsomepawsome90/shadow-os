import asyncio
import requests
from evenglasses.evenglasses import EvenGlasses

# --- Configuration ---
# The address of the G2 glasses. You'll need to find this using a BLE scanner.
# It can be the device name or its address (e.g., "XX:XX:XX:XX:XX:XX").
G2_DEVICE_ADDRESS = "G2-1234" # <--- IMPORTANT: Change this to your device's address/name.
BACKEND_URL = "http://127.0.0.1:8000"

async def send_to_glass(g2: EvenGlasses, text: str):
    """
    Connects to the glasses and pushes a string of text to the display.
    """
    if not g2.is_connected():
        print("Device not connected. Attempting to connect...")
        await g2.connect()
        if not g2.is_connected():
            print("Failed to connect to the glasses.")
            return

    print(f"Sending to G2: '{text}'")
    try:
        # The even-glasses library handles the protocol complexities 
        # (packet fragmentation, headers, etc.).
        await g2.send_text(text)
        print("Successfully sent text to G2 display.")
    except Exception as e:
        print(f"An error occurred while sending text: {e}")

async def main():
    """
    Main execution loop. Scans for the glasses, connects,
    and then enters a loop to query the user for intelligence requests.
    """
    print("Scanning for G2 glasses...")
    g2 = EvenGlasses(G2_DEVICE_ADDRESS)
    
    # The library handles the scanning and connection logic.
    # We prime it here.
    try:
        await g2.connect()
        print(f"Connected to {g2.name} ({g2.address})")
    except Exception as e:
        print(f"Could not connect to G2 glasses at address '{G2_DEVICE_ADDRESS}'.")
        print("Ensure the device is on and in range. Use a BLE scanner to verify the address.")
        print(f"Error: {e}")
        return

    # --- Main Interaction Loop ---
    while True:
        try:
            question = input("\n[Shadow OS] Enter your query (or 'quit' to exit): ")
            if question.lower() == 'quit':
                break
            
            # Query the backend RAG engine.
            print("Querying the intelligence backend...")
            response = requests.post(f"{BACKEND_URL}/query/", json={"question": question})

            if response.status_code == 200:
                data = response.json()
                g2_output = data.get("g2_output")
                
                # Send the formatted text to the glasses.
                await send_to_glass(g2, g2_output)
            else:
                print(f"Error from backend: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print("Connection Error: Could not connect to the backend. Is it running?")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"An unexpected error occurred in the main loop: {e}")

    if g2.is_connected():
        await g2.disconnect()
        print("Disconnected from G2 glasses.")

if __name__ == "__main__":
    asyncio.run(main())

