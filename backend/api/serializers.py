from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.password_validation import validate_password
from userauths.models import Profile, User

from api import models as api_models

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token =  super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name','email','password','password2']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password" : "Password fields didn't match"})
        
        return attr
    
    def create(self, validated_data):
        user = User.objects.create(
            full_name = validated_data['full_name'],
            email=validated_data['email'],
        )

        email_username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = api_models.Category
        fields = [
            "title", 
            "image", 
            "slug", 
            "course_count"
            ]

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = api_models.Teacher
        fields = [
            "user", 
            "image",
            "full_name", 
            "bio", 
            "facebook",
            "twitter",
            "linkedin",
            "about",
            "country",
            "students",
            "courses",
            "review"
            ]


class VariantItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.VariantItem
        fields = '__all__'

class VariantSerializer(serializers.ModelSerializer):
    variant_items = VariantItemSerializer()
    class Meta:
        model = api_models.Variant
        fields = '__all__'


class QuestionAnswerMessageSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Question_Answer_Message
        fields = '__all__'

class QuestionAnswerSerializer(serializers.ModelSerializer):
    messages = QuestionAnswerMessageSerializer(many=True)
    profile = ProfileSerializer(many = False)
    
    class Meta:
        model = api_models.Question_Answer
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Cart
        fields = '__all__'

class CartOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.CartOrderItem
        fields = '__all__'

class CartOrderSerializer(serializers.ModelSerializer):
    order_items = CartOrderItemSerializer(many=True)

    class Meta:
        model = api_models.CartOrder
        fields = '__all__'


class CertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Certificate
        fields = '__all__'

class CompletedLessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.CompletedLesson
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Note
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = api_models.Review
        fields = '__all__'

class EnrolledCourseSerializer(serializers.ModelSerializer):
    lectures = VariantItemSerializer(many=True, read_only = True)
    completed_lesson = CompletedLessonSerializer(many=True, read_only=True)
    curriculum = VariantItemSerializer(many=True, read_only=True)
    note = NoteSerializer(many=True, read_only=True)
    question_answer = QuestionAnswerSerializer(many=True, read_only=True)
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = api_models.EnrolledCourse
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    students = EnrolledCourseSerializer(many=True)
    curriculum = VariantItemSerializer(many=True)
    lectures = VariantItemSerializer(many=True)

    class Meta:
        model = api_models.Course
        fields = [
            "category",
            "teacher",
            "file",
            "image",
            "title",
            "description",
            "price",
            "language",
            "level",
            "platform_status",
            "teacher_course_status",
            "featured",
            "course_id",
            "slug",
            "date",
            "students",
            "curriculum",
            "lectures",
            "average_rating",
            "rating_count",
            "reviews"
        ]


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Notification
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Coupon
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Wishlist
        fields = '__all__'

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = api_models.Country
        fields = '__all__'