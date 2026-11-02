import asyncio

from camunda_orchestration_sdk import (
    CamundaAsyncClient,
    ConnectedJobContext,
    WorkerConfig,
)


async def reserveMaterials(job: ConnectedJobContext):

    variables = job.variables.to_dict()

    available = variables["availableStock"]
    requested_quantity = variables["requestedQuantity"]

    print(f"Reserving {requested_quantity} materials. Update Stock: {available - requested_quantity} materials")

    # Die Entscheidung wurde bereits von der DMN getroffen.
    if available  - requested_quantity < 0:
        print("Not enough stock available to reserve the requested quantity.")
        return {
            "reservationSuccessful": False,
            "reservedQuantity": 0,
            "availableStock": available
        }
    else:
        print("Materials successfully reserved!")

        return {
            "reservationSuccessful": True,
            "reservedQuantity": requested_quantity,
            "availableStock": available - requested_quantity
        }


async def orderMaterial(job: ConnectedJobContext):

    variables = job.variables.to_dict()

    requested_quantity = variables["requestedQuantity"]

    print(f"Ordering {requested_quantity} materials.")

    return {
        "orderedQuantity": requested_quantity
    }


async def main():

    async with CamundaAsyncClient() as client:

        config = WorkerConfig(
            job_type="reserveMaterials",
            job_timeout_milliseconds=30000,
            max_concurrent_jobs=1,
        )

        client.create_job_worker(
            config=config,
            callback=reserveMaterials,
        )

        print("Worker started. Waiting for jobs...")

        await client.run_workers()


if __name__ == "__main__":
    asyncio.run(main())