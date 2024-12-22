import subprocess
import logging
import time
from apscheduler.schedulers.background import BackgroundScheduler
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_shell_script(script_path, *args):
    """Run a shell script with the provided arguments."""
    command = [script_path] + list(args)
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Executed shell script: {script_path} with arguments: {args}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing shell script {script_path}: {e.stderr}")
        return None

def run_python_script(script_path, *args):
    """Run a Python script with the provided arguments."""
    command = ["python", script_path] + list(args)
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Executed Python script: {script_path} with arguments: {args}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing Python script {script_path}: {e.stderr}")
        return None

def process_environment(env):
    """Process a single APIC environment."""
    env_config = Config.get_config_for_env(env)
    catalog = env_config["catalog"]
    space = env_config["space"]
    org = env_config["org"]

    logging.info(f"Processing APIC environment: {env}, catalog: {catalog}, space: {space}")

    # Step 1: Login to APIC
    login_result = run_shell_script("./apic_login.sh", env, Config.USERNAME, Config.PASSWORD)
    if not login_result:
        logging.error(f"Login failed for environment: {env}")
        return

    # Step 2: Execute swagger-scraper.py
    scraper_result = run_python_script("swagger-scraper.py", env, catalog, space, org, Config.OUTPUT_DIR, Config.LOGS_DIR)
    if not scraper_result:
        logging.error(f"Swagger scraping failed for environment: {env}")
        return

    logging.info(f"Completed processing for environment: {env}")

def main_process():
    """Main process to handle all APIC environments."""
    apic_environments = Config.ENVIRONMENTS.keys()
    for env in apic_environments:
        process_environment(env)

def schedule_jobs():
    """Schedule the script to run every 24 hours."""
    logging.info("Setting up the scheduler...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(main_process, "interval", hours=24)
    scheduler.start()
    logging.info("Scheduler started, job will run every 24 hours.")

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    schedule_jobs()
