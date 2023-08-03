from django.urls import path

from . import views

#https://cs50.harvard.edu/web/2020/notes/3/#routes (lecture 3 notes) 

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("edit_save/", views.edit_save, name="edit_save"),
    path("random/", views.rand, name="random"),
]
