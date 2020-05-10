from django.http import HttpResponse
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException


def auth(request):
    signature = request.GET.get('signature')
    echostr = request.GET.get('echostr')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')
    token = '0bb2313787a2e2ba'
    try:
        check_signature(token, signature, timestamp, nonce)
    except InvalidSignatureException:
        raise
    return HttpResponse(echostr)
