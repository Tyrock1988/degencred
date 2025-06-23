
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "7821431024:AAHny9nHqOrZ-4gaM07_YST3OXrzHTieUSg")
ADMIN_IDS = [6668510825, 1642259333]

# PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL")

BUSTER_USERNAME = "GambleCodezBank"
BUSTER_USER_ID = 6668510825
LOAN_INTEREST_RATE = 0.10
LOAN_REPAYMENT_PERIOD_DAYS = 7

LOAN_LEVELS = {
    'L1': {'max_amount': 100, 'interest_rate': 0.12, 'repayment_period_days': 7},
    'L2': {'max_amount': 250, 'interest_rate': 0.10, 'repayment_period_days': 7},
    'L3': {'max_amount': 500, 'interest_rate': 0.08, 'repayment_period_days': 10},
    'L4': {'max_amount': 1000, 'interest_rate': 0.07, 'repayment_period_days': 14},
    'L5': {'max_amount': 2000, 'interest_rate': 0.05, 'repayment_period_days': 14},
}
