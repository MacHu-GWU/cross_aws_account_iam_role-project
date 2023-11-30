# -*- coding: utf-8 -*-

"""
This script tests the capability of giving a IAM role access to other AWS accounts.
"""

import json
import botocore.exceptions
from boto_session_manager import BotoSesManager
import cross_aws_account_iam_role.api as x_aws_acc

prefix = "a1b2-"

grantee_1_bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
grantee_1_role_name = "cross_aws_account_iam_role_iam_principal"
try:
    grantee_1_bsm.iam_client.create_role(
        RoleName=grantee_1_role_name,
        AssumeRolePolicyDocument=json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": f"arn:aws:iam::{grantee_1_bsm.aws_account_id}:user/sanhe"
                        },
                        "Action": "sts:AssumeRole",
                    }
                ],
            }
        ),
    )
except botocore.exceptions.ClientError as e:
    if e.response["Error"]["Code"] == "EntityAlreadyExists":
        pass
    else:
        raise e

iam_role_arn = x_aws_acc.IamRoleArn(
    account=grantee_1_bsm.aws_account_id,
    name=grantee_1_role_name,
)
grantee_1 = x_aws_acc.Grantee(
    bsm=grantee_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-iam-principal-grantee",
    iam_arn=iam_role_arn,
    policy_name=f"{prefix}cross_aws_account_iam_role_iam_principal_grantee",
)

owner_1_bsm = BotoSesManager(profile_name="bmt_app_test_us_east_1")
owner_1 = x_aws_acc.Owner(
    bsm=owner_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-iam-principal-test-owner",
    role_name=f"{prefix}cross_aws_account_iam_role_iam_principal_test_owner",
    policy_name=f"{prefix}cross_aws_account_iam_role_iam_principal_test_owner",
    policy_document={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:ListAccountAliases",
                    "sts:GetCallerIdentity",
                ],
                "Resource": "*",
            },
        ],
    },
)

owner_1.grant(grantee_1)


def deploy():
    x_aws_acc.deploy(
        grantee_list=[grantee_1],
        owner_list=[owner_1],
    )


def call_api(bsm: BotoSesManager):
    res = bsm.sts_client.get_caller_identity()
    parts = res["Arn"].split(":")
    parts[4] = parts[4][:2] + "********" + parts[4][-2:]
    arn = ":".join(parts)
    print(f"    now we are using principal {arn}")


def validate():
    grantee_1.test_bsm = grantee_1_bsm.assume_role(
        role_arn=x_aws_acc.IamRoleArn(
            account=grantee_1_bsm.aws_account_id,
            name=grantee_1_role_name,
        ).arn,
    )
    x_aws_acc.validate(
        grantee_list=[grantee_1],
        call_api=call_api,
        verbose=False,
    )


def delete():
    x_aws_acc.delete(
        grantee_list=[grantee_1],
        owner_list=[owner_1],
    )


if __name__ == "__main__":
    # deploy()
    # validate()
    delete()
