# from captcha.fields import CaptchaField
# from django import forms
#
# from .models import Comment2
#
# class CommentForm(forms.Form):
#     content = forms.CharField(widget=forms.Textarea)
#
# class UserCommentForm(forms.ModelForm) :
#     class Meta:
#         model = Comment2
#         exclude = ('is_active1')
#         widgets = {'GoITeens': forms.HiddenInput}
#
# class GuestCommentForm (forms. ModelForm) :
#     captcha = CaptchaField(label='Введіть текст із зображення', error_messages={'invalid': 'Неправильний текст'})
#     class Meta:
#         model = Comment2
#         exclude = ('is_active1')
#         widgets = {'GoITeens': forms.HiddenInput}
