from rest_framework import serializers
from .models import Person, Color
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# *** Normal serializers can be use for validation example for login,signup. so we can use serializers(normal) where we want to add custom functionality(want to do everything by ourselve, or have more control.)

#*** if you want to add custom field using SerializerMethodField, then you have to use a function whose name is field name prefixed with example(def get_country -> for country field.)
# *** to validate any field (add prefix of validate_) -> (example -> validate_age)

# this serializer help drf to serializer the foreing key data
#  basically foreign key model ki kon konsi fields show karni hai.

#*** When we serialize foreign key data using another class serializer, then we have more control over what to show, basically what fields we want to show. Basically jo fields = [] karke power hoti hai hamera pass serializer main woh use kar sakte hai.
# And when we use 'depth = 1', then it show all the fields of the foreign key model.

#*** SerializerMethodField is use to add custom fields to the serialized output of the model(or basically what we see as a output of an api), it means that this fields are not present in the model, but still we can show or maybe can add data to this field.

# Basically if you just want to serialize the data or just want to validate the data, then you don't use advance serializers

class LoginSerializer(serializers.Serializer):
     # email = serializers.EmailField()
     username = serializers.CharField()
     password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
     username = serializers.CharField()

     # first name and last name added afterwards.
     # first_name = serializers.CharField()
     # last_name = serializers.CharField()
     
     email = serializers.EmailField()
     password = serializers.CharField()

     def validate(self, data):
          

          if data['username']:
               user = User.objects.filter(username = data['username']).exists()
               if user:
                    raise serializers.ValidationError("Username name is already taken!")


          if data['email']:
               user = User.objects.filter(email = data['email']).exists()
               if user:
                    raise serializers.ValidationError("email is already taken!")
               
                    
          return data
          
     def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'],email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user = user)
        print('token.key is ',token.key)
        
        # Why returning validated_data is important
        return validated_data
     
   

class ColorSerializer(serializers.ModelSerializer):
     class Meta:
          model = Color
          fields = ['color_name']

          
class PersonSerializer(serializers.ModelSerializer):

    # custom field
    # color_info = serializers.SerializerMethodField()
    # country = serializers.SerializerMethodField()

    # it is saying color field of person model main konsa data show karna hai, so woh colorserializer ki help se pata chalega
    # color = ColorSerializer(many = True) # -> if multiple objects are available then why it is saying that 'Color' object is not iterable.
    # color = ColorSerializer()
    class Meta:
        model = Person
        # Here you can specify the fields you want to include by writing those fields name directly in the list
        # then you can also exclude fields like below code (in this it exclude only this field and include all the fields.)
        # exclude = ['name']
        # fields = '__all__'
        # fields = ['id','name','age','gender']
        fields = "__all__"
        # fields = ['id','name','age','gender','color_info','color']
        # fields = ['name','age','gender','country','color']
        # depth = 1

        
        
        # def get_color(self, obj):
        #      return obj.color.color_name

    # def validate_age(self,data):
    #         print("age is ",data)
    #          # if we use seperate validators for different field, then we can directly access the data over accessing it like data['age]
    #         if int(data) < 18:
    #             raise serializers.ValidationError('age should be greater than 18.')
    #         # Why returning data was important here?
    #         return data
    
    # my logic
    # def validate_name(self, data):
    #     print("name is ",data)
    #     special_characters = [ '!','@','#', '$','%','^','&','*', '(',')', '-','_','=','+','\\','|','[',']','{','}',';',':','\'','"',',','.','<','>','/','?','~','`']

    #     # if char in special_characters for char in data
    #     # @lex
    #     # for c in data:
    #     #  if c in special_characters:
    #     #       raise errors.
         
    #     a = [c in special_characters for c in data]
    #     # a = [c if c in special_characters for c in data] # wrong syntax.
    #     print(a)
    #     if True in a:
    #       raise  serializers.ValidationError("Name shouldn't contain any special characters.")
        
    #     # returning data is important here because we are posting data, so something need to be visible.
    #     return data

    
    # # by sir
    # def validate_name(self, data):
    #     special_characters = "!@#$%^&*()-+?_=,<>/"
    #     if any(c in special_characters for c in data):
    #         raise serializers.ValidationError('name cannot contain special chars')
        


         
    # For writing all the validation logic inside one function

    # def validate(self,data):
    #         print(data)

    #         special_characters = "!@#$%^&*()-+?_=,<>/"
    #         if any(c in special_characters for c in data['name']):
    #             raise serializers.ValidationError('name cannot contain special chars')
    
    #          # if we use seperate validators for different field, then we can directly access the data over accessing it like data['age]
    #         if int(data['age']) < 18:
    #             raise serializers.ValidationError('age should be greater than 18.')
    #         return data

    # for describing what vlaue we want to put under country field
    # where we are using obj?
    def get_color_info(self,obj):
    # def get_country(self,obj):
         # in custom field you can show data by fetching from other model also.
         # obj.color -> implies person ke andar jo color field hai uski value kya hai, woh iss custom field main likh sakte hai.

        color_obj = Color.objects.get(id = obj.color.id)
        #  return 'India'
        # here we can return whatever we want, so we are returning custom design hex code for colors.
        return {'color_name': color_obj.color_name, 'hex_code':'#000'}
         