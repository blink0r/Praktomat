# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.forms.models import ModelForm, inlineformset_factory, BaseInlineFormSet
from django.forms.formsets import formset_factory
from django import forms

from attestation.models import Attestation, AnnotatedSolutionFile, RatingResult, Script
from configuration.models import Settings
											

class AttestationForm(ModelForm):
	class Meta:
		model = Attestation
		exclude = ('solution', 'author', 'final', 'published')
		
	def __init__(self, *args, **kwargs): 
		super(AttestationForm, self).__init__(*args, **kwargs) 
		final_grade_rating_scale = kwargs['instance'].solution.task.final_grade_rating_scale
		if final_grade_rating_scale:
			self.fields['final_grade'].choices = [ (item['id'], item['name']) for item in final_grade_rating_scale.ratingscaleitem_set.values() ]
		else:
			del self.fields['final_grade']
	
class AttestationPreviewForm(ModelForm):
	class Meta:
		model = Attestation
		fields = ('final',)

class AnnotatedFileForm(ModelForm):
	class Meta:
		model = AnnotatedSolutionFile
		fields=('content',)
		
AnnotatedFileFormSet = inlineformset_factory(Attestation, AnnotatedSolutionFile, form=AnnotatedFileForm, formset=BaseInlineFormSet, can_delete=False, extra=0)


class RatingResultForm(ModelForm):
	def __init__(self, *args, **kwargs): 
		super(RatingResultForm, self).__init__(*args, **kwargs)
		ratingResult = kwargs['instance']
		self.fields['mark'].label = ratingResult.rating.aspect.name 
		self.fields['mark'].help_text = ratingResult.rating.aspect.description 
		self.fields['mark'].choices = [ (item['id'], item['name']) for item in ratingResult.rating.scale.ratingscaleitem_set.values() ]
	
	class Meta:
		model = RatingResult
		fields=('mark',)

RatingResultFormSet = inlineformset_factory(Attestation, RatingResult, form=RatingResultForm, formset=BaseInlineFormSet, can_delete=False, extra=0)

class ScriptForm(ModelForm):
	class Meta:
		model = Script

class PublishFinalGradeForm(ModelForm):
	class Meta:
		model = Settings
		fields = ('final_grades_published',)

class GenerateRatingScaleForm(forms.Form):
	name = forms.CharField(max_length=200,  help_text = 'The Name of the rating scale for the aspects. E.g.: "School marks"')
	start = forms.FloatField(initial=0, help_text="The first RatingScaleItem to generate.")
	end = forms.FloatField(initial=15, help_text="The last RatingScaleItem to generate.")
	step = forms.FloatField(initial=1, help_text="The step size between the RatingScaleItems.")