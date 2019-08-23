import binascii
import os
import subprocess
from base64 import b64decode

import boto3
import yaml
from botocore.exceptions import ClientError

kms = boto3.client('kms')

yaml.add_multi_constructor('!', lambda loader, suffix, node: None)


def hashable(x):
    """
    オブジェクトがハッシュ可能であるか判定する
    """
    try:
        hash(x)
        return True
    except TypeError:
        return False


def memoize(callable):
    """
    関数を Memoize するデコレータ
    """
    cache = {}

    def wrapper(*args, **kwargs):
        key = args + tuple(kwargs.items())
        if not hashable(key):
            return callable(*args, **kwargs)
        if key not in cache:
            cache[key] = callable(*args, **kwargs)
        return cache[key]
    return wrapper


@memoize
def get_secret_env(env):
    """
    暗号化されている環境変数を復号化した状態で返す
    """
    def decrypt(env):
        """
        必要であれば複合し､不必要(複合に失敗)ならそのまま返す
        """
        try:
            return kms.decrypt(CiphertextBlob=b64decode(env))['Plaintext'].decode()
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidCiphertextException':
                # invoke-local 用
                return env
            else:
                raise e
        except binascii.Error:
            return env

    if os.environ.get(env):
        return decrypt(os.environ.get(env))
    elif get_envs()[env]:
        return decrypt(get_envs()[env])
    else:
        return None


@memoize
def get_env(env):
    """
    環境変数を取得する
    """
    if os.environ.get(env):
        return os.environ.get(env)
    elif get_envs()[env]:
        return get_envs()[env]
    else:
        return None


def dict_to_env(d):
    """
    Dict(ネストなし)を環境変数にマッピングする
    """
    for key in d:
        os.environ[key] = str(d[key])


@memoize
def get_envs():
    """
    環境変数を取得する
    """
    serverless_yaml = None
    local_env = os.environ['LOCAL_ENV']
    try:
        serverless_yaml = yaml.load(subprocess.check_output(f'$(npm bin)/sls print --stage {local_env}', shell=True), Loader=yaml.SafeLoader)
        env_dict = serverless_yaml['provider']['environment']
        # 暗号化されている場合は、別の場所を参照する
        for key in env_dict:
            if env_dict[key] == 'ENCRYPTED':
                env_dict[key] = serverless_yaml['custom']['encrypted'][key]

        dict_to_env(env_dict)

        return env_dict

    except Exception as e:
        raise e


def set_env_name(sys_argv):
    if len(sys_argv) >= 2:
        if sys_argv[1] == 'dev':
            os.environ['LOCAL_ENV'] = 'dev'
        elif sys_argv[1] == 'prod':
            os.environ['LOCAL_ENV'] = 'prod'
    else:
        os.environ['LOCAL_ENV'] = 'dev'
