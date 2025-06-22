import os

# Bot configuration
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Group and admin configuration
GROUP_ID = -1002400589513  # 👑GambleCodez + Winna.com #PrizeHub 👑
ADMIN_IDS = [6668510825, 1642259333]

# Banker configuration
BUSTER_USERNAME = "GambleCodezBank"
BUSTER_USER_ID = 8055687062
CWALLET_BOT_ID = 61104674

# Payment configuration
CWALLET_ID = "61104674"
POLYGON_ADDRESS = "0xc9E942cd1971C1E33F0065B25A9DfD9b22c121f4"
PAYMENT_LINK = "https://cwallet.com/recevie/USDT-POLYGON-61104674-0"
ACCESS_FEE_AMOUNT = 5.0

# Loan configuration
LOAN_LEVELS = {
    'L1': {'max_amount': 5, 'interest_rate': 0.12, 'repayment_period_days': 7},
    'L2': {'max_amount': 10, 'interest_rate': 0.10, 'repayment_period_days': 7},
    'L3': {'max_amount': 15, 'interest_rate': 0.08, 'repayment_period_days': 10},
    'L4': {'max_amount': 20, 'interest_rate': 0.07, 'repayment_period_days': 14},
    'L5': {'max_amount': 25, 'interest_rate': 0.05, 'repayment_period_days': 14},
}

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

# Community configuration
COMMUNITY_LINK = "t.me/GambleCodezPrizeHub"...
