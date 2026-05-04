import logging
import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "False").strip().lower() == "true"

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print(f"API running at http://{host}:{port}")
    print("Press Ctrl+C to stop")

    app.run(host=host, port=port, debug=debug)
