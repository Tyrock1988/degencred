
import os
import logging
from bot import create_application
import database
from flask import Flask
import threading

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_health_server():
    """Create a simple health check server for Fly.io"""
    app = Flask(__name__)
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'degencred-bot'}, 200
    
    @app.route('/')
    def root():
        return {'message': 'DegenCred Bot is running on Fly.io'}, 200
    
    return app

def run_health_server():
    """Run the health check server in a separate thread"""
    app = create_health_server()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

def main():
    """Main entry point for the bot"""
    try:
        # Initialize database
        database.init_db()
        logger.info("Database initialized successfully")
        
        # Start health check server in background for Fly.io
        health_thread = threading.Thread(target=run_health_server, daemon=True)
        health_thread.start()
        logger.info(f"Health check server started on port {os.environ.get('PORT', 8080)}")
        
        # Create and run the application
        application = create_application()
        logger.info("Starting DegenCred Bot...")
        application.run_polling()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise
    finally:
        # Clean up database connections
        database.close_connection_pool()

if __name__ == "__main__":
    main()
  
