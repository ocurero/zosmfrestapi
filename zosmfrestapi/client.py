from zosmfrestapi.services.authentication import AuthenticationServices
from zosmfrestapi.services.dataset import DatasetServices
from zosmfrestapi.services.software import SoftwareServices
from zosmfrestapi.services.software_updates import SoftwareUpdatesServices
from zosmfrestapi.services.topology import TopologyServices
from zosmfrestapi.services.workflow import WorkflowServices


class ZosmfClient(
    AuthenticationServices,
    DatasetServices,
    TopologyServices,
    WorkflowServices,
    SoftwareServices,
    SoftwareUpdatesServices,
):
    """Synchronous client for the z/OSMF REST APIs.

    The client combines authentication, datasets, topology, workflows,
    software-instance management, and software-update operations around one
    reusable HTTP session. Update-start and resume methods can change the
    selected target zone; use them only when those changes are intended.

    Use it as a context manager to close the underlying HTTP session reliably.

    Examples:
        Use a context manager when making requests:

            with ZosmfClient("https://zosmf.example",
                             username="demouser", password="DEMOPASS") as client:
                systems = client.get_systems()

        Use a client without using a context manager:

            client = ZosmfClient("https://zosmf.example",
                                 username="demouser", password="DEMOPASS")
            systems = client.get_systems()
            client.close()

        Use a client with mTLS authentication:

            with ZosmfClient("https://zosmf.example",
                             username="demouser", password="DEMOPASS",
                             cert=("/path/to/cert", "/path/to/key")) as client:
                systems = client.get_systems()
    """
