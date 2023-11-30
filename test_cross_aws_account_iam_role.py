# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
import cross_aws_account_iam_role.api as x_aws_acc

prefix = "a1b2-"

bsm = BotoSesManager()

iam_role_arn = x_aws_acc.IamRoleArn(
    account=bsm.aws_account_id,
    name="cross-aws-account-iam-role-github-open-id-connection",
)
grantee_1 = x_aws_acc.Grantee(
    bsm=bsm,
    stack_name=f"{prefix}-dev-cross-aws-account-iam-role-github-open-id-connection",
    iam_arn=iam_role_arn,
    policy_name=f"{prefix}-dev-cross_aws_account_iam_role_github_open_id_connection",
    test_bsm=BotoSesManager(),
)

owner_1_bsm = BotoSesManager()
owner_1 = x_aws_acc.Owner(
    bsm=bsm,
    stack_name=f"{prefix}-test-cross-aws-account-iam-role-github-open-id-connection",
    role_name=f"{prefix}-test-cross_aws_account_iam_role_github_open_id_connection",
    policy_name=f"{prefix}-test-cross_aws_account_iam_role_github_open_id_connection",
    policy_document={
        "Version": "2012-10-17",
        "Statement": [
            {"Effect": "Allow", "Action": "sts:GetCallerIdentity", "Resource": "*"},
        ],
    },
)

owner_1.grant(grantee_1)


def call_api(bsm: BotoSesManager):
    res = bsm.sts_client.get_caller_identity()
    parts = res["Arn"].split(":")
    parts[4] = parts[4][:2] + "********" + parts[4][-2:]
    arn = ":".join(parts)
    print(f"    now we are  using principal {arn}")


x_aws_acc.validate(
    grantee_list=[grantee_1],
    call_api=call_api,
)
