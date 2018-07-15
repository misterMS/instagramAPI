from django.shortcuts import render
from django.http import HttpResponse
from InstagramAPI import InstagramAPI
import pandas

# Create your views here.

def instagram_login(request):
    return render(request,'Instagram\instagram_login.html')

def instagram_connection(request):
    if request.method=="POST":
        username=request.POST['UserName']
        password=request.POST['Password']
        InstagramAPIs = InstagramAPI(username,password)
        if InstagramAPIs.login():
            followers_usernames=[]
            followers_fullnames=[]

            # Read previous followers file
            df_old=pandas.read_excel('user_list\\followers_new.xlsx',sheetname="Sheet1")
            writer = pandas.ExcelWriter('user_list\\followers_old.xlsx', engine='xlsxwriter')
            df_old.to_excel(writer, sheet_name='Sheet1')
            writer.save()

            # Login to instagram
            InstagramAPIs.getProfileData()
            user_id=InstagramAPIs.LastJson['user']['pk']
            InstagramAPIs.getUserFollowers(user_id)
            for followers in InstagramAPIs.LastJson['users']:
                followers_usernames.append(followers['username'])
                followers_fullnames.append(followers['full_name'])

            # Write the current followers list in new file
            df_new=pandas.DataFrame({'Usernames':followers_usernames,'Full Names':followers_fullnames})
            writer = pandas.ExcelWriter('user_list\\followers_new.xlsx', engine='xlsxwriter')
            df_new.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            #df_new.iloc[:,1]


            if (df_old.shape[0]>df_new.shape[0]):
                unfollowed_username=[]
                unfollowed_fullname=[]
                df_unfollowed_old=pandas.read_excel('user_list\\unfollowed.xlsx',sheetname="Sheet1")
                for followers in range(df_old.shape[0]):
                    if df_old.iloc[followers,0] not in list(df_new.iloc[:,0]):
                        unfollowed_username.append(df_old.iloc[followers,0])
                        unfollowed_fullname.append(df_old.iloc[followers,1])
                df_unfollowed_new=pandas.DataFrame({'Usernames':unfollowed_username,'Full Names':unfollowed_fullname})
                df_unfollowed=df_unfollowed_old.append(df_unfollowed_new)
                writer = pandas.ExcelWriter('user_list\\unfollowed.xlsx', engine='xlsxwriter')
                df_unfollowed.to_excel(writer, sheet_name='Sheet1')
                writer.save()

            elif (df_old.shape[0]<df_new.shape[0]):

                followed_username=[]
                followed_fullname=[]
                df_followed_old=pandas.read_excel('user_list\\followed.xlsx',sheetname="Sheet1")
                for followers in range(df_new.shape[0]):
                    if df_new.iloc[followers,0] not in list(df_old.iloc[:,0]):
                        followed_username.append(df_new.iloc[followers,0])
                        followed_fullname.append(df_new.iloc[followers,1])
                df_followed_new=pandas.DataFrame({'Usernames':followed_username,'Full Names':followed_fullname})
                df_followed=df_followed_old.append(df_followed_new)
                writer = pandas.ExcelWriter('user_list\\followed.xlsx', engine='xlsxwriter')
                df_followed.to_excel(writer, sheet_name='Sheet1')
                writer.save()

            else:
                pass

        else:
            print("fail")
        return render(request,'Instagram\instagram_login.html')
