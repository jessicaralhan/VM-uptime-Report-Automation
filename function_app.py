from datetime import datetime
import logging
import azure.functions as func
from main import running_vms, get_configuration
import logging

app = func.FunctionApp()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.timer_trigger(
    schedule="5 * * * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
async def funcvmruntime(myTimer: func.TimerRequest) -> None:
    """This function will be triggered on a daily basis at 6 PM UTC."""
    logger.info("Azure function triggered.")

    report_days, azure_creds, aws_creds = get_configuration()

    if report_days is None:
        logger.error("Failed to retrieve configuration for report days.")
        return

    running_vms(report_days, azure_creds, aws_creds)
    logger.info(f"VM report generation executed at {datetime.now()}")

