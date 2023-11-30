# -*- coding: utf-8 -*-

"""
This script tests the cross account AWS permission in GitHub action without
showing the AWS Account id.
"""

import os
from boto_session_manager import BotoSesManager


def print_caller_identity(bsm: BotoSesManager):
    res = bsm.sts_client.get_caller_identity()
    parts = res["Arn"].split(":")
    parts[4] = parts[4][:2] + "********" + parts[4][-2:]
    arn = ":".join(parts)
    print(f"  now we are using principal {arn}")


prefix = "a1b2-"
bsm = BotoSesManager()
print("at begin:")
print_caller_identity(bsm)
print("validate cross account permission ...")
for env_name in ["dev", "test", "prod"]:
    aws_account_id = os.environ[f"{env_name.upper()}_AWS_ACCOUNT_ID"]
    role_name = f"{prefix}cross_aws_account_iam_role_github_oidc_{env_name}_owner"
    bsm_assumed = bsm.assume_role(
        role_arn=f"arn:aws:iam::{aws_account_id}:role/{role_name}",
        role_session_name="sample_role_session",
    )
    print_caller_identity(bsm_assumed)
