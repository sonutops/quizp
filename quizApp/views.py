from random import randint
from xml.etree.ElementInclude import default_loader
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.core.mail import send_mail
from django.conf import settings

default_data = {
    'app_name': 'Quiz',
}

def index(request):
    return render(request, "signin_page.html")

def signup_page(request):
    return render(request, "signup_page.html")

def my_collection(request):
    load_category()
    load_quizes(request)
    return render(request, "my_collection.html", default_data)

def payments(request):
    return render(request, "payments.html", default_data)

def security(request):
    return render(request, "security.html", default_data)

def otp_page(request):
    return render(request, "otp_page.html", default_data)

def favourite(request):
    return render(request, "favourite.html", default_data)

def load_category():
    categories = Category.objects.all()
    default_data['categories'] = categories

def profile_page(request):
    profile_data(request)
    return render(request, "profile_page.html", default_data)

# serialize
def serialize_data(obj):
    obj_dict = {}
    for k,v in obj.__dict__.items():
        if k.startswith('_') or k.endswith('_'):
            continue
        obj_dict.setdefault(k, v)
    return obj_dict

def load_quizes(request):
    # master = Master.objects.get(Email = request.session['email'])
    quesets = QuesSet.objects.all()
    # options = OptionSet.objects.all()
    q_sets = []
    for ques in quesets:
        op_set = OptionSet.objects.filter(QuesSet=ques)
        point = 0
        for op in op_set:
            point += op.Point

        q_sets.append(
            {'quesset': ques, 'questions': op_set, 'total': len(op_set), 'points': point}
        )

    print('question sets', q_sets)
    default_data['all_quizes'] = q_sets[::-1]
    return q_sets

# create quesset
def create_quesset(request):
    master = Master.objects.get(Email = request.session['email'])
    profile = Profile.objects.get(Master=master)

    category_id = int(request.POST['category'])
    category = Category.objects.get(id = category_id)
    
    QuesSet.objects.create(
        Profile = profile,
        Category = category,
        Title = request.POST['quiz_title']
    )

    return redirect(my_collection)
    # q_set = load_quizes(request)
    # qset = []
    # for i in q_set:
    #     s = serialize_data(i['quesset'])
    #     print(s)
    #     qset.append(s)
    # return JsonResponse({'quesset': qset})

# edit quesset
def edit_quesset(request, pk):
    category_id = int(request.POST['category'])
    category = Category.objects.get(id = category_id)
    
    quesset = QuesSet.objects.get(id=pk)
    quesset.Title = request.POST['quiz_title']
    quesset.Category = category

    quesset.save()

    return redirect(my_collection)

def delete_quesset(request, pk):
    QuesSet.objects.get(id=pk).delete()
    return redirect(my_collection)

# add options for quesset
def add_options(request, pk):
    quesset = QuesSet.objects.get(id=pk)

    # options = [
    #     request.POST['name_option_1'],
    #     request.POST['name_option_2'],
    # ]
    # options = '|'.join(options)

    OptionSet.objects.create(
        QuesSet = quesset,
        Question = request.POST['question'],
        Options = request.POST['all_values'],
        Correct = request.POST['correct_answer'],
        Point = request.POST['question_point'],
    )

    return redirect(my_collection)

def profile_data(request):
    master = Master.objects.get(Email = request.session['email'])
    
    profile = Profile.objects.get(Master = master)

    default_data['profile_data'] = profile

# profile image upload
def profile_image_upload(request):
    master = Master.objects.get(Email = request.session['email'])
    
    profile = Profile.objects.get(Master = master)

    profile.ProfileImage = request.FILES['profile_image']
    profile.save()

    return redirect(profile_page)


def update_profile(request):
    master = Master.objects.get(Email = request.session['email'])
    
    profile = Profile.objects.get(Master = master)

    print('update data:', request.POST['address'])

    profile.FullName = request.POST['full_name']
    profile.Mobile = request.POST['mobile']
    profile.City = request.POST['city']
    profile.State = request.POST['state']
    profile.AdderssLine = request.POST['address']

    profile.save()

    return redirect(profile_page)

def change_password(request):
    master = Master.objects.get(Email = request.session['email'])
    if master.Password == request.POST['old_password']:
        if request.POST['new_password'] == request.POST['confirm_password']:
            master.Password = request.POST['new_password']
            master.save()
            print('Password changed successfully.')
        else:
            print('password are differnt.')
    else:
        print('invalid current password.')
    
    return redirect(security)

# generate otp
# otp
def create_otp(request):
    email_to_list = [request.session['reg_data']['email'],]
    
    subject = 'OTP for NMS Registration'

    otp = randint(1000,9999)

    print('OTP is: ', otp)

    request.session['otp'] = otp

    message = f"Your One Time Password for verification is: {otp}"
    
    email_from = settings.EMAIL_HOST_USER

    send_mail(subject, message, email_from, email_to_list)

# verify otp
def verify_otp(request):
    if request.method == 'POST':
        otp = int(request.POST['otp'])

        if otp == request.session['otp']:
            master = Master.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True,
            )
            Profile.objects.create(
                Master = master,
            )

            del request.session['otp']
            del request.session['reg_data']

            print('otp verify success!')

        else:
            print('invalid otp')
            return redirect(otp_page)

        return redirect(signup_page)
    else:
        pass

def signup(request):
    print(request.POST)
    request.session['reg_data'] = {
        'email': request.POST['email'],
        'password': request.POST['password'],

    }
    
    create_otp(request)

    

    return redirect(otp_page)

def signin(request):
    try:
        master = Master.objects.get(Email = request.POST['email'])

        if master.Password == request.POST['password']:
            # create a session for current login
            request.session['email'] = master.Email

            return redirect(profile_page)
        else:
            print('---------- incorrect password')

    except Master.DoesNotExist as err:
        print('record not found.', err)
    
    return redirect(index)

def signout(request):
    if 'email' in request.session:
        del request.session['email']
        
    return redirect(index)