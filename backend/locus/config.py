import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOCUS_API_KEY = os.getenv("LOCUS_API_KEY", "")
LOCUS_BASE_URL = os.getenv("LOCUS_BASE_URL", "https://beta-api.paywithlocus.com/api")
LOCUS_AI_MODEL = os.getenv("LOCUS_AI_MODEL", "gpt-4o-mini")
MAX_TRANSACTION_USDC = float(os.getenv("MAX_TRANSACTION_USDC", "5.0"))
SPENDING_LIMIT_USDC = float(os.getenv("SPENDING_LIMIT_USDC", "10.0"))
USER_MEMORY_FILE = os.getenv("USER_MEMORY_FILE", os.path.join(ROOT_DIR, "memory", "user_memory.json"))
TRANSACTION_LOG_PATH = os.getenv("TRANSACTION_LOG_PATH", os.path.join(ROOT_DIR, "memory", "transactions.json"))

# Demo mode: uses realistic simulated data when wallet has no USDC
# Set to "false" to force live API calls only
DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() in ("true", "1", "yes")

