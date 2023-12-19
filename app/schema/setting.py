from pydantic import BaseModel


class Setting(BaseModel):
    user_agent: str = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0')
    timeout: int = 60
    accept_language: str = 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4'
