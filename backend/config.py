import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = "claude-haiku-4-5-20251001"

if __name__ == '__main__':
    # Set your LaunchDarkly SDK key.
    ldclient.set_config(Config(os.getenv("LAUNCHDARKLY_SDK_KEY", "")))

    if not ldclient.get().is_initialized():
        print('SDK failed to initialize')
        exit()

    # For onboarding purposes only we flush events as soon as
    # possible so we quickly detect your connection.
    # You don't have to do this in practice because events are automatically flushed.
    ldclient.get().flush()
    print('SDK successfully initialized')