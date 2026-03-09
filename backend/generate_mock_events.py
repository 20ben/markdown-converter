import ldclient
from ldclient import Context
from ldclient.config import Config
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

ldclient.set_config(Config(os.getenv("LAUNCHDARKLY_SDK_KEY", "")))
ld = ldclient.get()

# Simulate 20 users clicking helpful
for i in range(300):
    user_id = str(uuid.uuid4())
    ctx = Context.builder(user_id).kind('user').anonymous(True).build()

    # Let LD assign the variant (50/50 rollout)
    variant = ld.variation('ai-summary-variant', ctx, 'short')

    # Simulate a helpful click
    ld.track('helpful-click', ctx, 1)

    print(f"User {i+1}: variant={variant}")

ld.flush()
ld.close()
