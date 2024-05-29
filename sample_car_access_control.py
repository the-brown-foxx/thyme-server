import asyncio

from fastapi import FastAPI
from reactivex import Subject
from starlette.websockets import WebSocket

from service.authorizer.access.parking_entrance_control import ParkingEntranceControl
from service.authorizer.display.connected_display_controller import ConnectedDisplayController
from service.authorizer.display.printing_display_controller import PrintingDisplayController
from service.authorizer.display.subject_display_controller import SubjectDisplayController, DisplayControllerEvent
from service.authorizer.filter.scoring_registration_id_filter import ScoringRegistrationIdFilter
from service.authorizer.format.any_registration_id_format import AnyRegistrationIdFormat
from service.authorizer.gate.printing_gate_controller import PrintingGateController
from service.authorizer.log.actual_car_logger import ActualCarLogger
from service.authorizer.log.repository.actual_car_log_repository import ActualCarLogRepository
from service.authorizer.monitor.car.instant_checking_car_monitor import InstantCheckingCarMonitor
from service.authorizer.monitor.license.actual_license_plate_monitor import ActualLicensePlateMonitor
from service.authorizer.stream.dummy_video_stream_provider import DummyVideoStreamProvider
from service.authorizer.stream.webcam_video_stream_provider import WebcamVideoStreamProvider
from service.connection.web_socket_connection_manager import WebSocketConnectionManager
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.model.car import Car
from service.registry.repository.actual_car_repository import ActualCarRepository

video_stream_provider = WebcamVideoStreamProvider()
registration_id_format = AnyRegistrationIdFormat()
registration_id_filter = ScoringRegistrationIdFilter(registration_id_format)
license_plate_monitor = ActualLicensePlateMonitor(video_stream_provider, headless=False)
car_repository = ActualCarRepository()
car_registry = ActualCarRegistry(car_repository)
registration_id_format = AnyRegistrationIdFormat()
car_monitor = InstantCheckingCarMonitor(license_plate_monitor, car_registry, registration_id_format)
gate_controller = PrintingGateController()
display_controller_subject = Subject[DisplayControllerEvent]()
display_controller = SubjectDisplayController(display_controller_subject)
log_repository = ActualCarLogRepository()
car_logger = ActualCarLogger(log_repository, video_stream_provider)
parking_access_control = ParkingEntranceControl(
    car_monitor,
    gate_controller,
    display_controller,
    car_logger,
)

parking_access_control.start()

app = FastAPI()


@app.websocket('/ws')
async def display_web_socket(web_socket: WebSocket):
    connection_manager = WebSocketConnectionManager(web_socket)
    await connection_manager.connect()

    async def async_on_next(event: DisplayControllerEvent):
        if event is None:
            await connection_manager.send_message({
                'status': 'IDLE',
                'event': 'Waiting for a car to pass',
            })
        elif isinstance(event, Car):
            # The serializer is not working for some reason. 😁
            await connection_manager.send_message({
                'status': 'CAR_DETECTED',
                'car': {
                    'registration_id': event.registration_id,
                    'make': event.make,
                    'model': event.model,
                    'year': event.year,
                    'color': event.color,
                    'owner': event.owner,
                }
            })
        elif isinstance(event, str):
            await connection_manager.send_message({
                'status': 'ERROR',
                'registration_id': event,
            })

    def on_next(event: DisplayControllerEvent):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(async_on_next(event))
        loop.run_until_complete(task)

    display_controller_subject.subscribe(on_next)

    while True:
        await web_socket.receive_text()

# license_plate_monitor.get_thread().join()
