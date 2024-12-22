import subprocess
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_script(script_path, *args):
    command = [script_path] + list(args)
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Executed script: {script_path} with arguments: {args}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing script {script_path}: {e.stderr}")
        return None

def process_environment(env):
    env_config = Config.get_config_for_env(env)
    catalog = env_config["catalog"]
    space = env_config["space"]
    org = env_config["org"]

    logging.info(f"Processing environment: {env}, catalog: {catalog}, space: {space}")
    run_script("./apic_login.sh", env, Config.USERNAME, Config.PASSWORD)
    run_script("swagger-scraper.py", env, catalog, space, org, Config.OUTPUT_DIR, Config.LOGS_DIR)

def main_process():
    for env in Config.ENVIRONMENTS.keys():
        process_environment(env)

if __name__ == "__main__":
    main_process()
