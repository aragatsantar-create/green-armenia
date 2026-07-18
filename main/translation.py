from modeltranslation.translator import translator, TranslationOptions
from .models import Project, AboutPage, ContactInfo

class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class AboutPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

class ContactInfoTranslationOptions(TranslationOptions):
    fields = ('address', 'description')

translator.register(Project, ProjectTranslationOptions)
translator.register(AboutPage, AboutPageTranslationOptions)
translator.register(ContactInfo, ContactInfoTranslationOptions)