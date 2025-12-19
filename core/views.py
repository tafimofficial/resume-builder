from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .models import Resume, PersonalDetail
from .forms import (
    ResumeForm, PersonalDetailForm, 
    EducationFormSet, ExperienceFormSet, SkillFormSet,
    ResearchFormSet, PublicationFormSet, AwardFormSet
)

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard.html', {'resumes': resumes})

@login_required
def create_resume(request):
    doc_type = request.GET.get('type', 'resume')
    if doc_type not in ['resume', 'cv']:
        doc_type = 'resume'

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        personal_form = PersonalDetailForm(request.POST, request.FILES)
        
        if resume_form.is_valid() and personal_form.is_valid():
            resume = resume_form.save(commit=False)
            resume.user = request.user
            # Ensure doc_type is set correctly
            if not resume.doc_type:
                resume.doc_type = doc_type
            resume.save()
            
            personal_detail = personal_form.save(commit=False)
            personal_detail.resume = resume
            personal_detail.save()

            formsets = {
                'education': EducationFormSet(request.POST, instance=resume),
                'experience': ExperienceFormSet(request.POST, instance=resume),
                'skill': SkillFormSet(request.POST, instance=resume),
            }
            if resume.doc_type == 'cv':
                formsets.update({
                    'research': ResearchFormSet(request.POST, instance=resume),
                    'publication': PublicationFormSet(request.POST, instance=resume),
                    'award': AwardFormSet(request.POST, instance=resume),
                })

            if all(fs.is_valid() for fs in formsets.values()):
                for fs in formsets.values():
                    fs.save()
                messages.success(request, f'{resume.get_doc_type_display()} created successfully!')
                return redirect('dashboard')
    else:
        resume_form = ResumeForm(initial={'doc_type': doc_type})
        personal_form = PersonalDetailForm()
        formsets = {
            'education_formset': EducationFormSet(instance=Resume()),
            'experience_formset': ExperienceFormSet(instance=Resume()),
            'skill_formset': SkillFormSet(instance=Resume()),
            'research_formset': ResearchFormSet(instance=Resume()),
            'publication_formset': PublicationFormSet(instance=Resume()),
            'award_formset': AwardFormSet(instance=Resume()),
        }

    ctx = {
        'resume_form': resume_form,
        'personal_form': personal_form,
        'doc_type': doc_type,
        'title': f'Create {doc_type.upper()}'
    }
    if request.method == 'POST':
        ctx.update({f'{k}_formset': v for k, v in formsets.items()})
    else:
        ctx.update(formsets)
    
    return render(request, 'resume_form.html', ctx)

@login_required
def edit_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    doc_type = resume.doc_type
    try:
        personal_detail = resume.personal_detail
    except PersonalDetail.DoesNotExist:
        personal_detail = None

    if request.method == 'POST':
        resume_form = ResumeForm(request.POST, instance=resume)
        personal_form = PersonalDetailForm(request.POST, request.FILES, instance=personal_detail)
        
        formsets = {
            'education': EducationFormSet(request.POST, instance=resume),
            'experience': ExperienceFormSet(request.POST, instance=resume),
            'skill': SkillFormSet(request.POST, instance=resume),
        }
        if doc_type == 'cv':
            formsets.update({
                'research': ResearchFormSet(request.POST, instance=resume),
                'publication': PublicationFormSet(request.POST, instance=resume),
                'award': AwardFormSet(request.POST, instance=resume),
            })

        if (resume_form.is_valid() and personal_form.is_valid() and 
            all(fs.is_valid() for fs in formsets.values())):
            
            resume_form.save()
            if personal_detail:
                personal_form.save()
            else:
                pd = personal_form.save(commit=False)
                pd.resume = resume
                pd.save()
                
            for fs in formsets.values():
                fs.save()
                
            messages.success(request, f'{resume.get_doc_type_display()} updated successfully!')
            return redirect('dashboard')
    else:
        resume_form = ResumeForm(instance=resume)
        personal_form = PersonalDetailForm(instance=personal_detail)
        formsets = {
            'education_formset': EducationFormSet(instance=resume),
            'experience_formset': ExperienceFormSet(instance=resume),
            'skill_formset': SkillFormSet(instance=resume),
            'research_formset': ResearchFormSet(instance=resume),
            'publication_formset': PublicationFormSet(instance=resume),
            'award_formset': AwardFormSet(instance=resume),
        }

    ctx = {
        'resume_form': resume_form,
        'personal_form': personal_form,
        'doc_type': doc_type,
        'title': f'Edit {doc_type.upper()}'
    }
    if request.method == 'POST':
        ctx.update({f'{k}_formset': v for k, v in formsets.items()})
    else:
        ctx.update(formsets)

    return render(request, 'resume_form.html', ctx)

@login_required
@xframe_options_sameorigin
def view_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    template_name = request.GET.get('template', resume.template_name)
    
    # Ensure template name is valid to prevent path traversal
    valid_templates = [t[0] for t in Resume.TEMPLATE_CHOICES]
    if template_name not in valid_templates:
        template_name = 'modern'

    context = {'resume': resume}
    return render(request, f'{template_name}.html', context)

def template_gallery(request):
    templates = Resume.TEMPLATE_CHOICES
    return render(request, 'template_gallery.html', {'templates': templates})

@xframe_options_sameorigin
def demo_template_view(request, template_name):
    # Create a dummy resume structure for preview
    class DummyObj:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    
    # Check if template name is valid
    valid_templates = [t[0] for t in Resume.TEMPLATE_CHOICES]
    if template_name not in valid_templates:
        template_name = 'modern'

    # Mock Data
    personal = DummyObj(
        full_name='Alex Rivera',
        email='alex.rivera@example.com',
        phone='+1 (555) 123-4567',
        address='San Francisco, CA',
        linkedin_url='linkedin.com/in/alexrivera',
        portfolio_url='alexrivera.design',
        summary='Innovative Creative Director with 8+ years of experience in digital branding and UI/UX design. Proven track record of leading high-performance teams to deliver award-winning campaigns. Passionate about user-centric design and storytelling.'
    )
    
    experiences = [
        DummyObj(position='Senior Product Designer', company='TechFlow Inc.', start_date='2020-03', end_date='Present', is_current=True, description='Lead design systems and manage a team of 5 designers. Increased user engagement by 40% through UI overhaul.'),
        DummyObj(position='UX Designer', company='CreativAgency', start_date='2017-06', end_date='2020-02', is_current=False, description='Designed web and mobile interfaces for Fortune 500 clients. Conducted user research and usability testing.'),
    ]
    
    education = [
        DummyObj(degree='Master of Interaction Design', institution='Design Academy', start_date='2015', end_date='2017', is_current=False, description='Focus on Human-Computer Interaction.'),
        DummyObj(degree='Bachelor of Fine Arts', institution='University of Arts', start_date='2011', end_date='2015', is_current=False, description='Major in Graphic Design.'),
    ]
    
    skills = [
        DummyObj(name='UI/UX Design', proficiency=95),
        DummyObj(name='Figma & Sketch', proficiency=90),
        DummyObj(name='HTML/CSS', proficiency=80),
        DummyObj(name='Brand Identity', proficiency=85),
        DummyObj(name='Team Leadership', proficiency=90),
    ]

    research = [
        DummyObj(title='User Empathy in Digital Products', date='2019', description='Published research on how emotional design affects user retention.'),
    ]
    
    publications = [
        DummyObj(title='The Future of Minimalist UI', publisher='Design Weekly', date='2021', url='designweekly.com/minimalist'),
    ]
    
    awards = [
        DummyObj(title='Best Mobile App Design', issuer='Tech Design Awards', date='2022'),
    ]

    # Structuring like the Resume model relationship
    class ResumeMock:
        def __init__(self):
            self.personal_detail = personal
            self.experience = DummyList(experiences)
            self.education = DummyList(education)
            self.skills = DummyList(skills)
            self.research = DummyList(research)
            self.publications = DummyList(publications)
            self.awards = DummyList(awards)
            self.doc_type = 'cv'
            self.get_doc_type_display = 'CV' 

    class DummyList(list):
        def all(self): return self

    resume = ResumeMock()
    return render(request, f'{template_name}.html', {'resume': resume})

@login_required
def export_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    export_format = request.GET.get('format', 'txt')
    filename = f"{resume.personal_detail.full_name.replace(' ', '_')}_{resume.get_doc_type_display()}.{export_format}"
    
    if export_format == 'txt':
        # Generate Plain Text
        content = []
        pd = resume.personal_detail
        content.append(f"NAME: {pd.full_name}")
        content.append(f"EMAIL: {pd.email}")
        content.append(f"PHONE: {pd.phone}")
        content.append(f"ADDRESS: {pd.address}")
        if pd.linkedin_url: content.append(f"LINKEDIN: {pd.linkedin_url}")
        if pd.portfolio_url: content.append(f"PORTFOLIO: {pd.portfolio_url}")
        content.append(f"\nSUMMARY:\n{pd.summary}\n")
        
        if resume.education.exists():
            content.append("\nEDUCATION:")
            for edu in resume.education.all():
                content.append(f"- {edu.degree} at {edu.institution} ({edu.start_date} - {'Present' if edu.is_current else edu.end_date})")
                if edu.description: content.append(f"  {edu.description}")

        if resume.experience.exists():
            content.append("\nEXPERIENCE:")
            for exp in resume.experience.all():
                content.append(f"- {exp.position} at {exp.company} ({exp.start_date} - {'Present' if exp.is_current else exp.end_date})")
                if exp.description: content.append(f"  {exp.description}")

        if resume.skills.exists():
            content.append("\nSKILLS:")
            for skill in resume.skills.all():
                content.append(f"- {skill.name} ({skill.proficiency}%)")
        
        # CV Sections
        if resume.research.exists():
            content.append("\nRESEARCH:")
            for res in resume.research.all():
                content.append(f"- {res.title} ({res.date}): {res.description}")

        if resume.publications.exists():
            content.append("\nPUBLICATIONS:")
            for pub in resume.publications.all():
                content.append(f"- {pub.title} ({pub.publisher}, {pub.date})")

        if resume.awards.exists():
            content.append("\nAWARDS:")
            for award in resume.awards.all():
                content.append(f"- {award.title} ({award.issuer}, {award.date})")

        response = HttpResponse('\n'.join(content), content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    elif export_format == 'doc':
        # Generate HTML pretending to be Word Doc
        # Note: We use a simplified template or the actual template. 
        # Using the actual template is best for layout, but complex CSS might be weird in Word.
        # Let's try sending the actual rendered template first.
        
        # We need absolute URLs for images in Word, but local images are tricky without a full URL.
        # For now, we serve the standard template.
        response = render(request, f'{resume.template_name}.html', {'resume': resume})
        response['Content-Type'] = 'application/msword'
        return response

    elif export_format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Render HTML
        # We need absolute URIs for images/css to work in WeasyPrint
        # get_template handles standard rendering
        from django.template.loader import render_to_string
        from weasyprint import HTML, CSS
        
        html_string = render_to_string(f'{resume.template_name}.html', {'resume': resume}, request=request)
        
        # WeasyPrint needs a base_url to find static files
        base_url = request.build_absolute_uri('/')
        
        # Generate PDF
        HTML(string=html_string, base_url=base_url).write_pdf(response)
        return response

    return redirect('dashboard')
