from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item, List

# Create your tests here.

class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_save_post_data(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))


    def test_only_save_item_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id))
        self.assertTemplateUsed(response, 'list.html')


    def test_display_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='correct thing 1', list=correct_list)
        Item.objects.create(text='correct thing 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other thing 1', list=other_list)
        Item.objects.create(text='other thing 2', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'correct thing 1')
        self.assertContains(response, 'correct thing 2')
        self.assertNotContains(response, 'other thing 1')
        self.assertNotContains(response, 'other thing 2')

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='thing1', list=list_)
        Item.objects.create(text='thing1', list=list_)


    def test_pass_correct_list_to_template(self):
        the_list = List.objects.create()
        other_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(the_list.id))
        self.assertEqual(response.context['list'], the_list)


class NewListTest(TestCase):

    def test_save_post_data(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirect_after_post(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/{}/'.format(new_list.id))


class NewItemTest(TestCase):

    def test_save_post_data_to_existing_list(self):
        the_list = List.objects.create()
        other_list = List.objects.create()  # create other list to smoke out hacks

        self.client.post(
            '/lists/{}/add_item'.format(the_list.id),
            data={'item_text': 'The first list item'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'The first list item')
        self.assertEqual(new_item.list, the_list)


    def test_redirects_to_list_view(self):
        the_list = List.objects.create()
        other_list = List.objects.create()  # create other list to smoke out hacks

        response  = self.client.post(
            '/lists/{}/add_item'.format(the_list.id),
            data={'item_text': 'The first list item'}
        )

        self.assertRedirects(response, '/lists/{}/'.format(the_list.id))


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()  # instantiate local List to which to add to each item, created in models.py
        list_.save()

        first_item = Item()
        first_item.text = 'The first item, ever!'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item!'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first item, ever!')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second item!')
        self.assertEqual(second_saved_item.list, list_)
