from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Registration,Addpost,Reaction,Friend_request,Comments
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def index(request):
    addpost=Addpost.objects.all().order_by('-id')
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
            "addpost":addpost
        }
        return render(request,"index.html",{"reacting":reacting})
    except:
        reacting={
            "addpost":addpost,
        }
        return render(request,"index.html",{"reacting":reacting})
def login(request):
    if request.method=="POST":
        em=request.POST['email']
        pa=request.POST['pas']
        print(make_password(pa))
        try:
            item =Registration.objects.get(email=em)
        except:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
        if check_password(pa, item.password):
            request.session['email_id']=em
            email_id=request.session['email_id']
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('login')
    else:
        return render(request,'login.html')
def register(request):
    if request.method=="POST":
        name=request.POST['name']
        em=request.POST['email']
        un=request.POST['username']
        pa=request.POST['pas']
        try:
            request.FILES['picture']
            picture=request.FILES['picture']
        except:
            picture=None
        if Registration.objects.filter(username=un).exists():
            messages.info(request,"username exists")
            return redirect('register')
        elif Registration.objects.filter(email=em).exists():
            messages.info(request,"email exists")
            return redirect('register')
        else:
            user=Registration(username=un,name=name,email=em,password=make_password(pa),img=picture)
            user.save()
            return redirect('login')
    else:
        return render(request,'register.html')
def logout(request):
    try:
        del request.session['email_id']
    except:
        return redirect('/')

    return redirect('/')
def profile(request):
    email_id=request.session['email_id']
    userr=Registration.objects.get(email=email_id)
    if request.method=="POST":
        name=request.POST['name']
        em=email_id
        un=request.POST['username']
        try:
            request.FILES['picture']
            picture=request.FILES['picture']
        except:
            picture=userr.img
        if Registration.objects.filter(username=un).exists() and un!=userr.username:
            messages.info(request,"username exists")
            return render(request,"profile.html",{"userr":userr})
        else:
            user=Registration.objects.get(email=em)
            user.name=name
            user.email=em
            user.username=un
            user.img=picture
            user.password=userr.password
            user.save()
            return render(request,"profile.html",{"userr":user})
    else:
        return render(request,"profile.html",{"userr":userr})
def add_post(request):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        userr=Registration.objects.get(email=email_id)
        if request.method=="POST":
            post_image=request.FILES['post_image']
            title=request.POST['title']
            genre=request.POST['genre']
            description=request.POST['description']
            username=userr.username
            like=0
            dislike=0
            addpost=Addpost(title=title,description=description,username=username,email_id=email_id,img=post_image,like=like,dislike=dislike,genre=genre)
            addpost.save()
            return redirect("/")
        else:
            return render(request,"addpost.html")
    except:
        return redirect("/")

def remove_profile(request):
    email_id=request.session['email_id']
    userr=Registration.objects.get(email=email_id)
    picture=None
    user=Registration.objects.get(email=email_id)
    user.img=picture
    user.name=userr.name
    user.email=userr.email
    user.username=userr.username
    user.password=userr.password
    user.save()
    return render(request,"profile.html",{"userr":user})
def like(request,post_id,counter):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        try:
            reaction1=Reaction.objects.filter(post_id_id=post_id)
        except:
            reaction1=[]
        try:
            reaction3=Reaction.objects.filter(email_dislike=email_id)
        except:
            reaction3=[]
        try:
            reaction2=Reaction.objects.filter(email_like=email_id)
        except:
            reaction2=[]
        if reaction1==[] and reaction2==[] and reaction3==[]:
            react=Reaction(email_like=email_id,email_dislike="done",post_id_id=post_id)
            react.save()
            like=Addpost.objects.get(id=post_id)
            like.like+=1
            p=like.username
            like.save()
            messages.info(request,"liked")
            if counter==1:
                return redirect("/")
            elif counter==2:
                return redirect("/view_post/%d"%post_id)
            elif counter==3:
                return redirect("/view_profile/%s"%p)
            elif counter==4:
                return redirect("/user_post/%s"%p)
            elif counter==5:
                return redirect("/top_post")
            elif counter==6:
                return redirect("/my_post")
        else:
            l2=[]
            l3=[]
            for i in reaction1:
                l2.append(i.email_like)
                l3.append(i.email_dislike)
            if (email_id not in l2) and (email_id not in l3):
                react=Reaction(email_like=email_id,email_dislike="done",post_id_id=post_id)
                react.save()
                like=Addpost.objects.get(id=post_id)
                like.like+=1
                p=like.username
                like.save()
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            elif email_id in l2 and email_id not in l3:
                like=Addpost.objects.get(id=post_id)
                like.like-=1
                react=Reaction.objects.get(email_like=email_id,post_id_id=post_id)
                react.delete()
                p=like.username
                like.save()
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            else:
                like=Addpost.objects.get(id=post_id)
                p=like.username
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
                    
            l=[]
            for i in reaction2:
                l.append(i.post_id_id)
            l1=[]
            for i in reaction3:
                l1.append(i.post_id_id)
            if (post_id not in l) and (post_id not in l1):
                react=Reaction(email_like=email_id,email_dislike="done",post_id_id=post_id)
                react.save()
                like=Addpost.objects.get(id=post_id)
                like.like+=1
                p=like.username
                like.save()
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            else:
                like=Addpost.objects.get(id=post_id)
                p=like.username
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
    except:
        return redirect("/login")
            
def dislike(request,post_id,counter):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        try:
            request.session['email_id']
            email_id=request.session['email_id']
            reaction1=Reaction.objects.filter(post_id_id=post_id)
        except:
            reaction1=[]
        try:
            reaction3=Reaction.objects.filter(email_dislike=email_id)
        except:
            reaction3=[]
        try:
            reaction2=Reaction.objects.filter(email_like=email_id)
        except:
            reaction2=[]
        if reaction1==[] and reaction2==[] and reaction3==[]:
            react=Reaction(email_dislike=email_id,email_like="done",post_id_id=post_id)
            react.save()
            like=Addpost.objects.get(id=post_id)
            like.dislike+=1
            p=like.username
            like.save()
            if counter==1:
                return redirect("/")
            elif counter==2:
                return redirect("/view_post/%d"%post_id)
            elif counter==3:
                return redirect("/view_profile/%s"%p)
            elif counter==4:
                return redirect("/user_post/%s"%p)
            elif counter==5:
                return redirect("/top_post")
            elif counter==6:
                return redirect("/my_post")
        else:
            l2=[]
            l3=[]
            for i in reaction1:
                l2.append(i.email_like)
                l3.append(i.email_dislike)
            if (email_id not in l3) and (email_id not in l2):
                react=Reaction(email_dislike=email_id,email_like="done",post_id_id=post_id)
                react.save()
                like=Addpost.objects.get(id=post_id)
                like.dislike+=1
                p=like.username
                like.save()
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            elif email_id in l3 and email_id not in l2:
                like=Addpost.objects.get(id=post_id)
                like.dislike-=1
                p=like.username
                react=Reaction.objects.get(email_dislike=email_id,post_id_id=post_id)
                react.delete()
                like.save()
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            else:
                like=Addpost.objects.get(id=post_id)
                p=like.username
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            l=[]
            for i in reaction2:
                l.append(i.post_id_id)
            l1=[]
            for i in reaction3:
                l1.append(i.post_id_id)
            if (post_id not in l)and (post_id not in l):
                react=Reaction(email_dislike=email_id,email_like="done",post_id_id=post_id)
                react.save()
                like=Addpost.objects.get(id=post_id)
                like.dislike+=1
                p=like.username
                like.save()
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
            else:
                like=Addpost.objects.get(id=post_id)
                p=like.username
                if counter==1:
                    return redirect("/")
                elif counter==2:
                    return redirect("/view_post/%d"%post_id)
                elif counter==3:
                    return redirect("/view_profile/%s"%p)
                elif counter==4:
                    return redirect("/user_post/%s"%p)
                elif counter==5:
                    return redirect("/top_post")
                elif counter==6:
                    return redirect("/my_post")
    except:
        return redirect("/login")
def make_friends(request,ka,counter):
    registration=Registration.objects.all()
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        kashi=Friend_request.objects.filter(email_sender_id=email_id)
        mishi=Friend_request.objects.filter(email_reciever=email_id)
        kash=[]
        mish=[]
        for i in kashi:
            if i.confirmation==0:
                kash.append(i.email_reciever)
            else:
                mish.append(i.email_reciever)
        for i in mishi:
            if i.confirmation==0:
                kash.append(i.email_sender_id)
            else:
                mish.append(i.email_sender_id)
        dictionary={
            "registration":registration,
            "kashi":kash,
            "mish":mish
        }
        if ka=="0":
            return render(request,"make_friends.html",{"dictionary":dictionary})
        else:
            register=Registration.objects.get(username=ka)
            reciever_id=register.email
            if reciever_id not in kash:
                friends=Friend_request(email_sender_id=email_id,email_reciever=reciever_id,confirmation=0)
                friends.save()
                l=[]
                l1=[]
                friend=Friend_request.objects.filter(email_sender_id=email_id)
                mishi=Friend_request.objects.filter(email_reciever=email_id)
                for i in friend:
                    if i.confirmation==0:
                        l.append(i.email_reciever)
                    else:
                        l1.append(i.email_reciever)
                for i in mishi:
                    if i.confirmation==0:
                        l.append(i.email_sender_id)
                    else:
                        l1.append(i.email_sender_id)
                dictionary={
                    "registration":registration,
                    "kashi":l,
                    "mish":l1
                }
                if(counter=='1'):
                    return render(request,"make_friends.html",{"dictionary":dictionary})
                else:
                    register=Registration.objects.get(username=counter)
                    friends1=Friend_request.objects.filter(email_sender_id=register.email,confirmation=1)
                    friends2=Friend_request.objects.filter(email_reciever=register.email,confirmation=1)
                    l=[]
                    for i in friends1:
                        registration=Registration.objects.get(email=i.email_reciever)
                        l.append(registration)
                    for i in friends2:
                        registration=Registration.objects.get(email=i.email_sender_id)
                        l.append(registration)
                    return render(request,"friend_friend_list.html",{"friends":l,"username":register.username,"dictionary":dictionary})
                    
            else:
                if(counter=='1'):
                    return render(request,"make_friends.html",{"dictionary":dictionary})
                else:
                    register=Registration.objects.get(username=counter)
                    friends1=Friend_request.objects.filter(email_sender_id=register.email,confirmation=1)
                    friends2=Friend_request.objects.filter(email_reciever=register.email,confirmation=1)
                    l=[]
                    for i in friends1:
                        registration=Registration.objects.get(email=i.email_reciever)
                        l.append(registration)
                    for i in friends2:
                        registration=Registration.objects.get(email=i.email_sender_id)
                        l.append(registration)
                    return render(request,"friend_friend_list.html",{"friends":l,"username":register.username,"dictionary":dictionary})
    except:
        return render(request,"make_friends.html",{"dictionary":dictionary})
def follow_request(request):

    try:
        request.session['email_id']
        email_id=request.session['email_id']
        friend=Friend_request.objects.filter(email_reciever=email_id)
        d1={}
        for i in friend:
            d={}
            if i.confirmation==0:
                register=Registration.objects.get(email=i.email_sender_id)
                d={
                    "name":register.name,
                    "username":register.username,
                    "img":register.img
                }
                d1[i.email_sender_id]=d
        return render(request,"follow_request.html",{"d1":d1})
    except:
        return redirect("/login")
def confirm_request(request,username):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        register=Registration.objects.get(username=username)
        reciever_id=register.email
        friend=Friend_request.objects.get(email_sender_id=reciever_id,email_reciever=email_id)
        friend.confirmation=1
        friend.save()

        return redirect("/follow_request")
    except:
        return redirect("/login")
def delete_request(request,username,po):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        if po==1:
            register=Registration.objects.get(username=username)
            reciever_id=register.email
            friend=Friend_request.objects.get(email_sender_id=reciever_id,email_reciever=email_id)
            friend.delete()
        
            return redirect("/follow_request")
        if po==2:
            register=Registration.objects.get(username=username)
            reciever_id=register.email
            friend=Friend_request.objects.get(email_sender_id=email_id,email_reciever=reciever_id)
            friend.delete()
            return redirect("/requested")
    except:
        return redirect("/login")
def myfriends(request):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        friend=Friend_request.objects.filter(email_reciever=email_id)
        d1={}
        for i in friend:
            d={}
            if i.confirmation==1:
                register=Registration.objects.get(email=i.email_sender_id)
                d={
                    "name":register.name,
                    "username":register.username,
                    "img":register.img
                }
                d1[i.email_sender_id]=d
        friend1=Friend_request.objects.filter(email_sender=email_id)
        for i in friend1:
            d={}
            if i.confirmation==1:
                register=Registration.objects.get(email=i.email_reciever)
                d={
                    "name":register.name,
                    "username":register.username,
                    "img":register.img
                }
                d1[i.email_reciever]=d
        return render(request,"myfriends.html",{"d1":d1})
    except:
        return redirect("/login")
def requested(request):

    try:
        request.session['email_id']
        email_id=request.session['email_id']
        friend=Friend_request.objects.filter(email_sender_id=email_id)
        d1={}
        for i in friend:
            d={}
            if i.confirmation==0:
                register=Registration.objects.get(email=i.email_reciever)
                d={
                    "name":register.name,
                    "username":register.username,
                    "img":register.img
                }
                d1[i.email_reciever]=d
        return render(request,"requested.html",{"d1":d1})
    except:
        return redirect("/login")
def view_profile(request,username):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        register=Registration.objects.get(username=username)
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
        }
        friends1=Friend_request.objects.filter(email_sender_id=register.email,confirmation=1).count()
        friends2=Friend_request.objects.filter(email_reciever=register.email,confirmation=1).count()
        posts=Addpost.objects.filter(username=username).order_by('-id')
        p=posts.count()

        return render(request,"view_profile.html",{"register":register,"friends":friends1+friends2,"post_count":p,"posts":posts,"reacting":reacting})
    except:
        return redirect("/login")
def user_post(request,username):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
        }
        register=Registration.objects.get(username=username)
        posts=Addpost.objects.filter(username=username).order_by('-id')
        p=posts.count()

        return render(request,"view_post.html",{"register":register,"post_count":p,"posts":posts,"reacting":reacting})
    except:
        return redirect("/login")
def view_post(request,id):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
        }
        posts=Addpost.objects.get(id=id)
        return render(request,"post.html",{"i":posts,"reacting":reacting})
    except:
        return redirect("/login")
def view_friends(request,username):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        register=Registration.objects.get(username=username)
        friends1=Friend_request.objects.filter(email_sender_id=register.email,confirmation=1)
        friends2=Friend_request.objects.filter(email_reciever=register.email,confirmation=1)
        l=[]
        for i in friends1:
            registration=Registration.objects.get(email=i.email_reciever)
            l.append(registration)
        for i in friends2:
            registration=Registration.objects.get(email=i.email_sender_id)
            l.append(registration)
        kashi=Friend_request.objects.filter(email_sender_id=email_id)
        mishi=Friend_request.objects.filter(email_reciever=email_id)
        kash=[]
        mish=[]
        for i in kashi:
            if i.confirmation==0:
                kash.append(i.email_reciever)
            else:
                mish.append(i.email_reciever)
        for i in mishi:
            if i.confirmation==0:
                kash.append(i.email_sender_id)
            else:
                mish.append(i.email_sender_id)
        dictionary={
            "kashi":kash,
            "mish":mish
        }
        return render(request,"friend_friend_list.html",{"friends":l,"username":register.username,"dictionary":dictionary})
    except:
        return render(request,"friend_friend_list.html",{"friends":l})


def top_post(request):
    toppost=Addpost.objects.all().order_by('-like')
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
        }
        return render(request,"toppost.html",{"toppost":toppost,"reacting":reacting})
    except:
        return render(request,"toppost.html",{"toppost":toppost})
def my_post(request):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        register=Registration.objects.get(email=email_id)
        my_post=Addpost.objects.filter(username=register.username)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
        }
        return render(request,"mypost.html",{"my_post":my_post,"reacting":reacting})
    except:
        return redirect("/login")
def edit_post(request,id):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        if request.method=="POST":
            posty=Addpost.objects.get(id=id)
            title=request.POST['title']
            genre=request.POST['genre']
            description=request.POST['description']
            try:
                request.FILES['picture']
                picture=request.FILES['picture']
            except:
                picture=posty.img
            posts=Addpost.objects.get(id=id)
            posts.title=title
            posts.genre=genre
            posts.description=description
            posts.img=picture
            posts.save()
            post=Addpost.objects.get(id=id)
            return render(request,"edit_post.html",{"post":post})
        else:
            post=Addpost.objects.get(id=id)
            return render(request,"edit_post.html",{"post":post})
    except:
        return redirect("/login")
def remove_friend(request,username):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        register=Registration.objects.get(username=username)
        try:
            friend=Friend_request.objects.get(email_sender_id=email_id,email_reciever=register.email,confirmation=1)
        except:
            friend=Friend_request.objects.get(email_sender_id=register.email,email_reciever=email_id,confirmation=1)
        friend.delete()
        return redirect("/myfriends")
    except:
        return redirect("/login")
def view_comment(request):
    if request.method=="POST":
        id=request.POST.get("id")
        comments=Comments.objects.filter(post_id_id=id)
        l=[]
        for i in comments:
            register=Registration.objects.get(email=i.email_id)
            l.append(str(register.img))
        comment_list=serializers.serialize('json', comments)
        # user_list=serializers.serialize('json', userr)
        return JsonResponse({'status':1,"comments":comment_list,"user_image":l})
    else:
        return JsonResponse({'status':0})
def comment(request):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        if request.method=="POST":
            id=request.POST.get("id")
            email=request.POST.get("email")
            message=request.POST.get("message")
            com=Comments.objects.filter(post_id_id=id,email_id=email,message=message)
            if len(com)==1:
                return JsonResponse({'status':2})
            else:
                comment=Comments(post_id_id=id,email_id=email,message=message)
                comment.save()
                comments=Comments.objects.filter(post_id_id=id,email_id=email,message=message)
                l=[]
                for i in comments:
                    register=Registration.objects.get(email=i.email_id)
                    l.append(str(register.img))
                comment_list=serializers.serialize('json', comments)
                # user_list=serializers.serialize('json', userr)
                return JsonResponse({'status':1,"comments":comment_list,"user_image":l})
        else:
            return JsonResponse({'status':0})
    except:
        return redirect("/login")
def search(request):
    if request.method=="POST":
        search_element=request.POST["search"]
        post1=Addpost.objects.filter(title__icontains=search_element)
        post=[]
        for i in post1:
            post.append(i)  
        return render(request,"search.html",{"post":post})
    else:
        return redirect("/")
def search_related(request):
    if request.method=="POST":
        search_element=request.POST.get("search_element")
        post1=Addpost.objects.filter(title__icontains=search_element)
        post11=serializers.serialize('json', post1)
        return JsonResponse({"status":1,"post":post11})
    else:
        return JsonResponse({"status":0})
def search_user(request):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        if request.method=="POST":
            search_element=request.POST["search"]
            name1=Registration.objects.filter(name__icontains=search_element)
            name=[]
            for i in name1:
                name.append(i)
            kashi=Friend_request.objects.filter(email_sender_id=email_id)
            mishi=Friend_request.objects.filter(email_reciever=email_id)
            kash=[]
            mish=[]
            for i in kashi:
                if i.confirmation==0:
                    kash.append(i.email_reciever)
                else:
                    mish.append(i.email_reciever)
            for i in mishi:
                if i.confirmation==0:
                    kash.append(i.email_sender_id)
                else:
                    mish.append(i.email_sender_id)
            dictionary={
                "kashi":kash,
                "mish":mish
            }
            return render(request,"search_name.html",{"name":name,"dictionary":dictionary})
        else:
            return redirect("/")
    except:
        return redirect("login")
def search_related_name(request):
    if request.method=="POST":
        search_element=request.POST.get("search_element")
        name1=Registration.objects.filter(name__icontains=search_element)
        name11=serializers.serialize('json', name1)
        return JsonResponse({"status":1,"name":name11})
    else:
        return JsonResponse({"status":0})
def change_password(request):
    if request.method=="POST":
        em=request.POST['email']
        pa=request.POST['pas']
        pas=make_password(pa)
        try:
            item =Registration.objects.get(email=em)
        except:
            messages.info(request,"Wrong Email")
            return redirect('/change_password')
        item.password=pas
        item.save()
        messages.info(request,"Password Changed Successfuly")
        return redirect('/login')
    else:
        return render(request,"change_password.html")
def delete_user(request,email):
    user=Registration.objects.get(email=email)
    user.delete()
    del request.session['email_id']
    return redirect("/login")
def delete_post(request,id):
    try:
        request.session['email_id']
        email_id=request.session['email_id']
        post=Addpost.objects.get(id=id)
        post.delete()
        reacting1=Reaction.objects.filter(email_like=email_id)
        reacting2=Reaction.objects.filter(email_dislike=email_id)
        register=Registration.objects.get(email=email_id)
        my_post=Addpost.objects.filter(username=register.username)
        l1=[]
        l2=[]
        for i in reacting1:
            l1.append(i.post_id_id)
        for i in reacting2:
            l2.append(i.post_id_id)
        reacting={
            "reacting1":l1,
            "reacting2":l2,
        }
        return render(request,"mypost.html",{"my_post":my_post,"reacting":reacting})
    except:
        return redirect("/login")