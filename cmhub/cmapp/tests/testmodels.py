from django.contrib.auth.forms import UsernameField
from django.db.models.fields import EmailField
from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from  cmapp.models import Post
from django.contrib.auth.models import User

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