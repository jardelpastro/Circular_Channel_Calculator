import os
import sys
import logging
import fix_metadata
import webbrowser
import time
import socket

# Configuração de logging
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def wait_for_server(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if is_port_in_use(port):
            return True
        time.sleep(0.1)
    return False


def run_app():
    try:
        # Porta do servidor
        SERVER_PORT = 8501

        # Configurações do Streamlit
        os.environ.update({
            'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false',
            'STREAMLIT_SERVER_PORT': str(SERVER_PORT),
            'STREAMLIT_SERVER_HEADLESS': 'true',
            'STREAMLIT_CHECK_VERSION': 'false',
            'STREAMLIT_SERVER_ENABLEXSRFPROTECTION': 'false',
            'STREAMLIT_SERVER_ENABLECORS': 'true',
            'STREAMLIT_SERVER_ADDRESS': 'localhost',
            'STREAMLIT_BROWSER_SERVER_ADDRESS': 'localhost',
            'STREAMLIT_BROWSER_SERVER_PORT': str(SERVER_PORT),
            'STREAMLIT_CLIENT_TOOLBAR_MODE': 'minimal',
            'STREAMLIT_THEME_BASE': 'light',
            'STREAMLIT_DEVELOPMENT_MODE': 'false',
            'STREAMLIT_SERVER_RUN_ON_SAVE': 'false',
            'STREAMLIT_SERVER_FILE_WATCHER_TYPE': 'none',
            'STREAMLIT_BROWSER_GATHER_USAGE_STATS': 'false'
        })

        # Cria o metadata fake
        fix_metadata.create_fake_metadata()

        # Determina o caminho base
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            logging.debug(f"Running from frozen application. Base path: {base_path}")
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            logging.debug(f"Running from script. Base path: {base_path}")

        # Configura caminhos
        main_script = os.path.join(base_path, 'circular_channel_calculator.py')
        os.environ['BASE_DIR'] = base_path
        os.environ['ASSETS_DIR'] = os.path.join(base_path, 'assets')

        logging.debug(f"Main script path: {main_script}")
        logging.debug(f"Assets path: {os.environ['ASSETS_DIR']}")

        def open_browser():
            time.sleep(2)
            if wait_for_server(SERVER_PORT):
                url = f'http://localhost:{SERVER_PORT}'
                logging.debug(f"Opening browser at {url}")
                webbrowser.open(url)
            else:
                logging.error(f"Server did not start on port {SERVER_PORT}")

        # Inicia o thread do navegador
        import threading
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()

        # Importa e configura o Streamlit
        import streamlit.web.bootstrap as bootstrap
        import streamlit.config as config

        # Configura o Streamlit
        config.set_option('server.port', SERVER_PORT)
        config.set_option('server.address', 'localhost')
        config.set_option('server.headless', True)
        config.set_option('server.enableCORS', True)
        config.set_option('server.enableXsrfProtection', False)
        config.set_option('global.developmentMode', False)

        # Configura argumentos do Streamlit
        sys.argv = ["streamlit", "run", main_script,
                    "--server.port", str(SERVER_PORT),
                    "--server.address", "localhost",
                    "--server.headless", "true",
                    "--server.enableCORS", "true",
                    "--server.enableXsrfProtection", "false"]

        # Inicia o Streamlit
        logging.debug("Starting Streamlit server...")
        bootstrap.run(main_script, '', [], {
            'server.port': SERVER_PORT,
            'server.address': 'localhost',
            'server.headless': True,
            'server.enableCORS': True,
            'server.enableXsrfProtection': False,
            'browser.serverAddress': 'localhost',
            'browser.serverPort': SERVER_PORT,
            'global.developmentMode': False,
            'runner.fastReruns': False,
            'server.runOnSave': False
        })

    except Exception as e:
        logging.error(f"Error running app: {e}", exc_info=True)
        print(f"Error: {e}")
        input("Press Enter to exit...")


if __name__ == '__main__':
    run_app()