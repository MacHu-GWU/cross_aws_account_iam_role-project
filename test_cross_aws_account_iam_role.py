# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager

bsm = BotoSesManager()
bsm_assumed = bsm.assume_role(
    role_arn=f"arn:aws:iam::{bsm.aws_account_id}:role/cross-aws-account-iam-role-github-oidc-owner",
    role_session_name="sample_role_session",
)
res = bsm_assumed.sts_client.get_caller_identity()
parts = res["Arn"].split(":")
parts[4] = parts[4][:2] + "********" + parts[4][-2:]
arn = ":".join(parts)
print(f"    now we are using principal {arn}")
