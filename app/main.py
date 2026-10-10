from app.agent.loop import run_agent
import asyncio
async def main():
    while True:
        input_text = input("Enter a command (or 'exit' to quit): ")
        if input_text.lower() == "exit":
            break

        try:
            message = await run_agent(input_text)
            print("Agent Response:", message)
        except PermissionError as e:
            print(f"Permission Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())