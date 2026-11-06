import pytest

from zosmfrestapi.services import workflow as workflow_s

from zosmfrestapi import (
    WorkflowArchivedListItem,
    WorkflowInstance,
    WorkflowItem,
    WorkflowListItem,
    ZosmfClient,
    ZosmfWorkflowBaseError,
    ZosmfWorkflowError,
)


@pytest.mark.vcr
def test_get_workflows():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_workflows() == [
            WorkflowListItem(
                instanceURI="/zosmf/workflow/rest/1.0/workflows/8ed3a85e-6472-47eb-ba44-19e9511df450",
                owner="FOOBAR",
                vendor="Hooli Software",
                workflowDefinitionFileMD5Value="c87342978ad879837a9872899cse2001",
                workflowDescription="The Box III, Gavin Belson Signature Edition",
                workflowID="HOOLMC",
                workflowKey="8ed3a85e-6472-47eb-ba44-19e9511df450",
                workflowName="HOOLIE",
                workflowVersion="1.0",
            ),
        ]


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
        assert client.get_workflow(
            "fc4fc0fa-1fa3-4247-bb2d-7f5203e0c3c7"
        ) == WorkflowInstance(
            name="HOOLIE",
            percentComplete=0,
            workflowDefinitionFileMD5Value="c87342978ad879837a9872899cse2001",
            workflowArchiveSAFID="FOOBAR",
            jobStatement=None,
            globalVariableGroup=None,
            jobsOutputDirectory="/foo/bar/log",
            scope="sysplex",
            status="in-progress",
            vendor="Hooli Software",
            deleteCompletedJobs=False,
            autoDeleteOnCompletion=False,
            isInstanceVariableWithoutPrefix=False,
            workflowVersion="1.0",
            steps=[],
            access="Public",
            productVersion=None,
            productID=None,
            variables=[],
            category="general",
            system="TST01.TSTA",
            workflowDescription="The Box III, Gavin Belson Signature Edition",
            workflowID="myworkflow",
            owner="FOOBAR",
            accountInfo=None,
            automationStatus=None,
            containsParallelSteps=False,
            isCallable=None,
            workflowKey="fc4fc0fa-1fa3-4247-bb2d-7f5203e0c3c7",
            productName=None,
        )


@pytest.mark.vcr
def test_get_workflow_with_steps():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_workflow(
            "ef73bcd5-e904-4fcf-8d88-836dbffc0f62",
            steps=True,
        ) == WorkflowInstance(
            name="myworkflow",
            percentComplete=0,
            workflowDefinitionFileMD5Value="8e8fabbd0f72c54119a3748427fc0f25",
            workflowArchiveSAFID="FOOBAR",
            jobStatement=None,
            globalVariableGroup=None,
            jobsOutputDirectory="/foo/bar/log",
            scope="sysplex",
            status="in-progress",
            vendor="Hooli Software",
            deleteCompletedJobs=False,
            autoDeleteOnCompletion=False,
            isInstanceVariableWithoutPrefix=False,
            workflowVersion="1.0",
            steps=[
                {
                    "template": "//*********************************************************************\n//*              STEP - Cre"
                    "ate temporary directory using BPXBATCH     *\n//****************************************************"
                    "*****************\n//*\n//CREATE   EXEC PGM=BPXBATCH\n//*\n//STDOUT   DD SYSOUT=*\n//*\n//STDERR   DD"
                    " SYSOUT=*\n//*\n//STDPARM  DD *\nSH mkdir -m 700 /tmp/IZUWORKFLOW-17932912593740.328682\n/*\n//*\n//*"
                    "********************************************************************\n//*              STEP - Create "
                    "script in temp directory using BPXCOPY *\n//*********************************************************"
                    "************\n//*\n//UXCOPY   EXEC PGM=BPXCOPY,\n//             PARM='ELEMENT(MYSCRIPT) TYPE(TEXT) PA"
                    "THMODE(0,7,0,0)'\n//*\n//SYSTSPRT DD SYSOUT=*\n//*\n//SYSIN    DD DUMMY\n//*\n//SYSUT2   DD PATH='/tm"
                    "p/IZUWORKFLOW-17932912593740.328682'\n//*\n//SYSUT1   DD *,DLM=$$\n/bin/echo 'HELLO WORLD 1'\n$$\n//*"
                    "\n//*********************************************************************\n//*              STEP - Ex"
                    "ecute script using BPXBATCH                 *\n//****************************************************"
                    "*****************\n//*\n//XBATCH   EXEC PGM=BPXBATCH\n//*\n//STDOUT   DD SYSOUT=*\n//*\n//STDERR   DD"
                    " SYSOUT=*\n//*\n//STDPARM  DD *\nSH /tmp/IZUWORKFLOW-17932912593740.328682/MYSCRIPT\n/*\n//*\n//*****"
                    "****************************************************************\n//*              STEP - Delete temp"
                    "orary directory using BPXBATCH     *\n//*************************************************************"
                    "********\n//*\n//REMOVE   EXEC PGM=BPXBATCH\n//*\n//STDOUT   DD SYSOUT=*\n//*\n//STDERR   DD SYSOUT=*"
                    "\n//*\n//STDPARM  DD *\nSH rm -r /tmp/IZUWORKFLOW-17932912593740.328682\n/*\n//*\n//*****************"
                    "****************************************************",
                    "instructions": "",
                    "maxLrecl": 1024,
                    "failedPattern": [],
                    "description": "The Box III, Gavin Belson Signature Edition: because ordinary excellence was never enough",
                    "outputVariablesPrefix": None,
                    "variable-references": None,
                    "saveAsUnixFileSub": False,
                    "procName": "IZUFPROC",
                    "title": "Infinite Scale",
                    "jobInfo": None,
                    "timeout": 0,
                    "regionSize": 0,
                    "skills": None,
                    "isRestStep": False,
                    "output": None,
                    "outputSub": False,
                    "returnCode": None,
                    "outputSysoutDD": False,
                    "successPattern": None,
                    "state": "Unassigned",
                    "templateSub": False,
                    "owner": None,
                    "autoEnable": True,
                    "submitAs": "shell-JCL",
                    "userDefined": False,
                    "weight": "1",
                    "optional": False,
                    "steps": None,
                    "scriptParameters": None,
                    "saveAsUnixFile": None,
                    "instructionsSub": False,
                    "saveAsDatasetSub": False,
                    "isConditionStep": False,
                    "prereqStep": None,
                    "hasCalledWorkflow": False,
                    "name": "step1",
                    "stepNumber": "1",
                    "saveAsDataset": None,
                },
                {
                    "template": "//*********************************************************************\n//*              STEP - Cre"
                    "ate temporary directory using BPXBATCH     *\n//****************************************************"
                    "*****************\n//*\n//CREATE   EXEC PGM=BPXBATCH\n//*\n//STDOUT   DD SYSOUT=*\n//*\n//STDERR   D"
                    "D SYSOUT=*\n//*\n//STDPARM  DD *\nSH mkdir -m 700 /tmp/IZUWORKFLOW-17932912593750.432322\n/*\n//*\n/"
                    "/*********************************************************************\n//*              STEP - Crea"
                    "te script in temp directory using BPXCOPY *\n//*****************************************************"
                    "****************\n//*\n//UXCOPY   EXEC PGM=BPXCOPY,\n//             PARM='ELEMENT(MYSCRIPT) TYPE(TEXT) PATHM"
                    "ODE(0,7,0,0)'\n//*\n//SYSTSPRT DD SYSOUT=*\n//*\n//SYSIN    DD DUMMY\n//*\n//SYSUT2   DD PATH='/tmp/"
                    "IZUWORKFLOW-17932912593750.432322'\n//*\n//SYSUT1   DD *,DLM=$$\n/bin/echo 'HELLO WORLD 2'\n$$\n//*\n"
                    "//*********************************************************************\n//*              STEP - Exe"
                    "cute script using BPXBATCH                 *\n//****************************************************"
                    "*****************\n//*\n//XBATCH   EXEC PGM=BPXBATCH\n//*\n//STDOUT   DD SYSOUT=*\n//*\n//STDERR   D"
                    "D SYSOUT=*\n//*\n//STDPARM  DD *\nSH /tmp/IZUWORKFLOW-17932912593750.432322/MYSCRIPT\n/*\n//*\n//***"
                    "******************************************************************\n//*              STEP - Delete t"
                    "emporary directory using BPXBATCH     *\n//*********************************************************"
                    "************\n//*\n//REMOVE   EXEC PGM=BPXBATCH\n//*\n//STDOUT   DD SYSOUT=*\n//*\n//STDERR   DD SYS"
                    "OUT=*\n//*\n//STDPARM  DD *\nSH rm -r /tmp/IZUWORKFLOW-17932912593750.432322\n/*\n//*\n//***********"
                    "**********************************************************",
                    "instructions": "",
                    "maxLrecl": 1024,
                    "failedPattern": [],
                    "description": "Engineered for those who don't follow the future, but define it.",
                    "outputVariablesPrefix": None,
                    "variable-references": None,
                    "saveAsUnixFileSub": False,
                    "procName": "IZUFPROC",
                    "title": "Vision Engine",
                    "jobInfo": None,
                    "timeout": 0,
                    "regionSize": 0,
                    "skills": None,
                    "isRestStep": False,
                    "output": None,
                    "outputSub": False,
                    "returnCode": None,
                    "outputSysoutDD": False,
                    "successPattern": None,
                    "state": "Unassigned",
                    "templateSub": False,
                    "owner": None,
                    "autoEnable": True,
                    "submitAs": "shell-JCL",
                    "userDefined": False,
                    "weight": "1",
                    "optional": False,
                    "steps": None,
                    "scriptParameters": None,
                    "saveAsUnixFile": None,
                    "instructionsSub": False,
                    "saveAsDatasetSub": False,
                    "isConditionStep": False,
                    "prereqStep": None,
                    "hasCalledWorkflow": False,
                    "name": "step2",
                    "stepNumber": "2",
                    "saveAsDataset": None,
                },
            ],
            access="Public",
            productVersion=None,
            productID=None,
            variables=[],
            category="general",
            system="TST01.TSTA",
            workflowDescription="The Box III, Gavin Belson Signature Edition",
            workflowID="myworkflow",
            owner="FOOBAR",
            accountInfo=None,
            automationStatus=None,
            containsParallelSteps=False,
            isCallable=None,
            workflowKey="ef73bcd5-e904-4fcf-8d88-836dbffc0f62",
            productName=None,
        )


@pytest.mark.vcr
def test_get_workflow_with_variables():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_workflow(
            "ef73bcd5-e904-4fcf-8d88-836dbffc0f62",
            variables=True,
        ) == WorkflowInstance(
            name="myworkflow",
            percentComplete=0,
            workflowDefinitionFileMD5Value="8e8fabbd0f72c54119a3748427fc0f25",
            workflowArchiveSAFID="FOOBAR",
            jobStatement=None,
            globalVariableGroup=None,
            jobsOutputDirectory="/foo/bar/log",
            scope="sysplex",
            status="in-progress",
            vendor="Hooli Software",
            deleteCompletedJobs=False,
            autoDeleteOnCompletion=False,
            isInstanceVariableWithoutPrefix=False,
            workflowVersion="1.0",
            steps=[],
            access="Public",
            productVersion=None,
            productID=None,
            variables=[],
            category="general",
            system="TST01.TSTA",
            workflowDescription="The Box III, Gavin Belson Signature Edition",
            workflowID="myworkflow",
            owner="FOOBAR",
            accountInfo=None,
            automationStatus=None,
            containsParallelSteps=False,
            isCallable=None,
            workflowKey="ef73bcd5-e904-4fcf-8d88-836dbffc0f62",
            productName=None,
        )


@pytest.mark.vcr
def test_get_archived_workflows():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.get_archived_workflows() == [
            WorkflowArchivedListItem(
                archivedInstanceURI="/zosmf/workflow/rest/1.0/archivedworkflows/07775b08-2dd9-4810-abb4-26f7cb05152a",
                workflowKey="07775b08-2dd9-4810-abb4-26f7cb05152a",
                workflowName="myworkflow",
            )
        ]


@pytest.mark.vcr
def test_create_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert client.create_workflow(
            WorkflowItem(
                name="myworkflow1",
                definition="/u/demouser/test.xml",
                owner="demouser",
                system="TSTA",
            )
        ) == WorkflowInstance(
            name="myworkflow1",
            owner="demouser",
            system="TST01.TSTA (TSTA)",
            scope="sysplex",
            percentComplete=0,
            workflowDefinitionFileMD5Value="aca0b684798fb2dfd49261ca4d211d93",
            workflowArchiveSAFID="demouser",
            jobStatement=None,
            globalVariableGroup=None,
            jobsOutputDirectory=None,
            status="in-progress",
            vendor="Hoolie Software",
            deleteCompletedJobs=False,
            autoDeleteOnCompletion=False,
            isInstanceVariableWithoutPrefix=False,
            workflowVersion="1.0",
            steps=[],
            access="Public",
            productVersion=None,
            productID=None,
            variables=[],
            category="general",
            workflowDescription="The Box III, Gavin Belson Signature Edition",
            workflowID="Hoolie",
            accountInfo=None,
            automationStatus=None,
            containsParallelSteps=False,
            isCallable=None,
            workflowKey="f0541261-573d-48ed-8f3e-75884db326ec",
            productName=None,
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
            client.cancel_workflow(workflow_id="ef73bcd5-e904-4fcf-8d88-836dbffc0f62")
            is None
        )


@pytest.mark.vcr
def test_remove_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.remove_workflow(workflow_id="ef73bcd5-e904-4fcf-8d88-836dbffc0f62")
            is None
        )


@pytest.mark.vcr
def test_archive_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.archive_workflow(workflow_id="f0541261-573d-48ed-8f3e-75884db326ec")
            is None
        )


@pytest.mark.vcr
def test_remove_archived_workflow():
    with ZosmfClient("https://zosmf.example") as client:
        assert (
            client.remove_archived_workflow(
                workflow_id="f0541261-573d-48ed-8f3e-75884db326ec"
            )
            is None
        )


@pytest.mark.vcr
def test_workflow_raises_ZosmfWorkflowError():
    with ZosmfClient("https://zosmf.example") as client:
        with pytest.raises(ZosmfWorkflowError):
            client.cancel_workflow(workflow_id="ef73bcd5-e904-4fcf-8d88-836dbffc0f62")
