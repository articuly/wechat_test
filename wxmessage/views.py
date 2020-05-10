from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from wechatpy.replies import ArticlesReply
from wechatpy import WeChatClient

# 来自natapp，如果不用内网穿透，可自定义
AUTH_TOKEN = '0bb2313787a2e2ba'
APPID = 'wxc9918afe793ea0f2'
APPSECRET = '724137cf2f7eb16db291d32d27e4feea'


@csrf_exempt
def send_message(request):
    if request.method == 'GET':  # 验证URL
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(AUTH_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type='text/plain')
        return response
    elif request.method == 'POST':  # 接收来微信服务器信息
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = create_reply("<a href='https://articuly.com'>清心涟漪博客</a>", msg)
        elif msg.type == 'event':
            reply = ArticlesReply(message=msg)
            reply.add_article({
                'title': '清心涟漪博客',
                'description': '因缘相见，整合图谱，心理占星，Python全栈',
                'image': 'https://articuly.com/wp-content/uploads/2014/07/articuly.jpg',
                'url': 'https://articuly.com'
            })
        elif msg.type == 'image':
            reply = create_reply('你刚才发给我的是一张图片', msg)
        elif msg.type == 'voice':
            reply = create_reply('你刚才发给我的是语音', msg)
        else:
            reply = create_reply('这是其它类型消息', msg)
        response = HttpResponse(reply.render(), content_type='application/xml')
        return response
    else:
        print('-' * 50)


def create_menu(request):
    client = WeChatClient(APPID, APPSECRET)
    client.menu.create({
        "button": [
            {
                "type": "click",
                "name": "我的博客",
                "key": "articuly_blog"
            },
            {
                "name": "菜单",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    },
                    {
                        "name": "发送位置",
                        "type": "location_select",
                        "key": "rselfmenu_2_0"
                    },
                ]
            },
        ]
    })
    return HttpResponse('菜单已创建成功')
