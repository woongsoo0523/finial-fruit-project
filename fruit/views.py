from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import numpy as np
from keras.models import load_model
import cv2
from django.core.files.storage import default_storage
from .models import FruitTable,FruitImg,FruitSugar
from django.conf import settings
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor

# Create your views here.
def deep(imgfile):
    model = load_model(os.path.join(settings.BASE_DIR, 'fruit/fruits7-model.h5'))
    
    image = cv2.imread(f'./images/{imgfile}')
    
    # 이미지의 높이와 너비를 구한다.
    height, width, channels = image.shape

    # # 이미지의 픽셀을 배열로 만든다.
    pixels = image.reshape((height, width, channels))

    # # 이미지의 픽셀을 (28, 28, 1)로 바꾼다.
    resized_image = cv2.resize(pixels, (150, 150), interpolation=cv2.INTER_NEAREST)

    # # 이미지의 높이와 너비를 구한다.
    height, width, channels = resized_image.shape

    # # 이미지의 픽셀을 배열로 만든다.
    pixels = resized_image.reshape((height, width, channels))

    pixel_data = np.array(pixels)
    
    a = pixel_data.reshape(1,150,150,3)
    
    preds1 = model.predict(a)
    print(preds1)
    classes = ['사과' ,'포도','감귤' ,'복숭아' , '배' ,'바나나' ,'체리','딸기','수박']
    
    result = classes[np.argmax(preds1)-1]
    result2 = np.argmax(preds1)-1
    return result, result2

def machine():
    #print(FruitImg.objects.values_list())
    #print(FruitImg.objects.values_list().last())
    result = FruitImg.objects.values_list().last()[3]
    #print("result:", result)
    result2 = FruitImg.objects.values_list().last()[2]
    #print("result2:", result2)
    df = pd.read_excel('./fruit/datalab.xlsx')
    df = df.rename(columns={'날짜':'날짜.0'})
    
    apple = df[['날짜.0','사과 당도']]
    pear = df[['날짜.1','배 당도']]
    peach = df[['날짜.2','복숭아 당도']]
    grape = df[['날짜.3','포도 당도']]
    orange = df[['날짜.4','감귤 당도']]
    watermelon = df[['날짜.5','수박 당도']]
    strawberry = df[['날짜.6','딸기 당도']]
    banana = df[['날짜.7','바나나 당도']]
    cherry = df[['날짜.8','체리 당도']]
    
    def yearmonday(fruit, n):
        fruit.insert(loc=0, column='day',value=1)
        fruit.insert(loc=0, column='month',value=1)
        fruit.insert(loc=0, column='year',value=1)
        for i in range(len(fruit)):
            fruit.loc[i,'year']= int(fruit[f'날짜.{n}'][i][0:4])
            fruit.loc[i,'month']= int(fruit[f'날짜.{n}'][i][5:7])
            fruit.loc[i,'day']= int(fruit[f'날짜.{n}'][i][8:10])
        fruit = fruit.drop([f'날짜.{n}'],axis=1)
        return fruit
    
    apple = yearmonday(apple,0)
    pear = yearmonday(pear,1)
    peach = yearmonday(peach,2)
    grape = yearmonday(grape,3)
    orange = yearmonday(orange,4)
    watermelon = yearmonday(watermelon,5)
    strawberry = yearmonday(strawberry,6)
    banana = yearmonday(banana,7)
    cherry = yearmonday(cherry,8)
    fruit_li = [apple,grape,orange,peach,pear,banana,cherry,strawberry,watermelon]
    
    #print(fruit_li)
    
    #print(fruit_li[0])
    
    data = fruit_li[result].drop(f'{result2} 당도', axis=1)
    target = fruit_li[result][f'{result2} 당도']
    X_train, X_test, y_train, y_test = train_test_split(
        data, target)
    
    year = FruitTable.objects.values_list().last()[1]
    month = FruitTable.objects.values_list().last()[2]
    day = FruitTable.objects.values_list().last()[3]
    
    user = [[year, month, day]]
    
    gb = GradientBoostingRegressor(n_estimators=100)
    gb.fit(X_train,y_train)
    
    sugar = round(float(gb.predict(user)),2)
    return sugar

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.error(request, '비밀.')
            print("로그인 성공")
            return redirect('fruit:index')  # 로그인 후 index로 이동
        else:
            print("로그인 실패")
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')  # 인증 실패 시 오류 메시지 생성
            return redirect('fruit:login')
    return render(request, 'fruit/login.html', {'user': request.user})

def logout(request):
    auth_logout(request)
    return redirect('fruit:index')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, '중복된 아이디입니다.')  # Error message.
            return render(request, 'fruit/signup.html')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect(reverse('fruit:login'))

    return render(request, 'fruit/signup.html')
        
def index(request):
    if request.method == 'GET':
        return render(request, 'fruit/index.html')
    
def upload(request):
    if request.method == 'POST':
        year = request.POST.get('year', 0) # year = request.POST['year'] 
        month = request.POST['month']
        day = request.POST['day']
        imgfile = request.FILES['imgfiles']
        print(imgfile)
        
        fruit_table = FruitTable.objects.create(user=request.user, year=year, month=month, day=day, img=imgfile)
        
        fruit_result, fruit_result2 = deep(imgfile)
        
        if fruit_result is None:
            messages.error(request, '이미지를 읽을 수 없습니다.')
            return redirect('fruit:index')
        
        FruitImg.objects.create(fruittable=fruit_table, fruitresult=fruit_result, fruitresult2=fruit_result2)
        
        sugar = machine()
        print("sugar:", sugar)
        print(sugar)
        if sugar < 0:
            sugar = 0
        
        FruitSugar.objects.create(fruittable=fruit_table, sugar=sugar)
        
        return HttpResponseRedirect(reverse('fruit:detail2', args=(fruit_table.id,)))
    
def detail(request):
    fruit = FruitTable.objects.filter(user=request.user).last()
    if fruit:
        fruitlist = FruitImg.objects.values_list().last()[1]
        sugar = FruitSugar.objects.values_list().last()[1]
        fimg = FruitTable.objects.values_list().last()[4]
        year = FruitTable.objects.values_list().last()[1]
        month = FruitTable.objects.values_list().last()[2]
        day = FruitTable.objects.values_list().last()[3]
        id = FruitTable.objects.values_list().last()[0]
        
        if sugar < 0:
            sugar = 0
            
        #print(sugar)
        con = {
            'fruitlist':fruitlist,
            'sugar':sugar,
            'img':fimg,
            'year':year,
            'month':month,
            'day':day,
            'id' : id,
        }
        return render(request, 'fruit/detail.html',con)

def detail2(request,id):
    result = FruitImg.objects.get(id=id)

    ymd = FruitTable.objects.get(id=id)
    img = FruitTable.objects.get(id=id).img

    sugar = FruitSugar.objects.get(id=id).sugar
    sugar1 = FruitSugar.objects.get(id=id)
    id = FruitTable.objects.values_list().last()[0]
    
    if sugar < 0:
        sugar = 0
   
    con = {
        'fruitresult':result,
        'ymd':ymd,
        'fruitimg':img,
        'sugar':sugar,
        'id':id,
        'sugar1':sugar1,
    }
    return render(request,'fruit/detail2.html',con)

def fruitlist(request,):
    fruit_li = FruitTable.objects.filter(user=request.user)
    
    
    con = {
        'fruit_li':fruit_li,
    }
    
    return render(request, 'fruit/fruitlist.html',con)

def delete(request,id):
    fruit_table = get_object_or_404(FruitTable, id=id)
    fruit_table_id = fruit_table.id  # 해당 과일 테이블의 ID 저장
    fruit_table.delete()  # 해당 과일 테이블 삭제

    # 연결된 FruitImg 및 FruitSugar도 삭제
    FruitImg.objects.filter(fruittable_id=fruit_table_id).delete()
    FruitSugar.objects.filter(fruittable_id=fruit_table_id).delete()

    return HttpResponseRedirect(reverse('fruit:fruitlist'))
