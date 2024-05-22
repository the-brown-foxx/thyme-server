from service.authorizer.access.actual_parking_access_control import ActualParkingAccessControl
from service.authorizer.display.printing_display_controller import PrintingDisplayController
from service.authorizer.filter.scoring_registration_id_filter import ScoringRegistrationIdFilter
from service.authorizer.format.any_registration_id_format import AnyRegistrationIdFormat
from service.authorizer.gate.printing_gate_controller import PrintingGateController
from service.authorizer.log.actual_car_logger import ActualCarLogger
from service.authorizer.log.repository.actual_car_log_repository import ActualCarLogRepository
from service.authorizer.monitor.car.instant_checking_car_monitor import InstantCheckingCarMonitor
from service.authorizer.monitor.license.actual_license_plate_monitor import ActualLicensePlateMonitor
from service.authorizer.stream.dummy_video_stream_provider import DummyVideoStreamProvider
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.repository.actual_car_repository import ActualCarRepository

video_stream_provider = DummyVideoStreamProvider()
registration_id_format = AnyRegistrationIdFormat()
registration_id_filter = ScoringRegistrationIdFilter(registration_id_format)
license_plate_monitor = ActualLicensePlateMonitor(video_stream_provider, headless=False)
car_repository = ActualCarRepository()
car_registry = ActualCarRegistry(car_repository)
registration_id_format = AnyRegistrationIdFormat()
car_monitor = InstantCheckingCarMonitor(license_plate_monitor, car_registry, registration_id_format)
gate_controller = PrintingGateController()
display_controller = PrintingDisplayController()
log_repository = ActualCarLogRepository()
car_logger = ActualCarLogger(log_repository, video_stream_provider)
parking_access_control = ActualParkingAccessControl(
    car_monitor,
    gate_controller,
    display_controller,
    car_logger,
)

parking_access_control.start()

license_plate_monitor.get_thread().join()
