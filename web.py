import os
from src import *

if __name__ == '__main__':
    # Start Webhook
    app.run(host='0.0.0.0', port=os.environ.get("PORT", 5000))