# import asyncio
#
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from reactivex import Subject
# from serial import Serial
#
# from service.authorizer.access.parking_entrance_control import ParkingEntranceControl
# from service.authorizer.access.parking_exit_control import ParkingExitControl
# from service.authorizer.display.subject_display_controller import SubjectDisplayController, DisplayControllerEvent
# from service.authorizer.filter.scoring_registration_id_filter import ScoringRegistrationIdFilter
# from service.authorizer.format.any_registration_id_format import AnyRegistrationIdFormat
# from service.authorizer.gate.printing_gate_controller import PrintingGateController
# from service.authorizer.gate.serial_gate_controller import SerialGateController
# from service.authorizer.log.actual_car_logger import ActualCarLogger
# from service.authorizer.log.repository.actual_car_log_repository import ActualCarLogRepository
# from service.authorizer.monitor.car.instant_checking_car_monitor import InstantCheckingCarMonitor
# from service.authorizer.monitor.license.actual_license_plate_monitor import ActualLicensePlateMonitor
# from service.authorizer.parking.actual_parking_space_counter import ActualParkingSpaceCounter
# from service.authorizer.parking.repository.actual_parking_space_count_repository import \
#     ActualParkingSpaceCountRepository
# from service.authorizer.stream.webcam_video_stream_provider import SourceVideoStreamProvider
# from service.connection.websocket_manager import WebsocketManager
# from service.registry.actual_car_registry import ActualCarRegistry
# from service.registry.model.car import Car
# from service.registry.repository.actual_car_repository import ActualCarRepository
#
# registration_id_format = AnyRegistrationIdFormat()
# registration_id_filter = ScoringRegistrationIdFilter(registration_id_format)
# car_repository = ActualCarRepository()
# car_registry = ActualCarRegistry(car_repository)
# display_controller_subject = Subject[DisplayControllerEvent]()
# parking_space_counter = ActualParkingSpaceCounter(ActualParkingSpaceCountRepository())
# display_controller = SubjectDisplayController(display_controller_subject, parking_space_counter)
# log_repository = ActualCarLogRepository()
#
# entrance_video_stream_provider = SourceVideoStreamProvider(0)
# entrance_license_plate_monitor = ActualLicensePlateMonitor(entrance_video_stream_provider, headless=False)
# entrance_car_monitor = InstantCheckingCarMonitor(entrance_license_plate_monitor, car_registry, registration_id_format)
# entrance_gate_controller = PrintingGateController()
# # entrance_gate_controller = PrintingGateController()
# entrance_car_logger = ActualCarLogger(log_repository)
# parking_entrance_control = ParkingEntranceControl(
#     entrance_car_monitor,
#     entrance_gate_controller,
#     display_controller,
#     parking_space_counter,
#     entrance_car_logger,
# )
#
# parking_entrance_control.start()
#
# # exit_video_stream_provider = SourceVideoStreamProvider(1)
# # exit_license_plate_monitor = ActualLicensePlateMonitor(exit_video_stream_provider, headless=False)
# # exit_car_monitor = InstantCheckingCarMonitor(exit_license_plate_monitor, car_registry, registration_id_format)
# # exit_gate_controller = PrintingGateController()
# # # exit_gate_controller = PrintingGateController()
# # exit_car_logger = ActualCarLogger(log_repository)
# # parking_exit_control = ParkingExitControl(
# #     exit_car_monitor,
# #     exit_gate_controller,
# #     display_controller,
# #     parking_space_counter,
# #     exit_car_logger,
# # )
# #
# # parking_exit_control.start()
#
# app = FastAPI()
#
#
# @app.websocket('/ws')
# async def display_web_socket(websocket: WebSocket):
#     await websocket.accept()
#
#     vacant_space = parking_space_counter.get_parking_space_count().vacant_space
#     await websocket.send_json({
#         'status': 'VACANT_SPACE_UPDATE',
#         'vacant_space': vacant_space,
#     })
#
#     async def async_on_next(event: DisplayControllerEvent):
#         if event is None:
#             await websocket.send_json({
#                 'status': 'IDLE',
#                 'event': 'Waiting for a car to pass',
#             })
#         elif isinstance(event, int):
#             await websocket.send_json({
#                 'status': 'VACANT_SPACE_UPDATE',
#                 'vacant_space': event,
#             })
#         elif isinstance(event, Car):
#             # The serializer is not working for some reason. 😁
#             await websocket.send_json({
#                 'status': 'CAR_AUTHORIZED',
#                 'car': {
#                     'registration_id': event.registration_id,
#                     'make': event.make,
#                     'model': event.model,
#                     'year': event.year,
#                     'color': event.color,
#                     'owner': event.owner,
#                 }
#             })
#         elif isinstance(event, str):
#             await websocket.send_json({
#                 'status': 'CAR_UNAUTHORIZED',
#                 'registration_id': event,
#             })
#
#     def on_next(event: DisplayControllerEvent):
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)
#         task = loop.create_task(async_on_next(event))
#         loop.run_until_complete(task)
#
#     display_controller_subject.subscribe(on_next)
#
#     try:
#         while True:
#             await websocket.receive_text()
#     except WebSocketDisconnect:
#         pass
#
# # license_plate_monitor.get_thread().join()
