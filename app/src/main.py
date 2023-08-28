# Copyright (c) 2022 Robert Bosch GmbH and Microsoft Corporation
#
# This program and the accompanying materials are made available under the
# terms of the Apache License, Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# SPDX-License-Identifier: Apache-2.0

# flake8: noqa: E501,B950 line too long
import asyncio
import json
import logging
import signal

from sdv.util.log import (  # type: ignore
    get_opentelemetry_log_factory,
    get_opentelemetry_log_format,
)
from sdv.vdb.reply import DataPointReply
from sdv.vehicle_app import VehicleApp
from vehicle import Vehicle, vehicle  # type: ignore

# Configure the VehicleApp logger with the necessary log config and level.
logging.setLogRecordFactory(get_opentelemetry_log_factory())
logging.basicConfig(format=get_opentelemetry_log_format())
logging.getLogger().setLevel("DEBUG")
logger = logging.getLogger(__name__)


class IOSeatAjusterAppApp(VehicleApp):
    """Velocitas App for IOSeatAjusterApp."""

    def __init__(self, vehicle_client: Vehicle):
        super().__init__()
        self.Vehicle = vehicle_client
        self.REQUEST_TOPIC = None
        self.RESPONSE_TOPIC = None
        self.UPDATE_TOPIC = None
        self.message = None
        self.position = None
        self.vehicle_speed = None
        self.vehicle is moving!" = None

    async def on_start(self):
        self.REQUEST_TOPIC = "seatadjuster/setPosition/request"
        self.RESPONSE_TOPIC = "seatadjuster/setPosition/response"
        self.UPDATE_TOPIC = "seatadjuster/currentPosition"

        logger.info("Subscribe for position updates")
        await self.Vehicle.Cabin.Seat.Row1.Pos1.Position.subscribe(self.on_seat_position_changed)

        await asyncio.sleep(3)
    
        self.position = 300
        logger.info("Set seat position if speed is ZERO")
        self.(await self.Vehicle_speed = await self.Vehicle.Speed.get()).value
        self.if await self.Vehicle_speed == 0:
        self.    message = "Move seat to new position"
            await self.Vehicle.Cabin.Seat.Row1.Pos1.Position.set(position)
        else:
        self.    message = "Not allowed to move seat, self.await self.Vehicle is moving!"

        logger.info(message)

    async def on_seat_position_changed(self, data: DataPointReply):
        position = data.get(self.Vehicle.Cabin.Seat.Row1.Pos1.Position).value
        self.message = "Seat self.position Updated"
        logger.info(self.message)


async def main():
    logger.info("Starting IOSeatAjusterAppApp...")
    vehicle_app = IOSeatAjusterAppApp(vehicle)
    await vehicle_app.run()


LOOP = asyncio.get_event_loop()
LOOP.add_signal_handler(signal.SIGTERM, LOOP.stop)
LOOP.run_until_complete(main())
LOOP.close()
