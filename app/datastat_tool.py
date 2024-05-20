import os
import requests
import json
from typing import Annotated
from langchain_core.tools import tool

# https://datastat.openeuler.org/query/sig/info?community=openeuler&sig=Compiler
# https://datastat.openeuler.org/query/sig/name?community=openeuler
# https://datastat.openeuler.org/query/sig/usercontribute?contributeType=pr&timeRange=all&community=openeuler&sig=Compiler
# https://datastat.openeuler.org/query/sig/info?community=openeuler&sig=Compiler
# https://datastat.openeuler.org/query/sig/usercontribute?contributeType=pr&timeRange=lastonemonth&community=openeuler&sig=Compiler
# https://datastat.openeuler.org/query/sig/usercontribute?contributeType=pr&timeRange=lasthalfyear&community=openeuler&sig=Compiler
# https://datastat.openeuler.org/query/sig/usercontribute?contributeType=pr&timeRange=lastoneyear&community=openeuler&sig=Compiler

base_sig_url = "https://datastat.openeuler.org/query/sig/"

@tool
def query_community_detail_info(
    community: Annotated[str, "指定某个开源社区的名字."] = 'openeuler',
    sig: Annotated[str, "指定该开源社区下的某个sig组, 如果没有指定就会返回该开源社区的所有信息."] = '',
):
    """
    - 功能介绍：获取所有开源社区的详细信息，比如某个sig组下的maintainers、committers等详细信息，
        特别是获取检视人 reviewers 的联系方式时特别有用
    """
    url = base_sig_url + 'info'
    params = {
        'community': community,
        'sig': sig,
    }
    ret = requests.get(url, params=params)
    if ret.status_code == 200:
        data = ret.json()
    else:
        raise Exception(f"API Request failed with status code: {ret.status_code}")
    print(json.dumps(data))
    return data

@tool
def query_community_usercontribute(
    sig: Annotated[str, "指定该开源社区下的某个sig组."],
    contributeType: Annotated[str, "开发者贡献类型，可以是pr或者issue."] = 'pr',
    timeRange: Annotated[str, "指定某个时间范围段，可以是all、lastonemonth、lasthalfyear、lastoneyear."] = 'all',
    community: Annotated[str, "指定某个开源社区的名字."] = 'openeuler',
):
    """
    - 功能介绍：获取所有开源社区下所有sig组名称
    """
    url = base_sig_url + 'usercontribute'
    params = {
        'sig': sig,
        'contributeType': contributeType,
        'timeRange': timeRange,
        'community': community,
    }
    ret = requests.get(url, params=params)
    if ret.status_code == 200:
        data = ret.json()
    else:
        raise Exception(f"API Request failed with status code: {ret.status_code}")
    print(json.dumps(data))
    return data

@tool
def query_community_all_sigs(
    community: Annotated[str, "指定某个开源社区的名字."] = 'openeuler',
):
    """
    - 功能介绍：获取所有开源社区下所有sig组名称
    """
    url = base_sig_url + 'name'
    params = {
        'community': community,
    }
    ret = requests.get(url, params=params)
    if ret.status_code == 200:
        data = ret.json()
    else:
        raise Exception(f"API Request failed with status code: {ret.status_code}")
    print(json.dumps(data))
    return data
