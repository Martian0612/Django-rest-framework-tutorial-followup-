#### API VIEW CLASS IS DIFFERENT FROM API_VIEW DECORATOR, API VIEW DECORATOR IS BASICALLY A FUNCTION OR A DECORATOR WHICH MODIFY THE FUNCIONALITY OF ANY FUNCTION TO CONVERT IT INTO AN API
# AND API VIEW CLASS IS A CLASS, WHICH HAVE FUNTIONALITIES OF CLASS BASICALLY ALLOW US TO FOLLOW THE DRY PRINCIPLE AND INCREASE SECURITY BY ENCAPSULATION AND ABSTRACTION.



from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action


# Create your views here.

# This function is just for testing.

@api_view(['GET','POST','PUT','PATCH'])
def index(request):
    if(request.method == 'GET'):
        # url for doing the search -> http://127.0.0.1:8000/api/index/?search=Alex
        # we can't use request.data in GET request, we have to get the data like below, if required.
        print(request.GET.get('search'))
    # Creating a json object
        courses = {
            "Subject" : "Physics",
            "Subject_code" : "BT-201",
            "Instructor" : "Martian",
            "Start date": "24/07/2024"
        }
        print("This is GET request.")

        return Response(courses)

    elif(request.method == 'POST'):
        data = request.data
        # if data.is_valid():
        print("***")
        print(data)
        print("***")
            # return Response({"message":"Data stored successfully."})

        student = {
            "Name": "Muskan Kushwah",
            "Age": 23,
            "Courses" :[
                "Physics", "Maths", "Quantum Computing", "Machine Learning"
            ],
            "st_id": 68
        }
        print("This is post request.")
        return Response(student)
    
    elif(request.method == 'PUT'):

        return Response({'Message': "Data updated successfully."})
    
    else:
        return Response({"Message" : " Data partial updation is successful."})
    
# Creating an api to get all the people and create all the people

# *** Make particular fields in different api's when error occur or for the fields require option. ***
@api_view(['GET','POST','PUT','PATCH','DELETE'])
def person(request):
    if request.method == 'GET':
        # objs = Person.objects.all()
        # get only this people who have some color
        objs = Person.objects.filter(color__isnull = False).exclude(gender = "unknown")
        # many = True, if there are many person objects or basically person in database.
        serializer = PersonSerializer(objs,many = True)

        '''
        This is some extra lines of code written by sir, does it make any sense or what is the use of it?
        serializer_context = {
        " request" : (request),
        }

        context = serializer_context
        return Response(serializer.data)
        '''
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            print(data)
            serializer.save()
            return Response({'message':'Data saved in database.'})
    
        # else:

            '''
            This will be the error messages, if we use error_messages over errors in Response for errors.

            {
                "required": "This field is required.",
                "null": "This field may not be null.",
                "invalid": "Invalid data. Expected a dictionary, but got {datatype}."
            }

            '''
        return Response(serializer.errors)
        
    # Complete updation
    elif request.method == 'PUT':
        data = request.data
        obj = Person.objects.get(id = data['id'])

        # obj is the id in which we want to update the data, so if method is "put" then we need to pass all the fields of the person model.
        serializer = PersonSerializer(obj, data= data)
        if serializer.is_valid():
            # If you need to access data before committing to the database then inspect 'serializer.validated_data' instead.  
            print("data to update is ", serializer.validated_data)
            serializer.save()
            return Response({"Message": "Person data updated successfully using PUT method."})
        
        return Response(serializer.errors)
    

    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id = data['id'])
        print("person is ", obj)

        # It means perform a partial update.
        serializer = PersonSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            print("data to update is ", serializer.validated_data)
            serializer.save()
            return Response({"message":"Data updated successfully using PATCH method."})

        return Response(serializer.errors)
    
    else:
        # ??? How to delete the person data using only id over passing (name and age alongwith.) ???
        # data = request.data
        # # Find how to do it
        # # obj = Person.objects.filter(gender__isnull = True)
        # obj = Person.objects.get(id = data['id'])

        # serializer = PersonSerializer(data = data)
        # if serializer.is_valid():
            
        #     # serializer.delete() # It doesn't make any sense.
        #     obj.delete()
        #     return Response({"message": "Person data deleted successfully."})
        
        # return Response(serializer.errors)

        ##############
        # Here validation and other things are not required.
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message': 'person deleted succesfully.'})


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data = data)
    if serializer.is_valid():
        print(serializer.data)
        return Response({'message':'success'})
    return Response(serializer.errors)



### API CLASS VIEW
# In api class instead of writing the condition for different cases, you can write the function with that name only, and it get call by itself.
# basically reduces the redundancy or few lines of code.

class PersonAPI(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        # objs = Person.objects.filter(color__isnull = False).exclude(gender = "unknown")
        # many = True, if there are many person objects or basically person in database.


        # objs = Person.objects.filter(color__isnull = False)
        # serializer = PersonSerializer(objs,many = True)
        # return Response(serializer.data)

        ###### Demonstrating paginator
        objs = Person.objects.all()
        try:
            page = request.GET.get('page',1)
            page_size = 2
            # jis object ko jitni size main karn a hai
            paginator = Paginator(objs,page_size)

            # printing the page nubmer
            print(paginator.page(page))
            # didn't get this line
            serializer = PersonSerializer(paginator.page(page), many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'status':False, 'error': str(e)
            },status = status.HTTP_404_NOT_FOUND)
            
        ##############################
        # return Response({"message":"It's a get request."})
    
    def post(self,request):
        data = request.data
        serializer = PersonSerializer(data = data)
        if serializer.is_valid():
            print(data)
            serializer.save()
            return Response({'message':'Data saved in database.'})
        return Response(serializer.errors)
        ##############################
        # return Response({"message":"It's a post request."})

    def put(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'])

        # obj is the id in which we want to update the data, so if method is "put" then we need to pass all the fields of the person model.
        serializer = PersonSerializer(obj, data= data)
        if serializer.is_valid():
            # If you need to access data before committing to the database then inspect 'serializer.validated_data' instead.  
            print("data to update is ", serializer.validated_data)
            serializer.save()
            return Response({"Message": "Person data updated successfully using PUT method."})
        
        return Response(serializer.errors)

        ##############################
        # return Response({"message":"It's a put request."})
    

    def patch(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        print("person is ", obj)

        # It means perform a partial update.
        serializer = PersonSerializer(obj, data = data, partial = True)
        if serializer.is_valid():
            print("data to update is ", serializer.validated_data)
            serializer.save()
            return Response({"message":"Data updated successfully using PATCH method."})

        return Response(serializer.errors)

        ##############################
        # return Response({"message":"It's a patch request."})

    def delete(self,request):
        data = request.data
        obj = Person.objects.get(id = data['id'])
        obj.delete()
        return Response({'message': 'person deleted succesfully.'})
    
        ############################## 
        # return Response({"message":"It's a delete request."})

# Model viewset in django rest framework
# viewsets (modelviewset is a class)->which is capable of handling all the crud apis.

# ?????? I am unable to use crud features of viewset in django rest framework ????? (Why my override list function is not working?)
# $$$ you are typing the wrong url, you was not passing index value in the query, in model viewset (** index is necessary in the url**)
# class PersonViewSet(viewsets.ModelViewSet):
#     serializer_class = PersonSerializer
#     queryset = Person.objects.all()

#     # http_method_names for allowing only certain methods to work
#     http_method_names = ['get','post']


#     # Overriding builtin list method, to filter out data based on search query

#     def list(self, request):
#         print("i am inside list function")
#         # *** method is not subscriptable, basically you can't access method like this ***
#         # print(request.method)
#         print(request.GET.get('search'))
#         print()
#         search = request.GET.get('search')
#         # here it is not post data, so you don't need to validate it or don't need to pass into serializer
#         # serializer = PersonSerializer(search)

#         # why we did this? -> maybe it mean class_name.objects.all()
#         queryset = self.queryset
#         print("search is ", search)
#         # serializer.is_valid(): # this is the get data, which is not for validation
#         if search:
#             queryset = queryset.filter(name__startswith = search)
        
#         serializer = PersonSerializer(queryset, many = True)
#         print("serialized data vlaue is ", serializer.data)
#         # status :200 means everything works correctly
#         return Response({'status':200, 'data': serializer.data})

# class PersonViewSet(viewsets.ModelViewSet):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer

# Clearer code including list overriding
class PersonViewSet(viewsets.ModelViewSet):
    # defining which class to include or use in ModelViewSet
    serializer_class = PersonSerializer

    # What to include in queryset attribute of class
    # or Base queryset for all methods
    queryset = Person.objects.all()

    def list(self, request):
       
        # Creating a local variable which starts with the base queryset
        # Creating the local variable, allowing us to work(modifying it) with queryset inside the function only.
        # This is dynamic queryset
        queryset = self.queryset

        # Apply additonal filters or modifications
        '''
        # Using this default value is optional(just to avoid some additonal checking or any errors that might can occur.)

        Avoid Errors: If the search key is not present in the URL query parameters,
          request.GET.get('search') would return None by default. Providing an empty string ('') 
          as a default ensures that search will always be a string, which simplifies checking conditions
            and avoids potential errors related to type mismatches.
        '''
        
        search = request.GET.get('search','')
        print("search is", search)
        if search:
            queryset = queryset.filter(name__startswith = search)
        print("queryset is ",queryset)
        serializer = PersonSerializer(queryset, many = True)
        return Response({'status': 200, 'data':serializer.data},status= status.HTTP_200_OK)
    
    # Whatever we pass here as a status code, will appear at the top of postman output screen or in the web page or any application (to show the error or other method as needed.)
    # just an exmaple -> return Response({'status': 200, 'data':serializer.data},status= status.HTTP_302_FOUND)

    # detail = false, when you are passsing nothing or getting nothing(not sure)

    @action(detail = True, methods = ['post'])
    def send_mail_to_person(self, request,pk):
        print("pk is ",pk)
        # data = request.GET.get(pk)
        # obj = Person.objects.get(pk = pk)
        # serializer = PersonSerializer(obj)
        return Response({'status':True, 'message':'mail send successfully'})


# $$$ Working with authorization and permissions
class RegisterAPI(APIView):
    
    def post(self, request):
        data = request.data

        serializer = RegisterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status' : False,
                'message' : serializer.errors
            }, status= status.HTTP_400_BAD_REQUEST)

        #  ???? What does serializer.save() will do here ???
        serializer.save()

        return Response({'status': True, 'message':'user created'} , status.HTTP_200_OK)
    
# Do we generate different type of tokens at different time, such as when as when we create the user, we create the token and when we loggedin then again we create the token. is it?
class LoginAPI(APIView):
    
    def post(self, request):
        
        data = request.data

        serializer = LoginSerializer(data = data)

        # Basically if we are not getting any data, or not all the data which is required.
        if not serializer.is_valid():
            return Response({'status':False, 'message':serializer.errors},status= status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username = serializer.data['username'],password = serializer.data['password'])

        # returning none, means no such user exist
        if not user:
            return Response({
                'status':'False','message': 'Invalid credentials'
            }, status = status.HTTP_404_NOT_FOUND)
        
        # if user exist then create the token
        # token = Token.objects.get_or_create(user=user)

        return Response({'status': True, 'message':'User loggedin'}, status= status.HTTP_201_CREATED)
        # return Response({'status': 'True', 'message':'User loggedin','token':token}, status= status.HTTP_201_CREATED)

# token.key is  981421fce0ea06846b902cc9f2acde38b4b2e0cd