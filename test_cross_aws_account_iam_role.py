# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager
import cross_aws_account_iam_role.api as x_aws_acc

prefix = "a1b2-"

bsm = BotoSesManager()

grantee_1_bsm = bsm
iam_role_arn = x_aws_acc.IamRoleArn(
    account=grantee_1_bsm.aws_account_id,
    name="cross-aws-account-iam-role-github-open-id-connection",
)
grantee_1 = x_aws_acc.Grantee(
    bsm=grantee_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-oidc-grantee",
    iam_arn=iam_role_arn,
    policy_name=f"{prefix}cross_aws_account_iam_role_github_oidc-grantee",
)

owner_1_bsm = bsm
owner_1 = x_aws_acc.Owner(
    bsm=owner_1_bsm,
    stack_name=f"{prefix}cross-aws-account-iam-role-github-oidc-test-owner",
    role_name=f"{prefix}cross_aws_account_iam_role_github_oidc_test_owner",
    policy_name=f"{prefix}cross_aws_account_iam_role_github_oidc_test_owner",
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


def call_api(bsm: BotoSesManager):
    res = bsm.sts_client.get_caller_identity()
    parts = res["Arn"].split(":")
    parts[4] = parts[4][:2] + "********" + parts[4][-2:]
    arn = ":".join(parts)
    print(f"    now we are using principal {arn}")


def validate():
    grantee_1.test_bsm = bsm
    print("at begin:")
    call_api(bsm)
    print("validate cross account permission ...")
    x_aws_acc.validate(
        grantee_list=[grantee_1],
        call_api=call_api,
        verbose=False,
    )


if __name__ == "__main__":
    validate()
