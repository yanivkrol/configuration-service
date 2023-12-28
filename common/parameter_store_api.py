from typing import Optional

import boto3


class ParameterStoreApi:
    """From repo: natural-Intelligence/analysts-streamlit-apps"""

    AWS_SERVICE = 'ssm'

    def __init__(self,
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 region: str = 'us-east-1'):
        self._region = region
        self._ssm = boto3.client(ParameterStoreApi.AWS_SERVICE,
                                 region_name=region,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key)

    def get_param_value(self, key: str):
        parameters = self._ssm.get_parameters(Names=[key], WithDecryption=True)['Parameters']
        if not parameters:
            raise Exception(f'Parameter {key} is not configured in the Parameter Store')
        return parameters[0]['Value']
