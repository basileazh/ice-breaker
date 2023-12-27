from ice_breaker.core.log import logger
from ice_breaker.models.service_type import ServiceType
from ice_breaker.services.abstract_service import AbstractService
from ice_breaker.services.linkedin_service import LinkedInService

SERVICES = {
    str(ServiceType.LINKEDIN): LinkedInService,
    # str(ServiceType.TWITTER): TwitterService,  # Uncomment when TwitterService is implemented
}


def get_service_class(service_type: str) -> type[AbstractService]:
    """
    Returns the service class for the given service type.
    This is a factory method for the different services. This method is the one to use to get a service class.

    :param service_type: The service type. Must be one of the values in ServiceType.
    :return: The service class.
    """

    logger.debug(f"Getting service class for {service_type}...")
    if service_type not in list(SERVICES.keys()):
        raise ValueError(f"Service {service_type} is not implemented.")
    logger.debug(f"Service class for {service_type} : {SERVICES[service_type]}.")

    return SERVICES[service_type]


def get_services_list() -> list[str]:
    """
    Returns the list of available services.

    :return: The list of available services, as in ServiceType.
    """
    logger.debug("Getting services list...")
    logger.debug(f"Services list : {list(SERVICES.keys())}.")

    return list(SERVICES.keys())
