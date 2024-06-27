import os
import random

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from goods_interface.storedata import get

# specify the directory path
path = './tem'

# get a list of all HTML files in the directory
files = [f for f in os.listdir(path) if f.endswith('.txt')]

# randomly select 5 files



from langchain import PromptTemplate, LLMChain
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.llms import OpenAI

# 创建输出解析器
output_parser = StrOutputParser()
prompt=[
    HumanMessage(content="""
    
        现在,你是一个从html提取关键信息并进行整理的小助手,下面给出一个提取信息的例子,假如有这样一段html:
        EXAMPLE
    ###
    <img id="good-img" src="https://img2.baidu.com/it/u=1689202537,211159216&amp;fm=253&amp;fmt=auto&amp;app=120&amp;f=JPEG?w=800&amp;h=800"/>
<em>百家号/贴吧用户通用粉100-4W</em>
<div class="body">
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>

	简介：百家号粉丝(又名好看视频，度小视粉丝，全民***粉丝通用所有百度系通用，注意是贴吧用户粉丝，非贴吧粉，刷贴吧粉去百度贴吧渠道下单)

</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>
<br/>
</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>

	由于登录粉号源有限，如果多刷的下次会扣 ，尽量一次下完

</p>
<p>
<span>账号必须实明认证，不</span><span>实明账号刷完再实明后会掉粉，所以必须先实明</span><span>，后面</span><span>实明掉的无售后</span>
</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>
<br/>
</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>

	下单格式：百家号后台id下单，

</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>

	下单格式：https://baijiahao.baidu.com/u?app_id=1234567  或1234567

</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>
<br/>
</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>

	百家号ID下单，不会找顾客拿ID

</p>
<p style='color:#191919;font-family:-apple-system, BlinkMacSystemFont, "font-size:14px;'>

	新号可以说登录，部分上限号，不保证登录，也可能是游客。

</p>
<h1 style='color:rgba(0, 0, 0, 0.85);font-weight:500;font-family:-apple-system, BlinkMacSystemFont, "'>
</h1><p>

		百家号ID获取办法：

	</p>
<p>

		电脑端登录<a href="https://baijiahao.baidu.com/" target="_blank">https://baijiahao.baidu.com/</a>，找到账号权益--百家号设置---&gt;ID

	</p>
<p>

		手机端获取办法:下载"百家号APP"个人中心找到 百家号ID

	</p>
<p>
<br/>
</p>
</div>
<div class="money container">
<div class="price row">
<div class="col-12 fs-5">限时优惠价：
                            <div class="d-inline-block"><input class="layui-input fs-5" disabled="" id="need" style="border:0; backgroud-color:transparent" type="text" value="36元"/></div> </div>
<div class="mt-2 col-9">
                            限购数量: 1 - 24999                        </div>
</div>
</div>
###
    你需要输出下面关键信息:
    1.商品名称叫 百家号/贴吧用户通用粉100-4W
    2.单价36元 交易数量限制 1-24999
    3.商品的图片 https://img2.baidu.com/it/u=1689202537,211159216&amp;fm=253&amp;fmt=auto&amp;app=120&amp;f=JPEG?w=800&amp;h=800
    4.### 商品介绍

**简介**：
- 百家号粉丝，也称为好看视频、度小视粉丝，全民***粉丝，通用所有百度系产品。
- 注意区分：这是贴吧用户粉丝，非贴吧粉。如需刷贴吧粉，请前往百度贴吧渠道下单。

**注意事项**：
- 由于登录粉号源有限，如果多刷的下次会扣，建议尽量一次下完。
- 账号必须实明认证，未实明账号刷完后实明可能会掉粉，因此必须先实明，后续实明掉粉无售后。

**下单格式**：
- 百家号后台id下单，格式为百家号后台链接（如：<https://baijiahao.baidu.com/u?app_id=1234567>）或直接提供app_id（如：1234567）。
- 百家号ID下单，不会主动找顾客拿ID。

**百家号ID获取办法**：
- 电脑端：登录<https://baijiahao.baidu.com/>，找到账号权益--百家号设置-->ID。
- 手机端：下载"百家号APP"，在个人中心找到百家号ID。

**新号说明**：
- 新号可以登录，部分上限号不保证登录，也可能是游客。
    下面,你接收到的输入是,请按照上面的例子,将得出的结果输出:
    {example}
    """

                  ),
]
# 配置大语言模型
llm = ChatOpenAI(model='gpt-4o-2024-05-13',api_key='sk-qYvVzOAOo5nawGlfFb74652e697940Ac83D47b57D0E5D549',base_url='https://oneai.evanora.top/')
chain = ChatPromptTemplate.from_messages(prompt)| llm| output_parser

for file in files:
    with open(os.path.join(path, file), 'r',encoding='utf-8') as f:
        print(f.read())
        output = chain.invoke({"example": f.read()})
        print(type(output))
        print(output)