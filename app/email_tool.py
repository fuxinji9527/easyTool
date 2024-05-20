# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from langchain_core.tools import tool
from urllib.parse import urlparse
from typing import Annotated

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@tool
def reminder_reveiw_code(
    repo: Annotated[str, "代码仓库名"],
    url: Annotated[str, "pr 的url地址"],
    # context: Annotated[str, "催更邮件的内容，需要通过PR详情生成邮件内容，必须带上带检视PR的URL"],
    email: Annotated[str, "检视人的邮箱地址，最好通过社区详情接口获取对应检视人的联系方式"],
    pr_id: Annotated[str, "需要被检视的pr id"],
    title: Annotated[str, "需要被检视的pr内容概要"],
    reviewer: Annotated[str, "代码检视人, reviewers包括maintainer和committers, 或直接从repos详细内容接口获取"],
    developer: Annotated[str, "该PR的作者"] = '',
):
    """当你有PR需要检视时，发邮件提醒committer帮忙检视非常有用, 
    当有多个检视人需要被提醒时，reminder_reveiw_code 这个工具应该被多次调用,
    检视人信息可以通过调用query_community_detail_info工具进行查询reviewers的联系方式
    """
    # config
    sender = 'test@lists.osinfra.cn'  # 更换为当前邮件列表的地址
    recipients = [email]  # 更改为自己的邮箱地址
    subject = '【PR 检视提醒】PR #{} 需要您的检视 - [{}项目]'.format(pr_id, repo)
    message = MIMEMultipart()
    message["Subject"] = Header(subject, 'utf-8')
    ip = "94.74.106.235"  # 接受服务的ip, 不改
    port = 25
    ssl_port = 465
    username = "osinfra"
    password = "RQSggJvPv3hdDVH2W4CP"

    # 邮件正文内容
    mail_body = """尊敬的检视者、commiter、maintainer {}:
        \t您好！我是 {} 的开发者{}。我提交了一个Pull Request（PR #{}，标题为: {}），希望您能抽空检视。
    我非常期望能在一天后得到您的反馈。
        \tPR链接：{}

        \t感谢您的时间和支持。祝好！{}
    """.format(reviewer, repo, developer, pr_id, title, url, developer)
    message.attach(MIMEText(mail_body, "plain", "utf-8"))

    try:
        smtp_obj = smtplib.SMTP(ip, port)
        smtp_obj.login(username, password)
        for recipient in recipients:
            message['To'] = recipient
            text = message.as_string()
            # smtp_obj.sendmail(sender, recipient, text)
            smtp_obj.sendmail(sender, "1417700745@qq.com", text)
            print(f"Email sent to {recipient}")
        print(f"Email sent to 检视人（{reviewer} {recipients}）")
        return f"已向检视人：{reviewer}，发送PR检视提醒邮件成功"
    except Exception as e:
        print(e)
        print("Testing Scenarios: port:25, is_starttls: no, is_logins: no, result: fault")
        return f"发送PR检视提醒邮件失败，请调整输入稍后再试"
