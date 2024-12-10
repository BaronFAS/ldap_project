# import pytest
# from accounts.models import User
# from django.db.utils import IntegrityError
# from django_scopes import scope, scopes_disabled


# @pytest.mark.django_db
# def test_get_scoped_user_objects(user_factory):
#     """Один юзер сравнивается со списоком из двух. Под вопросом?"""
#     users = user_factory.create_batch(2)
#     with scope(company=users[0].company):
#         # assert [users[0]] == list(User.objects.all())
#         assert users[0] in User.objects.all()

#     with scope(company=users[1].company):
#         # assert [users[1]] == list(User.objects.all())
#         assert users[1] in User.objects.all()


# @pytest.mark.django_db
# def test_get_unscoped_user_objects(user_factory):
#     users = user_factory.create_batch(3)
#     with scopes_disabled():
#         assert users == list(User.objects.all())


# @pytest.mark.django_db
# def test_lowercase_email_user_field(user_factory):
#     user = user_factory.create(email="JohnDoe@acme.com")
#     assert user.email == "johndoe@acme.com"
#     with scopes_disabled():
#         saved_user = User.objects.first()
#     assert saved_user.email == "johndoe@acme.com"
#     with pytest.raises(IntegrityError):
#         user_factory.create(email="JohnDoe@acme.com")
