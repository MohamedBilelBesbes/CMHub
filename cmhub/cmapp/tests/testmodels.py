from django.contrib.auth.forms import UsernameField
from django.db.models.fields import EmailField
from django.http import request, response
from django.test import TestCase, Client
from django.urls import reverse
from  cmapp.models import Post
from django.contrib.auth.models import User
from selenium import webdriver as wb
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from django.test import LiveServerTestCase


class TestModels(TestCase):
    def SetUp(self):
        self.client = Client()
    def test_indexpage_status(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmapp/index.html')
        User.objects.create_user(
            'belel','belel@gmail.com','Bilel1998'
        )
        self.client.login(username='belel', password='Bilel1998')
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmapp/index.html')
    def test_loggedpages_status(self):
        User.objects.create_user(
            'bilal','bilal@gmail.com','Bilel1998'
        )
        self.client.login(username='bilal', password='Bilel1998')
        response = self.client.get(reverse('display_posts'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/display_posts.html')
        response = self.client.get(reverse('profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmapp/profile.html')
        response = self.client.get(reverse('edit_profile'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmapp/edit_profile.html')
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmapp/logout.html')
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'cmapp/login.html')
    def test_user(self):
        testuser = User.objects.create_user(
            'med','med@gmail.com','Bilel1998'
        )
        self.client.login(username='med', password='Bilel1998')
        self.assertEquals(User.objects.filter(pk=testuser.id).count(), 1)
        print('Adding users works !')
        User.objects.filter(pk=testuser.id).update(email = 'mohamed@supcom.tn')
        self.assertEquals(User.objects.get(pk=testuser.id).email, 'mohamed@supcom.tn')
        print('Modifying users info works !')
        User.objects.filter(pk=testuser.id).delete()
        self.assertEquals(User.objects.filter(pk=testuser.id).count(), 0)
        print('deleting post works !')
    def test_post_crud(self):
        testuser = User.objects.create_user(
            'bilale','bilale@gmail.com','Bilel1998'
        )
        self.client.login(username='bilale', password='Bilel1998')
        testpost = Post.objects.create(
                numberoffollowers = 10,
                numberoffollowing = 100,
                numberoftweets = 6,
                content = '@bilel #bilel',
                picture = False,
                video = True,
                owner= User.objects.get(pk=testuser.id).username
        )
        self.assertEquals(Post.objects.filter(pk=testpost.id).count(), 1)
        print('adding post works !')
        response = self.client.get(reverse('display_post',args=[testpost.id]))
        self.assertEquals(response.status_code,200)
        print('the post display works !')
        testpost_id = testpost.id
        Post.objects.filter(pk=testpost_id).update(numberoffollowers = 1000)
        self.assertEquals(Post.objects.get(pk=testpost_id).numberoffollowers, 1000)
        print('updating post works !')
        response = self.client.get(reverse('edit_post',args=[testpost.id]))
        self.assertEquals(response.status_code,200)
        print('the post edit function get method works !')
        response = self.client.post(reverse('edit_post',args=[testpost.id]),{'numberoffollowers':'100',
        'numberoffollowing' : '40',
        'numberoftweets' : '40',
        'content' : 'vghbjnk',
        'video' : True,
        'picture' : False
        })
        self.assertEquals(response.status_code, 302)
        print('post edited successfully !')
        Post.objects.filter(pk=testpost_id).delete()
        self.assertEquals(Post.objects.all().filter(pk=testpost_id).count(), 0)
        print('deleting post works !')
class FrontTest(LiveServerTestCase):
    # def testform(self):
    #     driver =wb.Chrome()
    #     driver.get('http://127.0.0.1:8000/login')
    #     time.sleep(5)
    #     username = driver.find_element_by_id('username')
    #     password = driver.find_element_by_id('password')
    #     time.sleep(5)
    #     login = driver.find_element_by_id('signin-links')
    #     username.send_keys('chaimabeldi')
    #     password.send_keys('123456')
    #     login.send_keys(Keys.RETURN)
    #     assert 'chaimabeldi' in driver.page_source
    def testPost(self):
        options = Options()
        options.add_argument("--headless")
        try:
            driver =wb.Chrome('./chromedriver',options=options)
        except:
            driver =wb.Chrome('/home/bilel/Desktop/cmhubproject/CMHub/chromedriver',options=options)
        driver.get('http://127.0.0.1:8000/login')
        time.sleep(2)
        username = driver.find_element_by_id('username')
        password = driver.find_element_by_id('password')
        time.sleep(2)
        login = driver.find_element_by_id('signin-links')
        username.send_keys('chaimabeldi')
        password.send_keys('123456')
        login.send_keys(Keys.RETURN)
        time.sleep(2)
        
        driver.find_element_by_xpath('/html/body/nav/div/ul/li[3]/a').click()

        time.sleep(2)
        numberofpredpost = Post.objects.all().count()
        print (numberofpredpost)
        Numberoffollowers = driver.find_element_by_id('numberoffollowers')
        Numberoffollowing = driver.find_element_by_id('numberoffollowing')
        Numberoftweets = driver.find_element_by_id('numberoftweets')
        Content = driver.find_element_by_id('content')
        video = driver.find_element_by_id('video')
        picture = driver.find_element_by_id('picture')
        time.sleep(2)
        # createpost = driver.find_element_by_id('createpost')
        Numberoffollowers.send_keys('58')
        Numberoffollowing.send_keys('12')
        Numberoftweets.send_keys('33')
        Content.send_keys('cg')
        video.send_keys('yes')
        picture.send_keys('no')
        time.sleep(2)
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/form/button').click()
        # createpost.send_keys(Keys.RETURN)
        time.sleep(2)
        numberofafterpost = Post.objects.all().count()
        print (numberofafterpost)
        # self.assertEquals(numberofpredpost + 1,numberofafterpost )
        # url = request.get(driver.current_url)
        # assert url.status_code == 302
        response = self.client.get(driver.current_url)
        self.assertEqual(response.status_code, 302)
        
