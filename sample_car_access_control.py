from service.authorizer.access.actual_parking_access_control import ActualParkingAccessControl
from service.authorizer.display.printing_display_controller import PrintingDisplayController
from service.authorizer.filter.scoring_registration_id_filter import ScoringRegistrationIdFilter
from service.authorizer.format.any_registration_id_format import AnyRegistrationIdFormat
from service.authorizer.gate.printing_gate_controller import PrintingGateController
from service.authorizer.monitor.actual_license_plate_monitor import ActualLicensePlateMonitor
from service.authorizer.stream.dummy_video_stream_provider import DummyVideoStreamProvider
from service.registry.actual_car_registry import ActualCarRegistry
from service.registry.repository.actual_car_repository import ActualCarRepository

video_stream_provider = DummyVideoStreamProvider()
registration_id_format = AnyRegistrationIdFormat()
registration_id_filter = ScoringRegistrationIdFilter(registration_id_format)
license_plate_monitor = ActualLicensePlateMonitor(video_stream_provider, registration_id_filter, headless=False)
car_repository = ActualCarRepository()
car_registry = ActualCarRegistry(car_repository)
gate_controller = PrintingGateController()
display_controller = PrintingDisplayController()
parking_access_control = ActualParkingAccessControl(
    license_plate_monitor,
    car_registry,
    gate_controller,
    display_controller,
)

parking_access_control.start()

license_plate_monitor.get_thread().join()
