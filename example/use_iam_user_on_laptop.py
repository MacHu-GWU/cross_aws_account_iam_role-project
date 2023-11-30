# -*- coding: utf-8 -*-

"""
This script tests the capability of giving a IAM role access to other AWS accounts.
"""

from boto_session_manager import BotoSesManager
import cross_aws_account_iam_role.api as x_aws_acc

prefix = "a1b2-"

grantee_1_bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
iam_user_arn = x_aws_acc.IamUserArn(
    account=grantee_1_bsm.aws_account_id,
    name="sanhe",  # this IAM user's AWS profile is bmt_app_dev_us_east_1
)
grantee_1 = x_aws_acc.Grantee(
    bsm=grantee_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-iam-user-principal-grantee",
    iam_arn=iam_user_arn,
    policy_name=f"{prefix}cross_aws_account_iam_role_iam_user_principal_grantee",
)

owner_1_bsm = BotoSesManager(profile_name="bmt_app_test_us_east_1")
owner_1 = x_aws_acc.Owner(
    bsm=owner_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-iam-user-principal-test-owner",
    role_name=f"{prefix}cross_aws_account_iam_role_iam_user_principal_test_owner",
    policy_name=f"{prefix}cross_aws_account_iam_role_iam_user_principal_test_owner",
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
    grantee_1.test_bsm = grantee_1_bsm
    print("at begin:")
    call_api(grantee_1.test_bsm)
    print("validate cross account permission ...")
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
    deploy()
    validate()
    # delete()
