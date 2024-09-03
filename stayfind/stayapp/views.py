from datetime import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from stayapp.models import Product, Cart, Order, Orderhistory
from django.db.models import Q
import razorpay
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.

def product(request):
    p=Product.objects.filter(is_active=True)
    print(p)
    context={}
    context['data']=p
    return render(request, 'product.html', context)

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method=='GET':
        return render(request, 'register.html')
    
    else:
        n=request.POST['uname']
        e=request.POST['email']
        p=request.POST['upass']
        cp=request.POST['ucpass']

    context={}
    if n=='' or e=='' or p=='' or cp=='': 
        context['errmsg']='Please enter the requed field'
    
    elif p!=cp:
        # print("Both the password are not same")
        context['errmsg']="Both the password are not same"

    elif len(p)<8:
        # print("Length should be grater than 8")
        context['errmsg']="Length should be grater than 8"

    else:
        u=User.objects.create(username=n, email=e)
        u.set_password(p)
        u.save()
        context['success']='User Created Successfully..!!!!'
    
    return render (request, 'register.html', context)

def user_login(request):
    if request.method=='GET':
        return render(request, 'login.html')
    
    else:
        n=request.POST['uname']
        p=request.POST['upass']
        # print(n, p)
        u=authenticate(username=n, password=p)
        print(u)

        context={}
        if u==None:
            context['errmsg']='Inavlid Username or Password'
            return render(request, 'login.html', context)
        
        else:
            login(request, u)
            return redirect('/index')
        
def city(request, cid):
    q1=Q(city=cid)
    q2=Q(is_active=True)
    p=Product.objects.filter(q1 & q2)
    context={}
    context['data']=p
    return render(request, 'product.html', context)

def sort(request, sid):
    context={}
    
    if sid=='1':
        # p=Product.objects.order_by('-price').filter(is_active=True)
        t='-price'
    else:
        # p=Product.objects.order_by('price').filter(is_active=True)
        t='price'

    p=Product.objects.order_by(t).filter(is_active=True)
    context ['data']=p
    return render (request, 'product.html', context)

def pricefilter(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    p=Product.objects.filter(q1 & q2).filter(is_active=True)
    context={}
    context['data']=p
    return render(request, 'product.html', context)

def search(request):
    srch=request.GET['search']
    n=Product.objects.filter(name__icontains=srch)
    para=Product.objects.filter(para__icontains=srch)
    context={}
    all=n.union(para)
    if len(all)==0:
        context['errmsg']='Search not found....'

    context['data']=all
    return render(request, 'product.html', context)
        
def user_logout(request):
    logout(request)
    return redirect('/index')

def index(request):
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def sort(request, sid):
    context={}
    if sid=='1':
        t='-price'
    else:
        t='price'

    p=Product.objects.order_by(t).filter(is_active=True)
    context['data']=p
    return render(request, 'product.html', context)

def products(request, pid):
    p=Product.objects.filter(id=pid)
    # print(p , pid)
    context={}
    context['data']=p
    return render(request, 'products.html', context)

def updateqty(request, x, cid):
    c=Cart.objects.filter(id=cid)
    q=c[0].qty
    if x=='1':
        q=q+1

    elif q>1:
        q=q-1

    c.update(qty=q)
    return redirect('/cart')

# ADD TO CART 
def addtocart(request, pid):
    if request.user.is_authenticated:
        u = User.objects.filter(id=request.user.id)
        cin = request.POST['checkin']
        cout = request.POST['checkout']
        print("cin", cin)
        print("cout", cout)
        p = Product.objects.filter(id=pid)
        context = {}
        context['data'] = p
        q1 = Q(uid=u[0])
        q2 = Q(pid=p[0])
        c = Cart.objects.filter(q1 & q2)
        if len(c) == 0:
            c = Cart.objects.create(uid=u[0], pid=p[0], checkin=cin, checkout=cout)
            c.save()
            context['success'] = "Room Selected Successfully"
            # return render(request, 'cart.html', context)
        else:
            context['errmsg'] = 'Room already exists'
            # return render(request, 'products.html', context)

        return render(request, 'products.html', context)

    else:
        return redirect('/login')

# def cart(request):
#     c=Cart.objects.filter(uid=request.user.id)
#     context={}
#     context['data']=c
#     s=0
#     if request.method=='GET':
#         return render(request, 'cart.html',context)
#     else:
        

        # Convert to datetime objects
        # cin_date = datetime.strptime(cin, '%Y-%m-%d')
        # cout_date = datetime.strptime(cout, '%Y-%m-%d')
        # print("cin_date",cin_date)
        # print("cout_date",cout_date)
        # if cin=='' or cout=='': 
        #     context['errmsg']='Please enter the requed field'
        # elif cin_date == cout_date:
        #     print("elif")
        #     context['errmsg']="Both should not same"
        # else:
        #     uc = User.objects.filter(id=request.user.id)
        #     c.update(checkin=cin_date.date(), checkout=cout_date.date())            
        #     context['success']='Dates added..!!!!'

        
        # for i in c:
        #     s=s+i.pid.price*i.qty
            # i.delete()
        # print('price',s)
        # context['total']=s
        # context['n']=len(c)
        # return render (request, 'cart.html', context)
    
def cart(request):
    c=Cart.objects.filter(uid=request.user.id)
    context={}
    context['data']=c
    s=0
    for i in c:
        s=s+i.pid.price*i.qty
    context['total']=s
    context['n']=len(c)
    return render (request, 'cart.html', context)

def remove(request, cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/cart')

@login_required
def makepayment(request):
    client = razorpay.Client(auth=("rzp_test_HeYv5uvRUwSNEa", "FKsfWPzm770aRcJaLCP1tSOh"))
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt
        # i.delete()
    data = { "amount": s*100, "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data)
    # print(payment)
    context={'payment':payment}
    for order in o:
        order_history = Orderhistory(
            uid=order.uid,
            pid=order.pid,
            qty=order.qty,
            amt=order.amt,
        )
        order_history.save()
        order.delete()

    return render(request, 'pay.html', context)

def placeorder(request):
    c=Cart.objects.filter(uid=request.user.id)
    for i in c:
        amt=i.qty*i.pid.price
        o=Order.objects.create(uid=i.uid, pid=i.pid, qty=i.qty, amt=amt)
        o.save()
        i.delete()
    return redirect('/fetchorder')

def fetchorder(request):
    o=Order.objects.filter(uid=request.user.id)
    s=0
    for i in o:
        s=s+i.amt
    context={'data': o, 'total': s, 'n': len(o)}
    return render(request, 'placeorder.html', context)

def paymentsuccess(request):
    sub='Order Status'
    msg='Hotel Booked Successfully'
    frm='anushkatiwari1212@gmail.com'
    u=User.objects.filter(id=request.user.id)
    to=u[0].email
    send_mail(
        sub, msg, frm, [to], fail_silently=False
    )
    return render(request, 'paymentsuccess.html')

def orderhistory(request):
    history = Orderhistory.objects.filter(uid = request.user.id)
    context = {
        'history' : history,
    } 
    return render ( request,'orderhistory.html',context)