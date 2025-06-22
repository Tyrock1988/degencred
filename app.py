import os
import logging
import threading
from flask import Flask, jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import bot components
from bot.main import setup_bot
from bot.database import init_db

# Flask app for health checks (required by Render)
app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "DegenCred Bot",
        "message": "Bot is running successfully"
    })

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

def run_bot():
    """Run the Telegram bot"""
    try:
        logger.info("🎯 Starting DegenCred Bot...")
        
        # Initialize database
        init_db()
        logger.info("✅ Database initialized")
        
        # Setup and run bot
        application = setup_bot()
        logger.info("✅ Bot setup complete")
        
        # Start polling
        application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")

if __name__ == '__main__':
    # Start bot in a separate thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start Flask server (main thread)
    logger.info("🌐 Starting Flask health server...")
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
