from zosmfrestapi.models.workflow import (
    WorkflowArchivedListItem,
    WorkflowInstance,
    WorkflowListItem,
)


def make_workflow_list():
    return [
        WorkflowListItem(
            instanceURI="/zosmf/workflow/rest/1.0/workflows/"
            "8ed3a85e-6472-47eb-ba44-19e9511df450",
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


def make_workflow(steps=[], variables=[]):
    return WorkflowInstance(
        name="HOOLIE",
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
        steps=steps,
        access="Public",
        productVersion=None,
        productID=None,
        variables=variables,
        category="general",
        system="TST01.TSTA",
        workflowDescription="The Box III, Gavin Belson Signature Edition",
        workflowID="Hoolie",
        owner="FOOBAR",
        accountInfo=None,
        automationStatus=None,
        containsParallelSteps=False,
        isCallable=None,
        workflowKey="fc4fc0fa-1fa3-4247-bb2d-7f5203e0c3c7",
        productName=None,
    )


def make_new_workflow():
    return WorkflowInstance(
        name="HOOLIE",
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
        workflowKey="fc4fc0fa-1fa3-4247-bb2d-7f5203e0c3c7",
        productName=None,
    )


def make_workflow_with_steps():

    step1 = """//*********************************************************************
//*              STEP - Create temporary directory using BPXBATCH     *
//*********************************************************************
//*
//CREATE   EXEC PGM=BPXBATCH
//*
//STDOUT   DD SYSOUT=*
//*
//STDERR   DD SYSOUT=*
//*
//STDPARM  DD *
SH mkdir -m 700 /tmp/IZUWORKFLOW-17932912593740.328682
/*
//*
//*********************************************************************
//*              STEP - Create script in temp directory using BPXCOPY *
//*********************************************************************
//*
//UXCOPY   EXEC PGM=BPXCOPY,
//             PARM='ELEMENT(MYSCRIPT) TYPE(TEXT) PATHMODE(0,7,0,0)'
//*
//SYSTSPRT DD SYSOUT=*
//*
//SYSIN    DD DUMMY
//*
//SYSUT2   DD PATH='/tmp/IZUWORKFLOW-17932912593740.328682'
//*
//SYSUT1   DD *,DLM=$$
/bin/echo 'HELLO WORLD 1'
$$
//*
//*********************************************************************
//*              STEP - Execute script using BPXBATCH                 *
//*********************************************************************
//*
//XBATCH   EXEC PGM=BPXBATCH
//*
//STDOUT   DD SYSOUT=*
//*
//STDERR   DD SYSOUT=*
//*
//STDPARM  DD *
SH /tmp/IZUWORKFLOW-17932912593740.328682/MYSCRIPT
/*
//*
//*********************************************************************
//*              STEP - Delete temporary directory using BPXBATCH     *
//*********************************************************************
//*
//REMOVE   EXEC PGM=BPXBATCH
//*
//STDOUT   DD SYSOUT=*
//*
//STDERR   DD SYSOUT=*
//*
//STDPARM  DD *
SH rm -r /tmp/IZUWORKFLOW-17932912593740.328682
/*
//*
//*********************************************************************"""
    step2 = """//*********************************************************************
//*              STEP - Create temporary directory using BPXBATCH     *
//*********************************************************************
//*
//CREATE   EXEC PGM=BPXBATCH
//*
//STDOUT   DD SYSOUT=*
//*
//STDERR   DD SYSOUT=*
//*
//STDPARM  DD *
SH mkdir -m 700 /tmp/IZUWORKFLOW-17932912593750.432322
/*
//*
//*********************************************************************
//*              STEP - Create script in temp directory using BPXCOPY *
//*********************************************************************
//*
//UXCOPY   EXEC PGM=BPXCOPY,
//             PARM='ELEMENT(MYSCRIPT) TYPE(TEXT) PATHMODE(0,7,0,0)'
//*
//SYSTSPRT DD SYSOUT=*
//*
//SYSIN    DD DUMMY
//*
//SYSUT2   DD PATH='/tmp/IZUWORKFLOW-17932912593750.432322'
//*
//SYSUT1   DD *,DLM=$$
/bin/echo 'HELLO WORLD 2'
$$
//*
//*********************************************************************
//*              STEP - Execute script using BPXBATCH                 *
//*********************************************************************
//*
//XBATCH   EXEC PGM=BPXBATCH
//*
//STDOUT   DD SYSOUT=*
//*
//STDERR   DD SYSOUT=*
//*
//STDPARM  DD *
SH /tmp/IZUWORKFLOW-17932912593750.432322/MYSCRIPT
/*
//*
//*********************************************************************
//*              STEP - Delete temporary directory using BPXBATCH     *
//*********************************************************************
//*
//REMOVE   EXEC PGM=BPXBATCH
//*
//STDOUT   DD SYSOUT=*
//*
//STDERR   DD SYSOUT=*
//*
//STDPARM  DD *
SH rm -r /tmp/IZUWORKFLOW-17932912593750.432322
/*
//*
//*********************************************************************"""

    return make_workflow(
        steps=[
            {
                "template": step1,
                "instructions": "",
                "maxLrecl": 1024,
                "failedPattern": [],
                "description": "The Box III, Gavin Belson Signature Edition: because"
                " ordinary excellence was never enough",
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
                "template": step2,
                "instructions": "",
                "maxLrecl": 1024,
                "failedPattern": [],
                "description": "Engineered for those who don't follow the"
                " future, but define it.",
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
        ]
    )


def make_workflow_with_variables():
    return make_workflow()


def make_archived_worfklow_list():
    return [
        WorkflowArchivedListItem(
            archivedInstanceURI="/zosmf/workflow/rest/1.0/archivedworkflows/"
            "07775b08-2dd9-4810-abb4-26f7cb05152a",
            workflowKey="07775b08-2dd9-4810-abb4-26f7cb05152a",
            workflowName="myworkflow",
        )
    ]
