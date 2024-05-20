import os
import requests
import json
from typing import Annotated
from langchain_core.tools import tool
from config_util import repo_base_url

base_repos_url = repo_base_url

@tool
def get_repos_info(
    sig: Annotated[str, "指定某个sig组的名称，比如Infrastructure, 如果为空就是获取所有repos的内容."] = '',
    keyword: Annotated[str, "模糊匹配代码仓repos的信息，该输入为repo名称的模糊匹配，给了代码仓名字时优先使用模糊查找."] = '',
    page: Annotated[int, "获取的第几页数，默认1."] = 1,
    per_page: Annotated[int, "每页能获取的数量，默认每次获取20个, 最大上限为100, 超过100后需要做分页查询处理."] = 20,
):
    """
    - 功能介绍：获取所有开源社区组织下sig组内的代码仓库列表或者模糊匹配某个关键字的代码仓信息, 可获取 reviewer 人员列表
    - URI: GET /repos
    - 示例输入: GET https://ipb.osinfra.cn/repos?sig=Infrastructure
    - 示例输出：可以获取代码仓的检视人 reviewers，归属sig组
    - 依赖关系: 检视人 reviewers 的联系方式需要调用 query_community_detail_info 工具进行查询，需要传入SIG信息
    """
    url = base_repos_url
    params = {
        'sig': sig,
        'keyword': keyword,
        'page': page,
        'per_page': per_page,
    }
    ret = requests.get(url, params=params)
    if ret.status_code == 200:
        data = ret.json()
    else:
        raise Exception(f"API Request failed with status code: {ret.status_code}")
    print(json.dumps(data))
    return data


