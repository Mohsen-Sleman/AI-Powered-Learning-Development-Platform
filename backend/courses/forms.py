
from django import forms
from .models import CourseContent

class CourseContentForm(forms.ModelForm)  :

    class Meta :
        
        model = CourseContent
        fields = ("__all__")
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['video_url'].required = False
        self.fields['file'].required = False
        self.fields['external_link'].required = False
        
