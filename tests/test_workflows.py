import pytest
from zosmfrestapi import ZosmfClient
from zosmfrestapi.exceptions import ZosmfWorkflowBaseError, ZosmfWorkflowError
from zosmfrestapi.models import WorkflowItem
from zosmfrestapi.services import workflow as workflow_s
from zosmfrestapi.testing import (
    make_archived_worfklow_list,
    make_new_workflow,
    make_workflow,
    make_workflow_list,
    make_workflow_with_steps,
    make_workflow_with_variables,
)


@pytest.mark.vcr
def test_get_workflows():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_workflows() == make_workflow_list()


@pytest.mark.vcr
def test_get_workflows_raises_ZosmfWorkflowError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(
            ZosmfWorkflowBaseError,
            match="Invalid status 'not-valid-error'. Valid options are: "
            "'in-progress', 'complete', 'automation-in-progress', 'canceled'.",
        ):
            client.get_workflows(status="not-valid-error")


@pytest.mark.vcr
def test_get_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_workflow("fc4fc0fa-1fa3-4247-bb2d-7f5203e0c3c7") == make_workflow()


@pytest.mark.vcr
def test_get_workflow_with_steps():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.get_workflow(
                "fc4fc0fa-1fa3-4247-bb2d-7f5203e0c3c7",
                steps=True,
            )
            == make_workflow_with_steps()
        )


@pytest.mark.vcr
def test_get_workflow_with_variables():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.get_workflow(
                "ef73bcd5-e904-4fcf-8d88-836dbffc0f62",
                variables=True,
            )
            == make_workflow_with_variables()
        )


@pytest.mark.vcr
def test_get_archived_workflows():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_archived_workflows() == make_archived_worfklow_list()


@pytest.mark.vcr
def test_create_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.create_workflow(
                WorkflowItem(
                    name="myworkflow1",
                    definition="/u/demouser/test.xml",
                    owner="demouser",
                    system="TSTA",
                )
            )
            == make_new_workflow()
        )


@pytest.mark.vcr
def test_start_workflow_nowait():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.start_workflow(
                workflow_id="f0541261-573d-48ed-8f3e-75884db326ec", wait=False
            )
            is True
        )


@pytest.mark.vcr
def test_start_workflow_wait(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        states = ["automation-in-progress", "complete"]
        states.reverse()
        monkeypatch.setattr(workflow_s.time, "sleep", lambda *_: None)
        for workflow in client.start_workflow(
            workflow_id="f0541261-573d-48ed-8f3e-75884db326ec",
            wait=True,
        ):
            if workflow.status == states[-1]:
                states.pop()
        assert not states


@pytest.mark.vcr
def test_wait_for_workflow(monkeypatch):
    with ZosmfClient("https://zosmf.example") as client:
        states = ["automation-in-progress", "complete"]
        states.reverse()
        monkeypatch.setattr(workflow_s.time, "sleep", lambda *_: None)
        for workflow in client.wait_for_workflow(
            workflow_id="f0541261-573d-48ed-8f3e-75884db326ec",
        ):
            if workflow.status == states[-1]:
                states.pop()
        assert not states


@pytest.mark.vcr
def test_cancel_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.cancel_workflow(workflow_id="ef73bcd5-e904-4fcf-8d88-836dbffc0f62") is None
        )


@pytest.mark.vcr
def test_remove_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.remove_workflow(workflow_id="ef73bcd5-e904-4fcf-8d88-836dbffc0f62") is None
        )


@pytest.mark.vcr
def test_archive_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.archive_workflow(workflow_id="f0541261-573d-48ed-8f3e-75884db326ec") is None
        )


@pytest.mark.vcr
def test_remove_archived_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.remove_archived_workflow(workflow_id="f0541261-573d-48ed-8f3e-75884db326ec")
            is None
        )


@pytest.mark.vcr
def test_workflow_raises_ZosmfWorkflowError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfWorkflowError):
            client.cancel_workflow(workflow_id="ef73bcd5-e904-4fcf-8d88-836dbffc0f62")
