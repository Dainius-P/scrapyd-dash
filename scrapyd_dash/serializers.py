from rest_framework import serializers
from .models import ScrapydProject, ScrapydProjectVersion

class ScrapyProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapydProject
        fields = ('name','server','pk')

class ScrapyProjectVersionSerializer(serializers.ModelSerializer):
	class Meta:
		model = ScrapydProjectVersion
		fiels = ('version',)