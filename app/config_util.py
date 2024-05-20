from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

# 现在可以像访问普通环境变量一样访问.env文件中的变量
openai_key = os.getenv('OPENAI_API_KEY')
tavily_key = os.getenv('TAVILY_API_KEY')
serpapi_key = os.getenv('SERPAPI_API_KEY')
datastat_base_url = os.getenv('DATASTAT_BASE_URL')
issues_base_url = os.getenv('ISSUES_BASE_URL')
meet_base_url = os.getenv('MEET_BASE_URL')
pull_base_url = os.getenv('PULL_BASE_URL')
repo_base_url = os.getenv('REPO_BASE_URL')

# def get_pull_base_url():
#     # print(f"Database URL: {pull_base_url}")
#     return pull_base_url

# def get_pull_base_url():
#     # print(f"Database URL: {pull_base_url}")
#     return pull_base_url

# def get_pull_base_url():
#     # print(f"Database URL: {pull_base_url}")
#     return pull_base_url


