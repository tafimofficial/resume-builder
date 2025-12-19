from django import forms
from django.forms import inlineformset_factory
from .models import Resume, PersonalDetail, Education, Experience, Skill,Research,Publication,Award

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'template_name', 'doc_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. My Software Engineer Resume'}),
            'template_name': forms.Select(attrs={'class': 'form-select'}),
            'doc_type': forms.HiddenInput(),
        }

class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields = ['image', 'full_name', 'email', 'phone', 'address', 'linkedin_url', 'portfolio_url', 'summary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 234 567 8900'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/johndoe'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://johndoe.com'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief professional summary...'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'University Name'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BSc Computer Science'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 'is_current', 'description']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Software Engineer'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python'}),
            'proficiency': forms.NumberInput(attrs={'class': 'form-control', 'type': 'range', 'min': '0', 'max': '100'}),
        }

class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = ['title', 'description', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Research Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'publisher', 'date', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Publication Title'}),
            'publisher': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Journal or Publisher'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }

class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ['title', 'issuer', 'date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Award Name'}),
            'issuer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issuing Organization'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Formsets for dynamic addition
EducationFormSet = inlineformset_factory(Resume, Education, form=EducationForm, extra=1, can_delete=True)
ExperienceFormSet = inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=1, can_delete=True)
SkillFormSet = inlineformset_factory(Resume, Skill, form=SkillForm, extra=3, can_delete=True)
ResearchFormSet = inlineformset_factory(Resume, Research, form=ResearchForm, extra=1, can_delete=True)
PublicationFormSet = inlineformset_factory(Resume, Publication, form=PublicationForm, extra=1, can_delete=True)
AwardFormSet = inlineformset_factory(Resume, Award, form=AwardForm, extra=1, can_delete=True)
