from typing import Optional

from fastapi import FastAPI, WebSocket, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from reactivex import Subject

from service.authenticator.admin.actual_admin_authenticator import ActualAdminAuthenticator
from service.authenticator.admin.admin_authenticator import AdminAuthenticator
from service.authenticator.admin.repository.actual_admin_password_repository import ActualAdminPasswordRepository
from service.authenticator.token.actual_token_processor import ActualTokenProcessor
from service.authorizer.access.parking_entrance_control import ParkingEntranceControl
from service.authorizer.display.subject_display_controller import DisplayControllerEvent, SubjectDisplayController
from service.authorizer.filter.scoring_registration_id_filter import ScoringRegistrationIdFilter
from service.authorizer.format.any_registration_id_format import AnyRegistrationIdFormat
from service.authorizer.format.philippine_registration_id_format import PhilippineRegistrationIdFormat
from service.authorizer.gate.printing_gate_controller import PrintingGateController
from service.authorizer.log.actual_car_logger import ActualCarLogger
from service.authorizer.log.car_logger import CarLogger
from service.authorizer.log.repository.actual_car_log_repository import ActualCarLogRepository
from service.authorizer.monitor.car.instant_checking_car_monitor import InstantCheckingCarMonitor
from service.authorizer.monitor.license.actual_license_plate_monitor import ActualLicensePlateMonitor
from service.authorizer.monitor.license.modular_license_plate_monitor import ModularLicensePlateMonitor
from service.authorizer.parking.actual_parking_space_counter import ActualParkingSpaceCounter
from service.authorizer.parking.repository.actual_parking_space_count_repository import \
    ActualParkingSpaceCountRepository
from service.authorizer.recognition.detector.yolo_license_plate_detector import YoloLicensePlateDetector
from service.authorizer.recognition.preprocessor.license_plate_preprocessor import LicensePlatePreprocessor
from service.authorizer.recognition.reader.easy_orc_text_reader import EasyOcrTextReader
from service.authorizer.stream.webcam_video_stream_provider import SourceVideoStreamProvider
from service.connection.websocket_manager import WebsocketManager
from service.exception import PasswordTooShortError, \
    IncorrectPasswordError, InvalidTokenError
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.repository.actual_car_repository import ActualCarRepository
from sockets.car_logger import handle_car_logger_websocket
from sockets.car_registry import handle_car_registry_websocket
from sockets.display_controller import handle_display_controller_websocket
from sockets.parking_space_counter import handle_parking_space_counter_websocket

app = FastAPI()

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

admin_authenticator: AdminAuthenticator = ActualAdminAuthenticator(
    ActualAdminPasswordRepository(),
    ActualTokenProcessor(),
)

car_registry_websocket_manager = WebsocketManager(admin_authenticator)

registration_id_format = PhilippineRegistrationIdFormat()
registration_id_filter = ScoringRegistrationIdFilter(registration_id_format)
car_repository = ActualCarRepository()
car_registry = ActualCarRegistry(car_repository)
display_controller_subject = Subject[DisplayControllerEvent]()
parking_space_counter = ActualParkingSpaceCounter(ActualParkingSpaceCountRepository())
display_controller = SubjectDisplayController(display_controller_subject, parking_space_counter)
log_repository = ActualCarLogRepository()

entrance_video_stream_provider = SourceVideoStreamProvider(1)
# entrance_license_plate_monitor = ActualLicensePlateMonitor(entrance_video_stream_provider, headless=False)
entrance_license_plate_monitor = ModularLicensePlateMonitor(
    'Entrance',
    entrance_video_stream_provider,
    YoloLicensePlateDetector(),
    LicensePlatePreprocessor(),
    EasyOcrTextReader(),
)
entrance_car_monitor = InstantCheckingCarMonitor(entrance_license_plate_monitor, car_registry, registration_id_format)
entrance_gate_controller = PrintingGateController()
# entrance_gate_controller = PrintingGateController()
car_logger: CarLogger = ActualCarLogger(ActualCarLogRepository())
parking_entrance_control = ParkingEntranceControl(
    entrance_car_monitor,
    entrance_gate_controller,
    display_controller,
    parking_space_counter,
    car_logger,
)

parking_entrance_control.start()

# TODO: Uncomment
# exit_video_stream_provider = SourceVideoStreamProvider(1)
# exit_license_plate_monitor = ActualLicensePlateMonitor(exit_video_stream_provider, headless=False)
# exit_license_plate_monitor = ModularLicensePlateMonitor(
#     'Entrance',
#     exit_video_stream_provider,
#     YoloLicensePlateDetector(),
#     LicensePlatePreprocessor(),
#     EasyOcrTextReader(),
# )
# exit_car_monitor = InstantCheckingCarMonitor(exit_license_plate_monitor, car_registry, registration_id_format)
# exit_gate_controller = PrintingGateController()
# # exit_gate_controller = PrintingGateController()
# exit_car_logger = ActualCarLogger(log_repository)
# parking_exit_control = ParkingExitControl(
#     exit_car_monitor,
#     exit_gate_controller,
#     display_controller,
#     parking_space_counter,
#     exit_car_logger,
# )
#
# parking_exit_control.start()


class Password(BaseModel):
    password: str


class PasswordChange(BaseModel):
    old_password: Optional[str] = None
    new_password: str


@app.exception_handler(PasswordTooShortError)
async def password_too_short_exception_handler(_, exception: PasswordTooShortError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "PASSWORD_TOO_SHORT",
            "min_length": exception.min_length,
            "message": exception.message,
        },
    )


@app.exception_handler(IncorrectPasswordError)
async def incorrect_password_exception_handler(_, exception: IncorrectPasswordError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": "INCORRECT_PASSWORD",
            "message": exception.message,
        },
    )


@app.exception_handler(InvalidTokenError)
async def invalid_token_exception_handler(_, exception: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "status": "INVALID_TOKEN",
            "message": exception.message,
        },
    )


@app.exception_handler(Exception)
async def internal_server_error_handler(_, exception: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "INTERNAL_SERVER_ERROR",
            "message": str(exception),
        },
    )


@app.get("/admin/password-set", status_code=status.HTTP_200_OK)
async def password_set():
    return {
        "status": "SUCCESSFUL",
        "password_set": admin_authenticator.password_set(),
    }


@app.post("/admin/login", status_code=status.HTTP_200_OK)
async def login(password: Password):
    return {
        "status": "SUCCESSFUL",
        "token": admin_authenticator.login(password.password),
    }


@app.post("/admin/change-password", status_code=status.HTTP_200_OK)
async def change_password(password_change: PasswordChange):
    admin_authenticator.change_password(password_change.old_password, password_change.new_password)
    return {
        "status": "SUCCESSFUL",
        "message": "Password changed successfully",
    }


@app.websocket('/car-registry')
async def car_registry_websocket(websocket: WebSocket):
    await handle_car_registry_websocket(car_registry_websocket_manager, car_registry, websocket)


@app.websocket('/car-logger')
async def car_logger_websocket(websocket: WebSocket):
    await handle_car_logger_websocket(car_registry_websocket_manager, car_logger, websocket)


@app.websocket('/parking-space-counter')
async def parking_space_counter_websocket(websocket: WebSocket):
    await handle_parking_space_counter_websocket(car_registry_websocket_manager, parking_space_counter, websocket)


@app.websocket('/display-controller')
async def display_controller_websocket(websocket: WebSocket):
    await handle_display_controller_websocket(websocket, parking_space_counter, display_controller_subject)
