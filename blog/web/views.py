from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from io import BytesIO
from web.utils.check_code import create_validate_code


def index(request):
    """
    @todo:首页
    :param request:
    :return:
    """
    return render(request,'blog/index.html')


def check_code(request):
    """
    @todo:验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    @todo:登陆
    :param request:
    :return:
    """
    if  request.method == 'POST':
        code = request.POST.get('check_code')
        if code.upper() == request.session['CheckCode'].upper():
            print('验证码正确')
        else:
            print('验证码错误')
    return render(request, 'blog/login.html')