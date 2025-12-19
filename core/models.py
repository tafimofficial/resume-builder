from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    TEMPLATE_CHOICES = [
        ('modern', 'Modern'),
        ('classic', 'Classic'),
        ('creative', 'Creative'),
        ('elegant', 'Elegant Serif'),
        ('executive', 'Executive Pro'),
        ('minimalist', 'Minimalist Clean'),
        ('timeline', 'Vertical Timeline'),
        ('tech', 'Tech Modern'),
        ('academic', 'Academic Professional'),
        ('designer', 'Designer Bold'),
        ('compact', 'Compact Single Page'),
        # City Collection - Sidebar Left
        ('newyork', 'New York (Modern Blue)'),
        ('london', 'London (Royal)'),
        ('paris', 'Paris (Chic)'),
        ('tokyo', 'Tokyo (Clean)'),
        ('sidney', 'Sidney (Ocean)'),
        ('dubai', 'Dubai (Gold)'),
        ('singapore', 'Singapore (Efficient)'),
        ('hongkong', 'Hong Kong (Dynamic)'),
        ('losangeles', 'Los Angeles (Creative)'),
        ('toronto', 'Toronto (Structure)'),
        # City Collection - Classic
        ('berlin', 'Berlin (Industrial)'),
        ('rome', 'Rome (Classic)'),
        ('madrid', 'Madrid (Warm)'),
        ('lisbon', 'Lisbon (Sunny)'),
        ('vienna', 'Vienna (Elegant)'),
        ('prague', 'Prague (Historic)'),
        ('budapest', 'Budapest (Bold)'),
        ('warsaw', 'Warsaw (Sturdy)'),
        ('oslo', 'Oslo (Minimal)'),
        ('stockholm', 'Stockholm (Clean)'),
        # City Collection - Sidebar Right
        ('chicago', 'Chicago (Bold)'),
        ('miami', 'Miami (Vibrant)'),
        ('seattle', 'Seattle (Green)'),
        ('austin', 'Austin (Fresh)'),
        ('denver', 'Denver (Nature)'),
        ('boston', 'Boston (Academic)'),
        ('atlanta', 'Atlanta (Peach)'),
        ('houston', 'Houston (Space)'),
        ('phoenix', 'Phoenix (Desert)'),
        ('lasvegas', 'Las Vegas (Night)'),
    ]
    DOC_TYPE_CHOICES = [
        ('resume', 'Resume'),
        ('cv', 'CV'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=10, choices=DOC_TYPE_CHOICES, default='resume')
    title = models.CharField(max_length=100, default='My Document')
    template_name = models.CharField(max_length=50, choices=TEMPLATE_CHOICES, default='modern')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.title} ({self.get_doc_type_display()})"

class PersonalDetail(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name='personal_detail')
    image=models.ImageField(upload_to='profile_pics', blank=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255, blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    summary = models.TextField(blank=True, help_text="A brief professional summary")

    def __str__(self):
        return self.full_name

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"

class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=50, help_text="Percentage 0-100")

    def __str__(self):
        return self.name

class Research(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='research')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Research"

    def __str__(self):
        return self.title

class Publication(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255, blank=True)
    date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

class Award(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
