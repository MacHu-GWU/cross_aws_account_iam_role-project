# -*- coding: utf-8 -*-

"""
Usage::

    import cross_aws_account_iam_role as x_aws_acc
"""

from .impl import IamRootArn
from .impl import IamGroupArn
from .impl import IamUserArn
from .impl import IamRoleArn
from .impl import T_GRANTEE_ARN
from .impl import Grantee
from .impl import Owner
from .impl import deploy
from .impl import get_account_info
from .impl import print_account_info
from .impl import validate
from .impl import delete