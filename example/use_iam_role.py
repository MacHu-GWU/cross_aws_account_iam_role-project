# -*- coding: utf-8 -*-

"""
This script setup cross AWS account IAM for the GitHub action open id connect IAM Role defined in.
https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/blob/main/example/setup_cross_aws_account_iam_role_project.py
"""

from boto_session_manager import BotoSesManager
import cross_aws_account_iam_role.api as x_aws_acc

prefix = "a1b2-"

grantee_1_bsm = BotoSesManager(profile_name="bmt_app_dev_us_east_1")
iam_role_arn = x_aws_acc.IamRoleArn(
    account=grantee_1_bsm.aws_account_id,
    name="cross-aws-account-iam-role-github-open-id-connection",
)
grantee_1 = x_aws_acc.Grantee(
    bsm=grantee_1_bsm,
    stack_name=f"{prefix}-dev-cross-aws-account-iam-role-github-open-id-connection",
    iam_arn=iam_role_arn,
    policy_name=f"{prefix}-dev-cross_aws_account_iam_role_github_open_id_connection",
    test_bsm=BotoSesManager(),
)

owner_1_bsm = BotoSesManager(profile_name="bmt_app_test_us_east_1")
owner_1 = x_aws_acc.Owner(
    bsm=owner_1_bsm,
    stack_name=f"{prefix}-test-cross-aws-account-iam-role-github-open-id-connection",
    role_name=f"{prefix}-test-cross_aws_account_iam_role_github_open_id_connection",
    policy_name=f"{prefix}-test-cross_aws_account_iam_role_github_open_id_connection",
    policy_document={
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "iam:ListAccountAliases",
                    "sts:GetCallerIdentity",
                ],
                "Resource": "*"
            },
        ],
    },
)

owner_1.grant(grantee_1)

x_aws_acc.deploy(
    grantee_list=[grantee_1],
    owner_list=[owner_1],
)

# x_aws_acc.delete(
#     grantee_list=[grantee_1],
#     owner_list=[owner_1],
# )
