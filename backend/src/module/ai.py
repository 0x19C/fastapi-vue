import asyncio
import random

from datetime import datetime


async def ai_training_process(model_id: int, dataset_id: int) -> dict:
    # Training Process
    await asyncio.sleep(2)
    return {
        "experiment_name": "Experiment_" + str(datetime.now().timestamp()),
        "model_id": model_id,
        "dataset_id": dataset_id,
        "precision": random.uniform(0.9, 1),
        "recall": random.uniform(0.8, 1)
    }
