from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.text import slugify
# Create your models here.

class Level(models.TextChoices):
    BEGINNER = 'BEG', _('Beginner')
    INTERMEDIATE = 'INT', _('Intermediate')
    ADVANCED = 'ADV', _('Advanced')

class Status(models.TextChoices) :
        DRAFT = "DRF" ,_('Draft')
        PUBLISHED = "PSH" ,_('Published')
        HIDDEN = "HIDE" ,_('Hidden')

class Track(models.Model) :


    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=3,choices=Level.choices,default=Level.BEGINNER)
    instructor = models.ForeignKey('users.User',related_name='tracks',on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='tracks/thumbnails/')
    status = models.CharField(max_length=4,choices=Status.choices,default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    courses = models.ManyToManyField('Course',through='TrackCourse',related_name='tracks')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Course(models.Model) :

    # 
    # class CourseType(models.TextChoices) :
    #     FREE = "FREE" , _('Free')
    #     PAID = "PAID" , _("Paid")

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField()
    difficulty_level = models.CharField(max_length=3,choices=Level.choices,default=Level.BEGINNER)
    instructor = models.ForeignKey('users.User',related_name='courses',on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/')
    # course_type = models.CharField(max_length=5 , choices=CourseType.choices,default=CourseType.FREE)
    # price = models.DecimalField(max_digits=6,decimal_places=2)
    status = models.CharField(max_length=4,choices=Status.choices,default=Status.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) : 
        return self.name
    
    def save(self,*args,**kwargs):
        
        if not self.slug :
            slug_name = slugify(self.name)
            i = 0
            while True :
                slug = slug_name
                if i > 0 : slug +=f'-{i}'
                if not Course.objects.filter(slug = slug).exclude(pk = self.pk).exists() :
                    self.slug = slug
                    break
                i+=1
        return super().save(*args,**kwargs)

class TrackCourse(models.Model) :
    track = models.ForeignKey('Track',on_delete=models.CASCADE,related_name='track_courses')
    course = models.ForeignKey('Course',on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta :
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['track','order'],
                name='unique_track_course_order'
            ),
            models.UniqueConstraint(
                fields=['track','course'],
                name='unique_track_course'
            )
        ]

    
class Section(models.Model) :
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    course = models.ForeignKey('Course' , related_name='sections',on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['course','order'],
                name='unique_section_order'
            )
        ]

    def __str__(self) : 
        return self.title


class CourseContent(models.Model) :
    
    class ContentType(models.TextChoices) :
        VIDEO = 'VID' , _('Video')
        FILE = 'FILE' , _('File')
        EXTERNAL_LINK = 'EX_LINK' , _('External_Link')

    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='courses/lessons/thumbnails/')
    content_type = models.CharField(max_length=10,choices=ContentType.choices,default=ContentType.VIDEO)
    video_url = models.URLField(blank=True,null=True)
    file = models.FileField(blank=True,null=True)
    external_link = models.URLField(blank=True,null=True)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    section = models.ForeignKey('Section',related_name='lessons',on_delete=models.CASCADE)


    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(
                fields=['section','order'],
                name='unique_section_content_order'
            )
        ]

    def __str__(self):
        return self.title

    
    def clean(self):
        """
        Ensures that only the field corresponding to the selected
        content_type is filled, and all others remain empty.
        """

        super().clean()

        content_map = {
        self.ContentType.VIDEO: 'video_url',
        self.ContentType.FILE: 'file',
        self.ContentType.EXTERNAL_LINK: 'external_link',
        }

        errors = {}

        required_field = content_map.get(self.content_type)
        if required_field and not getattr(self,required_field) :
            errors[required_field] = (
                f"This field is required when content type is '{required_field}'."
            )
        
        for c_type, field_name in content_map.items():
            if c_type != self.content_type and getattr(self, field_name):
                errors[field_name] = (
                    f"This field must be empty when content type is '{required_field}'."
                )
        
        if errors:
            raise ValidationError(errors)
    
    def save(self,*args, **kwargs):
        
        self.full_clean()
        super().save(*args, **kwargs)


class Enrollment(models.Model) :
    user = models.ForeignKey('users.User',related_name='enrollments',on_delete=models.CASCADE)
    course = models.ForeignKey('Course',related_name='enrollments',on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0)

    class Meta :
        constraints = [
            models.UniqueConstraint(
                fields=['user','course'],
                name='uniqe_user_course_enrollment'
            )
        ]
    
    def __str__(self):
        return f"{self.user} - {self.course}"
    
class TrackEnrollment(models.Model) :
    user = models.ForeignKey('users.User',related_name='track_enrollments',on_delete=models.CASCADE)
    track = models.ForeignKey('Track',related_name='enrollments',on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(null=True,blank=True)
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta :
        constraints = [
            models.UniqueConstraint(
                fields=['user','track'],
                name='uniqe_user_track_enrollment'
            )
        ]
