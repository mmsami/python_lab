from langchain_openrouter import ChatOpenRouter
from pathlib import Path
import os
from dotenv import load_dotenv
import asyncio

load_dotenv(Path(__file__).parent.parent.parent / ".env")


model = ChatOpenRouter(
    model="google/gemma-4-26b-a4b-it:free",
    temperature=0,
    max_tokens=1024,
    max_retries=2
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to German. Translate the user sentence.",
    ),
    ("human", "Learning German is hard but I will make it."),
]

messages_fr = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "Learning German is hard but I will make it."),
]


def use_invoke():
    # Waits for the full response, no streaming.
    ai_response = model.invoke(messages)
    print(ai_response.content)


def use_stream_sync():
    print("Streaming response:\n")

    stream = model.stream_events(messages, version="v3")

    for chunk in stream.text:
        print(chunk, end="", flush=True)

    final_message = stream.output

    print("\n\n--- Final Metadata ---")

    print("\nResponse metadata:")
    print(final_message.response_metadata)

    print("\nUsage metadata:")
    print(final_message.usage_metadata)

    print("\nFull message:")
    print(final_message)


# --- Async version (for learning) ---
# Same idea as above, but for use inside async code (e.g. FastAPI, a bot,
# or calling several prompts concurrently with asyncio.gather). Not needed
# for a single one-off call like this script — sync is simpler there.
#
# Note: unlike the sync `stream.output` (a plain blocking property), the
# async `stream.output` is itself awaitable, so it needs `await` too.


async def stream_async():
    stream = await model.astream_events(messages, version="v3")

    async for token in stream.text:
        print(token, end="", flush=True)

    final = await stream.output
    print("\n\nusage:", final.usage_metadata)


# --- Multiple concurrent requests (for learning) ---
# A single `await`ed call only ever has one request in flight at a time —
# it's non-blocking, but still one at a time. To actually send several
# requests together and have them processed concurrently, launch multiple
# coroutines at once with asyncio.gather. Each one opens its own stream;
# while one is waiting on the network, the event loop works on the others.


async def stream_labeled(label, msgs):
    stream = await model.astream_events(msgs, version="v3")

    text_parts = []
    async for token in stream.text:
        text_parts.append(token)

    final = await stream.output
    print(f"[{label}] {''.join(text_parts)}")
    return final


async def stream_concurrent():
    # Both requests are sent essentially at the same time; gather waits
    # for both to finish, whichever order they actually complete in.
    results = await asyncio.gather(
        stream_labeled("DE", messages),
        stream_labeled("FR", messages_fr),
    )
    for r in results:
        print(r.usage_metadata)


# Uncomment ONE line below to run that mode:

# use_invoke()
# use_stream_sync()
# asyncio.run(stream_async())
asyncio.run(stream_concurrent())
