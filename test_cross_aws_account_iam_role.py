# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager


def print_caller_identity(bsm: BotoSesManager):
    res = bsm.sts_client.get_caller_identity()
    parts = res["Arn"].split(":")
    parts[4] = parts[4][:2] + "********" + parts[4][-2:]
    arn = ":".join(parts)
    print(f"    now we are using principal {arn}")

bsm = BotoSesManager()
print_caller_identity(bsm)

bsm_assumed = bsm.assume_role(
    role_arn=f"arn:aws:iam::{bsm.aws_account_id}:role/cross-aws-account-iam-role-github-oidc-owner",
    role_session_name="sample_role_session",
)
print_caller_identity(bsm_assumed)
