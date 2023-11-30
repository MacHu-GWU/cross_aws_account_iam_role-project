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
    name="cross-aws-account-iam-role-github-oidc",
)
grantee_1 = x_aws_acc.Grantee(
    bsm=grantee_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-github-oidc-grantee",
    iam_arn=iam_role_arn,
    policy_name=f"{prefix}cross_aws_account_iam_role_github_oidc-grantee",
)

owner_list = list()
for aws_profile, env_name in [
    ("bmt_app_dev_us_east_1", "dev"),
    ("bmt_app_test_us_east_1", "test"),
    ("bmt_app_prod_us_east_1", "prod"),
]:
    owner_bsm = BotoSesManager(profile_name=aws_profile)
    owner = x_aws_acc.Owner(
        bsm=owner_bsm,
        stack_name=f"{prefix}cross-aws-account-iam-role-github-oidc-{env_name}-owner",
        role_name=f"{prefix}cross_aws_account_iam_role_github_oidc_{env_name}_owner",
        policy_name=f"{prefix}cross_aws_account_iam_role_github_oidc_{env_name}_owner",
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
    owner.grant(grantee_1)
    owner_list.append(owner)


def deploy():
    x_aws_acc.deploy(
        grantee_list=[grantee_1],
        owner_list=owner_list,
    )


def delete():
    x_aws_acc.delete(
        grantee_list=[grantee_1],
        owner_list=owner_list,
    )


if __name__ == "__main__":
    deploy()
    # delete()
