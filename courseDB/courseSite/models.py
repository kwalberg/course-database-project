from django.db import models
from django import forms
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import django_tables2 as table
import json
# Create your models here.


class Course(models.Model):
    # Ex: COMP 225-01
    course_id = models.CharField(max_length=20)
    full_title = models.CharField(max_length=250)
    course_number = models.IntegerField()
    department = models.CharField(max_length=5)
    description = models.TextField()
    instructor = models.CharField(max_length=150)
    days = models.CharField(max_length=5)
    times = models.CharField(max_length=20)
    tags = TaggableManager()

    def get_review_list(self):
        return Review.objects.filter(course=self)[::-1]

    def __str__(self):
        return self.course_id

    def get_all_tags(self):
        tags = set()
        review_list = Review.objects.filter(course=self)
        for review in review_list:
            tags = tags.union(review.get_tags())
        tags.discard('')
        tags.discard('none')
        return list(tags)

    def get_percent_recommend(self):
        # Calculate average values for all metrics to be displayed on course pages
        recommended_percent = 0
        # Calculates number of times this individual metric was provided by a reviewer
        num_recommends = len([review for review in self.get_review_list() if review.recommend is not None])
        for review in self.get_review_list():
            if review.recommend is not None:
                recommended_percent += review.recommend
        # Handle potential division by zero
        if num_recommends != 0:
            recommended_percent = int(round(recommended_percent * 100 / num_recommends, -1))
        return recommended_percent

    def get_percent_enjoyed_teaching(self):
        enjoyed_teaching = 0
        num_teaching_rated = len([review for review in self.get_review_list() if review.liked_teaching is not None])
        for review in self.get_review_list():
            if review.liked_teaching is not None:
                enjoyed_teaching += review.liked_teaching
        if num_teaching_rated != 0:
            enjoyed_teaching = int(round(enjoyed_teaching * 100 / num_teaching_rated, -1))
        return enjoyed_teaching

    def get_average_rating(self):
        overall_rating = 0
        num_ratings = len([review for review in self.get_review_list() if review.ratings is not None])
        for review in self.get_review_list():
            if review.ratings is not None:
                overall_rating += review.ratings
        if num_ratings != 0:
            overall_rating = int(round(overall_rating / num_ratings))
        return overall_rating

    def get_average_difficulty(self):
        difficulty = 0
        average_difficulty = 0
        num_diff_rated = len([review for review in self.get_review_list() if review.test_difficulty is not None])
        for review in self.get_review_list():
            if review.test_difficulty is not None:
                difficulty += review.test_difficulty
        if num_diff_rated != 0:
            average_difficulty = int(round(difficulty / num_diff_rated))
        return average_difficulty

    def get_average_workload(self):
        workload = 0
        average_workload = 0
        num_workload_rated = len([review for review in self.get_review_list() if review.workload is not None])
        for review in self.get_review_list():
            if review.workload is not None:
                workload += review.workload
        if num_workload_rated != 0:
            average_workload = int(round(workload / num_workload_rated))
        scaled_dict = {'0': '0',
                       '1': '1-3',
                       '2': '4-5',
                       '3': '6-7',
                       '4': '8-9',
                       '5': '10+'}
        return scaled_dict[str(average_workload)]


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add='true')
    workload = models.IntegerField(null=True)
    attendance = models.IntegerField(null=True)
    test_difficulty = models.IntegerField(null=True)
    attend_class = models.IntegerField(null=True)
    recommend = models.IntegerField(null=True)
    has_book = models.IntegerField(null=True)
    liked_teaching = models.IntegerField(null=True)
    ratings = models.IntegerField(null=True)
    tags = models.TextField()

    # Convert bool to readable format
    def get_has_book(self):
        if self.has_book == 0:
            return "No"
        elif self.has_book == 1:
            return "Yes"
        else:
            return "Not Rated"

    # Convert bool to readable format
    def get_recommend(self):
        if self.recommend == 0:
            return "No"
        elif self.has_book == 1:
            return "Yes"
        else:
            return "Not Rated"

    # Convert bool to readable format
    def get_enjoyed_teaching(self):
        if self.liked_teaching == 0:
            return "No"
        elif self.liked_teaching == 1:
            return "Yes"
        else:
            return "Not Rated"

    # Convert "None" to "Not Rated" for all remaining fields (makes more sense from UI perspective)
    def get_workload(self):
        if self.workload:
            return self.workload
        else:
            return "Not Rated"

    def get_attend_class(self):
        if self.attend_class:
            return self.attend_class
        else:
            return "Not Rated"

    def get_difficulty(self):
        if self.test_difficulty:
            return self.test_difficulty
        else:
            return "Not Rated"

    def get_overall_rating(self):
        if self.ratings:
            return self.ratings
        else:
            return "Not Rated"

    # Convert date to correct format
    def simple_date(self):
        return self.pub_date.strftime("%m/%d/%Y")

    # Convert string of tags to list
    def get_tags(self):
        return self.tags.split(",")
